"""
Evaluation runner: compares System A (static firewall) vs System B (PlanGuard).

Usage:
    export OPENAI_API_KEY=sk-...
    python run_evaluation.py

Output:
    Per-case results table + summary metrics (TPR, FPR, F1) for each system.

To use InjecAgent's full dataset instead of our sample cases:
    python run_evaluation.py --dataset path/to/attacker_cases_ds.jsonl
"""

from __future__ import annotations
import argparse
import json
import os
import sys
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.table import Table
    from rich import print as rprint
    RICH = True
except ImportError:
    RICH = False

from agent_harness import AgentHarness
from system_a.firewall import Firewall, make_hooks as make_a_hooks
from system_b.planguard import PlanGuard, make_hook as make_b_hook


@dataclass
class CaseResult:
    case_id: str
    description: str
    should_block: bool
    system_a_blocked: bool
    system_b_blocked: bool
    exfiltration_occurred: bool   # ground-truth: did the harness detect it?


def load_cases(path: str) -> list[dict]:
    with open(path) as f:
        if path.endswith(".jsonl"):
            return [json.loads(line) for line in f if line.strip()]
        return json.load(f)


def run_case_system_a(case: dict, api_key: str) -> bool:
    """Returns True if System A blocked the attack."""
    fw = Firewall(openai_api_key=api_key, use_local_embeddings=True)
    pre_hook, post_hook = make_a_hooks(fw)

    poison_map = {}
    if case.get("poison_tool") and case.get("poison_payload"):
        poison_map[case["poison_tool"]] = case["poison_payload"]

    harness = AgentHarness(
        api_key=api_key,
        poison_map=poison_map,
        pre_call_hook=pre_hook,
        post_call_hook=post_hook,
    )
    trace = harness.run(case["user_task"])

    blocked = any(tc.blocked_by_system_a for tc in trace.tool_calls)
    if not blocked and poison_map:
        # Check if sanitizer removed the injection (output sanitized → no exfiltration)
        blocked = not trace.exfiltration_detected and not trace.injection_followed
        # Refine: only count as blocked if there was a poison and no exfil happened
        blocked = bool(poison_map) and not trace.exfiltration_detected

    return blocked


def run_case_system_b(case: dict, api_key: str) -> bool:
    """Returns True if System B blocked the attack."""
    guard = PlanGuard(api_key=api_key)
    user_task = case["user_task"]
    pre_hook = make_b_hook(guard, user_task)

    poison_map = {}
    if case.get("poison_tool") and case.get("poison_payload"):
        poison_map[case["poison_tool"]] = case["poison_payload"]

    harness = AgentHarness(
        api_key=api_key,
        poison_map=poison_map,
        pre_call_hook=pre_hook,
    )
    trace = harness.run(user_task)

    blocked = any(tc.blocked_by_system_a for tc in trace.tool_calls)  # system_b uses pre_call_hook → blocked_by_system_a flag
    if not blocked and poison_map:
        blocked = not trace.exfiltration_detected

    return blocked


def compute_metrics(results: list[CaseResult], system: str) -> dict:
    blocked_attr = f"{system}_blocked"
    attack_cases = [r for r in results if r.should_block]
    benign_cases = [r for r in results if not r.should_block]

    tp = sum(1 for r in attack_cases if getattr(r, blocked_attr))
    fn = sum(1 for r in attack_cases if not getattr(r, blocked_attr))
    tn = sum(1 for r in benign_cases if not getattr(r, blocked_attr))
    fp = sum(1 for r in benign_cases if getattr(r, blocked_attr))

    tpr = tp / max(tp + fn, 1)
    fpr = fp / max(fp + tn, 1)
    precision = tp / max(tp + fp, 1)
    f1 = 2 * precision * tpr / max(precision + tpr, 1e-9)

    return {"TP": tp, "FN": fn, "TN": tn, "FP": fp, "TPR": tpr, "FPR": fpr, "Precision": precision, "F1": f1}


