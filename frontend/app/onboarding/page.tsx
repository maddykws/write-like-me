"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { getSession } from "@/lib/auth";
import { api } from "@/lib/api";
import SampleUploader from "@/components/SampleUploader";
import type { Session } from "@supabase/supabase-js";

export default function OnboardingPage() {
  const router = useRouter();
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getSession().then((s) => {
      if (!s) router.replace("/login");
      else setSession(s);
    });
  }, [router]);

  async function handleSamples(samples: string[]) {
    if (!session) return;
    setLoading(true);
    try {
      await api.samples.create(session.access_token, samples);
      toast.success("Voice profile created! Let's try a rewrite.");
      router.replace("/rewrite");
    } catch (e: unknown) {
      toast.error(e instanceof Error ? e.message : "Failed to save samples");
    } finally {
      setLoading(false);
    }
  }

  if (!session) return null;

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Teach me your voice</h1>
        <p className="text-gray-600">
          Paste 5–20 things you&apos;ve written — emails, messages, posts, anything.
          The more varied, the better. We&apos;ll learn your unique style from them.
        </p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <SampleUploader onSubmit={handleSamples} loading={loading} />
      </div>

      <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
        <p className="text-sm text-amber-800">
          <strong>Good samples:</strong> casual emails, Slack messages, blog posts, tweets, notes to yourself.
          Mix short and long pieces for the best voice profile.
        </p>
      </div>
    </div>
  );
}
