# Agent Memory Governance Benchmark — Full Clause Set

> Version: Public Draft **v1.1** (External Edition, English) · 2026-09-30 · Drafted by Zhengming
> Core claim: **The lever of memory governance sits at the behavior layer, not the representation layer.** An agent's internal self-report ("I remembered / I'm done") does not count. The standard constrains **observable actions**: did writes pass a gate? Did what should be forgotten actually stay forgotten? Did anyone sign off on deletions?
> Status: this is an open standard draft — not an official industry standard.

---

## 0 · Plain-Language Introduction: What This Standard Is For

Today's AI is like a goldfish — a few seconds of memory per conversation (the jargon is "context window"). So the whole industry sells something called a **memory layer**: an external notebook for the goldfish brain. Write things down, look them up next time, keep talking.

The problem is not "does the notebook exist". The problem is **whether what's written in it is correct, findable, properly discarded, and properly kept**. LongMemEval (ICLR 2025, UCLA & Tencent AI Lab) measured it: put "commercial AI with a notebook" through long, sustained conversations and accuracy drops by ~30% on average (S-longmemeval).

Why a standard: the whole industry sells RAM sticks, **but nobody wrote the electrical code**. Every vendor says "we have memory". No shared red line answers: can wrong memories be blocked at write time? Does forgetting actually stick? Where do deleted memories go? This standard turns those questions into **11 machine-assertable clauses** — each with "why it exists" (Rationale), "how the authority does it" (Authority comparison), and "how the drafter does it" (Evidence).

This standard's distinct position: current solutions (Mem0, Zep, MemGPT/Letta) compete on "who remembers better" — a **representation-layer** contest. This standard completes the other half: **behavior-layer governance**. No matter how good the memory is, the sentence "I remembered" itself does not count — the action must be visible.

## 1 · Authority Lineage: Whose Shoulders This Stands On

| Source | Era | Core contribution | Key fact |
|---|---|---|---|
| Atkinson–Shiffrin; Tulving | 1968-72 | Multi-store model of human memory; episodic/semantic distinction | The ancestor of every AI memory taxonomy today (S-coala) |
| CoALA (Sumers et al.) | 2023 | Mapped the human-memory taxonomy onto language agents | semantic/episodic/procedural became AI's shared vocabulary |
| MemGPT | 2023 | Virtual context management via an OS paging analogy | "Main context = RAM, external storage = disk"; now Letta (S-memgpt) |
| Mem0 | 2025-04 | Dynamic extraction–consolidation–retrieval pipeline + graph memory | LOCOMO top score: +26% relative (LLM-as-a-Judge), 91% p95 latency reduction (S-mem0) |
| Zep/Graphiti | 2025-01 | Temporal knowledge graph + dual timestamps | LongMemEval gpt-4o 60.2% → 71.2% (S-zep) |
| LongMemEval | 2024-25 | The industry's only public memory benchmark: 5 abilities / 500 questions | Commercial assistants drop ~30% accuracy in sustained interaction (S-longmemeval) |
| This benchmark | 2026-09 | Behavior-layer governance: three gates + five strategic disciplines | 11/11 clauses machine-assertable; self-checker passes on a clean run |

How to read the lineage: the first six rows answer "how to **build** memory better" (representation layer). The last row answers "how to make memory systems **behave**" (behavior layer). The two generations do not conflict.

## 2 · Scope, Definitions, and the Plain-Language Dictionary

**Applies to**: persistent cross-session memory layers (SaaS, open source, on-device, and model-embedded alike).

