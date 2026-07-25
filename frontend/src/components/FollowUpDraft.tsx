import { useState } from "react";
import type { FollowUpDraftResponse } from "../types";

interface Props {
  onGenerate: () => Promise<void>;
  draft: FollowUpDraftResponse | null;
  loading: boolean;
}

export default function FollowUpDraft({ onGenerate, draft, loading }: Props) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    if (!draft) return;
    await navigator.clipboard.writeText(`Subject: ${draft.subject}\n\n${draft.body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <section className="panel">
      <h2>Client Follow-Up</h2>
      <button type="button" className="primary-button" onClick={onGenerate} disabled={loading}>
        {loading ? "Drafting…" : "Generate Client Follow-Up"}
      </button>

      {draft && (
        <div className="followup-preview">
          <div className="followup-subject">
            <strong>Subject:</strong> {draft.subject}
          </div>
          <textarea readOnly value={draft.body} rows={10} />
          <button type="button" className="link-button" onClick={handleCopy}>
            {copied ? "Copied!" : "Copy to clipboard"}
          </button>
        </div>
      )}
    </section>
  );
}
