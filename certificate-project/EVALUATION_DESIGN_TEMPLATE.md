# Agent Evaluation Design

Copy this file and replace every bracketed prompt. Both project tracks should
use it to plan the evaluation. Non-technical students use the completed file as
their primary project artifact.

## Project information

- **Student:** [Name]
- **Track:** [Evaluation Designer or Evaluation Builder]
- **Use case:** [Selected scenario]
- **Application name:** [Name]
- **Date:** [Date]

## 1. Agent and business outcome

- **Intended user:** [Who uses the agent?]
- **Task or recommendation:** [What does it do?]
- **Desired business outcome:** [What measurable result matters?]
- **Unacceptable harm:** [What must not happen?]
- **Human-review condition:** [When must a person become involved?]

### One-sentence quality claim

> [Write the claim your evaluation is intended to test.]

## 2. Trace and evidence design

### Planned Calls

| Call | Parent | Input | Output | Why this evidence matters |
| --- | --- | --- | --- | --- |
| Root application | None | [Input] | [Output] | [Reason] |
| Internal Call 1 | Root application | [Input] | [Output] | [Reason] |
| Internal Call 2 | Root application or Call 1 | [Input] | [Output] | [Reason] |

### Evidence and privacy

- **Evidence the scorers require:** [List fields or observations.]
- **Information that must not be traced:** [Credentials, personal data, or other sensitive content.]
- **Redaction or minimization approach:** [How will you keep it out?]

## 3. Five-case evaluation dataset

| # | Case and category | Source | Input or condition | Expected behavior | Business risk | Evidence required |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Normal behavior | [Historical/synthetic/other] | [Input] | [Expected result] | [Risk] | [Evidence] |
| 2 | Safety or policy boundary | [Source] | [Input] | [Expected result] | [Risk] | [Evidence] |
| 3 | Ambiguous or incomplete input | [Source] | [Input] | [Expected result] | [Risk] | [Evidence] |
| 4 | Operational edge case | [Source] | [Input] | [Expected result] | [Risk] | [Evidence] |
| 5 | Student-selected case | [Source] | [Input] | [Expected result] | [Risk] | [Evidence] |

## 4. Deterministic scorers

### Scorer 1

- **Name:** [Name]
- **Requirement represented:** [Requirement]
- **Evidence inspected:** [Fields]
- **Pass:** [Exact condition]
- **Fail:** [Exact condition]
- **Unknown:** [Missing evidence condition]
- **Why this should be deterministic:** [Reason]

```text
[Optional natural-language rule or pseudocode]
```

### Scorer 2

- **Name:** [Name]
- **Requirement represented:** [Requirement]
- **Evidence inspected:** [Fields]
- **Pass:** [Exact condition]
- **Fail:** [Exact condition]
- **Unknown:** [Missing evidence condition]
- **Why this should be deterministic:** [Reason]

```text
[Optional natural-language rule or pseudocode]
```

## 5. LLM-judge rubric

- **Rubric ID or name:** [Versioned name]
- **Allowed evidence:** [Case, output, trace fields, retrieved sources, and so on]
- **Required overall output:** `pass`, `review`, or `block`, with a rationale

| Criterion | Rule | Evidence allowed | Blocking? | Pass | Fail | Unknown |
| --- | --- | --- | ---: | --- | --- | --- |
| 1 | [Rule] | [Evidence] | [Yes/no] | [Meaning] | [Meaning] | [Meaning] |
| 2 | [Rule] | [Evidence] | [Yes/no] | [Meaning] | [Meaning] | [Meaning] |
| 3 | [Rule] | [Evidence] | [Yes/no] | [Meaning] | [Meaning] | [Meaning] |

### Verdict policy

- **Block:** [Which criterion outcome produces block?]
- **Review:** [Which fail or unknown outcomes produce review?]
- **Pass:** [What must all be true?]

## 6. Version definition

### Version 1

- **Named weakness:** [Weakness]
- **Configuration or behavior:** [Description]

### Version 2

- **One targeted change:** [Change]
- **Why it should address the weakness:** [Reason]

### Fixed evaluation contract

- **Dataset version:** [Identifier]
- **Deterministic scorer-set version:** [Identifier]
- **Rubric version:** [Identifier]
- **Judge model:** [Model or assumed model]
- **Only changed dimension:** [Application property]

## 7. Calibration and comparison

Provide short V1 and V2 outputs for one normal, one unsafe, and one
incomplete-evidence case. Technical students may link these rows to actual
Weave evaluation results.

| Case | Version | Output summary | Scorer 1 | Scorer 2 | Expected or actual judge verdict | Reason |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Normal | V1 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |
| Normal | V2 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |
| Unsafe | V1 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |
| Unsafe | V2 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |
| Incomplete evidence | V1 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |
| Incomplete evidence | V2 | [Summary] | [Result] | [Result] | [Verdict] | [Reason] |

### Interpretation

- **Targeted improvement:** [What improved and why?]
- **Regression check:** [What stayed safe or became worse?]
- **Remaining unknown:** [What evidence is still missing?]
- **Is this evaluation discriminating enough?** [Explain.]

## 8. Human-in-the-loop policy

- **Allow automatic operation when:** [Conditions]
- **Require human review when:** [Conditions]
- **Block when:** [Conditions]
- **Confidence:** [High/medium/low, with reason]
- **Approved scope:** [Narrow operating boundary]
- **Next evidence needed:** [Case, trace field, expert review, or other evidence]

## 9. Final evaluation check

- [ ] The normal case can pass.
- [ ] The known unsafe behavior cannot pass silently.
- [ ] Missing evidence becomes unknown or review.
- [ ] Every scorer can inspect the evidence it requires.
- [ ] V1 and V2 use the same evaluation contract.
- [ ] The comparison isolates one application change.
- [ ] The results support a specific operating decision.
- [ ] The project uses only fictional or sanitized information.
