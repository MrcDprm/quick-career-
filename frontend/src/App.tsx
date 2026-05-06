// AI Optimized by Skills Agent: App shell exposes every planned workflow route before feature internals land.
import { useEffect, useMemo, useState } from "react";

import { AsyncStateBlock } from "./components/AsyncStateBlock";
import { findWorkflowRoute, workflowRoutes, type RouteId, type WorkflowRoute } from "./routes";
import type { WorkflowSnapshot, WorkflowStatus } from "./types/workflow";

type RouteState = {
  status: WorkflowStatus;
  summary: string;
  primaryAction: string;
  snapshots: WorkflowSnapshot[];
};

const routeStates: Record<RouteId, RouteState> = {
  jobAnalysis: {
    status: "empty",
    summary: "No job post has been analyzed in this session.",
    primaryAction: "Analyze job",
    snapshots: [
      { label: "Input", value: "Text or URL" },
      { label: "Output", value: "Role, skills, keywords" },
      { label: "Trace", value: "Pending", tone: "warning" },
    ],
  },
  resumeUpload: {
    status: "empty",
    summary: "No resume profile has been parsed in this session.",
    primaryAction: "Parse resume",
    snapshots: [
      { label: "Input", value: "CV text or file" },
      { label: "Output", value: "ResumeProfile" },
      { label: "Privacy", value: "Raw logs blocked", tone: "good" },
    ],
  },
  matchScore: {
    status: "loading",
    summary: "Match scoring waits for both upstream profiles.",
    primaryAction: "Refresh score",
    snapshots: [
      { label: "Score", value: "--" },
      { label: "Strong matches", value: "Waiting" },
      { label: "Gaps", value: "Waiting" },
    ],
  },
  optimizationReview: {
    status: "ready",
    summary: "Diff rows will render here after the optimizer creates proposed CV changes.",
    primaryAction: "Open diff",
    snapshots: [
      { label: "Sections", value: "Summary, experience, skills" },
      { label: "Review", value: "Approve or reject" },
      { label: "Export", value: "Blocked until approval", tone: "warning" },
    ],
  },
  documentExport: {
    status: "empty",
    summary: "Approved resume outputs will be listed in this route.",
    primaryAction: "Create export",
    snapshots: [
      { label: "Markdown", value: "Pending" },
      { label: "PDF or DOCX", value: "Pending" },
      { label: "Source", value: "Approved optimization", tone: "warning" },
    ],
  },
  applicationSubmit: {
    status: "error",
    summary: "Submission API failures are shown without breaking the workflow shell.",
    primaryAction: "Retry submit",
    snapshots: [
      { label: "Target", value: "Not selected" },
      { label: "Package", value: "Not approved" },
      { label: "Receipt", value: "Unavailable", tone: "warning" },
    ],
  },
  metricsDashboard: {
    status: "ready",
    summary: "Demo metrics will compare manual effort against the automated workflow.",
    primaryAction: "View metrics",
    snapshots: [
      { label: "Manual", value: "85 min" },
      { label: "Automated", value: "17 min", tone: "good" },
      { label: "Reduction", value: "80%", tone: "good" },
    ],
  },
};

export function App() {
  const [pathname, setPathname] = useState(() => window.location.pathname);
  const activeRoute = useMemo(() => findWorkflowRoute(pathname), [pathname]);
  const activeState = routeStates[activeRoute.id];

  useEffect(() => {
    const syncPathname = () => setPathname(window.location.pathname);
    window.addEventListener("popstate", syncPathname);
    return () => window.removeEventListener("popstate", syncPathname);
  }, []);

  function navigateTo(route: WorkflowRoute) {
    window.history.pushState(null, "", route.path);
    setPathname(route.path);
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Workflow navigation">
        <div>
          <p className="brand-kicker">Quick-Career</p>
          <h1>Workflow Console</h1>
        </div>

        <nav className="route-list">
          {workflowRoutes.map((route, index) => (
            <a
              aria-current={activeRoute.id === route.id ? "page" : undefined}
              className="route-link"
              href={route.path}
              key={route.id}
              onClick={(event) => {
                event.preventDefault();
                navigateTo(route);
              }}
            >
              <span>{String(index + 1).padStart(2, "0")}</span>
              {route.shortTitle}
            </a>
          ))}
        </nav>
      </aside>

      <section className="workspace" aria-labelledby="workspace-title">
        <header className="workspace-header">
          <div>
            <p className="eyebrow">{activeRoute.stage}</p>
            <h2 id="workspace-title">{activeRoute.title}</h2>
            <p>{activeState.summary}</p>
          </div>
          <button className="primary-action" type="button">
            {activeState.primaryAction}
          </button>
        </header>

        <section className="snapshot-grid" aria-label={`${activeRoute.title} snapshot`}>
          {activeState.snapshots.map((snapshot) => (
            <article className={`snapshot snapshot--${snapshot.tone ?? "neutral"}`} key={snapshot.label}>
              <span>{snapshot.label}</span>
              <strong>{snapshot.value}</strong>
            </article>
          ))}
        </section>

        <section className="route-detail" aria-label={`${activeRoute.title} route contract`}>
          <dl>
            <div>
              <dt>Route</dt>
              <dd>{activeRoute.path}</dd>
            </div>
            <div>
              <dt>API</dt>
              <dd>{activeRoute.apiPath}</dd>
            </div>
            <div>
              <dt>Depends on</dt>
              <dd>{activeRoute.dependsOn}</dd>
            </div>
          </dl>
        </section>

        <AsyncStateBlock
          actionLabel={activeState.status === "error" ? "Retry" : undefined}
          detail={
            activeState.status === "error"
              ? "Latest request failed. Retry keeps the current workflow context."
              : "Waiting for live workflow data."
          }
          onAction={() => setPathname(activeRoute.path)}
          status={activeState.status}
          title={`${activeRoute.title} state`}
        />
      </section>
    </main>
  );
}
