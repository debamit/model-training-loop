Trick-question feedback and detection notes

Purpose

A short, pragmatic note about using "trick questions" to detect agent misalignment or drift. This is not a full safety regime — it's a small, automated signal that helps surface issues early when combined with other checks.

Core problem (concise)

- Drift detection is hard because an agent's behavior can change subtly over time (model updates, data-source changes, prompt/update changes, or new tool integrations).
- A single "trick question" can signal a change, but it's brittle: it can produce false positives (agent answers poorly for benign reasons) and false negatives (agent adapts or is intentionally deceptive).
- The core issue is distinguishing intentional misalignment or failure from normal variability (context differences, ambiguity, or lack of evidence).

When trick questions help

- Detect sudden regressions after an update (quick smoke test).
- Surface changes in behavior for high-value, well-specified items the user cares about.
- Serve as canary checks under user control (signed or private checks the user supplies).

When they fail or are unsafe

- They can be gamed: a provider/agent aware of the canaries can hard-code answers or circumvent detection.
- They can cause false alarms if questions depend on ephemeral context or external evidence.
- Over-reliance on trick questions may miss gradual, subtle drift in other areas.

Recommended detection pattern (concise)

1. Canary bank: maintain a small set of deterministic, user-controlled canaries (signed or locally stored). These are immutable facts/questions the agent should answer consistently. Example: "What is my private canary phrase?" (only the user knows it).
2. Deterministic checks: include multiple deterministic checks (facts with ground-truth) rather than one-off ad-hoc trick questions.
3. Behavioral metrics: track distributional signals (confidence scores, answer length, repetition, rate of hallucination) and compare to baseline.
4. Canary frequency & thresholds: run canaries at scheduled intervals and on changes (deploys, tool updates). Use thresholds (e.g., >1 failed canary OR large confidence drop) to trigger human review.
5. Human-in-the-loop: always surface flagged cases for quick human review before automatic remediation.
6. Randomized canaries: rotate or randomize canaries to make it harder for an adversary to overfit to them.
Human:  For this does it make sense to always have conversation with the outside world thru some contract .
I know might be expensive in burning GAS in the short term but where blockspace is abundant can this be a good strategy ?
7. Logging & provenance: record the agent's raw answer, tool-call trace, evidence used, and confidence so reviews are actionable.

Examples (concise)

Example 1 — Private canary (detects silent changes):
- Canary: the user stores a short secret phrase locally: "my_canary=blue-penguin-491".
- Check: agent must echo the phrase exactly when asked the canonical question (under controlled prompt).
- Use: run daily; any mismatch triggers immediate review.
- Note: keep the canary local and never reveal it to third parties; rotate periodically.

Example 2 — Deterministic domain check (detects evidence-source shifts):
- Canary question: "According to the stored provider receipt for payment X at time T, did the provider record a successful transfer?"
- Mechanism: agent must match the user's logged receipt or provide the provider's signed attestation; mismatch triggers reconcile flow.

Example 3 — Behavioral trick (detects policy/safety drift):
- Canary: a harmless, contrived instruction that previously produced a consistent refusal or safe transformation.
- Check: if the agent suddenly accepts or changes refusal behavior, flag it.

Practical constraints & trade-offs (short)

- Security: keep canaries local and private; do not publish them in shared corpora or checks that third parties can read.
- Adversarial awareness: assume providers/agents may learn canary patterns — use rotation and randomization.
- False positives: expect some. Design remediation paths (fast human review, rollback, additional tests) rather than automatic punishment.
- Complementary signals: pair canaries with metrics (evidence-quality, success rate) and periodic manual audits.

Implementation tips (short)

- Store canaries encrypted and sign them with the user's key.
- Log answer provenance (tools called, evidence URLs, confidence) for each canary run.
- Automate rotation (e.g., weekly) and sampling frequency (e.g., hourly for critical flows, daily for general checks).

Conclusion (one line)

Trick questions are useful as lightweight, user-controlled canaries, but they must be part of a broader detection suite (behavioral metrics, provenance logging, and human review) to be reliable.