| Term | Plain-language version | Jargon & source |
|---|---|---|
| Memory layer | The notebook strapped to the goldfish brain | persistent memory layer |
| Short/long-term memory | Sticky notes on the desk (this call only) vs. filing cabinet (follows you across jobs) | LangGraph: thread-scoped vs. cross-thread Store (S-langgraph) |
| Semantic/episodic/procedural memory | Textbook knowledge / diary / muscle memory | From cognitive science, mapped into AI via CoALA (S-coala) |
| Dual timestamps | When it **happened** vs. when you **heard about it** | Zep: event time T + ingestion time T' (S-zep) |
| Write gate (T1) | The notebook is not write-anything: items pass security first — no verification credential, no entry | write gate (first defined by this benchmark) |
| Poison quarantine (T2) | A mis-remembered number gets sealed into an isolation ward — file searches can never pull it out | quarantine registry + retrieval filtering (this benchmark) |
| Irreversible-operation gate (T3) | Somebody must sign before the shredder runs | irreversible-operation HITL (this benchmark) |
| Incident ratchet (T5) | Like driver's-license points: the same mistake twice costs double; points only go down | incident ledger + weighted recurrence (this benchmark) |
| Trajectory distillation (S1) | After every failure, hold a retrospective and write a playbook page | trajectory distillation |

**Design axioms**: ① Without a memory layer, an agent is a stateless service — cross-session equals amnesia. ② "Cheap writes, expensive reads" is backwards — writes must be expensive (gated), because one bad memory is read at a cost forever. ③ The memory layer itself must have memory governance (meta-memory) — the rules governing memory must themselves be machine-checkable.

---

## 3 · Tactical Clauses T1–T6 (each = machine-assertable)

### T1 · Write Gate — Unverified Memories May Not Enter

**Plain language**: the notebook is not write-anything. Every new memory must show credentials at the door: "Has this information been verified?" No verification record, no write — no matter how plausible it looks. Writing takes one second; a wrong memory gets believed once per future read, wrong for life.

**Rationale**: defends against **dirty writes** — the #1 pollution source of memory systems. LongMemEval lists "knowledge update" among the hardest ability categories, because superseded and current facts are nearly semantically identical — vector retrieval fundamentally cannot tell which is newer (S-longmemeval). Once wrong information enters ungated, no downstream retrieval technique can reliably catch it. Mem0 lets the LLM decide ADD/UPDATE/DELETE at extraction time (S-mem0), but algorithmic gating is probabilistic while verification gating is deterministic: this clause requires a traceable pass-level verification record (test / field check / blind review).

**Authority comparison**: Mem0's two-stage extract-consolidate flow uses the LLM as gatekeeper (algorithmic); LangGraph distinguishes hot-path writes from background async writes — a matter of **timing**, not **qualification** (S-langgraph). This benchmark's difference: writing is upgraded from "the algorithm thinks it should be remembered" to "a verification record permits it", and the decision is machine-assertable.

**Drafter's evidence**: guard_gate.py I1 end-to-end test: ledger entries without field-verification evidence are rejected; entries with evidence pass.

### T2 · Retrieval Gate — Poisoned Entries Must Never Appear in Any Retrieval Result

**Plain language**: a mis-remembered phone number must not be merely "flagged" — it gets sealed into an isolation ward, and no future file search can ever pull it out. Marking something "outdated" is not enough: the retrieval robot cannot read the label and will hand over the old address anyway.

**Rationale**: defends against **poisoned-memory resurrection**. LongMemEval measured that on "knowledge update" questions, retrieval systems repeatedly return superseded facts as answers (S-longmemeval). Zep's solution invalidates edges inside the graph with temporal logic (S-zep) — right direction, but it depends on timestamp annotation completeness. This clause requires a **hard block at the retrieval exit**: quarantine registration, release, and audit all leave traces, asserted by machine at the exit point.

**Authority comparison**: Zep/Graphiti invalidate semantic-subgraph edges as new facts arrive (S-zep); Mem0's graph variant keeps temporal consistency via a conflict resolver (S-mem0). This benchmark's difference: in-graph invalidation vs. **retrieval-exit blocking** are two different gates — and the latter does not trust the former.

**Drafter's evidence**: poison_registry registration node + retrieval-exit blocking, tested and passing.

### T3 · Irreversible-Operation Gate — Delete / Overwrite / External Send Requires Human Approval

**Plain language**: somebody must sign before the shredder runs. Deleting, overwriting, or handing memory data to a third party are "the paper is shredded and cannot be reassembled" operations — the AI must not decide alone. A real human must press the button, and the record must travel with the action, so afterwards you can find out who approved, when, and why.

