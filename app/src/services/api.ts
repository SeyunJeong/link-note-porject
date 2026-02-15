import axios from 'axios';
import { Link, LinkListResponse } from '../types/link';
import { config } from '../config';
import { supabase } from './supabase';

const API_BASE_URL = config.apiBaseUrl;

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request 인터셉터: Bearer 토큰 자동 첨부
api.interceptors.request.use(async (requestConfig) => {
  const { data: { session } } = await supabase.auth.getSession();
  if (session?.access_token) {
    requestConfig.headers.Authorization = `Bearer ${session.access_token}`;
  }
  return requestConfig;
});

// Response 인터셉터: 401 시 토큰 갱신 후 재요청
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 401이고 아직 재시도하지 않은 경우
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const { data, error: refreshError } = await supabase.auth.refreshSession();

      if (refreshError || !data.session) {
        // 갱신 실패 → 로그아웃 처리
        await supabase.auth.signOut();
        return Promise.reject(error);
      }

      // 갱신된 토큰으로 재요청
      originalRequest.headers.Authorization = `Bearer ${data.session.access_token}`;
      return api(originalRequest);
    }

    return Promise.reject(error);
  }
);

export const linkApi = {
  saveLink: async (url: string): Promise<Link> => {
    const response = await api.post<Link>('/links/save', { url });
    return response.data;
  },

  getLinks: async (
    limit = 50,
    offset = 0,
    mediaType?: string | null,
    category?: string | null,
  ): Promise<LinkListResponse> => {
    const params: Record<string, string | number> = { limit, offset };
    if (mediaType) params.media_type = mediaType;
    if (category) params.category = category;
    const response = await api.get<LinkListResponse>('/links/', { params });
    return response.data;
  },

  getLink: async (id: string): Promise<Link> => {
    const response = await api.get<Link>(`/links/${id}`);
    return response.data;
  },

  deleteLink: async (id: string): Promise<void> => {
    await api.delete(`/links/${id}`);
  },
};

export const setApiBaseUrl = (url: string) => {
  api.defaults.baseURL = url;
};
