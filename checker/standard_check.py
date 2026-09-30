"""standard_check — Agent Memory Governance Benchmark 自检器（免费层，MIT）.

Default mode (--structure, also run with no args) machine-asserts that
standard/STANDARD.md keeps all 11 clauses four-layer complete
(Feynman / rationale / authority / evidence) — docs can never silently
degrade into a "conclusions-only clause list".

Certification mode (--target) runs per-clause probes against a memory
system; production probes stay in the collaboration layer.

Exit codes are the machine contract; conformance/ tests consume them.
  0 = all green   2 = evidence missing   3 = clause failed
  4 = provenance chain broken            5 = doc structure invalid
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- Machine contract: exit codes (free layer) -----------------------------
EXIT_ALL_GREEN = 0         # all clauses pass at declared level
EXIT_EVIDENCE_MISSING = 2  # evidence file absent -> capability not established
EXIT_CLAUSE_FAILED = 3     # at least one clause failed
EXIT_TAMPER_DETECTED = 4   # provenance chain broken (see provenance hook below)
EXIT_STRUCTURE_INVALID = 5 # clause doc lacks feyman/rationale/authority/evidence layers

# --- Conformance levels ----------------------------------------------------
LEVELS = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}


@dataclass
class ClauseResult:
    clause_id: str          # e.g. "T1" write gate
    level_claimed: str      # what the target declares
    level_proven: str       # what the evidence supports
    evidence_path: str      # file path; missing file == capability absent
    passed: bool
    detail: str = ""


@dataclass
class Report:
    target: str
    results: list[ClauseResult] = field(default_factory=list)

    def verdict(self) -> int:
        if any(r.evidence_path == "" or not Path(r.evidence_path).exists()
               for r in self.results):
            return EXIT_EVIDENCE_MISSING
        if all(r.passed for r in self.results):
            return EXIT_ALL_GREEN
        return EXIT_CLAUSE_FAILED


# --- Structure mode (runnable in the free layer) ---------------------------

def load_cases(cases_path: Path) -> list[dict] | None:
    """Read conformance cases (JSONL, one case per line)."""
    if not cases_path.exists():
        return None
    cases = []
    try:
        for line in cases_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return cases


def clause_section(text: str, clause_id: str) -> str | None:
    """Slice one clause's section (up to the next same-level heading)."""
    pattern = re.compile(
        r"^###\s+" + re.escape(clause_id) + r"\b.*?(?=^###\s+|\Z)",
        re.S | re.M,
    )
    m = pattern.search(text)
    return m.group(0) if m else None


def _fallback_section(text: str, cid: str) -> str | None:
    if cid == "RATING":
        m = re.search(r"^##\s+5 ·.*?(?=^##\s+|\Z)", text, re.S | re.M)
    elif cid == "SOURCES":
        m = re.search(r"^##\s+附录 A ·.*?(?=^##\s+|\Z)", text, re.S | re.M)
    else:
        return None
    return m.group(0) if m else None


def run_structure_check(root: Path) -> tuple[int, list[str]]:
    """Assert every clause in cases.jsonl exists with all required layers."""
    std_path = root / "standard" / "STANDARD.md"
    cases_path = root / "conformance" / "cases.jsonl"

    if not std_path.exists():
        return EXIT_EVIDENCE_MISSING, [f"standard doc missing: {std_path}"]
    cases = load_cases(cases_path)
    if cases is None:
        return EXIT_CLAUSE_FAILED, [f"conformance cases missing/unreadable: {cases_path}"]

    text = std_path.read_text(encoding="utf-8")
    failures: list[str] = []
    for case in cases:
        cid = case.get("id", "?")
        section = clause_section(text, cid) or _fallback_section(text, cid)
        if section is None:
            failures.append(f"[{cid}] clause section missing")
            continue
        for marker in case.get("required_markers", []):
            if marker not in section:
                failures.append(f"[{cid}] missing layer: {marker}")

    print(f"structure check: {len(cases)} cases against {std_path.name}")
    if failures:
        print(f"RESULT: FAIL ({len(failures)})")
        for f in failures:
            print("  -", f)
        return EXIT_STRUCTURE_INVALID, failures
    print("RESULT: PASS — 11 clauses four-layer complete, rating & sources present")
    return EXIT_ALL_GREEN, []


# --- Certification mode (collaboration layer) ------------------------------

def check_clause(clause_id: str, target_dir: Path, claim: str) -> ClauseResult:
    """Run one clause probe by executing its evidence script.

    # available via collaboration — see Contact
    (Production probe battery per clause — evidence-file schema, subprocess
    harness and anti-self-report guards — is a collaboration-layer recipe.
    The free layer ships the interface only.)
    """
    raise NotImplementedError("clause probes pending content extraction")


def verify_provenance(chain_file: Path) -> bool:
    """Replay the memory provenance hash chain; any break -> EXIT_TAMPER_DETECTED.

    # available via collaboration — see Contact
    (Production parameters: block sizing, snapshot cadence, concurrent-write
    sequencing and recovery-point strategy are collaboration-layer recipes,
    NOT included in this free-layer skeleton.)
    """
    raise NotImplementedError("free-layer reference parameters only")


def verify_threshold(claim: str, observed: float) -> bool:
    """Compare observed metric against the L3 bar for the claimed level.

    # available via collaboration — see Contact
    (Threshold calibration methodology — boundary-sample construction and
    false-positive/false-negative tradeoff parameters — is a collaboration-
    layer recipe. The free layer ships the comparison interface only.)
    """
    raise NotImplementedError("free-layer interface only")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Agent memory conformance check")
    parser.add_argument("--structure", action="store_true", default=True,
                        help="(default) structure-check standard/STANDARD.md")
    parser.add_argument("--target", type=Path, default=None,
                        help="root dir of the memory system under test (certification mode)")
    parser.add_argument("--report", type=Path, default=None,
                        help="write JSON report here")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent.parent

    if args.target is not None:
        # Certification mode: per-clause probes live in the collaboration layer.
        try:
            check_clause("T1", args.target, "L3")
        except NotImplementedError:
            print("certification probes are collaboration-layer — see COLLABORATION.md")
            return EXIT_EVIDENCE_MISSING

    code, failures = run_structure_check(root)

    if args.report:
        args.report.write_text(json.dumps(
            {"exit_code": code, "failures": failures}, ensure_ascii=False, indent=2),
            encoding="utf-8")
    return code


if __name__ == "__main__":
    sys.exit(main())
