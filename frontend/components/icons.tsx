/* Hand-drawn line icons (24×24, stroke = currentColor).
   Kept in one file so the visual language stays consistent. */

type P = { className?: string; size?: number; style?: React.CSSProperties };

const base = (size = 24, className?: string, style?: React.CSSProperties) => ({
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.6,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  className,
  style,
});

export const ScanMark = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M3 8V5a2 2 0 0 1 2-2h3M16 3h3a2 2 0 0 1 2 2v3M21 16v3a2 2 0 0 1-2 2h-3M8 21H5a2 2 0 0 1-2-2v-3" />
    <path d="M3 12h18" strokeWidth="2" />
    <circle cx="12" cy="12" r="3.4" />
  </svg>
);

export const Aperture = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <circle cx="12" cy="12" r="9" />
    <path d="M12 3a9 9 0 0 0-7.8 4.5L12 12M21 12a9 9 0 0 0-3.2-6.9L12 12M12 21a9 9 0 0 0 7.8-4.5L12 12" />
  </svg>
);

export const Beaker = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M9 3h6M10 3v6.5L5.2 17a2 2 0 0 0 1.8 3h10a2 2 0 0 0 1.8-3L14 9.5V3" />
    <path d="M7.5 14h9" />
  </svg>
);

export const Pulse = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M3 12h4l2.5-7 5 14L17 12h4" />
  </svg>
);

export const Eye = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7Z" />
    <circle cx="12" cy="12" r="3" />
  </svg>
);

export const Twin = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <circle cx="9" cy="6" r="2.4" />
    <path d="M5 21v-5a4 4 0 0 1 4-4 4 4 0 0 1 4 4v5" />
    <path d="M15.5 8.5c2.5 0 4 1.8 4 4s-1.5 4-4 4" strokeDasharray="2 2" />
  </svg>
);

export const Shield = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6l-7-3Z" />
    <path d="m9 12 2 2 4-4" />
  </svg>
);

export const Swap = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M4 8h13l-3-3M20 16H7l3 3" />
  </svg>
);

export const Doc = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M6 3h8l4 4v14a0 0 0 0 1 0 0H6a0 0 0 0 1 0 0V3Z" />
    <path d="M14 3v4h4M9 13h6M9 17h6" />
  </svg>
);

export const User = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <circle cx="12" cy="8" r="3.4" />
    <path d="M5 21a7 7 0 0 1 14 0" />
  </svg>
);

export const Check = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="m4 12 5 5L20 6" strokeWidth="1.8" />
  </svg>
);

export const Alert = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M12 9v4M12 17h.01" />
    <path d="M10.3 3.9 2.4 18a2 2 0 0 0 1.7 3h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" />
  </svg>
);

export const Cross = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M6 6l12 12M18 6 6 18" />
  </svg>
);

export const Upload = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5" />
    <path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2" />
  </svg>
);

export const Arrow = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M5 12h14m0 0-5-5m5 5-5 5" />
  </svg>
);

export const Leaf = ({ className, size, style }: P) => (
  <svg {...base(size)} className={className} style={style}>
    <path d="M4 20C3 12 8 4 20 4c0 12-8 17-16 16Z" />
    <path d="M9 15c3-4 6-6 9-7" />
  </svg>
);
