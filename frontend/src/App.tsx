import { useEffect, useState } from "react";
import { analyze, generateFollowUp, getChecklist } from "./api";
import type { FollowUpDraftResponse, ReadinessReport, RequestChecklist } from "./types";
import ChecklistPanel from "./components/ChecklistPanel";
import UploadDropzone from "./components/UploadDropzone";
import ReadinessDashboard from "./components/ReadinessDashboard";

export default function App() {
  const [checklist, setChecklist] = useState<RequestChecklist | null>(null);
  const [report, setReport] = useState<ReadinessReport | null>(null);
  const [followUpDraft, setFollowUpDraft] = useState<FollowUpDraftResponse | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [followUpLoading, setFollowUpLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getChecklist()
      .then(setChecklist)
      .catch((err) => setError(err.message));
  }, []);

  async function handleAnalyze(files: File[]) {
    setAnalyzing(true);
    setError(null);
    setFollowUpDraft(null);
    try {
      const result = await analyze(files);
      setReport(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed.");
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleGenerateFollowUp() {
    if (!report) return;
    setFollowUpLoading(true);
    setError(null);
    try {
      const draft = await generateFollowUp(report);
      setFollowUpDraft(draft);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not generate follow-up.");
    } finally {
      setFollowUpLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Return Readiness Checker</h1>
        <p className="muted">Drop in what the client sent — see exactly what's still missing.</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="app-main">
        <div className="app-sidebar">
          {checklist && <ChecklistPanel checklist={checklist} />}
          <UploadDropzone onAnalyze={handleAnalyze} loading={analyzing} />
        </div>

        <div className="app-content">
          {report ? (
            <ReadinessDashboard
              report={report}
              onGenerateFollowUp={handleGenerateFollowUp}
              followUpDraft={followUpDraft}
              followUpLoading={followUpLoading}
            />
          ) : (
            <div className="empty-state">
              <p>Upload client documents to see the readiness verdict.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
