-- Write Like Me — Initial Schema
-- Run this in your Supabase SQL editor after enabling the pgvector extension

CREATE EXTENSION IF NOT EXISTS vector;

-- Mirror of auth.users for app-level metadata
CREATE TABLE users (
  id         UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  provider   TEXT DEFAULT 'claude',
  onboarded  BOOLEAN DEFAULT FALSE
);

-- Trigger: auto-insert row on new Supabase auth signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.users (id) VALUES (NEW.id);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Writing samples with 384-dim embeddings (all-MiniLM-L6-v2)
CREATE TABLE writing_samples (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  content    TEXT NOT NULL,
  char_count INT,
  embedding  VECTOR(384)
);

CREATE INDEX ON writing_samples USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Aggregated voice profile per user
CREATE TABLE voice_profiles (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id               UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  updated_at            TIMESTAMPTZ DEFAULT NOW(),
  sample_count          INT DEFAULT 0,
  avg_sentence_length   FLOAT,
  formality_score       FLOAT,      -- 0.0 casual → 1.0 formal (Heylighen & Dewaele)
  type_token_ratio      FLOAT,      -- MATTR 50-token window
  punct_signature       JSONB,      -- em_dash, ellipsis, semicolon, colon, parens per 1000 chars
  preferred_connectives TEXT[],
  summary_prompt        TEXT        -- cached NL style description for LLM system prompt
);

-- Rewrite history
CREATE TABLE rewrites (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id        UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at     TIMESTAMPTZ DEFAULT NOW(),
  original_text  TEXT NOT NULL,
  rewritten_text TEXT NOT NULL,
  provider       TEXT NOT NULL,    -- 'claude' | 'openai'
  model          TEXT NOT NULL,
  few_shot_ids   UUID[],           -- writing_samples used as few-shot examples
  status         TEXT DEFAULT 'pending'  -- 'pending' | 'accepted' | 'edited' | 'rejected'
);

-- User feedback on rewrites
CREATE TABLE feedback (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  rewrite_id  UUID UNIQUE NOT NULL REFERENCES rewrites(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  action      TEXT NOT NULL,    -- 'accepted' | 'edited' | 'rejected'
  edited_text TEXT              -- only set when action = 'edited'
);

-- Row Level Security: each user can only access their own data
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE writing_samples ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE rewrites ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users: own row" ON users
  FOR ALL USING (id = auth.uid());

CREATE POLICY "writing_samples: own rows" ON writing_samples
  FOR ALL USING (user_id = auth.uid());

CREATE POLICY "voice_profiles: own row" ON voice_profiles
  FOR ALL USING (user_id = auth.uid());

CREATE POLICY "rewrites: own rows" ON rewrites
  FOR ALL USING (user_id = auth.uid());

CREATE POLICY "feedback: own rows" ON feedback
  FOR ALL USING (user_id = auth.uid());

-- pgvector similarity search RPC (called by retrieval.py)
CREATE OR REPLACE FUNCTION match_writing_samples(
  query_embedding VECTOR(384),
  match_user_id   UUID,
  match_count     INT DEFAULT 6
)
RETURNS TABLE (
  id         UUID,
  content    TEXT,
  similarity FLOAT
)
LANGUAGE SQL STABLE AS $$
  SELECT
    id,
    content,
    1 - (embedding <=> query_embedding) AS similarity
  FROM writing_samples
  WHERE user_id = match_user_id
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
