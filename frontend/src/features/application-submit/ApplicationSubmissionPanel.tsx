// AI Optimized by Skills Agent: UI for automatic application submission package and receipt states.
import "./applicationSubmission.css";

export type ApplicationPackage = {
  target: string;
  resumeFileName: string;
  coverLetter: string;
  mode: "mock" | "email" | "platform";
};

export type SubmissionReceipt = {
  status: "queued" | "submitted" | "failed";
  receipt?: string;
  errorMessage?: string;
};

type ApplicationSubmissionPanelProps = {
  applicationPackage: ApplicationPackage;
  receipt?: SubmissionReceipt;
  isSubmitting?: boolean;
  onSubmit: () => void;
};

// AI Optimized by Skills Agent: Completeness check blocks broken packages without asking for manual approval.
function isPackageReady(applicationPackage: ApplicationPackage) {
  return (
    applicationPackage.target.trim().length > 1 &&
    applicationPackage.resumeFileName.trim().length > 3 &&
    applicationPackage.coverLetter.trim().length > 20
  );
}

// AI Optimized by Skills Agent: Shows the final autonomous package and send result in one compact surface.
export function ApplicationSubmissionPanel({
  applicationPackage,
  receipt,
  isSubmitting = false,
  onSubmit,
}: ApplicationSubmissionPanelProps) {
  const packageReady = isPackageReady(applicationPackage);

  return (
    <section className="submission-panel" aria-label="Automatic application submission">
      <header className="submission-header">
        <div>
          <p className="submission-eyebrow">Automatic submission</p>
          <h2>{applicationPackage.target}</h2>
        </div>
        <span className="submission-mode">{applicationPackage.mode}</span>
      </header>

      <dl className="package-summary">
        <div>
          <dt>Resume</dt>
          <dd>{applicationPackage.resumeFileName}</dd>
        </div>
        <div>
          <dt>Cover letter</dt>
          <dd>{applicationPackage.coverLetter}</dd>
        </div>
      </dl>

      {receipt ? (
        <div className={`receipt receipt-${receipt.status}`} role="status">
          <strong>{receipt.status}</strong>
          <span>{receipt.receipt ?? receipt.errorMessage}</span>
        </div>
      ) : null}

      <button type="button" disabled={!packageReady || isSubmitting} onClick={onSubmit}>
        {isSubmitting ? "Submitting..." : "Run automatic submission"}
      </button>
    </section>
  );
}
