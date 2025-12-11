import { Article, Insights } from '../types';

// Use env var or default to localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function fetchNews(
  limit: number = 500,
  threatType?: string,
  search?: string
): Promise<Article[]> {
  const params = new URLSearchParams();
  params.append('limit', limit.toString());

  if (threatType) {
    params.append('threat_type', threatType);
  }

  if (search) {
    params.append('search', search);
  }

  const response = await fetch(`${API_BASE_URL}/api/news?${params.toString()}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch news: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchInsights(): Promise<Insights> {
  const response = await fetch(`${API_BASE_URL}/api/insights`);

  if (!response.ok) {
    throw new Error(`Failed to fetch insights: ${response.statusText}`);
  }

  return response.json();
}

export async function refreshData(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/refresh`, {
    method: 'POST'
  });

  if (!response.ok) {
    throw new Error(`Failed to refresh data: ${response.statusText}`);
  }
}
