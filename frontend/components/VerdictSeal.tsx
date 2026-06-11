"use client";

import { useId } from "react";

type Verdict = "DAILY" | "OCCASIONAL" | "AVOID" | string;

const COLORS: Record<string, string> = {
  DAILY: "var(--jade)",
  OCCASIONAL: "var(--clay)",
  AVOID: "var(--chili)",
};

const SUBTITLE: Record<string, string> = {
  DAILY: "Everyday-safe",
  OCCASIONAL: "Now & then",
  AVOID: "Leave it",
};

export default function VerdictSeal({
  verdict = "OCCASIONAL",
  score,
  size = 168,
  ring = "SCANIX VERDICT · FSSAI CROSS-CHECKED · ",
  stamp = false,
}: {
  verdict?: Verdict;
  score?: number;
  size?: number;
  ring?: string;
  stamp?: boolean;
}) {
  const id = useId().replace(/:/g, "");
  const pathId = `seal-${id}`;
  const color = COLORS[verdict] ?? "var(--marigold)";

  // repeat the ring phrase so it wraps the full circumference
  const ringText = ring.repeat(4).slice(0, 88);

  return (
    <div
      className={`seal${stamp ? " seal__stamp" : ""}`}
      style={
        {
          ["--seal-size" as string]: `${size}px`,
          ["--seal-color" as string]: color,
        } as React.CSSProperties
      }
      role="img"
      aria-label={`Verdict: ${verdict}${score != null ? `, score ${score} out of 100` : ""}`}
    >
      <svg viewBox="0 0 200 200" aria-hidden="true">
        <defs>
          <path
            id={pathId}
            d="M 100,100 m -80,0 a 80,80 0 1,1 160,0 a 80,80 0 1,1 -160,0"
            fill="none"
          />
        </defs>

        {/* outer + inner rules */}
        <circle cx="100" cy="100" r="92" fill="none" stroke="currentColor" strokeOpacity="0.28" strokeWidth="1" />
        <circle cx="100" cy="100" r="62" fill="none" stroke="currentColor" strokeOpacity="0.22" strokeWidth="1" />

        {/* rotating type ring */}
        <g className="seal__ring">
          <text
            fill="currentColor"
            style={{
              fontFamily: "var(--font-mono)",
              fontSize: "9.5px",
              letterSpacing: "0.18em",
              textTransform: "uppercase",
            }}
          >
            <textPath href={`#${pathId}`} startOffset="0">
              {ringText}
            </textPath>
          </text>

          {/* tick marks between rings */}
          {Array.from({ length: 48 }).map((_, i) => {
            const a = (i / 48) * Math.PI * 2;
            const r1 = 70;
            const r2 = i % 4 === 0 ? 76 : 73;
            // round so server + client render byte-identical strings (no hydration mismatch)
            const r = (v: number) => Math.round(v * 100) / 100;
            return (
              <line
                key={i}
                x1={r(100 + Math.cos(a) * r1)}
                y1={r(100 + Math.sin(a) * r1)}
                x2={r(100 + Math.cos(a) * r2)}
                y2={r(100 + Math.sin(a) * r2)}
                stroke="currentColor"
                strokeOpacity={i % 4 === 0 ? 0.5 : 0.22}
                strokeWidth="1"
              />
            );
          })}
        </g>
      </svg>

      <div className="seal__center">
        <span className="seal__verdict">{verdict}</span>
        {score != null ? (
          <span className="seal__score">
            {score}/100 · {SUBTITLE[verdict] ?? "Reviewed"}
          </span>
        ) : (
          <span className="seal__score">{SUBTITLE[verdict] ?? "Reviewed"}</span>
        )}
      </div>
    </div>
  );
}
