import type { RequestChecklist } from "../types";

interface Props {
  checklist: RequestChecklist;
}

export default function ChecklistPanel({ checklist }: Props) {
  return (
    <section className="panel">
      <h2>Requested Documents</h2>
      <p className="muted">
        {checklist.client_name} · Tax Year {checklist.tax_year}
      </p>
      <ul className="checklist-plain">
        {checklist.items.map((item) => (
          <li key={item.id}>
            <span>{item.label}</span>
            {!item.required && <span className="badge badge-optional">optional</span>}
          </li>
        ))}
      </ul>
    </section>
  );
}