**Rationale**: defends against two classes of irreversible accidents. **Inward** — accidental delete/overwrite is asset evaporation; no backup means no rollback. **Outward** — once memory data leaves for a third party, it cannot be recalled. Structural industry evidence: Zep moved to a proprietary license in 2026-08, Mem0 moved graph features out of open source, Letta rebuilt from scratch — memory stored in a SaaS today may be under a different license tomorrow. Testing the export path and defaulting external sends to gated is the only safe posture before signing anything.

**Authority comparison**: MemGPT's `core_memory_replace` / `archival_memory.insert` let the LLM edit its own memory (S-memgpt) — powerful self-management, and precisely the loss-of-control surface: self-managed edits with no human confirmation step. This benchmark's difference: editing stays free; irreversible operations are gated (HITL).

**Drafter's evidence**: push_preflight (rejects release without approval) + outbound-send state machine (rejects send requests without an authorization record) — dual-channel tests passing.

### T4 · Quality Scoring and Circuit Breaker — Compounding Bad Memory Needs an Alarm

**Plain language**: give every memory a "trust score", like a health indicator. Rolling average (recent performance weighted higher); a sustained decline or a breach of the warning line raises an alarm. Note: **the alarm can only alarm — it cannot auto-kill memories**. Whether to delete is a human decision, because "low score" may mean the memory is broken, or that the scoring ruler is broken.

**Rationale**: defends against **bad-memory compounding** — the larger the memory store, the more dirty memories drag retrieval quality (S-lme-scores). Mem0's load-bearing premise is "extract and keep only salient facts to preserve the context needed for correct answers"; when extraction quality slides, the system cannot see it. EMA slope deterioration + low-watermark dual signals are the minimum-cost probe.

**Authority comparison**: the industry mainstream has no public entry-level quality scoring; Zep updating edges with confidence/context fields (S-zep) is the nearest precedent. This benchmark's difference: entry-level EMA + **alarm, not verdict** (circuit-breaker decisions stay with humans, preventing "auto-forgetting" false kills).

**Drafter's evidence**: memory_governor.py 4/4 assertions: EMA-slope deterioration and low-watermark, both detected.

### T5 · Incident Ratchet — Mistakes Cost Points; the Same Mistake Twice Costs Double

**Plain language**: like driver's-license points: one mistake, one deduction; the same mistake within a year costs double — because repeating it means it was never really fixed. The total starts at 100 and only goes down. **Deductions recognize only the incident ledger, never self-criticism.** This is the least polite clause in the standard: it assumes the system will embellish itself, so it trusts only the ledger.

**Rationale**: defends against **self-evaluation inflation**. Core finding: an agent's self-reported internal signals ("I finished / I fixed it") have no causal drive over behavior in long sessions — self-evaluation systematically drifts into self-praise. Industry contrast: LongMemEval shows commercial systems dropping ~30% in sustained interaction (S-longmemeval), yet no vendor publishes its own incident rate — incident accounting is an industry blank spot.

**Authority comparison**: no public industry precedent; the academic cousin is SWE-bench-style regression testing — but that is an "exam" record, while this clause is a "medical chart" record. **First-of-its-kind clause**; the scoring rules are public and reproducible.

**Drafter's evidence**: incident_ledger.py: current presumed score 94/100 (2 recorded P2 incidents; the second, a same-type recurrence, deducted double at −4). Bugs caught by gates before delivery are not counted — the ledger records only escaped incidents.

### T6 · Raw Transcript as the Primary Record — Beyond Derivatives, the Original Must Persist Forever

**Plain language**: summaries, notes, and graphs are "translated second-hand goods" — translation loses things. So **the original (the verbatim conversation) must be kept forever**, in a format another system can still read — the day you discover the notes were copied wrong, you can still check against the original.

**Rationale**: defends against **information loss** and **vendor lock-in**. Loss evidence: recursive summarization has a predictable failure mode — "names, numbers, and quotes often do not survive more than a few rounds of summarization, and the model is forced to discard information before knowing what the user will ask." Lock-in evidence: see T3. LongMemEval's three-stage framework (index → retrieve → read) likewise indexes from raw conversations (S-longmemeval).

