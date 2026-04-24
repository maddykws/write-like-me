"use client";
import { diffWords, type Change } from "diff";
import { cn } from "@/lib/utils";

interface Props {
  original: string;
  rewritten: string;
}

export default function DiffView({ original, rewritten }: Props) {
  const changes: Change[] = diffWords(original, rewritten);

  return (
    <div className="font-mono text-sm leading-relaxed p-4 bg-gray-50 rounded-lg border border-gray-200 whitespace-pre-wrap">
      {changes.map((change, i) => {
        if (change.removed) {
          return (
            <span key={i} className="bg-red-100 text-red-700 line-through">
              {change.value}
            </span>
          );
        }
        if (change.added) {
          return (
            <span key={i} className="bg-green-100 text-green-700">
              {change.value}
            </span>
          );
        }
        return <span key={i} className="text-gray-700">{change.value}</span>;
      })}
    </div>
  );
}
