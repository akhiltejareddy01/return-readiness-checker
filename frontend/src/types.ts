export type DocType =
  | "W-2"
  | "1099-INT"
  | "1099-DIV"
  | "1099-NEC"
  | "1099-MISC"
  | "K-1"
  | "1098"
  | "Prior-Year Return"
  | "Other"
  | "Unknown";

export interface RequestChecklistItem {
  id: string;
  doc_type: DocType;
  label: string;
  issuer_hint: string | null;
  required: boolean;
  notes: string | null;
}

export interface RequestChecklist {
  client_name: string;
  tax_year: number;
  items: RequestChecklistItem[];
}

export interface ExtractedField {
  name: string;
  value: string;
  confidence: number;
}

export interface DocClassification {
  doc_type: DocType;
  confidence: number;
  issuer: string | null;
  recipient_name: string | null;
  tax_year: number | null;
  fields: ExtractedField[];
  is_readable: boolean;
  raw_text_excerpt: string | null;
  warnings: string[];
}

export interface UploadedDocument {
  id: string;
  filename: string;
  classification: DocClassification;
}

export type MatchStatus = "received" | "missing" | "needs_review";

export interface ChecklistItemResult {
  item: RequestChecklistItem;
  status: MatchStatus;
  matched_document_id: string | null;
  reason: string | null;
}

export interface ExtraDocument {
  document_id: string;
  filename: string;
  doc_type: DocType;
  reason: string;
}

export type OwnerRole = "staff" | "client" | "partner";

export interface OpenQuestion {
  id: string;
  description: string;
  owner: OwnerRole;
  related_document_id: string | null;
  related_checklist_item_id: string | null;
}

export interface ReadinessVerdict {
  score: number;
  ready: boolean;
  summary: string;
}

export interface ReadinessReport {
  client_name: string;
  tax_year: number;
  checklist_results: ChecklistItemResult[];
  extra_documents: ExtraDocument[];
  open_questions: OpenQuestion[];
  verdict: ReadinessVerdict;
  uploaded_documents: UploadedDocument[];
}

export interface FollowUpDraftResponse {
  subject: string;
  body: string;
}
