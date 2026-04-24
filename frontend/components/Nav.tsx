"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { signOut } from "@/lib/auth";
import { cn } from "@/lib/utils";

const LINKS = [
  { href: "/rewrite", label: "Rewrite" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/settings", label: "Settings" },
];

export default function Nav() {
  const path = usePathname();
  const isAuth = !path.startsWith("/login") && !path.startsWith("/signup");

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="font-semibold text-brand-600 text-lg">
          Write Like Me
        </Link>
        {isAuth && (
          <div className="flex items-center gap-1">
            {LINKS.map((l) => (
              <Link
                key={l.href}
                href={l.href}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-sm transition-colors",
                  path.startsWith(l.href)
                    ? "bg-brand-50 text-brand-700 font-medium"
                    : "text-gray-600 hover:bg-gray-100"
                )}
              >
                {l.label}
              </Link>
            ))}
            <button
              onClick={() => signOut().then(() => (window.location.href = "/login"))}
              className="ml-2 px-3 py-1.5 text-sm text-gray-500 hover:text-gray-700 transition-colors"
            >
              Sign out
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
