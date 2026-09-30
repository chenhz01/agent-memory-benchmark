# MANIFEST — What's open, what's not

> 3-sentence read: this table decides what in this repo is **free** (the exam:
> clauses + tool skeletons), what is **collaboration-only** (the grading recipes:
> calibration methodology), and what is **never in this repo** (the house cards:
> pricing, customer lists, roadmap). The split is deliberate — the standard
> spreads for free; the services around it pay the bills.

## 🌱 Free layer (MIT)

| # | Asset | Where |
|---|-------|-------|
| F1 | Full standard text: 11 clauses (T1-T6 + S1-S5), each four-layer (Feynman / rationale / authority / evidence) | `standard/STANDARD.md` |
| F2 | L1-L5 conformance rating table | `standard/STANDARD.md` §5 |
| F3 | Self-checker skeleton: interface + exit-code contract + structure assertions | `checker/standard_check.py` |
| F4 | Conformance cases (machine-readable) | `conformance/cases.jsonl` |
| F5 | Toy example: write gate + quarantine in ~80 lines, zero deps | `tools/examples/toy_memory_gate.py` |
| F6 | Feynman intro + authority lineage + case conclusions (sanitized) + AMTF schema (public part) | `standard/STANDARD.md` §0-2, §6, 附录 B |
| F7 | NMR leaderboard submission spec (open data-flywheel channel) | `leaderboard/SUBMISSION.md` |

## 🔒 Collaboration layer (available via collaboration — see `COLLABORATION.md`)

| # | Asset | Why locked |
|---|-------|-----------|
| L1 | Production calibration recipes (NMR cost-anchor derivation, threshold calibration methodology, provenance-chain production parameters) | Holders could resell enterprise grading services; the recipe IS the pricing power |
| L2 | Certification re-run harness (per-clause probe battery, anti-self-report guards) | The certification service itself |
| L3 | Poison-corpus construction recipes + pattern library | Publicly shipping attack patterns helps attackers, not defenders |
| L4 | Industry playbook templates | Engagement-layer deliverables |

## 💎 Never in this repo

Pricing sheets · customer/partner lists · roadmap commitments · internal
incident ledgers · production memory data. No exceptions.

> Split discipline: every asset must pass the three questions (distillability /
> trust / funnel) before entering the free layer. If the free layer ever exceeds
> ~70% independently monetizable content, the split has failed and gets re-cut.
