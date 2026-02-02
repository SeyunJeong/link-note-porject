import axios from 'axios';
import { Link, LinkListResponse } from '../types/link';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const linkApi = {
  saveLink: async (url: string): Promise<Link> => {
    const response = await api.post<Link>('/links/save', { url });
    return response.data;
  },

  getLinks: async (limit = 50, offset = 0): Promise<LinkListResponse> => {
    const response = await api.get<LinkListResponse>('/links/', {
      params: { limit, offset },
    });
    return response.data;
  },

  getLink: async (id: string): Promise<Link> => {
    const response = await api.get<Link>(`/links/${id}`);
    return response.data;
  },
};

export const setApiBaseUrl = (url: string) => {
  api.defaults.baseURL = url;
};
