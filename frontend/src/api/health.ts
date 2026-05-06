// AI Optimized by Skills Agent: Health API contract validates frontend-backend connectivity.
import { apiGet } from "./client";

export type HealthResponse = {
  status: string;
  service: string;
  version: string;
};

// AI Optimized by Skills Agent: Small typed request used by the app shell smoke state.
export function getHealth() {
  return apiGet<HealthResponse>("/health");
}
