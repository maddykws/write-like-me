"use client";
import { useState, useEffect } from "react";
import type { Provider, ApiSettings } from "@/lib/types";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

const STORAGE_KEY = "wlm_api_settings";

const MODELS: Record<Provider, { id: string; label: string }[]> = {
  claude: [
    { id: "claude-opus-4-5", label: "Claude Opus 4.5" },
    { id: "claude-sonnet-4-6", label: "Claude Sonnet 4.6 (faster)" },
    { id: "claude-haiku-4-5", label: "Claude Haiku 4.5 (cheapest)" },
  ],
  openai: [
    { id: "gpt-4o", label: "GPT-4o" },
    { id: "gpt-4o-mini", label: "GPT-4o mini (cheaper)" },
  ],
};

interface Props {
  onChange?: (settings: ApiSettings) => void;
}

export default function ProviderSelector({ onChange }: Props) {
  const [provider, setProvider] = useState<Provider>("claude");
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState(MODELS.claude[0].id);
  const [status, setStatus] = useState<"idle" | "checking" | "valid" | "invalid">("idle");
  const [message, setMessage] = useState("");

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const s: ApiSettings = JSON.parse(stored);
        setProvider(s.provider);
        setApiKey(s.apiKey);
        setModel(s.model ?? MODELS[s.provider][0].id);
      }
    } catch {}
  }, []);

  function save(p: Provider, k: string, m: string) {
    const settings: ApiSettings = { provider: p, apiKey: k, model: m };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    onChange?.(settings);
  }

  async function handleValidate() {
    if (!apiKey.trim()) return;
    setStatus("checking");
    try {
      const result = await api.settings.validateKey(provider, apiKey.trim());
      setStatus(result.valid ? "valid" : "invalid");
      setMessage(result.message);
      if (result.valid) save(provider, apiKey.trim(), model);
    } catch (e: unknown) {
      setStatus("invalid");
      setMessage(e instanceof Error ? e.message : "Validation failed");
    }
  }

  function handleProviderChange(p: Provider) {
    setProvider(p);
    setModel(MODELS[p][0].id);
    setStatus("idle");
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        {(["claude", "openai"] as Provider[]).map((p) => (
          <button
            key={p}
            onClick={() => handleProviderChange(p)}
            className={cn(
              "px-4 py-2 rounded-lg border text-sm font-medium transition-colors",
              provider === p
                ? "bg-brand-600 text-white border-brand-600"
                : "bg-white text-gray-700 border-gray-300 hover:border-brand-500"
            )}
          >
            {p === "claude" ? "Claude (Anthropic)" : "OpenAI"}
          </button>
        ))}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          {provider === "claude" ? "Anthropic API Key" : "OpenAI API Key"}
        </label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => { setApiKey(e.target.value); setStatus("idle"); }}
          placeholder={provider === "claude" ? "sk-ant-..." : "sk-..."}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <p className="mt-1 text-xs text-gray-500">Stored in your browser only — never sent to our servers.</p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Model</label>
        <select
          value={model}
          onChange={(e) => { setModel(e.target.value); save(provider, apiKey, e.target.value); }}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        >
          {MODELS[provider].map((m) => (
            <option key={m.id} value={m.id}>{m.label}</option>
          ))}
        </select>
      </div>

      <button
        onClick={handleValidate}
        disabled={!apiKey.trim() || status === "checking"}
        className="px-4 py-2 bg-brand-600 text-white rounded-lg text-sm font-medium disabled:opacity-50 hover:bg-brand-700 transition-colors"
      >
        {status === "checking" ? "Checking…" : "Save & Validate"}
      </button>

      {message && (
        <p className={cn("text-sm", status === "valid" ? "text-green-600" : "text-red-600")}>
          {status === "valid" ? "✓ " : "✗ "}{message}
        </p>
      )}
    </div>
  );
}

export function loadSettings(): ApiSettings | null {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : null;
  } catch {
    return null;
  }
}
