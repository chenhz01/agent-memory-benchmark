# agent-memory-benchmark

> The **behavior-layer quality benchmark** for AI agent memory.
> 11 machine-assertable clauses · L1–L5 conformance rating · zero-dependency checker · first public "forgetting quality" metric (NMR).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![clauses](https://img.shields.io/badge/clauses-11%20machine--assertable-blue)](standard/STANDARD.md)
[![deps](https://img.shields.io/badge/deps-zero-orange)]()

## What is this

Commercial AI products ship "memory" with no common acceptance bar. LongMemEval
(ICLR 2025) showed commercial assistants lose ~30% accuracy in long-horizon
conversations. Everyone competes on *representing* memory better — nobody sets
the bar for whether memory **behaves**: are bad entries blocked at write time?
do superseded facts stay dead? does anyone sign off before irreversible deletes?

**We do not trust self-reported "I remembered." We check observable actions.**

- 11 clauses: T1–T6 tactical (gates, quarantine, HITL, ratchet, raw-transcript) + S1–S5 strategic (distillation, intent reconciliation, preregistered A/B, behavior monitoring, correction loop).
- Each clause is **four-layer complete**: Feynman explanation → rationale → authority comparison → evidence.
- Conformance rating **L1–L5**: knows / runs / self-proves / orchestrates / spills over.
- **NMR (Negative Memory Rate)**: the first public metric for *forgetting quality* — see `leaderboard/SUBMISSION.md`.
- **AMTF schema**: portable agent-memory export format (content + temporality + provenance + confidence) — the GDPR-Art.20 analog for agent memory.

## Quickstart (2 min, zero deps)

```bash
git clone https://github.com/chenhz01/agent-memory-benchmark.git
cd agent-memory-benchmark

# 1) structure-check the standard itself (exit 0 = 11 clauses four-layer complete)
python checker/standard_check.py

# 2) run the toy write-gate demo (3/3 PASS)
python tools/examples/toy_memory_gate.py
```

Wire the checker into CI as an acceptance gate for your own memory docs & systems.

## What's in the box

```
standard/STANDARD.md      # full standard text (Chinese)
standard/STANDARD_EN.md   # full standard text (English, External Edition v1.1)
checker/                  # self-checker: exit-code contract 0/2/3/4/5
conformance/cases.jsonl   # machine-readable clause cases
tools/examples/           # zero-dep toy implementations
leaderboard/              # NMR submission spec
MANIFEST.md               # what's open / collaboration-only / never-in-repo
COLLABORATION.md          # how to work with us
```

## Status

Open standard **draft** (not an official industry standard). v1.1 (External Edition), 2026-09-30.
Issue-driven: clause feedback, conformance case proposals, and NMR submissions
all welcome via issues.

## Contact

hcac4735@agent.qq.com · see `COLLABORATION.md`
