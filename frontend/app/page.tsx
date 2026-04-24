"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getSession } from "@/lib/auth";
import { api } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    (async () => {
      const session = await getSession();
      if (!session) {
        router.replace("/login");
        return;
      }
      // Check if user has completed onboarding
      try {
        const profile = await api.profile.get(session.access_token);
        if (profile.sample_count >= 5) {
          router.replace("/rewrite");
        } else {
          router.replace("/onboarding");
        }
      } catch {
        router.replace("/onboarding");
      }
    })();
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="animate-pulse text-gray-400">Loading…</div>
    </div>
  );
}
