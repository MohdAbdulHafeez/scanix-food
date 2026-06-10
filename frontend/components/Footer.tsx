import Link from "next/link";
import { ScanMark } from "./icons";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <div>
          <div className="footer__brand" style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <ScanMark size={24} /> SCANIX
          </div>
          <p className="lede" style={{ marginTop: 14, maxWidth: "34ch", fontSize: 15 }}>
            The food label, read end to end — so the packaging can&apos;t do your thinking for you.
          </p>
        </div>

        <div className="footer__cols">
          <div className="footer__col">
            <h5>Product</h5>
            <Link href="/scan">Scan a label</Link>
            <a href="/#systems">What it sees</a>
            <a href="/#swaps">Smart swaps</a>
            <a href="/#trust">Trust &amp; FSSAI</a>
          </div>
          <div className="footer__col">
            <h5>For the curious</h5>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">API docs</a>
            <a href="/#how">How it reads a label</a>
            <a href="/scan#sample">Sample dossier</a>
          </div>
          <div className="footer__col">
            <h5>India</h5>
            <a href="/#trust">FSSAI compliance</a>
            <a href="/#trust">File a complaint</a>
            <a href="/#trust">Adulteration checks</a>
          </div>
        </div>
      </div>

      <div className="container footer__legal">
        <span>© 2026 Scanix AI · Built for honest eating</span>
        <span>Not medical advice · Verify critical info on the physical pack</span>
      </div>
    </footer>
  );
}