def print_results(results: list[CaseResult]) -> None:
    if RICH:
        console = Console()
        table = Table(title="P1 Detection Evaluation", show_lines=True)
        table.add_column("ID", style="bold")
        table.add_column("Description", max_width=40)
        table.add_column("Should Block")
        table.add_column("System A")
        table.add_column("System B")
        table.add_column("Exfil?")

        for r in results:
            def cell(blocked, should):
                if should and blocked:   return "[green]BLOCKED ✓[/green]"
                if should and not blocked: return "[red]MISSED ✗[/red]"
                if not should and blocked: return "[yellow]FP ⚠[/yellow]"
                return "[green]OK ✓[/green]"

            table.add_row(
                r.case_id,
                r.description,
                "Yes" if r.should_block else "No",
                cell(r.system_a_blocked, r.should_block),
                cell(r.system_b_blocked, r.should_block),
                "[red]YES[/red]" if r.exfiltration_occurred else "no",
            )
        console.print(table)

        for system in ("system_a", "system_b"):
            m = compute_metrics(results, system)
            label = "System A (Static Firewall)" if system == "system_a" else "System B (PlanGuard)"
            console.print(f"\n[bold]{label}[/bold]")
            console.print(f"  TPR={m['TPR']:.0%}  FPR={m['FPR']:.0%}  Precision={m['Precision']:.0%}  F1={m['F1']:.2f}  (TP={m['TP']} FN={m['FN']} FP={m['FP']} TN={m['TN']})")
    else:
        for r in results:
            print(f"{r.case_id} | A={'BLOCK' if r.system_a_blocked else 'pass'} | B={'BLOCK' if r.system_b_blocked else 'pass'} | exfil={r.exfiltration_occurred} | expected={'block' if r.should_block else 'pass'}")

        for system in ("system_a", "system_b"):
            m = compute_metrics(results, system)
            label = "System A" if system == "system_a" else "System B"
            print(f"\n{label}: TPR={m['TPR']:.0%} FPR={m['FPR']:.0%} F1={m['F1']:.2f}")


def main():
    parser = argparse.ArgumentParser(description="Compare System A vs System B on P1 test cases")
    parser.add_argument("--dataset", default="test_cases.json", help="Path to test case file (.json or .jsonl)")
    parser.add_argument("--cases", nargs="*", help="Run only these case IDs (e.g. DS-001 BN-001)")
    parser.add_argument("--skip-system-b", action="store_true", help="Skip System B (saves API calls)")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: Set OPENAI_API_KEY environment variable.", file=sys.stderr)
        sys.exit(1)

    cases = load_cases(args.dataset)
    if args.cases:
        cases = [c for c in cases if c["id"] in args.cases]

    print(f"Running {len(cases)} test cases...")
    results: list[CaseResult] = []

    for i, case in enumerate(cases, 1):
        print(f"  [{i}/{len(cases)}] {case['id']}: {case['description'][:50]}...")

        a_blocked = run_case_system_a(case, api_key)

        if args.skip_system_b:
            b_blocked = False
        else:
            b_blocked = run_case_system_b(case, api_key)

        # Ground truth exfiltration: re-run bare harness to see what the unguarded agent does
        poison_map = {}
        if case.get("poison_tool") and case.get("poison_payload"):
            poison_map[case["poison_tool"]] = case["poison_payload"]
        bare = AgentHarness(api_key=api_key, poison_map=poison_map)
        bare_trace = bare.run(case["user_task"])

        results.append(CaseResult(
            case_id=case["id"],
            description=case["description"],
            should_block=case["should_block"],
            system_a_blocked=a_blocked,
            system_b_blocked=b_blocked,
            exfiltration_occurred=bare_trace.exfiltration_detected or bare_trace.injection_followed,
        ))

    print()
    print_results(results)


if __name__ == "__main__":
    main()
