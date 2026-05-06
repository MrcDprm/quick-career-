# Quick-Career Roadmap

Bu roadmap, SolveX AI Hackathon 2026 teknik sartnamesine uygun olarak Quick-Career projesinin Plan Agent tarafindan olusturulan uygulama planidir. Hedef, FastAPI backend ve React frontend ile is ilani analizi, CV optimizasyonu ve otomatik basvuru akisini demo edilebilir bir MVP'ye donusturmektir.

## Success Criteria

- Kullanici bir is ilani ve CV ile baslayip optimize edilmis CV, basvuru metni ve basvuru gonderim sonucuna tek akista ulasir.
- Manuel kariyer basvuru hazirligi adimlari en az `%50` azalir; demo hedefi `%70+` azaltimdir.
- CV final cikti optimizasyon tamamlandiktan sonra kullanici onayi beklemeden uretilir.
- Tam otomatik basvuru gonderimi, optimize edilmis basvuru paketiyle otonom calisir.
- Plan Agent ve Skills Agent katkisi PR aciklamalari, issue notlari veya kod yorumlariyla izlenebilir olur.
- Backend ve frontend temel testleri mock AI provider ile calisir.

## Team And GitHub Flow

| Role | Responsibility |
| --- | --- |
| Lead Developer / Maintainer | Repository yonetimi, mimari kararlar, PR onayi, final review ve teslim kalitesi. |
| Feature Developer 1 | Backend API, AI provider adapter, veri modelleri, job/resume/optimization servisleri. |
| Feature Developer 2 | React frontend, review UI, export/application ekranlari, metrics dashboard. |

Git standards:

- `main` dagitima hazir stabil dal olarak korunur.
- Dogrudan `main` push yapilmaz.
- Yeni isler `feature/gorev-adi`, hatalar `fix/hata-adi` formatinda branch alir.
- Commit mesajlari simdiki zaman kipinde teknik ve kisa olur: `feat: add job analysis endpoint`.
- Her merge Pull Request ile yapilir ve en az bir ekip uyesi review verir.
- PR aciklamalarinda AI traceability bolumu bulunur.

## Sprint 0 - Project Foundation

Goal: Repo disiplinini, dokumantasyonu ve hackathon izlenebilirligini hazirlamak.

Tasks:

- `ARCHITECTURE.md` ve `ROADMAP.md` dosyalarini repo kokune ekle.
- GitHub repo olustur, branch protection ve PR review kuralini ayarla.
- Issue template hazirla: `Feature`, `Bug`, `AI Traceability`, `Demo Checklist`.
- `.env.example` tanimla: `DATABASE_URL`, `AI_PROVIDER`, `AI_API_KEY`, `EXPORT_STORAGE_PATH`, `APPLICATION_SUBMISSION_MODE`.
- Backend/frontend klasor yapisini ve README baslangic komutlarini planla.
- Plan Agent notunu dokumanlarda, Skills Agent kullanim kuralini PR template'inde belirt.

Acceptance:

- Repo acilmis ve takim rolleri atanmis olur.
- En az 8 MVP issue'su acilir ve gelistiricilere atanir.
- PR template AI traceability alanini zorunlu kilacak sekilde hazirlanir.

## Sprint 1 - Application Skeleton

Goal: FastAPI + React temel uygulamasini, mock AI provider'i ve ortak tipleri ayaga kaldirmak.

Backend tasks:

- FastAPI uygulama iskeletini olustur.
- Pydantic schema gruplarini ekle: job, resume, optimization, application, metrics.
- SQLAlchemy modellerini ve Alembic migration altyapisini hazirla.
- AI provider interface ve deterministic `mock_provider` ekle.
- Healthcheck endpoint'i ekle: `GET /api/health`.

Frontend tasks:

- React + TypeScript + Vite iskeletini olustur.
- API client, route yapisi ve temel layout ekle.
- Ana workflow ekranlarini bos durumlarla hazirla: job intake, resume intake, match report, optimization review, application submit, metrics.
- Loading, error ve retry state pattern'lerini tanimla.

Acceptance:

- Backend ve frontend local olarak calisir.
- Mock AI provider ile testler ag baglantisi olmadan calisir.
- Frontend API hatalarini kullaniciya geri denenebilir bicimde gosterir.

