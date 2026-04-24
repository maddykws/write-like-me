"use client";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface Props {
  rewriteId: string;
  rewrittenText: string;
  onFeedback: (
    rewriteId: string,
    action: "accepted" | "edited" | "rejected",
    editedText?: string
  ) => Promise<void>;
  disabled?: boolean;
}

export default function FeedbackBar({ rewriteId, rewrittenText, onFeedback, disabled }: Props) {
  const [mode, setMode] = useState<"idle" | "editing" | "done">("idle");
  const [editedText, setEditedText] = useState(rewrittenText);
  const [loading, setLoading] = useState(false);

  async function handle(action: "accepted" | "edited" | "rejected", text?: string) {
    setLoading(true);
    try {
      await onFeedback(rewriteId, action, text);
      setMode("done");
    } finally {
      setLoading(false);
    }
  }

  if (mode === "done") {
    return (
      <div className="flex items-center gap-2 text-sm text-green-600">
        <span>✓</span>
        <span>Feedback saved — your voice profile has been updated.</span>
      </div>
    );
  }

  if (mode === "editing") {
    return (
      <div className="space-y-2">
        <textarea
          value={editedText}
          onChange={(e) => setEditedText(e.target.value)}
          rows={6}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm resize-y focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <div className="flex gap-2">
          <button
            onClick={() => handle("edited", editedText)}
            disabled={loading}
            className="px-4 py-2 bg-brand-600 text-white text-sm rounded-lg disabled:opacity-50 hover:bg-brand-700 transition-colors"
          >
            {loading ? "Saving…" : "Save edit"}
          </button>
          <button
            onClick={() => setMode("idle")}
            className="px-4 py-2 border border-gray-300 text-gray-700 text-sm rounded-lg hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-500 mr-1">Was this in your voice?</span>
      <button
        onClick={() => handle("accepted")}
        disabled={loading || disabled}
        className="px-3 py-1.5 bg-green-600 text-white text-sm rounded-lg disabled:opacity-50 hover:bg-green-700 transition-colors"
      >
        ✓ Accept
      </button>
      <button
        onClick={() => setMode("editing")}
        disabled={loading || disabled}
        className="px-3 py-1.5 bg-yellow-500 text-white text-sm rounded-lg disabled:opacity-50 hover:bg-yellow-600 transition-colors"
      >
        ✎ Edit
      </button>
      <button
        onClick={() => handle("rejected")}
        disabled={loading || disabled}
        className="px-3 py-1.5 bg-red-500 text-white text-sm rounded-lg disabled:opacity-50 hover:bg-red-600 transition-colors"
      >
        ✗ Reject
      </button>
    </div>
  );
}
