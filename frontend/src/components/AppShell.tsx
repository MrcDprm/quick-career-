// AI Optimized by Skills Agent: Shared app shell gives every workflow screen a consistent frame.
import type { ReactNode } from "react";

type AppShellProps = {
  children: ReactNode;
};

// AI Optimized by Skills Agent: Keeps navigation compact for an operational hackathon MVP UI.
export function AppShell({ children }: AppShellProps) {
  return (
    <main className="app-shell">
      <header className="topbar" aria-label="Quick-Career çalışma alanı">
        <div>
          <p className="eyebrow">Quick-Career MVP</p>
          <h1>Otonom kariyer iş akışı</h1>
        </div>
        <span className="status-pill">AI adaptörü hazır</span>
      </header>
      {children}
    </main>
  );
}