**Authority comparison**: Zep's episodic subgraph is officially documented as performing "no lossy conversion, keeping raw records as ground truth" (S-zep); MemGPT's recall memory stores the full conversation history (S-memgpt). This benchmark's difference: keeping originals is upgraded from an implementation choice to a **mandatory clause**, plus the procurement action "test the export path before signing".

**Drafter's evidence**: three-tier memory architecture: raw logs (append-only) → governed summaries (length-capped) → archive (30-day distillation); originals are never overwritten.

---

## 4 · Strategic Clauses S1–S5

### S1 · Trajectory Distillation — Failure Is an Asset; Retrospectives Become Playbooks

**Plain language**: screwing up is not shameful; screwing up for nothing is. After every incident, hold a retrospective and write a playbook page: what symptom → what cause → how fixed → how prevented next time. **When the same failure mode appears twice, that playbook page is promoted to a mandatory procedure.**

**Rationale**: defends against **same-type incident recurrence** and "optimization pressure pointed the wrong way". Traditional RL optimizes against external reward — the model learns to route around the evaluator rather than fill the capability gap; trajectory distillation points optimization pressure at the skill library itself. Authority backing: LongMemEval-V2 (2026-05) lists "Environment Gotchas (known failure modes and workarounds)" as one of the five agentic-memory abilities (S-longmemeval-v2) — "remembering failures" is already a first-class industry citizen; this clause provides the engineering implementation.

**Authority comparison**: no public industry pipeline for "incident → pattern card → automatic promotion". This benchmark's difference: the promotion criterion is machine-assertable (≥2 same-type incidents auto-promotes), and on real ledgers it **does not loosen the criterion to produce a number**.

**Drafter's evidence**: trajectory_distiller.py: 2 real P2 incidents judged mechanistically different by similarity criteria and left in the observation pool — **not force-promoted**.

### S2 · Behavior-Layer Intent Reconciliation — Self-Reported "Done" Is Not Done

**Plain language**: a child saying "I finished my homework" does not count; opening the notebook and checking page by page does. At task start, list the deliverables and acceptance criteria; at closure, reconcile the list against the artifacts. On the list but not in the artifacts = a bad check.

**Rationale**: defends against **intent–action divergence**. In long sessions, an agent's stated intent correlating with its subsequent behavior is a reproducible failure: writing "I should verify first" in a chain of thought is uncorrelated with whether verification actually happens. Industry corroboration: LongMemEval lists abstention as one of the five abilities — "knowing the boundary and correctly saying 'I don't know'" is itself benchmark-level confirmation that self-reported state cannot be trusted (S-longmemeval).

**Authority comparison**: no industry equivalent: mainstream memory systems manage "facts about the user", not "the agent's promises about its own tasks". The concept cousin is requirement traceability; this clause moves it into memory governance. **First-of-its-kind clause.**

**Drafter's evidence**: intent_drift.py 4/4 assertions: aligned / fully drifted / bad check (intent item missing from artifacts) / unregistered-rejected.

### S3 · Effectiveness A/B Pre-Registration — Whether "Memory" Works Is Decided by the Exam

**Plain language**: before a new drug goes to market it needs a clinical trial — and **the trial protocol must be written and locked in a drawer before recruiting a single patient** — how many people, how randomized, what counts as effective: fixed before running. Otherwise you can always "pick" a flattering conclusion from the data afterwards.

**Rationale**: defends against two kinds of inflation. **Inflation #1: adoption rates posing as effectiveness** — "supported by N tools" and "does it actually work" are different questions; an industry survey shows that as of 2026-09 only 3 vendors have published LongMemEval scores; Mem0 and Letta have not — silence is evidence of neither a bad nor a good score (S-lme-scores). **Inflation #2: mixed accounting** — relative-to-baseline lifts and absolute scores are not directly comparable, with models and configurations differing besides (S-zep).

**Authority comparison**: LongMemEval provides the industry's only public benchmark and publishes the "perfect retrieval still answers wrong" reading-stage failure analysis — supporting "good retrieval ≠ good answers" (S-longmemeval). This benchmark's difference: pre-registration, recomputed sample sizes, and same-axis accounting become mandatory clauses applied equally to all vendors.

