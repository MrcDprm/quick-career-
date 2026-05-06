// AI Optimized by Skills Agent: Shared app shell gives every workflow screen a consistent frame.
import type { ReactNode } from "react";

type AppShellProps = {
  children: ReactNode;
};

// AI Optimized by Skills Agent: Keeps navigation compact for an operational hackathon MVP UI.
export function AppShell({ children }: AppShellProps) {
  return (
    <main className="app-shell">
      <header className="topbar" aria-label="Quick-Career workspace">
        <div>
          <p className="eyebrow">Quick-Career MVP</p>
          <h1>Autonomous career workflow</h1>
        </div>
        <span className="status-pill">Mock AI ready</span>
      </header>
      {children}
    </main>
  );
}
