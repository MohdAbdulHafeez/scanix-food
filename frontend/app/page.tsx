import Link from "next/link";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import Reveal from "@/components/Reveal";
import VerdictSeal from "@/components/VerdictSeal";
import {
  ScanMark,
  Beaker,
  Pulse,
  Eye,
  Twin,
  Leaf,
  Swap,
  Shield,
  User,
  Arrow,
} from "@/components/icons";

const SYSTEMS = [
  { n: "01", Icon: ScanMark, t: "Identity", tag: "Scan", d: "OCR, barcode and OpenFoodFacts agree on exactly what you're holding — brand, category, the works." },
  { n: "02", Icon: Beaker, t: "Ingredients", tag: "Decode", d: "Every additive named in plain words, with the E-numbers that actually matter pulled to the front." },
  { n: "03", Icon: Pulse, t: "Metabolism", tag: "After you eat", d: "Glycemic and insulin load, so you know what it does to your blood sugar — not just its calorie count." },
  { n: "04", Icon: Eye, t: "Honesty", tag: "Claims", d: "Front-of-pack claims checked against the ingredient list. “No added MSG” doesn't get a free pass." },
  { n: "05", Icon: Twin, t: "Digital Twin", tag: "Your body", d: "A body model estimates the hit to your liver, heart, pancreas and kidneys from this product." },
  { n: "06", Icon: Leaf, t: "Explain", tag: "AI read", d: "A nutritionist-style explanation grounded in real sources — the why behind the verdict, in your words." },
  { n: "07", Icon: Swap, t: "Smart Swap", tag: "Do better", d: "Healthier products you can actually buy in India, ranked and compared nutrient by nutrient." },
  { n: "08", Icon: Shield, t: "Trust", tag: "Authentic?", d: "Adulteration and counterfeit signals, FSSAI licence validation, and an authenticity grade." },
  { n: "09", Icon: User, t: "Memory", tag: "About you", d: "Your allergies, medicines and scan history — so every future verdict is tuned to your body." },
];

