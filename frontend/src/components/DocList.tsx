import type { ExtraDocument } from "../types";

interface Props {
  extras: ExtraDocument[];
}

export default function DocList({ extras }: Props) {
  if (extras.length === 0) return null;

  return (
    <section className="panel">
      <h2>Extra / Unexpected Documents</h2>
      <ul className="doc-list">
        {extras.map((doc) => (
          <li key={doc.document_id}>
            <div className="doc-list-header">
              <strong>{doc.filename}</strong>
              <span className="badge badge-doctype">{doc.doc_type}</span>
            </div>
            <p className="muted">{doc.reason}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
