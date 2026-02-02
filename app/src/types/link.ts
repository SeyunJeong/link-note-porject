export interface Link {
  id: string;
  url: string;
  title: string;
  thumbnail: string | null;
  summary: string;
  tags: string[];
  category: string | null;
  created_at: string;
}

export interface LinkListResponse {
  links: Link[];
  total: number;
}