export default function Home() {
  return (
    <>
      <Nav />

      {/* ===================== HERO ===================== */}
      <section className="hero">
        <div className="container hero__grid">
          <div>
            <p className="eyebrow">Food-label intelligence · made for India</p>
            <h1 className="hero__title">
              The label says one thing.
              <br />
              <em>Scanix reads the truth.</em>
            </h1>
            <p className="lede hero__sub">
              Snap a photo of any packaged food. In one tap, nine systems cross-examine
              the pack — ingredients, additives, FSSAI compliance, metabolic impact — and
              hand you a single honest verdict: <strong>eat daily, occasionally, or avoid.</strong>
            </p>

            <div className="hero__cta">
              <Link className="btn btn--solid" href="/scan">
                <ScanMark size={17} /> Scan a label
              </Link>
              <Link className="btn btn--ghost" href="/scan#sample">
                See a sample dossier <Arrow size={16} />
              </Link>
            </div>

            <div className="hero__stats">
              <div className="hero__stat">
                <div className="n">9</div>
                <div className="l">systems · one tap</div>
              </div>
              <div className="hero__stat">
                <div className="n">FSSAI</div>
                <div className="l">licences cross-checked</div>
              </div>
              <div className="hero__stat">
                <div className="n">~4s</div>
                <div className="l">photo to verdict</div>
              </div>
            </div>
          </div>

          {/* live-read panel */}
          <div className="hero__visual">
            <div className="scanpanel">
              <div className="scanpanel__bar">
                <span className="scanpanel__dot" /> Reading label · scan_3f9c…
                <span style={{ marginLeft: "auto" }}>OCR 84%</span>
              </div>
              <div className="scanpanel__body">
                <div className="scanline" aria-hidden="true" />
                <div className="readout">
                  <span className="readout__k">Product</span>
                  <span className="readout__v">Crunchwave Masala Magic</span>
                </div>
                <div className="readout">
                  <span className="readout__k">FSSAI licence</span>
                  <span className="readout__v good">valid · 100120…0123</span>
                </div>
                <div className="readout">
                  <span className="readout__k">Saturated fat</span>
                  <span className="readout__v flag">14.8g / 100g · high</span>
                </div>
                <div className="readout">
                  <span className="readout__k">Claim check</span>
                  <span className="readout__v flag">“No added MSG” vs INS 627</span>
                </div>
                <div className="readout">
                  <span className="readout__k">Hidden sugar</span>
                  <span className="readout__v warn">maltodextrin found</span>
                </div>
              </div>

              <div
                style={{
                  marginTop: 22,
                  display: "flex",
                  alignItems: "center",
                  gap: 18,
                  borderTop: "1px solid var(--line)",
                  paddingTop: 20,
                }}
              >
                <VerdictSeal verdict="AVOID" score={34} size={104} stamp />
                <div>
                  <div className="readout__k" style={{ marginBottom: 6 }}>Final verdict</div>
                  <div style={{ fontFamily: "var(--font-display)", fontSize: 19, lineHeight: 1.2 }}>
                    Ultra-processed. High sat-fat &amp; sodium.
                  </div>
                  <Link
                    href="/scan#sample"
                    className="mono"
                    style={{ color: "var(--marigold)", fontSize: 13, marginTop: 8, display: "inline-block" }}
                  >
                    Read the full dossier →
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ===================== MANIFESTO ===================== */}
      <section className="manifesto" id="how">
        <div className="container">
          <p className="manifesto__eyebrow">Why this exists</p>
          <h2 className="manifesto__title">
            Packaged food is engineered to look healthier <span>than it is.</span>
          </h2>
          <div className="manifesto__row">
            <Reveal className="manifesto__item">
              <b>Palm oil</b>
              <p>hides behind “baked”, “light” and a wholesome green leaf on the front of pack.</p>
            </Reveal>
            <Reveal className="manifesto__item" delay={90}>
              <b>627 · 631</b>
              <p>flavour enhancers that quietly survive a confident “No Added MSG” claim.</p>
            </Reveal>
            <Reveal className="manifesto__item" delay={180}>
              <b>712 mg</b>
              <p>of sodium in 100g of a snack that markets itself as the smart choice.</p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ===================== SYSTEMS PIPELINE ===================== */}
      <section className="section" id="systems">
        <div className="container">
          <Reveal className="sec-head">
            <p className="eyebrow">Nine ways to look at one pack</p>
            <h2>One scan runs a full interrogation.</h2>
            <p className="lede">
              These aren&apos;t menu items you pick from — every scan runs the whole pipeline,
              System 01 to 09, and folds the findings into a single dossier.
            </p>
          </Reveal>

          <Reveal className="pipeline">
            {SYSTEMS.map(({ n, Icon, t, tag, d }) => (
              <div className="pcard" key={n}>
                <span className="pcard__tag">{tag}</span>
                <div className="pcard__num">SYSTEM {n}</div>
                <Icon className="pcard__icon" size={34} />
                <h3>{t}</h3>
                <p>{d}</p>
              </div>
            ))}
          </Reveal>
        </div>
      </section>

      {/* ===================== TRUST / FSSAI ===================== */}
      <section className="section" id="trust" style={{ background: "var(--ink-1)" }}>
        <div className="container">
          <Reveal className="sec-head">
            <p className="eyebrow">Trust &amp; FSSAI · System 08</p>
            <h2>Is it even what it claims to be?</h2>
            <p className="lede">
              Beyond nutrition, Scanix checks the pack against India&apos;s food law — validating
              the FSSAI licence, watching for adulteration and counterfeit signals, and, when
              something&apos;s wrong, helping you do something about it.
            </p>
          </Reveal>

          <div className="trust__grid">
            <Reveal className="card card--paper">
              <p className="eyebrow" style={{ color: "var(--marigold-deep)" }}>Authenticity check</p>
              <h3 style={{ fontSize: 24, marginTop: 12 }}>Crunchwave Masala Magic · Grade B</h3>
              <div className="checklist">
                <div className="check">
                  <Shield className="check__mark" size={22} />
                  <div><b>FSSAI licence 10012021000123 — valid</b><span>Matched against the public registry.</span></div>
                </div>
                <div className="check">
                  <Shield className="check__mark" size={22} />
                  <div><b>No adulteration pattern detected</b><span>Low risk for this product category.</span></div>
                </div>
                <div className="check">
                  <Shield className="check__mark" size={22} />
                  <div><b>No counterfeit indicators</b><span>Label format and barcode are consistent.</span></div>
                </div>
                <div className="check">
                  <Eye className="check__mark" size={22} style={{ color: "var(--chili)" }} />
                  <div><b>2 claim contradictions flagged</b><span>“No added MSG” and “baked” don&apos;t match the ingredients.</span></div>
                </div>
              </div>
            </Reveal>

            <Reveal className="complaint" delay={90}>
              <span className="complaint__stamp">FSSAI complaint · ready to file</span>
              <h3>Found a violation? Don&apos;t just scroll past it.</h3>
              <p>
                When a scan turns up a real breach, Scanix drafts a formal FSSAI complaint from
                the evidence — a filled PDF with a QR code and the right portal link.
              </p>
              <div className="complaint__steps">
                <div><span>01</span> Scan flags the contradiction or violation</div>
                <div><span>02</span> Complaint PDF is generated from the dossier</div>
                <div><span>03</span> You download, review, and submit to FSSAI</div>
              </div>
              <Link className="btn btn--ghost" href="/scan" style={{ marginTop: 24, alignSelf: "flex-start" }}>
                Start with a scan <Arrow size={16} />
              </Link>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ===================== SMART SWAP ===================== */}
      <section className="section" id="swaps">
        <div className="container">
          <Reveal className="sec-head">
            <p className="eyebrow">Smart swaps · System 07</p>
            <h2>A verdict you can act on.</h2>
            <p className="lede">
              An &ldquo;avoid&rdquo; is only useful if you know what to reach for instead. Scanix ranks
              healthier products from the Indian market and compares them nutrient by nutrient.
            </p>
          </Reveal>

          <div className="swap__grid">
            <Reveal className="swapcard swapcard--from">
              <span className="swapcard__label">You scanned</span>
              <h4>Crunchwave Masala Magic</h4>
              <div className="swapcard__brand">Crunchwave · NOVA 4 · health 34/100</div>
              <SwapBars sat={14.8} sodium={712} sugar={7.4} protein={6.8} />
            </Reveal>

            <Reveal className="swapcard swapcard--to" delay={90}>
              <span className="swapcard__label">Buy instead</span>
              <h4>Roasted Masala Chana</h4>
              <div className="swapcard__brand">Tasty Nibbles · NOVA 2 · health 78/100</div>
              <SwapBars sat={2.1} sodium={410} sugar={1.2} protein={19} to />
            </Reveal>
          </div>
        </div>
      </section>

      {/* ===================== CTA ===================== */}
      <section className="section cta">
        <div className="container">
          <Reveal>
            <p className="eyebrow" style={{ justifyContent: "center", display: "inline-flex" }}>
              Your next snack, cross-examined
            </p>
            <h2 style={{ marginTop: 18 }}>Point your camera. Get the truth.</h2>
            <p className="lede" style={{ textAlign: "center" }}>
              No account needed to try it. Scan a label, or open the sample dossier to see
              everything Scanix pulls from a single photo.
            </p>
            <div className="cta__btns">
              <Link className="btn btn--solid" href="/scan">
                <ScanMark size={17} /> Scan a label
              </Link>
              <Link className="btn btn--ghost" href="/scan#sample">
                Open the sample dossier
              </Link>
            </div>
          </Reveal>
        </div>
      </section>

      <Footer />
    </>
  );
}

