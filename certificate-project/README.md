# MasterClass Certificate Project

## Apply the Agent Loop to a new use case

This is the project to complete **after** the Agent Loop Workshop. Your goal is
to demonstrate that you can transfer the workshop method to an AI application
other than BeeVerse/PatchPilot.

You will define what good behavior means, identify the evidence needed to
measure it, design an evaluation, compare two application versions, and set a
human-in-the-loop policy.

## Choose one track

| Track | Best for | What you produce | Expected effort |
| --- | --- | --- | ---: |
| [Evaluation Designer](NON_TECHNICAL_TRACK.md) | Learners who do not want to write Python | A completed evaluation design with cases, scorer rules, a judge rubric, a manual comparison, and an operating policy | 45–60 minutes |
| [Evaluation Builder](TECHNICAL_TRACK.md) | Learners comfortable writing and running Python | A working, traced AI application with a Weave dataset, scorers, two evaluation runs, and a comparison | 2–4 hours |

Both tracks demonstrate the same evaluation skills. Writing more code does not
compensate for a weak evaluation design.

## Helpful references

- Start with the [beginner glossary](GLOSSARY.md) when a term is unfamiliar.
- Review the [completed example](EXAMPLE_COMPLETED_EVALUATION.md) to see the
  expected level of detail. Use its structure, but create your own project.

## Start here

1. Read the [beginner glossary](GLOSSARY.md) and
   [completed example](EXAMPLE_COMPLETED_EVALUATION.md).
2. Read the [use-case options](USE_CASE_OPTIONS.md).
3. Choose a scenario other than BeeVerse/PatchPilot.
4. Copy [the evaluation design template](EVALUATION_DESIGN_TEMPLATE.md) into a
   new local file and complete it as you work.
5. Follow either the
   [non-technical instructions](NON_TECHNICAL_TRACK.md) or the
   [technical instructions](TECHNICAL_TRACK.md).

You may complete the Markdown template in a text editor, move its headings into
a document or slide tool, or use an equivalent format.

## Requirements shared by both tracks

Your project must include all six parts below.

### 1. Define the agent

State:

- Who uses it.
- What task it completes or recommends.
- The desired business outcome.
- One unacceptable harm.
- The conditions that should require a person.

### 2. Define the trace

Identify:

- The root application operation.
- At least two important internal operations or Calls.
- The inputs, outputs, decisions, and evidence that must be recorded.
- Sensitive information that must not appear in the trace.

### 3. Design a five-case dataset

Include:

1. A normal case.
2. An important safety or policy boundary.
3. An ambiguous or incomplete-input case.
4. An operational edge case, such as a retry, stale source, or tool failure.
5. One additional case of your choice.

Every case must state its source, input or condition, expected behavior,
business risk, and required evidence.

### 4. Define the scorers

Create:

- Two deterministic scorers.
- One LLM-judge rubric with three criteria.

For each deterministic scorer, state what evidence it inspects and exactly
what produces `pass`, `fail`, or `unknown`. At least one judge criterion must be
blocking. The judge must return `pass`, `review`, or `block` with reasons.

### 5. Compare two versions

- Name a specific weakness in Version 1.
- Make one targeted change in Version 2.
- Keep the dataset, deterministic scorers, judge rubric, and judge model fixed.
- Evaluate at least one normal result, one unsafe result, and one result with
  insufficient evidence.

### 6. Set the human-in-the-loop policy

Define:

- What may operate automatically.
- What requires human review.
- What must be blocked.
- Your confidence and approved operating scope.
- The next evidence needed before expanding that scope.

## How to determine whether your evaluation is good

Your completed project should answer these questions:

- Does the evaluation measure the stated business outcome?
- Does it detect the known unsafe behavior?
- Does the normal case continue to pass?
- Does missing evidence become `unknown` or `review` instead of passing?
- Can every scorer inspect evidence that the trace or output actually contains?
- Does Version 2 improve the targeted case under unchanged test conditions?
- Are the results specific enough to guide an operating decision?
- Could another person understand why each case passed, failed, or required
  review?

An evaluation is incomplete if it reports only an average, relies entirely on
an LLM judge, silently passes missing evidence, or changes the test conditions
between versions.

## Privacy and security

Use fictional or sanitized data. Do not show or include:

- W&B API keys.
- `.env` contents.
- Passwords or access tokens.
- Real customer, employee, financial, health, or legal data.
- Confidential prompts, documents, or source code.

If a credential appears in any project artifact or Weave trace, remove it,
rotate the credential, and verify that the replacement artifact is safe before
sharing it.

## Final checklist

- [ ] I used a new use case rather than BeeVerse/PatchPilot.
- [ ] I selected either the Evaluation Designer or Evaluation Builder track.
- [ ] I defined the agent, success outcome, harm, and human-review conditions.
- [ ] I described a root operation and at least two internal Calls.
- [ ] I created five complete dataset cases.
- [ ] I defined two deterministic scorers and one three-criterion judge rubric.
- [ ] I compared V1 and V2 under the same evaluation contract.
- [ ] I covered normal, unsafe, and insufficient-evidence results.
- [ ] I defined automate, review, and block conditions.
- [ ] My project contains no credentials or private data.
