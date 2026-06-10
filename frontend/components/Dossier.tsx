"use client";

import type { ScanResult } from "@/lib/types";
import VerdictSeal from "./VerdictSeal";
import {
  Beaker,
  Pulse,
  Eye,
  Twin,
  Shield,
  Swap,
  Leaf,
  Check,
  Alert,
  Cross,
  ScanMark,
} from "./icons";

/* ---------- helpers ---------- */

const n = (v: unknown, d = 0): number =>
  typeof v === "number" && !Number.isNaN(v) ? v : d;

const scoreColor = (v: number) =>
  v >= 70 ? "var(--jade)" : v >= 45 ? "var(--marigold)" : "var(--chili)";

const clampPct = (v: number, max: number) =>
  Math.max(2, Math.min((v / max) * 100, 100));

function Ring({ value, color }: { value: number; color: string }) {
  return (
    <svg className="organ__ring" viewBox="0 0 36 36" aria-hidden="true">
      <circle cx="18" cy="18" r="15.5" fill="none" stroke="var(--ink-3)" strokeWidth="3" />
      <circle
        cx="18"
        cy="18"
        r="15.5"
        fill="none"
        stroke={color}
        strokeWidth="3"
        strokeLinecap="round"
        pathLength={100}
        strokeDasharray={`${Math.max(value, 2)} 100`}
        transform="rotate(-90 18 18)"
      />
      <text
        x="18"
        y="21"
        textAnchor="middle"
        fill="var(--paper)"
        style={{ fontFamily: "var(--font-mono)", fontSize: 10 }}
      >
        {value}
      </text>
    </svg>
  );
}

