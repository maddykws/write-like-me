"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { getSession } from "@/lib/auth";
import { api } from "@/lib/api";
import { loadSettings } from "@/components/ProviderSelector";
import RewriteEditor from "@/components/RewriteEditor";
import type { Session } from "@supabase/supabase-js";
import type { RewriteResult } from "@/lib/types";
import Link from "next/link";

export default function RewritePage() {
  const router = useRouter();
  const [session, setSession] = useState<Session | null>(null);

  useEffect(() => {
    getSession().then((s) => {
      if (!s) router.replace("/login");
      else setSession(s);
    });
  }, [router]);

  async function handleRewrite(text: string): Promise<RewriteResult> {
    if (!session) throw new Error("Not authenticated");
    const settings = loadSettings();
    if (!settings?.apiKey) {
      throw new Error("No API key set. Go to Settings to add your key.");
    }
    return api.rewrite.create(
      session.access_token,
      text,
      settings.provider,
      settings.apiKey,
      settings.model
    );
  }

  async function handleFeedback(
    rewriteId: string,
    action: "accepted" | "edited" | "rejected",
    editedText?: string
  ) {
    if (!session) return;
    try {
      await api.feedback.submit(session.access_token, rewriteId, action, editedText);
      if (action !== "rejected") {
        toast.success("Voice profile updated with your feedback.");
      }
    } catch (e: unknown) {
      toast.error(e instanceof Error ? e.message : "Failed to save feedback");
    }
  }

  if (!session) return null;

  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Rewrite</h1>
          <p className="text-sm text-gray-500">Paste any text and get it back in your voice.</p>
        </div>
        <Link
          href="/settings"
          className="text-sm text-gray-500 hover:text-brand-600 transition-colors"
        >
          ⚙ Settings
        </Link>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <RewriteEditor onRewrite={handleRewrite} onFeedback={handleFeedback} />
      </div>
    </div>
  );
}
