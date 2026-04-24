"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { getSession } from "@/lib/auth";
import { api } from "@/lib/api";
import VoiceProfileCard from "@/components/VoiceProfileCard";
import StyleMetricsPanel from "@/components/StyleMetricsPanel";
import type { Session } from "@supabase/supabase-js";
import type { VoiceProfile } from "@/lib/types";
import Link from "next/link";

export default function DashboardPage() {
  const router = useRouter();
  const [session, setSession] = useState<Session | null>(null);
  const [profile, setProfile] = useState<VoiceProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSession().then(async (s) => {
      if (!s) { router.replace("/login"); return; }
      setSession(s);
      try {
        const p = await api.profile.get(s.access_token);
        setProfile(p);
      } catch {
        // No profile yet
      } finally {
        setLoading(false);
      }
    });
  }, [router]);

  async function handleRecompute() {
    if (!session) return;
    try {
      const p = await api.profile.recompute(session.access_token);
      setProfile(p);
      toast.success("Profile recomputed.");
    } catch (e: unknown) {
      toast.error(e instanceof Error ? e.message : "Failed to recompute");
    }
  }

  if (!session || loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-4">
        <div className="h-8 bg-gray-200 rounded animate-pulse w-48" />
        <div className="h-32 bg-gray-200 rounded animate-pulse" />
        <div className="h-48 bg-gray-200 rounded animate-pulse" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12 text-center">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">No voice profile yet</h1>
        <p className="text-gray-500 mb-6">Add writing samples to build your profile.</p>
        <Link href="/onboarding" className="px-5 py-2.5 bg-brand-600 text-white rounded-lg font-medium hover:bg-brand-700 transition-colors">
          Get started →
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={handleRecompute}
          className="text-sm text-gray-500 hover:text-brand-600 transition-colors"
        >
          ↻ Recompute profile
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <VoiceProfileCard profile={profile} />
      </div>

      <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
        <StyleMetricsPanel profile={profile} />
      </div>
    </div>
  );
}
