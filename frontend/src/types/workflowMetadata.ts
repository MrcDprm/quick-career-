// AI Optimized by Skills Agent: Workflow metadata keeps route labels and descriptions centralized.
import type { WorkflowStage } from "./workflow";

export type WorkflowStep = {
  stage: WorkflowStage;
  label: string;
  description: string;
};

// AI Optimized by Skills Agent: Describes the full autonomous flow without hard-coding strings in views.
export const workflowSteps: WorkflowStep[] = [
  {
    stage: "job-analysis",
    label: "Job Analysis",
    description: "Extract role, seniority, required skills and keywords from a job post.",
  },
  {
    stage: "resume-parsing",
    label: "Resume Parsing",
    description: "Convert CV content into a structured candidate profile.",
  },
  {
    stage: "match-scoring",
    label: "Match Scoring",
    description: "Score fit and identify the highest-impact improvement gaps.",
  },
  {
    stage: "cv-optimization",
    label: "Autonomous CV Optimization",
    description: "Rewrite the CV for the target job and record an automation diff.",
  },
  {
    stage: "document-export",
    label: "Document Export",
    description: "Generate Markdown and document outputs after optimization finalizes.",
  },
  {
    stage: "application-submission",
    label: "Automatic Application",
    description: "Submit the optimized package through the configured adapter.",
  },
  {
    stage: "efficiency-metrics",
    label: "Efficiency Metrics",
    description: "Prove repetitive-work reduction against the manual baseline.",
  },
];
