// AI Optimized by Skills Agent: Shared workflow type mirrors the autonomous product stages.
export type WorkflowStage =
  | "job-analysis"
  | "resume-parsing"
  | "match-scoring"
  | "cv-optimization"
  | "document-export"
  | "application-submission"
  | "efficiency-metrics";

export type WorkflowStatus = "empty" | "loading" | "ready" | "error";

export type WorkflowSnapshot = {
  label: string;
  value: string;
  tone?: "neutral" | "good" | "warning";
};
