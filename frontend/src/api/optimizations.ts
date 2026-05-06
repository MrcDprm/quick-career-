// AI Optimized by Skills Agent: Typed optimization client mirrors the QC-007 backend contract.
import { apiPost } from "./client";

export type OptimizationStatus =
  | "draft"
  | "optimizing"
  | "finalized"
  | "exported"
  | "submitted"
  | "failed";

export type OptimizationDiffItem = {
  section: string;
  before: string;
  after: string;
  reason: string;
};

export type OptimizationRunResponse = {
  id: string;
  status: OptimizationStatus;
  target_role: string;
  match_score_before: number;
  match_score_after: number;
  diff: OptimizationDiffItem[];
  highlighted_skills: string[];
  ats_resume_markdown: string;
  application_brief: string;
};

export type OptimizationRequest = {
  target_role: string;
  resume_text: string;
  job_keywords: string[];
  job_post_id?: string | null;
  candidate_brief?: string;
  candidate_name?: string;
};

export function createOptimization(payload: OptimizationRequest) {
  return apiPost<OptimizationRequest, OptimizationRunResponse>("/optimizations/", payload);
}
