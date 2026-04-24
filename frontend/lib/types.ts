export type Provider = "claude" | "openai";

export interface WritingSample {
  id: string;
  content: string;
  char_count: number;
  created_at: string;
}

export interface PunctSignature {
  em_dash: number;
  ellipsis: number;
  semicolon: number;
  colon: number;
  parens: number;
}

export interface VoiceProfile {
  sample_count: number;
  avg_sentence_length: number | null;
  formality_score: number | null;
  type_token_ratio: number | null;
  punct_signature: PunctSignature | null;
  preferred_connectives: string[] | null;
  summary_prompt: string | null;
  updated_at: string | null;
}

export interface RewriteResult {
  rewrite_id: string;
  original_text: string;
  rewritten_text: string;
  provider: Provider;
  model: string;
}

export interface FeedbackResult {
  feedback_id: string;
  action: string;
  sample_added: boolean;
}

export interface ValidateKeyResult {
  valid: boolean;
  message: string;
}

export interface ApiSettings {
  provider: Provider;
  apiKey: string;
  model?: string;
}