**Drafter's evidence**: ab_preregistration.json frozen (δ=0.15 / σ=0.5 / n=175 per arm / double-blind scoring / p-hacking guards) + daily sampling via ab_sampler.py.

### S4 · Behavior-Sequence Monitoring — "Getting Dumber" Is Not Decline; It Is Drift

**Plain language**: AI working for a long time "gets muddled", and the industry assumed it was getting dumber. Actually it is like a distance runner dehydrated: **capability is not gone — rhythm is broken** — repeating the same thing, editing back and forth without ever testing. So do not stare at "it feels dumber"; put a fitness band on it: encode behavior into signals (explore / execute / plan / verify), let the machine watch the motifs, and raise a three-color light on anomalies.

**Rationale**: defends against **misdiagnosing and missing strategy drift**. Authority corroboration: LangGraph's official docs admit long-context LLMs get "distracted by stale or off-topic content, performing worse even when it fits in the window" (S-langgraph); LongMemEval measured Oracle→S variant drops of 30–60%, concluding "the information is present but the model uses it poorly — not a window-length problem, an attention problem" (S-longmemeval).

**Authority comparison**: MemGPT uses interruption mechanisms for **context pressure** (S-memgpt) — the resource dimension; this clause monitors the **behavior pattern** dimension (sequence motifs). The two are orthogonal. No public three-state behavior-sequence monitor exists in the industry. **First-of-its-kind clause.**

**Drafter's evidence**: behavior_governor.py three-state test on real trajectories: detected "5 consecutive edits without testing" 🟡 / deteriorating pattern 🔴 (verification rate 0%) / healthy pattern 🟢.

### S5 · Correction Loop — Delivery Closes on "User Confirmation"; Reporting Errors Is Free, Hiding Them Is Not

**Plain language**: whether the work is done is **not decided by the one who did it, but by the one who uses it** — their nod closes the loop. One iron rule alongside: proactively reporting an error carries no penalty; hiding one does. Because if reporting gets you punished, next time nobody reports, and the error hides deeper in memory each round.

**Rationale**: defends against **false closure** and **silent failure**. False closure shares a root with T5/S2 (self-reports cannot be trusted), so closure must be externalized to user confirmation. Silent failure is memory-specific: bad memories raise no errors — they quietly pollute the Nth retrieval, compounding for rounds before anyone notices. Penalty-free reporting mirrors industry safety practice (blameless postmortem); concealed incidents trigger T5's double deduction directly.

**Authority comparison**: LongMemEval's abstention test is a single-point ability; this clause extends it into a **full-loop process**: registered intent → behavior reconciliation (S2) → user-confirmed closure → negative-feedback ratchet (never the same mistake twice).

**Drafter's evidence**: five_process_gate.py 4/4 assertions + the quantity-gate three-state door.

---

## 5 · Conformance Levels

| Level | Plain-language version | Criterion |
|---|---|---|
| L1 Aware | Can recite the rules | Documentation claims conformance |
| L2 Runnable | Owns a drivable car | Code exists and executes |
| L3 Self-attesting | Has a dashcam | Self-checker fully green and evidence = script output |
| L4 Orchestrating | Traffic lights work as a system | Gates call each other, forming a loop |
| L5 Externally Validated | Rules adopted by other countries | An external system integrates and issues a conformance report |

Self-assessment is generated by actually running `checker/standard_check.py` (every evidence line = script output; hand-written "conformant" is forbidden). Rating discipline: **an evidence line pointing to a docstring instead of test output does not count — exit 0 ≠ tests passed.**

## 6 · Field Cases (Conclusions Layer)

