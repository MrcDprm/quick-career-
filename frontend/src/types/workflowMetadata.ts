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
    label: "İlan Analizi",
    description: "İlandan rol, seviye, gerekli yetenekler ve anahtar kelimeleri çıkarır.",
  },
  {
    stage: "resume-parsing",
    label: "CV Ayrıştırma",
    description: "CV içeriğini yapılandırılmış aday profiline dönüştürür.",
  },
  {
    stage: "match-scoring",
    label: "Eşleşme Skoru",
    description: "Uygunluğu puanlar ve en yüksek etkili iyileştirme boşluklarını belirler.",
  },
  {
    stage: "cv-optimization",
    label: "Otonom CV Optimizasyonu",
    description: "CV'yi hedef ilana göre yeniden yazar ve otomasyon fark kaydını oluşturur.",
  },
  {
    stage: "document-export",
    label: "Doküman Çıktısı",
    description: "Optimizasyon tamamlanınca Markdown ve doküman çıktıları üretir.",
  },
  {
    stage: "application-submission",
    label: "Otomatik Başvuru",
    description: "Optimize edilmiş paketi yapılandırılan adaptör üzerinden gönderir.",
  },
  {
    stage: "efficiency-metrics",
    label: "Verimlilik Metrikleri",
    description: "Tekrarlı iş azaltımını manuel temel değerlerle karşılaştırarak kanıtlar.",
  },
];
