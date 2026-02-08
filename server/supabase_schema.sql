-- Supabase 테이블 생성 SQL
-- Supabase Dashboard > SQL Editor 에서 실행

-- UUID 확장 활성화
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- links 테이블 생성
CREATE TABLE IF NOT EXISTS links (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  thumbnail TEXT,
  summary TEXT NOT NULL,
  tags TEXT[] DEFAULT '{}',
  category TEXT,
  user_id UUID NOT NULL REFERENCES auth.users(id),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_links_category ON links(category);
CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id);
CREATE INDEX IF NOT EXISTS idx_links_user_id_created_at ON links(user_id, created_at DESC);

-- RLS (Row Level Security) 활성화
ALTER TABLE links ENABLE ROW LEVEL SECURITY;

-- 사용자별 접근 정책
CREATE POLICY "Users read own links" ON links
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users insert own links" ON links
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users delete own links" ON links
  FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================
-- 마이그레이션 SQL (기존 테이블에 user_id 추가 시)
-- ============================================================
-- ALTER TABLE links ADD COLUMN user_id UUID REFERENCES auth.users(id);
-- UPDATE links SET user_id = '<your-user-uuid>' WHERE user_id IS NULL;
-- ALTER TABLE links ALTER COLUMN user_id SET NOT NULL;
-- CREATE INDEX idx_links_user_id ON links(user_id);
-- CREATE INDEX idx_links_user_id_created_at ON links(user_id, created_at DESC);
-- DROP POLICY IF EXISTS "Enable all access for all users" ON links;
