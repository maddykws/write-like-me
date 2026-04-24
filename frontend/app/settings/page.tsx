"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { getSession } from "@/lib/auth";
import ProviderSelector from "@/components/ProviderSelector";
import { api } from "@/lib/api";
import type { Session } from "@supabase/supabase-js";
import type { WritingSample } from "@/lib/types";

export default function SettingsPage() {
  const router = useRouter();
  const [session, setSession] = useState<Session | null>(null);
  const [samples, setSamples] = useState<WritingSample[]>([]);
  const [loadingSamples, setLoadingSamples] = useState(true);

  useEffect(() => {
    getSession().then(async (s) => {
      if (!s) { router.replace("/login"); return; }
      setSession(s);
      try {
        const list = await api.samples.list(s.access_token);
        setSamples(list);
      } finally {
        setLoadingSamples(false);
      }
    });
  }, [router]);

  async function handleDelete(id: string) {
    if (!session) return;
    try {
      await api.samples.delete(session.access_token, id);
      setSamples((prev) => prev.filter((s) => s.id !== id));
      toast.success("Sample removed.");
    } catch (e: unknown) {
      toast.error(e instanceof Error ? e.message : "Failed to delete");
    }
  }

  if (!session) return null;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-2xl font-bold text-gray-900">Settings</h1>

      <section className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-base font-semibold text-gray-900 mb-4">AI Provider & API Key</h2>
        <ProviderSelector onChange={() => toast.success("Settings saved.")} />
      </section>

      <section className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <h2 className="text-base font-semibold text-gray-900 mb-1">Writing Samples</h2>
        <p className="text-sm text-gray-500 mb-4">
          {samples.length} sample{samples.length !== 1 ? "s" : ""} in your voice profile.
        </p>

        {loadingSamples ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 bg-gray-100 rounded animate-pulse" />
            ))}
          </div>
        ) : samples.length === 0 ? (
          <p className="text-sm text-gray-400">No samples yet.</p>
        ) : (
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {samples.map((s) => (
              <div key={s.id} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                <p className="flex-1 text-sm text-gray-700 line-clamp-2">{s.content}</p>
                <div className="text-right shrink-0 text-xs text-gray-400">
                  <p>{s.char_count} chars</p>
                  <button
                    onClick={() => handleDelete(s.id)}
                    className="text-red-400 hover:text-red-600 mt-1 transition-colors"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
