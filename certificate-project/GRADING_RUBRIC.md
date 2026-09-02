# Certificate Project Grading Rubric

Both tracks use the same 100-point rubric. Evaluation Designer submissions are
assessed through their completed design and manual calibration. Evaluation
Builder submissions must demonstrate the same reasoning plus a working coded
implementation.

Writing more code does not compensate for an unclear business requirement,
weak dataset, or unjustified policy.

## 1. Use case and business risk — 15 points

**13–15 points**

- Defines a narrow agent, intended user, action, and measurable outcome.
- Names a concrete unacceptable harm.
- Explains why the use case needs evaluation and human-review boundaries.

**8–12 points**

- The use case is understandable but one important element is vague or overly
  broad.

**0–7 points**

- The submission does not define observable behavior or a meaningful risk.

## 2. Trace and required evidence — 15 points

**13–15 points**

- Defines a root operation and at least two meaningful Calls.
- Identifies the inputs, outputs, decisions, and evidence needed by scorers.
- Explicitly excludes or protects sensitive information.
- Technical track: shows an inspectable nested Weave trace without secrets.

**8–12 points**

- The workflow is present, but its evidence or Call relationships are
  incomplete.

**0–7 points**

- The trace is treated only as a final output, or the proposed scorers depend on
  evidence that is never recorded.

## 3. Dataset quality and coverage — 20 points

**17–20 points**

- Includes all five required case categories.
- Each row has a source, input, expected behavior, risk, and required evidence.
- Includes expected pass, fail or block, and unknown or review outcomes.
- Cases are meaningfully different and connected to the stated business risk.

**10–16 points**

- Five cases exist, but some are repetitive, underspecified, or weakly tied to
  the business requirement.

**0–9 points**

- Important categories are missing, most cases are happy-path variations, or
  expected behavior is not defined.

## 4. Scorer and rubric quality — 25 points

**22–25 points**

- Defines two exact deterministic scorers with pass, fail, and unknown logic.
- Scorers use evidence actually available in the output or trace.
- Uses deterministic logic for hard boundaries rather than delegating every
  decision to an LLM.
- Defines three clear judge criteria, including at least one blocking criterion.
- Requires evidence-based reasons and prevents missing evidence from silently
  passing.
- Technical track: shows passing local assertions and a structured live judge.

**13–21 points**

- The scorer set is mostly usable, but one rule, evidence dependency, unknown
  condition, or judge criterion is ambiguous.

**0–12 points**

- Scorers are subjective without a rubric, rely entirely on an LLM, cannot be
  applied to the recorded evidence, or treat missing evidence as success.

## 5. Controlled comparison — 15 points

**13–15 points**

- Gives V1 a specific weakness and V2 one targeted change.
- Keeps the dataset, scorers, rubric, and judge model fixed.
- Applies the evaluation to normal, unsafe, and incomplete-evidence outputs.
- Explains the targeted improvement, regression check, and remaining unknown.
- Technical track: shows separate V1 and V2 Weave evaluation runs with V1 as
  the baseline.

**8–12 points**

- A comparison is present, but multiple dimensions change or case-level
  interpretation is incomplete.

**0–7 points**

- Only one version is evaluated, the evaluation contract changes between
  versions, or the student relies only on an aggregate score.

## 6. Human-in-the-loop policy and explanation — 10 points

**9–10 points**

- Defines specific automatic, review, and block conditions.
- Limits the approved scope to what the evidence supports.
- States confidence and the next evidence needed.
- Communicates the project clearly within the 5–7 minute video.

**5–8 points**

- A policy exists, but it is broader than the evidence or lacks confidence,
  scope, or next steps.

**0–4 points**

- The submission treats evaluation output as an automatic release decision or
  does not define where a person remains involved.

## What is not graded

- A predetermined LLM-judge verdict.
- Identical wording from different model runs.
- Presentation polish beyond a clear, understandable walkthrough.
- Production deployment.
- Writing code in the Evaluation Designer track.
- Using every optional tool in the Evaluation Builder track.

## Submission problems requiring revision

Return the submission for revision before final grading when:

- The video cannot be opened or does not identify a project track.
- The project reuses BeeVerse/PatchPilot instead of applying the method to a new
  use case.
- The submission omits the dataset, scorer design, version comparison, or
  human-in-the-loop policy.
- A credential, `.env` value, or real private data is visible. The student must
  rotate any exposed credential and replace the recording.

MasterClass may apply its program-wide completion threshold to the final
100-point score.
