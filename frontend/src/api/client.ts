// AI Optimized by Skills Agent: Shared API client base for future Quick-Career feature modules.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

// AI Optimized by Skills Agent: Central fetch wrapper keeps retries and tracing easy to add later.
export async function apiGet<TResponse>(path: string): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(await readApiError(response));
  }

  return response.json() as Promise<TResponse>;
}

// AI Optimized by Skills Agent: Shared POST wrapper keeps feature modules focused on typed payloads.
export async function apiPost<TRequest, TResponse>(
  path: string,
  payload: TRequest,
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(await readApiError(response));
  }

  return response.json() as Promise<TResponse>;
}

// AI Optimized by Skills Agent: Converts FastAPI error payloads into Turkish UI-ready messages.
async function readApiError(response: Response) {
  try {
    const payload = (await response.json()) as { detail?: string };
    if (payload.detail) {
      return payload.detail;
    }
  } catch {
    return `API isteği ${response.status} durum koduyla başarısız oldu.`;
  }

  return `API isteği ${response.status} durum koduyla başarısız oldu.`;
}
