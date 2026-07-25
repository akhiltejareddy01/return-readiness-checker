import type { FollowUpDraftResponse, MatchStatus, ReadinessReport } from "../types";
import ScoreGauge from "./ScoreGauge";
import DocList from "./DocList";
import OpenQuestionsList from "./OpenQuestionsList";
import FollowUpDraft from "./FollowUpDraft";

interface Props {
  report: ReadinessReport;
  onGenerateFollowUp: () => Promise<void>;
  followUpDraft: FollowUpDraftResponse | null;
  followUpLoading: boolean;
}

const STATUS_LABELS: Record<MatchStatus, string> = {
  received: "Received",
  missing: "Missing",
  needs_review: "Needs Review",
};

export default function ReadinessDashboard({ report, onGenerateFollowUp, followUpDraft, followUpLoading }: Props) {
  return (
    <div className="dashboard">
      <ScoreGauge verdict={report.verdict} />

      <section className="panel">
        <h2>Checklist</h2>
        <ul className="checklist-results">
          {report.checklist_results.map((result) => (
            <li key={result.item.id}>
              <div className="checklist-result-row">
                <span className={`badge badge-status-${result.status}`}>{STATUS_LABELS[result.status]}</span>
                <span>{result.item.label}</span>
                {!result.item.required && <span className="badge badge-optional">optional</span>}
              </div>
              {result.reason && <p className="muted checklist-reason">{result.reason}</p>}
            </li>
          ))}
        </ul>
      </section>

      <DocList extras={report.extra_documents} />
      <OpenQuestionsList questions={report.open_questions} />
      <FollowUpDraft onGenerate={onGenerateFollowUp} draft={followUpDraft} loading={followUpLoading} />
    </div>
  );
}
