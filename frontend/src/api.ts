import type { FollowUpDraftResponse, ReadinessReport, RequestChecklist } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Request failed (${res.status}): ${body}`);
  }
  return res.json() as Promise<T>;
}

export async function getChecklist(): Promise<RequestChecklist> {
  const res = await fetch(`${API_BASE_URL}/api/checklist`);
  return handleResponse<RequestChecklist>(res);
}

export async function analyze(files: File[]): Promise<ReadinessReport> {
  const formData = new FormData();
  for (const file of files) {
    formData.append("files", file);
  }
  const res = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: "POST",
    body: formData,
  });
  return handleResponse<ReadinessReport>(res);
}

export async function generateFollowUp(report: ReadinessReport): Promise<FollowUpDraftResponse> {
  const res = await fetch(`${API_BASE_URL}/api/followup-draft`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ report }),
  });
  return handleResponse<FollowUpDraftResponse>(res);
}
