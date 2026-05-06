// AI Optimized by Skills Agent: Shared API client base for future Quick-Career feature modules.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

export class ApiError extends Error {
  readonly status: number;
  readonly path: string;

  constructor(path: string, status: number) {
    super(`API request failed with status ${status}`);
    this.name = "ApiError";
    this.status = status;
    this.path = path;
  }
}

type JsonBody = Record<string, unknown> | unknown[];

// AI Optimized by Skills Agent: Central fetch wrapper keeps failures renderable by every route shell.
export async function apiRequest<TResponse>(
  path: string,
  options: RequestInit & { json?: JsonBody } = {},
): Promise<TResponse> {
  const headers = new Headers(options.headers);

  if (options.json) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    body: options.json ? JSON.stringify(options.json) : options.body,
    headers,
  });

  if (!response.ok) {
    throw new ApiError(path, response.status);
  }

  return response.json() as Promise<TResponse>;
}

export function apiGet<TResponse>(path: string): Promise<TResponse> {
  return apiRequest<TResponse>(path);
}

export function apiPost<TResponse>(path: string, json: JsonBody): Promise<TResponse> {
  return apiRequest<TResponse>(path, { method: "POST", json });
}
