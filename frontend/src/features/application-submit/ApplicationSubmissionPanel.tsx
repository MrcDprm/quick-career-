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

// AI Optimized by Skills Agent: İngilizce enum değerlerini Türkçe görünür etiketlere çevirir.
function statusLabel(status: SubmissionReceipt["status"]) {
  const labels: Record<SubmissionReceipt["status"], string> = {
    queued: "Sırada",
    submitted: "Gönderildi",
    failed: "Başarısız",
  };
  return labels[status];
}

// AI Optimized by Skills Agent: Başvuru kanalını kullanıcıya teknik enum yerine anlaşılır gösterir.
function modeLabel(mode: ApplicationPackage["mode"]) {
  const labels: Record<ApplicationPackage["mode"], string> = {
    mock: "Demo",
    email: "E-posta",
    platform: "LinkedIn",
  };
  return labels[mode];
}

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
    <section className="submission-panel" aria-label="Otomatik başvuru gönderimi">
      <header className="submission-header">
        <div>
          <p className="submission-eyebrow">Otomatik başvuru</p>
          <h2>{applicationPackage.target}</h2>
        </div>
        <span className="submission-mode">{modeLabel(applicationPackage.mode)}</span>
      </header>

      <dl className="package-summary">
        <div>
          <dt>CV</dt>
          <dd>{applicationPackage.resumeFileName}</dd>
        </div>
        <div>
          <dt>Genel bilgilendirme</dt>
          <dd>{applicationPackage.coverLetter}</dd>
        </div>
      </dl>

      {receipt ? (
        <div className={`receipt receipt-${receipt.status}`} role="status">
          <strong>{statusLabel(receipt.status)}</strong>
          <span>{receipt.receipt ?? receipt.errorMessage}</span>
        </div>
      ) : null}

      <button type="button" disabled={!packageReady || isSubmitting} onClick={onSubmit}>
        {isSubmitting ? "Gönderiliyor..." : "Otomatik başvuruyu çalıştır"}
      </button>
    </section>
  );
}
