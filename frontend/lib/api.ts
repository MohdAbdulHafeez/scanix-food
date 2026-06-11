import type { ScanResult } from "./types";

/* Requests go to the same origin and are proxied to FastAPI by
   next.config rewrites, so there is no CORS to configure in dev.
   Set NEXT_PUBLIC_API_BASE to call a remote backend directly. */
const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "";

export async function scanProduct(file: File): Promise<ScanResult> {
  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API_BASE}/api/v1/scan`, {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    let detail = `Scan failed (${res.status})`;
    try {
      const body = await res.json();
      if (typeof body?.detail === "string") detail = body.detail;
      else if (body?.detail?.message) detail = body.detail.message;
    } catch {
      /* non-JSON error body */
    }
    throw new Error(detail);
  }

  return res.json();
}
