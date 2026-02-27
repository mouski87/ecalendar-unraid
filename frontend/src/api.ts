const API = "/api";

export type Event = {
  id: number;
  title: string;
  description: string | null;
  start: string;
  end: string;
  all_day: boolean;
  recurrence: string | null;
  category_id: number | null;
};

export type Chore = {
  id: number;
  title: string;
  description: string | null;
  assignee: string | null;
  due_date: string | null;
  completed: boolean;
  completed_at: string | null;
  category_id: number | null;
};

export type TodoList = {
  id: number;
  title: string;
  color: string | null;
  category_id: number | null;
};

export type TodoItem = {
  id: number;
  list_id: number;
  title: string;
  completed: boolean;
  sort_order: number;
};

export type Category = {
  id: number;
  name: string;
  color: string;
};

export type Weather = {
  temp: number;
  feels_like: number;
  description: string;
  icon: string;
  humidity: number;
  wind_speed: number;
  city: string;
};

async function req<T>(path: string, opts?: RequestInit): Promise<T> {
  const r = await fetch(API + path, {
    ...opts,
    headers: { "Content-Type": "application/json", ...opts?.headers },
  });
  if (!r.ok) throw new Error(await r.text());
  if (r.status === 204) return {} as T;
  return r.json();
}

export const eventsApi = {
  list: (start?: string, end?: string) => {
    const p = new URLSearchParams();
    if (start) p.set("start", start);
    if (end) p.set("end", end);
    return req<Event[]>(`/events${p.toString() ? "?" + p : ""}`);
  },
  create: (e: Partial<Event>) => req<Event>("/events", { method: "POST", body: JSON.stringify(e) }),
  get: (id: number) => req<Event>(`/events/${id}`),
  update: (id: number, e: Partial<Event>) => req<Event>(`/events/${id}`, { method: "PATCH", body: JSON.stringify(e) }),
  delete: (id: number) => req<void>(`/events/${id}`, { method: "DELETE" }),
};

export const choresApi = {
  list: (params?: { completed?: boolean; assignee?: string }) => {
    const p = new URLSearchParams();
    if (params?.completed != null) p.set("completed", String(params.completed));
    if (params?.assignee) p.set("assignee", params.assignee);
    return req<Chore[]>(`/chores${p.toString() ? "?" + p : ""}`);
  },
  create: (c: Partial<Chore>) => req<Chore>("/chores", { method: "POST", body: JSON.stringify(c) }),
  get: (id: number) => req<Chore>(`/chores/${id}`),
  update: (id: number, c: Partial<Chore>) => req<Chore>(`/chores/${id}`, { method: "PATCH", body: JSON.stringify(c) }),
  delete: (id: number) => req<void>(`/chores/${id}`, { method: "DELETE" }),
};

export const listsApi = {
  list: () => req<TodoList[]>("/lists"),
  create: (l: Partial<TodoList>) => req<TodoList>("/lists", { method: "POST", body: JSON.stringify(l) }),
  delete: (id: number) => req<void>(`/lists/${id}`, { method: "DELETE" }),
  items: (listId: number) => req<TodoItem[]>(`/lists/${listId}/items`),
  addItem: (listId: number, title: string, sortOrder = 0) =>
    req<TodoItem>(`/lists/${listId}/items`, { method: "POST", body: JSON.stringify({ title, sort_order: sortOrder }) }),
  updateItem: (listId: number, itemId: number, u: Partial<TodoItem>) =>
    req<TodoItem>(`/lists/${listId}/items/${itemId}`, { method: "PATCH", body: JSON.stringify(u) }),
  deleteItem: (listId: number, itemId: number) =>
    req<void>(`/lists/${listId}/items/${itemId}`, { method: "DELETE" }),
};

export const categoriesApi = {
  list: () => req<Category[]>("/categories"),
  create: (c: Partial<Category>) => req<Category>("/categories", { method: "POST", body: JSON.stringify(c) }),
  delete: (id: number) => req<void>(`/categories/${id}`, { method: "DELETE" }),
};

export const weatherApi = {
  get: (city?: string, lat?: number, lon?: number) => {
    const p = new URLSearchParams();
    if (city) p.set("city", city);
    if (lat != null) p.set("lat", String(lat));
    if (lon != null) p.set("lon", String(lon));
    return req<Weather>(`/weather?${p}`);
  },
};