## Sprint 2 - Job Analysis And Resume Profile

Goal: Ilan ve CV verisini yapilandirilmis profile donusturmek.

Backend tasks:

- `POST /api/jobs/analyze` endpoint'ini ekle.
- Job analysis ciktisini Pydantic ile dogrula: rol, seviye, gerekli beceriler, tercih edilen beceriler, anahtar kelimeler, sorumluluklar.
- `POST /api/resumes/upload` endpoint'ini ekle.
- CV metninden ozet, deneyimler, beceriler, projeler, egitim ve dil alanlarini cikar.
- `MatchScoringService` ile ilk uyum skoru ve eksik kriter listesini hesapla.
- `AITraceLog` kaydini her AI cagrisi icin olustur.

Frontend tasks:

- Ilan metni/URL giris ekranini tamamla.
- CV yukleme veya metin yapistirma akisini tamamla.
- Match report ekraninda skor, guclu eslesmeler ve eksikleri goster.
- Uzun metinlerde responsive ve tasmasiz UI kontrolu yap.

Acceptance:

- Kullanici ilan ve CV girisiyle yapilandirilmis analiz gorur.
- Mock AI ile tekrarlanabilir skor uretilebilir.
- Backend testleri ilan analizi ve CV parsing icin temel senaryolari kapsar.

## Sprint 3 - Autonomous CV Optimization And Export

Goal: Otonom CV optimizasyonunu ve otomatik cikti uretimini tamamlamak.

Backend tasks:

- `POST /api/resumes/{id}/optimize` endpoint'ini ekle.
- `OptimizationRun` status akisini tanimla: `draft`, `optimizing`, `finalized`, `exported`, `submitted`, `failed`.
- CV optimizer ile hedef ilana gore ozet, deneyim maddeleri, beceri siralamasi ve proje vurgularini yeniden yaz.
- `GET /api/optimizations/{id}/diff` endpoint'i ile alan bazli farklari dondur.
- `POST /api/optimizations/{id}/finalize` endpoint'i ile otonom degisiklikleri final hale getir.
- `POST /api/optimizations/{id}/export` ile PDF, DOCX ve Markdown cikti uret.

Frontend tasks:

- Optimization review ekraninda once/sonra farklarini goster.
- Degisiklikleri otomasyon logu ve fark ekrani olarak goster.
- Export center'da PDF, DOCX ve Markdown ciktilarini goster.
- Optimizasyon tamamlanmadan export durumunu beklemede goster.

Acceptance:

- Sistem kullanici onayi beklemeden final CV ciktisi uretir.
- Finalize edilen optimizasyon icin en az Markdown ve bir dosya formati ciktisi alinabilir.
- Tests: autonomous finalization, mock provider response validation, export happy path.

## Sprint 4 - Automatic Application, Metrics And Final Review

Goal: Tam otomatik basvuru gonderimini, verimlilik metriklerini ve final demo akisini tamamlamak.

Backend tasks:

- `POST /api/applications/submit` endpoint'ini ekle.
- Application submission adapter'larini tanimla: `mock`, `email`, `platform`.
- Optimize edilmis CV, basvuru metni ve hedef bilgisi olmadan basvuru gonderimini engelle.
- Submission receipt ve hata kaydini `ApplicationSubmission` modelinde sakla.
- `GET /api/metrics/efficiency` endpoint'i ile manuel ve otomatik efor karsilastirmasini dondur.
- Final refactoring ve optimization taramasini yap; bulgulari PR aciklamasinda belirt.

Frontend tasks:

- Application submit ekraninda hedef, CV, cover letter ve cevap ozetini goster.
- Optimizasyon ve export tamamlandiktan sonra otomatik basvuru gonderimini baslat.
- Submission receipt, hata ve retry durumlarini goster.
- Metrics dashboard'da sure, adim ve azaltim yuzdesini goster.
- Demo modu icin deterministik ornek ilan, CV ve basvuru senaryosu ekle.

Acceptance:

- Optimize edilmis paketle mock veya email adapter uzerinden basvuru gonderimi calisir.
- Dashboard `%50+` tekrar azaltimini net sekilde raporlar.
- Demo akisinda ilan analizi, CV optimizasyonu, export ve basvuru gonderimi kesintisiz tamamlanir.

