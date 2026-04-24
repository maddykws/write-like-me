import type {
  WritingSample,
  VoiceProfile,
  RewriteResult,
  FeedbackResult,
  ValidateKeyResult,
  Provider,
} from "./types";

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function request<T>(
  path: string,
  options: RequestInit & { token?: string }
): Promise<T> {
  const { token, ...init } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string>),
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...init, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  samples: {
    create(token: string, texts: string[]): Promise<WritingSample[]> {
      return request("/samples", {
        method: "POST",
        token,
        body: JSON.stringify({ samples: texts.map((t) => ({ content: t })) }),
      });
    },
    list(token: string): Promise<WritingSample[]> {
      return request("/samples", { method: "GET", token });
    },
    delete(token: string, id: string): Promise<void> {
      return request(`/samples/${id}`, { method: "DELETE", token });
    },
  },

  profile: {
    get(token: string): Promise<VoiceProfile> {
      return request("/profile", { method: "GET", token });
    },
    recompute(token: string): Promise<VoiceProfile> {
      return request("/profile/recompute", { method: "POST", token });
    },
  },

  rewrite: {
    create(
      token: string,
      text: string,
      provider: Provider,
      apiKey: string,
      model?: string
    ): Promise<RewriteResult> {
      return request("/rewrite", {
        method: "POST",
        token,
        body: JSON.stringify({ text, provider, api_key: apiKey, model }),
      });
    },
  },

  feedback: {
    submit(
      token: string,
      rewriteId: string,
      action: "accepted" | "edited" | "rejected",
      editedText?: string
    ): Promise<FeedbackResult> {
      return request("/feedback", {
        method: "POST",
        token,
        body: JSON.stringify({ rewrite_id: rewriteId, action, edited_text: editedText }),
      });
    },
  },

  settings: {
    validateKey(provider: Provider, apiKey: string): Promise<ValidateKeyResult> {
      return request("/settings/validate-key", {
        method: "POST",
        body: JSON.stringify({ provider, api_key: apiKey }),
      });
    },
  },
};
