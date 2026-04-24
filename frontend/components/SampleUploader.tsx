"use client";
import { useState } from "react";
import { cn } from "@/lib/utils";

const MIN_CHARS = 50;
const MAX_SAMPLES = 20;

interface Props {
  onSubmit: (samples: string[]) => Promise<void>;
  loading?: boolean;
}

export default function SampleUploader({ onSubmit, loading }: Props) {
  const [text, setText] = useState("");
  const [samples, setSamples] = useState<string[]>([]);
  const [error, setError] = useState("");

  function addSample() {
    const trimmed = text.trim();
    if (trimmed.length < MIN_CHARS) {
      setError(`Each sample needs at least ${MIN_CHARS} characters.`);
      return;
    }
    if (samples.length >= MAX_SAMPLES) {
      setError(`Maximum ${MAX_SAMPLES} samples allowed.`);
      return;
    }
    setSamples((prev) => [...prev, trimmed]);
    setText("");
    setError("");
  }

  function removeSample(i: number) {
    setSamples((prev) => prev.filter((_, idx) => idx !== i));
  }

  async function handleSubmit() {
    if (samples.length < 5) {
      setError("Add at least 5 writing samples for good results.");
      return;
    }
    setError("");
    await onSubmit(samples);
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Paste a writing sample
        </label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows={6}
          placeholder="Paste an email, blog post, Slack message, tweet thread — anything you've written. The more varied, the better."
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm resize-y focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <div className="flex justify-between items-center mt-1">
          <span className={cn("text-xs", text.length < MIN_CHARS ? "text-gray-400" : "text-green-600")}>
            {text.length} characters
          </span>
          <button
            onClick={addSample}
            disabled={text.trim().length < MIN_CHARS}
            className="px-3 py-1.5 bg-brand-600 text-white text-sm rounded-lg disabled:opacity-40 hover:bg-brand-700 transition-colors"
          >
            + Add sample
          </button>
        </div>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {samples.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-700">{samples.length} sample{samples.length !== 1 ? "s" : ""} added</p>
          {samples.map((s, i) => (
            <div key={i} className="flex items-start gap-2 p-3 bg-gray-50 rounded-lg border border-gray-200">
              <p className="flex-1 text-sm text-gray-700 line-clamp-2">{s}</p>
              <button
                onClick={() => removeSample(i)}
                className="text-gray-400 hover:text-red-500 text-xs shrink-0"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || samples.length < 5}
        className="w-full py-2.5 bg-brand-600 text-white font-medium rounded-lg disabled:opacity-40 hover:bg-brand-700 transition-colors"
      >
        {loading ? "Building your voice profile…" : `Analyze my writing style (${samples.length}/5+ samples)`}
      </button>
    </div>
  );
}
