# Local Setup — P1 Detection Systems

## Install

```bash
cd detection
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your OpenAI key
```

## Run all test cases

```bash
export OPENAI_API_KEY=sk-...
python run_evaluation.py
```

## Run a single case (faster for iteration)

```bash
python run_evaluation.py --cases DS-001
```

## System A only (no extra LLM calls, cheapest)

```bash
python run_evaluation.py --skip-system-b
```

## Use InjecAgent's full dataset (1,054 cases)

```bash
git clone https://github.com/uiuc-kang-lab/InjecAgent
python run_evaluation.py --dataset InjecAgent/data/attacker_cases_ds.jsonl
```

---

## Architecture recap

```
user_task
    │
    ├─► System B: IsolatedPlanner ──► reference_plan
    │                                       │
    │                               RuntimeMonitor ──► BLOCK / allow
    │                                       │
    ▼                               IntentVerifier (borderline)
AgentHarness (mock connectors)
    │
    ├─ read_email / read_file / web_search  ←── poison_map injects payload here
    │
    ├─► System A: ToolOutputSanitizer ──► strips injection before agent sees it
    │
    ├─► System A: ToolInputFirewall  ──► blocks before exfiltration tool executes
    │
    └─► send_email (exfiltration attempt)
```

## What to add for real OpenAI Operator/Connector testing

Replace mock tools in `agent_harness.py` with real Connector API calls:
- `read_email` → Gmail API / Outlook Graph API
- `send_email` → same, on your own test account
- Use two accounts: victim (with connectors) and observer (monitors outbound)
- Plant payloads in your own victim account's inbox/Drive before triggering the agent
