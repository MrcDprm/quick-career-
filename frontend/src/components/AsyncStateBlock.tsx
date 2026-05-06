// AI Optimized by Skills Agent: Shared async-state block keeps loading, error and empty screens consistent.
import type { WorkflowStatus } from "../types/workflow";

type AsyncStateBlockProps = {
  status: WorkflowStatus;
  title: string;
  detail: string;
  actionLabel?: string;
  onAction?: () => void;
};

export function AsyncStateBlock({
  status,
  title,
  detail,
  actionLabel,
  onAction,
}: AsyncStateBlockProps) {
  return (
    <section className={`state-block state-block--${status}`} aria-live="polite">
      <div className="state-indicator" aria-hidden="true" />
      <div>
        <p className="state-label">{status}</p>
        <h2>{title}</h2>
        <p>{detail}</p>
        {actionLabel ? (
          <button className="secondary-action" type="button" onClick={onAction}>
            {actionLabel}
          </button>
        ) : null}
      </div>
    </section>
  );
}
