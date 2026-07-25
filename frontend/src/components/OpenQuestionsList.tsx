import type { OpenQuestion } from "../types";

interface Props {
  questions: OpenQuestion[];
}

const OWNER_LABELS: Record<string, string> = {
  staff: "Staff",
  client: "Client",
  partner: "Partner",
};

export default function OpenQuestionsList({ questions }: Props) {
  if (questions.length === 0) {
    return (
      <section className="panel">
        <h2>Open Questions</h2>
        <p className="muted">No open questions — nothing to follow up on.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2>Open Questions</h2>
      <ul className="question-list">
        {questions.map((q) => (
          <li key={q.id}>
            <span className={`badge badge-owner-${q.owner}`}>{OWNER_LABELS[q.owner]}</span>
            <span>{q.description}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
