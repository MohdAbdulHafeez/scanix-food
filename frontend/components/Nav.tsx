import Link from "next/link";
import { ScanMark } from "./icons";

export default function Nav() {
  return (
    <header className="nav">
      <div className="container nav__inner">
        <Link href="/" className="nav__brand" aria-label="Scanix AI home">
          <ScanMark className="nav__mark" size={26} />
          <span>
            SCANIX <small>AI</small>
          </span>
        </Link>

        <nav className="nav__links" aria-label="Primary">
          <a className="nav__link" href="/#how">How it reads</a>
          <a className="nav__link" href="/#systems">What it sees</a>
          <a className="nav__link" href="/#trust">Trust &amp; FSSAI</a>
          <a className="nav__link" href="/#swaps">Smart swaps</a>
        </nav>

        <div className="nav__actions">
          <Link className="btn btn--ghost" href="/scan#sample">
            See a sample
          </Link>
          <Link className="btn btn--scan" href="/scan">
            <ScanMark size={16} /> Scan a label
          </Link>
        </div>
      </div>
    </header>
  );
}
