export interface PlatformConfig {
  label: string;
  color: string;
  openLabel: string;
}

export const PLATFORM_CONFIG: Record<string, PlatformConfig> = {
  youtube: { label: 'YouTube', color: '#FF0000', openLabel: 'YouTube에서 보기' },
  instagram: { label: 'Instagram', color: '#E4405F', openLabel: 'Instagram에서 보기' },
  threads: { label: 'Threads', color: '#000000', openLabel: 'Threads에서 보기' },
  x: { label: 'X', color: '#000000', openLabel: 'X에서 보기' },
  tiktok: { label: 'TikTok', color: '#010101', openLabel: 'TikTok에서 보기' },
  web: { label: 'Web', color: '#4A90D9', openLabel: '웹에서 보기' },
};

export const CATEGORIES = [
  '개발', '투자', '건강', '교육', '엔터테인먼트', '뉴스', '라이프스타일', '기타',
];

export function getPlatformConfig(mediaType: string): PlatformConfig {
  return PLATFORM_CONFIG[mediaType] || PLATFORM_CONFIG.web;
}