export default function Dossier({ result }: { result: ScanResult }) {
  const p = result.product ?? {};
  const nut = result.nutrition ?? {};
  const ti = result.trust_intelligence ?? {};
  const ing = result.ingredients ?? {};
  const swaps = result.smart_swaps ?? {};
  const dt = result.digital_twin ?? {};
  const organ = (dt.organ_impact ?? {}) as Record<string, number>;

  const verdict = (result.recommendation?.recommendation ?? "OCCASIONAL").toUpperCase();
  const healthScore = n(swaps.current_health_score, n(result.scan_quality?.scan_quality_score, 50));

  const metabScore = n(result.metabolic_intelligence?.verdict?.overall?.score, 0);
  const bodyScore = n(dt.overall_digital_twin_score, 0);
  const trustScore = n(ti.overall_trust_score, n(result.trust?.trust_score, 0));
  const authScore = n(ti.authenticity_score, 0);
  const deception = n(result.consumer_intelligence?.summary?.deception_score, 0);

  const tiles = [
    { k: "Health", v: healthScore, note: (swaps.current_processing_level ?? "").replace(/_/g, " ").toLowerCase() || "overall" },
    { k: "Trust", v: trustScore, note: (ti.overall_trust_level ?? "—").toLowerCase() },
    { k: "Authenticity", v: authScore, note: `grade ${ti.authenticity_grade ?? "—"}` },
    { k: "Metabolic", v: metabScore, note: result.metabolic_intelligence?.verdict?.overall?.label?.toLowerCase?.() ?? "after eating" },
    { k: "Body twin", v: bodyScore, note: (dt.overall_verdict ?? "—").replace(/_/g, " ").toLowerCase() },
  ];

  const nutriRows: { k: string; v: number; unit: string; max: number; good?: boolean }[] = [
    { k: "Energy", v: n(nut.calories), unit: "kcal", max: 600 },
    { k: "Protein", v: n(nut.protein), unit: "g", max: 25, good: true },
    { k: "Fibre", v: n(nut.fiber), unit: "g", max: 15, good: true },
    { k: "Total fat", v: n(nut.fat), unit: "g", max: 40 },
    { k: "Saturated fat", v: n(nut.saturated_fat), unit: "g", max: 20 },
    { k: "Sugar", v: n(nut.sugar), unit: "g", max: 40 },
    { k: "Sodium", v: n(nut.sodium), unit: "mg", max: 1000 },
    { k: "Carbs", v: n(nut.carbohydrates), unit: "g", max: 80 },
  ];

  const eNums = (ing.e_numbers ?? []) as string[];
  const ingList = (ing.ingredients ?? []) as string[];
  const allergens = result.allergens ?? [];
  const negatives = result.negatives ?? [];
  const positives = result.positives ?? [];
  const risks = result.risks?.risks ?? [];
  const overallRisk = result.risks?.overall_risk ?? "—";
  const claims = result.claims?.claims_detected ?? [];
  const warnings = ti.warnings ?? [];
  const topSwaps = swaps.top_swaps ?? [];

  const explainer =
    result.food_explainer?.summary?.final_verdict?.verdict ??
    result.food_explainer?.explainer?.final_verdict?.verdict ??
    null;
  const nutritionistText =
    result.nutritionist?.answer ??
    result.nutritionist?.summary?.answer ??
    null;

  const organKeys: { key: string; label: string }[] = [
    { key: "liver_impact_score", label: "Liver" },
    { key: "heart_impact_score", label: "Heart" },
    { key: "pancreas_impact_score", label: "Pancreas" },
    { key: "kidney_impact_score", label: "Kidneys" },
  ];
  const organsPresent = organKeys.filter((o) => typeof organ[o.key] === "number");

  const ocrText =
    result.metadata?.audit_trail?.ocr_corrected ?? result.ocr?.extracted_text ?? "";

  return (
    <div className="dossier">
      <div className="dossier__bar">
        <span className="id">DOSSIER · {result.metadata?.scan_id ?? "scan"}</span>
        <span className="spacer" />
        <span>read in {(n(result.metadata?.processing_time_ms) / 1000).toFixed(1)}s</span>
        <span>· OCR {Math.round(n(result.ocr?.average_confidence) * 100) || n(result.ocr?.ocr_quality_score)}%</span>
        <span>· {result.verification?.verification_level ?? "—"} verification</span>
      </div>

      {/* identity + verdict */}
      <div className="dossier__top">
        <div className="idcard">
          <div className="idcard__img">
            {p.image_url ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img src={p.image_url} alt={p.product_name ?? "product"} />
            ) : (
              <ScanMark className="ph" size={40} />
            )}
          </div>
          <div>
            <div className="idcard__cat">{(p.category ?? "food").replace(/_/g, " ")}</div>
            <h2>{p.product_name ?? "Unidentified product"}</h2>
            <div className="idcard__brand">{p.brand ?? "Unknown brand"}</div>
            <div className="idcard__meta">
              {p.barcode && <span className="chip">barcode {p.barcode}</span>}
              {typeof p.nova === "number" && (
                <span className={`chip ${p.nova >= 4 ? "chip--bad" : p.nova >= 3 ? "chip--warn" : "chip--good"}`}>
                  NOVA {p.nova}
                </span>
              )}
              {p.nutriscore && (
                <span className="chip chip--warn">Nutri-Score {String(p.nutriscore).toUpperCase()}</span>
              )}
              {typeof p.identity_confidence === "number" && (
                <span className="chip">ID {p.identity_confidence}%</span>
              )}
            </div>
          </div>
        </div>

        <div className="verdictcard">
          <VerdictSeal verdict={verdict} score={healthScore} size={134} stamp />
          <div className="verdictcard__body">
            <h3>Scanix verdict</h3>
            <div className="reason">{result.recommendation?.reason ?? "Reviewed across nine systems."}</div>
            {(result.recommendation?.best_for ?? []).length > 0 && (
              <div className="best">
                {result.recommendation!.best_for!.map((b) => (
                  <span className="chip chip--good" key={b}>{b}</span>
                ))}
              </div>
            )}
            {(result.badges ?? []).length > 0 && (
              <div className="best">
                {result.badges!.map((b) => (
                  <span className="chip chip--warn" key={b}>{b.replace(/_/g, " ").toLowerCase()}</span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* score strip */}
      <div className="scorestrip">
        {tiles.map((t) => (
          <div className="scoretile" key={t.k}>
            <div className="scoretile__k">{t.k}</div>
            <div className="scoretile__v" style={{ color: scoreColor(t.v) }}>
              {t.v}
              <small> /100</small>
            </div>
            <div className="scoretile__meter">
              <i style={{ width: `${Math.max(t.v, 3)}%`, background: scoreColor(t.v) }} />
            </div>
            <div className="scoretile__note">{t.note}</div>
          </div>
        ))}
      </div>

      {/* detail grid */}
      <div className="dgrid">
        {/* nutrition */}
        <div className="panel">
          <span className="eyebrow"><Pulse size={14} /> Nutrition · per 100g</span>
          <h3>{nut.nutrition_detected === false ? "No nutrition table found" : "What's in 100 grams"}</h3>
          {nut.nutrition_detected === false ? (
            <p className="panel__sub">The label didn&apos;t expose a readable nutrition panel — scores below lean on ingredients and processing instead.</p>
          ) : (
            <div className="nutri">
              {nutriRows.map((r) => {
                const pct = clampPct(r.v, r.max);
                const good = r.good ? pct > 45 : pct < 35;
                const color = good ? "var(--jade)" : pct > 70 ? "var(--chili)" : "var(--marigold)";
                return (
                  <div className="nutri__row" key={r.k}>
                    <span className="nutri__k">{r.k}</span>
                    <span className="nutri__track">
                      <span className="nutri__fill" style={{ width: `${pct}%`, background: color }} />
                    </span>
                    <span className="nutri__v">{r.v}{r.unit}</span>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* ingredients */}
        <div className="panel">
          <span className="eyebrow"><Beaker size={14} /> Ingredients · System 02</span>
          <h3>{n(ing.ingredient_count)} ingredients, {n(ing.additive_count)} additives</h3>
          <div className="countgrid">
            <div className="cg"><b>{n(ing.ingredient_count)}</b><span>ingredients</span></div>
            <div className="cg"><b style={{ color: n(ing.additive_count) > 3 ? "var(--chili)" : "var(--paper)" }}>{n(ing.additive_count)}</b><span>additives</span></div>
            <div className="cg"><b>{n(ing.preservative_count)}</b><span>preservatives</span></div>
            <div className="cg"><b style={{ color: n(ing.artificial_count) > 0 ? "var(--marigold)" : "var(--paper)" }}>{n(ing.artificial_count)}</b><span>artificial</span></div>
          </div>
          {eNums.length > 0 && (
            <div className="taglist">
              {eNums.map((e) => <span className="chip chip--warn" key={e}>{e}</span>)}
            </div>
          )}
          {ingList.length > 0 && (
            <div className="taglist">
              {ingList.slice(0, 14).map((i, idx) => <span className="chip" key={`${i}-${idx}`}>{i}</span>)}
            </div>
          )}
        </div>

        {/* honesty / claims */}
        <div className="panel">
          <span className="eyebrow"><Eye size={14} /> Honesty · System 04</span>
          <h3>Does the front of pack tell the truth?</h3>
          <p className="panel__sub">Deception score {deception}/100 · {result.consumer_intelligence?.summary?.overall_alert ?? "reviewed"}</p>
          {claims.length > 0 && (
            <div className="taglist">
              {claims.map((c) => <span className="chip chip--warn" key={c}>“{c}”</span>)}
            </div>
          )}
          <div className="warnlist">
            {warnings.length > 0 ? (
              warnings.map((w, i) => (
                <div className="warn-item bad" key={i}><Alert size={18} /> <span>{w}</span></div>
              ))
            ) : (
              <div className="warn-item good"><Check size={18} /> <span>No claim contradictions detected.</span></div>
            )}
          </div>
        </div>

        {/* risks & flags */}
        <div className="panel">
          <span className="eyebrow"><Alert size={14} /> Risk profile</span>
          <h3>Overall risk: <span style={{ color: overallRisk === "HIGH" ? "var(--chili)" : overallRisk === "MEDIUM" ? "var(--marigold)" : "var(--jade)" }}>{overallRisk}</span></h3>
          {risks.length > 0 && (
            <div className="taglist">
              {risks.map((r) => <span className="chip chip--bad" key={r}>{r}</span>)}
            </div>
          )}
          <div className="warnlist">
            {negatives.map((ngt, i) => (
              <div className="warn-item warn" key={`neg-${i}`}><Alert size={18} /> <span><b style={{ color: "var(--paper)" }}>{ngt.title}</b> — {ngt.reason}</span></div>
            ))}
            {positives.map((pos, i) => (
              <div className="warn-item good" key={`pos-${i}`}><Check size={18} /> <span><b style={{ color: "var(--paper)" }}>{pos.title}</b> {pos.value ? `(${pos.value})` : ""} — {pos.reason}</span></div>
            ))}
            {negatives.length === 0 && positives.length === 0 && (
              <div className="warn-item good"><Check size={18} /> <span>Nothing notable flagged in the ingredient list.</span></div>
            )}
          </div>
        </div>

        {/* trust & FSSAI */}
        <div className="panel span2">
          <span className="eyebrow"><Shield size={14} /> Trust &amp; FSSAI · System 08</span>
          <h3>Authentic, compliant — and honest?</h3>
          <div className="dgrid" style={{ marginTop: 16, gap: 16 }}>
            <div className="trustrows">
              <div className="trustrow"><span className="trustrow__k">FSSAI licence</span><span className="trustrow__v" style={{ color: ti.is_fssai_valid ? "var(--jade)" : "var(--chili)" }}>{ti.is_fssai_valid ? "valid" : "not verified"}</span></div>
              <div className="trustrow"><span className="trustrow__k">Adulteration risk</span><span className="trustrow__v" style={{ color: (ti.adulteration_risk_level ?? "low") === "low" ? "var(--jade)" : "var(--chili)" }}>{ti.adulteration_risk_level ?? "—"}</span></div>
              <div className="trustrow"><span className="trustrow__k">Counterfeit risk</span><span className="trustrow__v" style={{ color: (ti.counterfeit_risk_level ?? "low") === "low" ? "var(--jade)" : "var(--chili)" }}>{ti.counterfeit_risk_level ?? "—"}</span></div>
              <div className="trustrow"><span className="trustrow__k">Authenticity</span><span className="trustrow__v">{authScore}/100 · grade {ti.authenticity_grade ?? "—"}</span></div>
              <div className="trustrow"><span className="trustrow__k">Brand trust</span><span className="trustrow__v">{n(ti.brand_trust_score)}/100</span></div>
            </div>
            <div className="warnlist">
              {(ti.recommendations ?? []).map((r, i) => (
                <div className="warn-item good" key={`rec-${i}`}><Check size={18} /> <span>{r}</span></div>
              ))}
              {warnings.map((w, i) => (
                <div className="warn-item bad" key={`w-${i}`}><Alert size={18} /> <span>{w}</span></div>
              ))}
            </div>
          </div>
        </div>

        {/* allergens */}
        {allergens.length > 0 && (
          <div className="panel">
            <span className="eyebrow"><Cross size={14} /> Allergens</span>
            <h3>Declared &amp; detected</h3>
            <div className="taglist">
              {allergens.map((a, i) => (
                <span className="chip chip--bad" key={i}>{a.allergen}</span>
              ))}
            </div>
          </div>
        )}

        {/* digital twin organs */}
        {organsPresent.length > 0 && (
          <div className="panel">
            <span className="eyebrow"><Twin size={14} /> Digital twin · System 05</span>
            <h3>Estimated organ impact</h3>
            <div className="organs">
              {organsPresent.map((o) => {
                const v = n(organ[o.key]);
                return (
                  <div className="organ" key={o.key}>
                    <Ring value={v} color={scoreColor(v)} />
                    <div><b>{o.label}</b><span>{v >= 70 ? "low strain" : v >= 45 ? "moderate" : "high strain"}</span></div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* smart swaps */}
        {topSwaps.length > 0 && (
          <div className="panel span2">
            <span className="eyebrow"><Swap size={14} /> Smart swaps · System 07</span>
            <h3>Healthier things to buy instead</h3>
            {swaps.recommendation && <p className="panel__sub">{swaps.recommendation}</p>}
            <div className="swapmini">
              {topSwaps.slice(0, 3).map((s, i) => (
                <div className={`swapmini__row ${i === 0 ? "best" : ""}`} key={i}>
                  <span className="swapmini__rank">#{i + 1}</span>
                  <div className="swapmini__name">
                    <b>{s.name}</b>
                    <span>{s.brand ?? ""} {typeof s.nova_group === "number" ? `· NOVA ${s.nova_group}` : ""}</span>
                  </div>
                  <div className="taglist" style={{ marginTop: 0 }}>
                    {(s.why_better ?? []).slice(0, 3).map((w, j) => (
                      <span className="chip chip--good" key={j}>{w}</span>
                    ))}
                  </div>
                  <span className="swapmini__score" style={{ color: scoreColor(n(s.overall_score)) }}>{Math.round(n(s.overall_score))}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI explainer */}
        {(explainer || nutritionistText) && (
          <div className="panel span2">
            <span className="eyebrow"><Leaf size={14} /> The read · System 06</span>
            <div className="panel__head" style={{ marginTop: 12 }}>
              <h3>In plain words</h3>
              <span className="ai-badge">AI · grounded</span>
            </div>
            <div className="ai-text">
              {explainer && <p>{explainer}</p>}
              {nutritionistText && <p>{nutritionistText}</p>}
            </div>
          </div>
        )}

        {/* raw OCR */}
        {ocrText && (
          <div className="panel span2">
            <details>
              <summary>View the raw label text Scanix read ↓</summary>
              <div className="ocrbox">{ocrText}</div>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
