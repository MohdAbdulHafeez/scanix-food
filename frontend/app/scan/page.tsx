"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import Dossier from "@/components/Dossier";
import { Upload, ScanMark, Arrow } from "@/components/icons";
import { scanProduct } from "@/lib/api";
import { SAMPLE_SCAN } from "@/lib/sample";
import type { ScanResult } from "@/lib/types";

type Status = "idle" | "scanning" | "done" | "error";

const STEPS = [
  "Reading the label text (OCR)",
  "Identifying brand, barcode & product",
  "Decoding ingredients & additives",
  "Checking FSSAI licence & front-of-pack claims",
  "Modelling metabolic & organ impact",
  "Finding healthier swaps",
];

export default function ScanPage() {
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<ScanResult | null>(null);
  const [error, setError] = useState("");
  const [preview, setPreview] = useState<string | null>(null);
  const [drag, setDrag] = useState(false);
  const [step, setStep] = useState(0);
  const [isSample, setIsSample] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const resultsRef = useRef<HTMLDivElement>(null);
  const previewUrl = useRef<string | null>(null);

  const loadSample = useCallback(() => {
    setResult(SAMPLE_SCAN);
    setIsSample(true);
    setStatus("done");
    setError("");
    setPreview(null);
  }, []);

  // deep link: /scan#sample opens the sample dossier
  useEffect(() => {
    if (typeof window !== "undefined" && window.location.hash === "#sample") {
      loadSample();
    }
  }, [loadSample]);

  // cosmetic step ticker while the request is in flight
  useEffect(() => {
    if (status !== "scanning") return;
    setStep(0);
    const id = setInterval(
      () => setStep((s) => Math.min(s + 1, STEPS.length - 1)),
      750
    );
    return () => clearInterval(id);
  }, [status]);

  // bring results into view
  useEffect(() => {
    if (status === "done") {
      resultsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [status]);

  const handleFile = useCallback(async (file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("That doesn't look like an image. Use a JPG, PNG or WebP photo of the label.");
      setStatus("error");
      return;
    }
    if (previewUrl.current) URL.revokeObjectURL(previewUrl.current);
    const url = URL.createObjectURL(file);
    previewUrl.current = url;
    setPreview(url);
    setIsSample(false);
    setError("");
    setStatus("scanning");
    try {
      const r = await scanProduct(file);
      setResult(r);
      setStatus("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Scan failed. Is the backend running on :8000?");
      setStatus("error");
    }
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDrag(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const reset = () => {
    setStatus("idle");
    setResult(null);
    setError("");
    setPreview(null);
    setIsSample(false);
  };

  return (
    <>
      <Nav />
      <main className="scanpage">
        <div className="container">
          <div className="scanpage__head">
            <p className="eyebrow">Scan · System 01 → 09</p>
            <h1>Hand Scanix a label.</h1>
            <p className="lede">
              Upload a clear photo of the back-of-pack — the ingredients list and nutrition
              table. Scanix reads it nine ways and returns one dossier. No account needed.
            </p>
          </div>

          {/* ---------- idle: uploader ---------- */}
          {status === "idle" && (
            <div className="uploader">
              <div
                className={`dropzone ${drag ? "drag" : ""}`}
                onClick={() => inputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
                onDragLeave={() => setDrag(false)}
                onDrop={onDrop}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") inputRef.current?.click(); }}
                aria-label="Upload a label photo"
              >
                <Upload className="dropzone__icon" size={52} />
                <h3>Drop a label photo</h3>
                <p>or click to browse · or take one with your camera</p>
                <div className="dropzone__formats">JPG · PNG · WEBP · up to 10MB</div>
                <input
                  ref={inputRef}
                  type="file"
                  accept="image/*"
                  capture="environment"
                  hidden
                  onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
                />
              </div>

              <aside className="uploader__aside" id="sample">
                <h4>Best results</h4>
                <div className="uploader__tip"><span>01</span><p>Photograph the <strong>back of pack</strong> — ingredients + nutrition table.</p></div>
                <div className="uploader__tip"><span>02</span><p>Fill the frame, keep it flat, avoid glare and shadows.</p></div>
                <div className="uploader__tip"><span>03</span><p>Hindi &amp; regional labels are supported alongside English.</p></div>
                <div className="uploader__sep">— or —</div>
                <button className="btn btn--ghost" onClick={loadSample}>
                  Open a sample dossier <Arrow size={16} />
                </button>
                <p style={{ fontSize: 13, color: "var(--paper-faint)", fontFamily: "var(--font-mono)" }}>
                  See everything a scan produces, instantly.
                </p>
              </aside>
            </div>
          )}

          {/* ---------- scanning ---------- */}
          {status === "scanning" && (
            <div className="scanning">
              {preview ? (
                <div className="dropzone" style={{ minHeight: 220, padding: 0, cursor: "default" }}>
                  <div className="dropzone__preview">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={preview} alt="label being scanned" />
                    <div className="scanline" aria-hidden="true" />
                  </div>
                </div>
              ) : (
                <div className="spinner" />
              )}
              <h3>Reading the label…</h3>
              <p>This can take a few seconds on the first scan while OCR warms up.</p>
              <div className="scanning__steps">
                {STEPS.map((s, i) => (
                  <div
                    key={s}
                    className={`scanning__step ${i < step ? "done" : i === step ? "active" : ""}`}
                  >
                    <i>{i < step ? "✓" : i === step ? "›" : ""}</i> {s}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ---------- error ---------- */}
          {status === "error" && (
            <>
              <div className="errbox">
                <b>Couldn&apos;t finish the scan</b>
                <p>{error}</p>
              </div>
              <div className="dossier__actions">
                <button className="btn btn--solid" onClick={reset}><ScanMark size={16} /> Try another photo</button>
                <button className="btn btn--ghost" onClick={loadSample}>Open the sample dossier instead</button>
              </div>
            </>
          )}

          {/* ---------- done ---------- */}
          {status === "done" && result && (
            <div ref={resultsRef}>
              {isSample && (
                <div
                  className="errbox"
                  style={{
                    borderColor: "var(--line)",
                    background: "var(--marigold-soft)",
                    marginTop: 30,
                  }}
                >
                  <b style={{ color: "var(--marigold)" }}>Sample dossier</b>
                  <p>
                    A fictional product, shaped exactly like a real scan response. Scan an actual
                    label to see your own.
                  </p>
                </div>
              )}

              <Dossier result={result} />

              <div className="dossier__actions">
                <button className="btn btn--solid" onClick={reset}>
                  <ScanMark size={16} /> Scan another label
                </button>
                <Link className="btn btn--ghost" href="/#trust">
                  About FSSAI complaints
                </Link>
              </div>
            </div>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