## Suggested GitHub Issues

| Issue | Title | Owner | Acceptance |
| --- | --- | --- | --- |
| `QC-001` | Initialize FastAPI backend skeleton | Feature Developer 1 | Healthcheck and test runner pass. |
| `QC-002` | Initialize React frontend skeleton | Feature Developer 2 | App shell and routes render. |
| `QC-003` | Add AI provider abstraction and mock provider | Feature Developer 1 | AI calls run through provider interface. |
| `QC-004` | Implement job analysis API | Feature Developer 1 | Job text returns structured analysis. |
| `QC-005` | Implement resume upload and parsing | Feature Developer 1 | CV text/file creates `ResumeProfile`. |
| `QC-006` | Build match report UI | Feature Developer 2 | Score and gaps are visible. |
| `QC-007` | Implement CV optimization diff API | Feature Developer 1 | Proposed changes are reviewable. |
| `QC-008` | Build optimization trace UI | Feature Developer 2 | User can inspect autonomous changes. |
| `QC-009` | Implement export service | Feature Developer 1 | Optimized CV exports to Markdown and one file format. |
| `QC-010` | Implement automatic application submission | Feature Developer 1 | Optimized package submits via mock/email adapter. |
| `QC-011` | Build application submission UI | Feature Developer 2 | Final confirmation and receipt are visible. |
| `QC-012` | Add efficiency metrics dashboard | Feature Developer 2 | Dashboard shows `%50+` reduction. |
| `QC-013` | Add AI traceability records | Lead Developer | Runtime calls and PR notes are traceable. |
| `QC-014` | Run final refactor and optimization review | Lead Developer | Final checklist is complete before delivery. |

## Test Plan

Backend tests:

- `POST /api/jobs/analyze` extracts role, skills, experience, keywords and responsibilities from a sample job post.
- `POST /api/resumes/upload` creates a structured resume profile from sample CV text.
- `POST /api/resumes/{id}/optimize` starts an optimization with mock AI output.
- `GET /api/optimizations/{id}/diff` returns before/after changes.
- `POST /api/optimizations/{id}/finalize` persists autonomous final changes.
- Export endpoint rejects unfinished optimization runs.
- Application submission endpoint rejects incomplete packages.
- AI provider can be swapped between `mock` and configured real provider without service changes.
- Efficiency metric calculation reports at least `%50` reduction for the demo baseline.

Frontend tests:

- Job intake validates empty input and renders analysis result.
- Resume upload handles long text and parsing errors.
- Match report displays score, missing skills and improvement suggestions.
- Optimization review shows autonomous diffs and pending export state before finalization.
- Application submit screen shows final confirmation before sending.
- Metrics dashboard renders time, step and reduction values.
- Long job and CV content do not overlap or overflow on desktop and mobile widths.

Demo acceptance scenario:

1. User pastes a software developer job post.
2. User uploads or pastes a CV.
3. System analyzes the job and parses the CV.
4. System shows match score, missing keywords and suggested priorities.
5. System generates targeted CV changes.
6. System finalizes selected changes autonomously and shows the diff log.
7. System exports the optimized CV.
8. User confirms the application package.
9. System submits the application through the configured adapter.
10. Dashboard shows `%50+` repetitive work reduction.

## AI-Augmented Development Rules

- Plan Agent output lives in `ARCHITECTURE.md` and `ROADMAP.md`.
- Skills Agent should be used for complex prompt/schema design, security-sensitive flows, database optimization and scoring algorithm tuning.
- PR descriptions must include:

```text
AI Traceability:
- Plan Agent:
- Skills Agent:
- Human Review:
```

- Complex AI-assisted code blocks should include short comments explaining which agent optimized the logic.
- Final delivery must include an AI-assisted refactoring and optimization pass.

## Final Delivery Checklist

- `ARCHITECTURE.md` and `ROADMAP.md` exist in repo root.
- FastAPI backend runs locally.
- React frontend runs locally.
- Mock AI provider works without external API keys.
- Job analysis, CV parsing, optimization, autonomous export and application submission demo path works.
- Efficiency dashboard proves at least `%50` reduction.
- GitHub Issues and PRs show role ownership and AI traceability.
- Final review has checked code quality, security basics, UI responsiveness and demo stability.
