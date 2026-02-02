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
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_links_category ON links(category);

-- RLS (Row Level Security) 활성화
ALTER TABLE links ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽기/쓰기 가능하도록 정책 설정 (개인용 앱)
CREATE POLICY "Enable all access for all users" ON links
  FOR ALL
  USING (true)
  WITH CHECK (true);
