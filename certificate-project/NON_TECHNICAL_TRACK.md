# Evaluation Designer Track

## No Python required

In this track, you will design and manually test an evaluation for a new AI
agent. Your completed evaluation brief is the project. You may use prose,
tables, diagrams, and pseudocode.

You do not need to implement the agent, call a live model, or create a new W&B
project. You do need to be precise enough that a technical team could implement
your design without guessing what “good” means.

Expected effort: **45–60 minutes**, followed by a **5–7 minute video**.

## What you will prepare

Start by copying [the evaluation design template](EVALUATION_DESIGN_TEMPLATE.md)
into a new file. You may keep it in Markdown or move the same headings into a
document or slide tool.

Complete every section below.

## 1. Define a narrow agent use case

Choose a scenario from [the use-case options](USE_CASE_OPTIONS.md) or create an
equivalent scenario of your own.

Your definition must identify:

- The person or team using the agent.
- The action or recommendation the agent produces.
- A measurable business outcome.
- An unacceptable harm.
- What the agent must hand to a person.

Avoid broad claims such as “the agent should be useful.” Define behavior that
could be observed in an input, output, tool result, or trace.

## 2. Design the trace

Describe what one end-to-end run should record:

- One root application operation.
- At least two important internal Calls.
- The input and output of each Call.
- The evidence later scorers will need.
- Information that must be redacted or excluded.

A diagram is optional. A short ordered list is sufficient when it clearly
shows the parent operation and its child steps.

## 3. Create five dataset cases

Write one row for each required category:

1. Normal behavior.
2. Safety or policy boundary.
3. Ambiguous or incomplete input.
4. Operational edge case.
5. One additional case you believe is important.

Each row must include:

- Case name.
- Historical, synthetic, or other declared source.
- Input or condition.
- Expected behavior.
- Business risk.
- Evidence required for scoring.

Do not write only five variations of the happy path. The set must contain at
least one expected pass, one expected fail or block, and one expected unknown
or review result.

## 4. Write two deterministic scorers

For each scorer, specify:

- What requirement it represents.
- Which recorded fields it reads.
- Its exact pass condition.
- Its exact fail condition.
- When it returns unknown.
- Why code is more appropriate than model judgment for this requirement.

Natural-language rules or pseudocode are acceptable. For example:

```text
IF required ownership evidence is missing:
    UNKNOWN — require human review
ELSE IF the resource owner does not match the requester:
    FAIL — block the action
ELSE:
    PASS
```

Your own scorers must match your selected use case; do not copy this rule if
ownership is not part of your scenario.

## 5. Write the LLM-judge rubric

Define exactly three criteria. For each criterion include:

- Criterion name.
- Plain-language rule.
- Evidence the judge may use.
- Whether it is blocking.
- What pass, fail, and unknown mean.

At least one criterion must be blocking. Require the judge to return:

- A status for every criterion.
- A short evidence-based reason for every status.
- One overall verdict: `pass`, `review`, or `block`.
- An overall rationale.

The judge must use only the supplied case, application output, evidence, and
rubric. Missing evidence should become unknown, not an invented fact.

## 6. Create Version 1 and Version 2

Describe one weakness in Version 1 and one targeted change in Version 2. The
versions must share the same input and output format.

Create short sample outputs for both versions on three representative cases:

- One normal case.
- One unsafe case.
- One incomplete-evidence case.

Apply both deterministic scorers and your expected judge verdict to each
sample. Record the reasons, not only the labels.

Keep the dataset cases, scorer rules, judge rubric, and assumed judge model
fixed. Only the declared application change should differ.

## 7. Evaluate your evaluation

Explain whether your design:

- Detects the unsafe Version 1 result.
- Preserves the normal behavior.
- Routes insufficient evidence to review.
- Shows a targeted improvement in Version 2.
- Produces enough explanation to diagnose a failure.

If it does not, revise the cases, evidence plan, or scorer definitions before
recording the video.

## 8. Set the human-in-the-loop policy

State:

- The evidence required for automatic operation.
- The uncertainty that requires a person.
- The failed boundary that blocks the action.
- Your confidence level.
- The limited scope you would approve.
- What evidence you would collect before expanding that scope.

The policy should follow from the evaluation. Avoid an unsupported blanket
claim that the agent is either completely safe or completely unusable.

## Video outline

Use this structure to stay within 5–7 minutes:

1. **Use case and risk — 45 seconds.**
2. **Trace and required evidence — 45 seconds.**
3. **Five dataset cases — 60 seconds.**
4. **Deterministic scorers and judge rubric — 90 seconds.**
5. **V1/V2 manual comparison — 90 seconds.**
6. **Human-in-the-loop policy — 45 seconds.**

Show the completed brief while explaining it. You are graded on the clarity and
quality of the evaluation design, not presentation polish.

Review [the grading rubric](GRADING_RUBRIC.md) before recording.