/* compact nutrient bars used in the swap comparison.
   max scales: sat 20g, sodium 1000mg, sugar 30g, protein 25g */
function SwapBars({
  sat,
  sodium,
  sugar,
  protein,
  to = false,
}: {
  sat: number;
  sodium: number;
  sugar: number;
  protein: number;
  to?: boolean;
}) {
  const rows = [
    { k: "Sat fat", v: `${sat}g`, pct: Math.min((sat / 20) * 100, 100), bad: true },
    { k: "Sodium", v: `${sodium}mg`, pct: Math.min((sodium / 1000) * 100, 100), bad: true },
    { k: "Sugar", v: `${sugar}g`, pct: Math.min((sugar / 30) * 100, 100), bad: true },
    { k: "Protein", v: `${protein}g`, pct: Math.min((protein / 25) * 100, 100), bad: false },
  ];
  return (
    <div className="bars">
      {rows.map((r) => {
        // for "bad" nutrients low is good; for protein high is good
        const good = r.bad ? r.pct < 35 : r.pct > 45;
        const color = good ? "var(--jade)" : r.pct > 70 ? "var(--chili)" : "var(--marigold)";
        return (
          <div className="bar__row" key={r.k}>
            <span className="bar__k">{r.k}</span>
            <span className="bar__track">
              <span className="bar__fill" style={{ width: `${Math.max(r.pct, 4)}%`, background: color }} />
            </span>
            <span className="bar__v">{r.v}</span>
          </div>
        );
      })}
    </div>
  );
}
