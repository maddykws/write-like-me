"use client";
import { useState } from "react";
import DiffView from "./DiffView";
import FeedbackBar from "./FeedbackBar";
import type { RewriteResult } from "@/lib/types";
import { cn } from "@/lib/utils";

interface Props {
  onRewrite: (text: string) => Promise<RewriteResult>;
  onFeedback: (
    rewriteId: string,
    action: "accepted" | "edited" | "rejected",
    editedText?: string
  ) => Promise<void>;
}

type ViewMode = "side-by-side" | "diff";

export default function RewriteEditor({ onRewrite, onFeedback }: Props) {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<RewriteResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [viewMode, setViewMode] = useState<ViewMode>("side-by-side");

  async function handleRewrite() {
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const r = await onRewrite(input.trim());
      setResult(r);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Rewrite failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      {/* Input pane */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Your text</label>
        <textarea
          value={input}
          onChange={(e) => { setInput(e.target.value); setResult(null); }}
          rows={8}
          placeholder="Paste any text here — an email draft, a message, a paragraph — and we'll rewrite it in your voice."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm resize-y focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <div className="flex justify-end mt-2">
          <button
            onClick={handleRewrite}
            disabled={!input.trim() || loading}
            className="px-5 py-2 bg-brand-600 text-white font-medium rounded-lg disabled:opacity-40 hover:bg-brand-700 transition-colors"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="animate-spin">⟳</span> Rewriting…
              </span>
            ) : (
              "Rewrite in my voice →"
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-700">
          {error}
        </div>
      )}

      {loading && (
        <div className="space-y-2">
          <div className="h-4 bg-gray-200 rounded animate-pulse w-3/4" />
          <div className="h-4 bg-gray-200 rounded animate-pulse w-full" />
          <div className="h-4 bg-gray-200 rounded animate-pulse w-5/6" />
          <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3" />
        </div>
      )}

      {result && !loading && (
        <div className="space-y-4">
          {/* View toggle */}
          <div className="flex gap-1 text-sm border border-gray-200 rounded-lg p-1 w-fit">
            {(["side-by-side", "diff"] as ViewMode[]).map((m) => (
              <button
                key={m}
                onClick={() => setViewMode(m)}
                className={cn(
                  "px-3 py-1 rounded-md transition-colors",
                  viewMode === m ? "bg-brand-600 text-white" : "text-gray-600 hover:bg-gray-100"
                )}
              >
                {m === "side-by-side" ? "Side by side" : "Show changes"}
              </button>
            ))}
          </div>

          {viewMode === "side-by-side" ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Original</p>
                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 text-sm text-gray-700 whitespace-pre-wrap">
                  {result.original_text}
                </div>
              </div>
              <div>
                <p className="text-xs font-medium text-brand-600 uppercase tracking-wide mb-2">In your voice</p>
                <div className="p-4 bg-brand-50 rounded-lg border border-brand-200 text-sm text-gray-900 whitespace-pre-wrap">
                  {result.rewritten_text}
                </div>
              </div>
            </div>
          ) : (
            <div>
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">Changes</p>
              <DiffView original={result.original_text} rewritten={result.rewritten_text} />
            </div>
          )}

          <FeedbackBar
            rewriteId={result.rewrite_id}
            rewrittenText={result.rewritten_text}
            onFeedback={onFeedback}
          />
        </div>
      )}
    </div>
  );
}
