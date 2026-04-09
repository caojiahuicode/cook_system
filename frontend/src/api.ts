const BASE = '';

async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${url}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export interface TaskStatus {
  id: number;
  title: string | null;
  status: 'processing' | 'generating' | 'completed' | 'failed';
  status_text: string;
  progress: number;
  time_left: string;
  thumbnail: string | null;
  stats: { words: number; images: number } | null;
  created_at: string;
}

export interface RecipeListItem {
  id: number;
  title: string;
  category: string | null;
  date: string;
  time: string;
  image: string | null;
  tag_color: string;
}

export interface RecipeDetail {
  id: number;
  title: string;
  tags: string[];
  video_link: string;
  time: string;
  ingredients: { name: string; amount: string }[];
  tools: { name: string; icon: string }[];
  steps: { number: number; title: string; content: string; image: string | null; timestamp: string | null }[];
  tip: string;
  category: string | null;
  created_at: string;
}

export const api = {
  createRecipe(url: string) {
    return request<{ id: number; status: string }>('/api/recipes', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
  },

  listTasks() {
    return request<TaskStatus[]>('/api/tasks');
  },

  getRecipeStatus(id: number) {
    return request<TaskStatus>(`/api/recipes/${id}/status`);
  },

  listRecipes(category?: string) {
    const params = category && category !== '全部' ? `?category=${encodeURIComponent(category)}` : '';
    return request<{ recipes: RecipeListItem[]; total: number }>(`/api/recipes${params}`);
  },

  getRecipe(id: number) {
    return request<RecipeDetail>(`/api/recipes/${id}`);
  },

  deleteRecipe(id: number) {
    return request<{ ok: boolean }>(`/api/recipes/${id}`, { method: 'DELETE' });
  },
};