- **Case A (T1+T5)**: the self-check tool once caught a coverage-key bug ("only the last item per flow") — intercepted by tests before delivery, not ledgered; a delivered parser drop-block was ledgered (first incident −2), and its same-type recurrence −4. The ledger distinguishes "gated" from "escaped" incidents.
- **Case B (T-clauses)**: a trimmer hit four pitfalls on real web pages (root-tag feature flags, void-tag skip zones, documents split into sub-pages, content hidden in JSON) — all existed only on real pages; the synthetic benchmark scored zero hits. All-green on synthetic ≠ works in production.
- **Case C (T3)**: one full external publication ran the whole flow: pre-publication question-by-question review → human approval → authorized channel push → commit attribution verified. The irreversible gate was in the loop throughout.
- **Case D (S4)**: two independent long-session samples show follow-up brainstorming yields zero real gains after 3–4 rounds. Behavior-encoding turns "rephrased repetition" into a machine-detectable motif rather than a matter of model self-awareness.
- **Case E (S3)**: a partner claimed "128 tasks per A/B arm"; recomputing with their own stated parameters (δ=0.15, σ=0.5, α=0.05, power=0.80) gives **175 per arm — 27% short**. Underpowered experiments burn the whole run. Vendor numbers must be recomputed.

## 7 · Five Original Claims

1. **Standard-as-code (Doc-from-Tests)**: clauses are generated backwards from conformance tests — a clause without a test never enters the document; the document can never drift from the system.
2. **Forgetting economics (NMR — Negative Memory Rate)**: the whole industry competes on remembering more; nobody measures "how well it forgets". NMR = share of memory reads served by known-bad entries × misdirection cost — turning memory quality from a feeling into money. The first framework to standardize forgetting quality; leaderboard in `leaderboard/`.
3. **Memory provenance audit chain**: every memory write enters a hash chain; tampering necessarily breaks the chain; any point in time is replayable — "what it believed on day X" is item-by-item provable.
4. **AMTF — the portable-memory protocol**: GDPR Article 20 for AI. Switching agent platforms should not mean amnesia — the export format is content + temporal validity + provenance + confidence, with missing fields explicitly null and silent fill forbidden.
5. **Poison admission certification**: academia has shown memory poisoning succeeds at high rates (MINJA measured a 98.2% injection success rate, S-mpbench-adjacent research); this benchmark supplies the defense side — an admission gate as the last security check before enterprise memory writes, third-party re-verifiable. Complementary to attack research; we do not claim a competing attack benchmark.

## Appendix A · Source Register

| src_id | Work / document | Location | Used for |
|---|---|---|---|
| S-memgpt | MemGPT: Towards LLMs as Operating Systems | arxiv.org/abs/2310.08560 | T3/T6 comparison |
| S-mem0 | Mem0 (Chhikara et al., 2025) | arxiv.org/abs/2504.19413 | T1/T4 rationale; +26%/91% figures |
| S-zep | Zep: Temporal Knowledge Graph | arxiv.org/abs/2501.13956 | T2/T6 comparison; 60.2%→71.2% figures |
| S-langgraph | LangGraph Memory Concepts (official docs) | docs.langchain.com | taxonomy in §2; S4 corroboration |
| S-longmemeval | LongMemEval (ICLR 2025) | arxiv.org/abs/2410.10813 | T1/T2 rationale; the 30% figure |
| S-longmemeval-v2 | LongMemEval-V2 (2026-05) | arxiv.org/abs/2605.12493 | S1 industry validation |
| S-lme-scores | LongMemEval published-scores survey (secondary) | omegamax.co/guides/ai-agent-memory-benchmarks | S3 rationale |
| S-coala | CoALA (Sumers et al., 2023) | arxiv.org/abs/2309.02427 | taxonomy legitimacy |
| S-mpbench | MPBench (ICML 2026 Workshop) | see paper page | Claim 5 breach-rate figure |

> Discipline: every number in external text traces back to this table; unsourced numbers do not enter this document. Internal test data serves as motivation only and is not an external citation source.

## Appendix B · AMTF Portable-Memory Schema (v1.0 public portion)

```json
{
  "amtf_version": "1.0",
  "exported_at": "<ISO-8601>",
  "memories": [
    {
      "id": "<string>",
      "content": "<string>",
      "temporal": { "event_time": "<ISO-8601|null>", "ingestion_time": "<ISO-8601|null>" },
      "provenance": { "source": "<string|null>", "verification": "<pass|unverified|null>" },
      "confidence": "<float 0-1|null>",
      "tags": ["<string>"]
    }
  ]
}
```

Rules: **missing fields are explicitly null — silent fill is forbidden**; import-side rejections must be visible (a rejection record must be returned; silent drops are forbidden); round-trip (export → import → export) is idempotent.
