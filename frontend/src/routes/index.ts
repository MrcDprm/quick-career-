// AI Optimized by Skills Agent: Central route metadata keeps the skeleton navigable without adding router dependencies.
import type { WorkflowStage } from "../types/workflow";

export const routes = {
  home: "/",
  jobAnalysis: "/jobs",
  resumeUpload: "/resumes",
  matchScore: "/match",
  optimizationReview: "/optimizations",
  documentExport: "/exports",
  applicationSubmit: "/applications",
  metricsDashboard: "/metrics",
} as const;

export type RouteId = Exclude<keyof typeof routes, "home">;

export type WorkflowRoute = {
  id: RouteId;
  path: (typeof routes)[RouteId];
  title: string;
  shortTitle: string;
  stage: WorkflowStage;
  apiPath: string;
  dependsOn: string;
};

export const workflowRoutes: WorkflowRoute[] = [
  {
    id: "jobAnalysis",
    path: routes.jobAnalysis,
    title: "Job Intake",
    shortTitle: "Job",
    stage: "job-analysis",
    apiPath: "POST /api/jobs/analyze",
    dependsOn: "Raw job text or URL",
  },
  {
    id: "resumeUpload",
    path: routes.resumeUpload,
    title: "Resume Intake",
    shortTitle: "Resume",
    stage: "resume-parsing",
    apiPath: "POST /api/resumes/upload",
    dependsOn: "Pasted CV text or upload",
  },
  {
    id: "matchScore",
    path: routes.matchScore,
    title: "Match Report",
    shortTitle: "Match",
    stage: "match-scoring",
    apiPath: "Job and resume analysis payloads",
    dependsOn: "Job analysis and resume profile",
  },
  {
    id: "optimizationReview",
    path: routes.optimizationReview,
    title: "Optimization Review",
    shortTitle: "Review",
    stage: "cv-optimization",
    apiPath: "GET /api/optimizations/{id}/diff",
    dependsOn: "Optimization run",
  },
  {
    id: "documentExport",
    path: routes.documentExport,
    title: "Export Center",
    shortTitle: "Export",
    stage: "document-export",
    apiPath: "POST /api/optimizations/{id}/export",
    dependsOn: "Approved optimization",
  },
  {
    id: "applicationSubmit",
    path: routes.applicationSubmit,
    title: "Application Submit",
    shortTitle: "Apply",
    stage: "application-submission",
    apiPath: "POST /api/applications/submit",
    dependsOn: "Exported application package",
  },
  {
    id: "metricsDashboard",
    path: routes.metricsDashboard,
    title: "Efficiency Dashboard",
    shortTitle: "Metrics",
    stage: "efficiency-metrics",
    apiPath: "GET /api/metrics/efficiency",
    dependsOn: "Completed workflow events",
  },
];

export function findWorkflowRoute(pathname: string): WorkflowRoute {
  return workflowRoutes.find((route) => route.path === pathname) ?? workflowRoutes[0];
}
