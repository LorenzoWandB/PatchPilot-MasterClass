# Evaluation Builder Track

## Build and evaluate a new AI application

In this track, you will implement the same evaluation-design assignment in
Python and use W&B Weave to trace and compare two versions of a new AI
application.

Expected effort: **2–4 hours**.

Before starting, use the [beginner glossary](GLOSSARY.md) for unfamiliar terms
and review the [completed example](EXAMPLE_COMPLETED_EVALUATION.md) for the
evaluation-design detail expected before implementation.

The existing technical workshop is a reference, not the certificate project. You
may study and reuse its patterns, but your certificate project must use a new
scenario rather than BeeVerse/PatchPilot.

Launch the reference workshop with:

```bash
uv run --locked python start_workshop.py --technical
```

## Prerequisites

- Complete or review the guided Agent Loop Workshop.
- Be comfortable writing and running Python.
- Have a W&B account, API key, entity, and project.
- Have W&B Serverless Inference access and sufficient credits.
- Be signed in to `wandb.ai` in the browser used to inspect Weave.

Use the repository's locked environment when practical. You may create a new
local Python file or notebook for your project. Do not commit credentials or
real private data.

## What you will build

Your project must produce:

- Two model-powered versions of one application.
- An end-to-end trace with meaningful nested Calls.
- A versioned five-row Weave dataset.
- Two deterministic Python scorers.
- One live LLM judge with a three-criterion rubric.
- A V1 baseline evaluation run.
- A V2 candidate evaluation run using the same evaluation contract.
- A case-level comparison and human-in-the-loop decision.

## 1. Define the use case and contract

Choose a scenario from [the use-case options](USE_CASE_OPTIONS.md) or propose
your own qualifying scenario.

Before coding, complete the relevant sections of
[the evaluation design template](EVALUATION_DESIGN_TEMPLATE.md). Define:

- The input and output schema shared by both versions.
- The intended user, action, outcome, and unacceptable harm.
- The one application dimension that changes between V1 and V2.
- The evaluation contract that must remain fixed.

Record enough application metadata to identify:

- Application version.
- Changed dimension.
- Change summary.
- Dataset version or fingerprint.
- Scorer-set version.
- Rubric ID.
- Judge model.

## 2. Implement two application versions

Implement V1 with one named weakness and V2 with one targeted improvement.

Requirements:

- Both versions accept the same input fields.
- Both versions return the same structured output fields.
- The application uses a model through W&B Serverless Inference.
- Only one declared prompt, model, retrieval, tool, validation, or code
  dimension changes.
- Outputs include the evidence required by the scorers, or explicitly indicate
  that evidence is unavailable.

Do not silently manufacture evidence in V2. If the application cannot observe
a required fact, return that uncertainty in the output.

## 3. Add Weave tracing

Instrument:

- One root application operation.
- At least two meaningful internal operations.

At least one trace must make the end-to-end relationship clear between the
application input, model or tool behavior, and final structured output.

Inspect the trace in Weave and confirm:

- Inputs and outputs are readable.
- Child Calls are nested under the root.
- The V1 weakness can be located in recorded evidence.
- No credential or sensitive data appears.

The technical workshop demonstrates `weave.Model`, `@weave.op`, nested tool
Calls, and direct Call inspection. Use those implementations as references.

## 4. Publish the five-case dataset

Create and publish a `weave.Dataset` containing:

1. Normal behavior.
2. Safety or policy boundary.
3. Ambiguous or incomplete input.
4. Operational edge case.
5. One additional case.

Every row must provide the application input, expected behavior, risk, source,
and evidence needed by the scorers.

Use the exact same dataset version for V1 and V2. Record or display its version
or fingerprint in the evaluation metadata.

## 5. Implement deterministic scorers

Implement two Python scorers that return a structured status and reason.

Each scorer must:

- Read explicit fields from the application output or expected behavior.
- Return `pass`, `fail`, or `unknown`.
- Return `unknown` when required evidence is unavailable.
- Explain the result in a short reason.
- Avoid using an LLM for an exact rule.

Add at least three local assertions or fixtures demonstrating:

- A passing result.
- A failing result.
- An unknown result caused by missing evidence.

Keep the passing assertion results with your project output or notes.

## 6. Implement the LLM judge

Create a model-powered scorer using W&B Serverless Inference. The judge must:

- Receive the dataset case, application output, recorded evidence, and rubric.
- Use exactly three written criteria.
- Mark at least one criterion as blocking.
- Return a status and evidence-based reason for every criterion.
- Return an overall `pass`, `review`, or `block` verdict and rationale.
- Treat missing evidence as unknown rather than inventing a fact.
- Produce structured output that can be inspected in Weave.

Keep the LLM judge separate from the deterministic safety rules. A model
explanation may add context, but it must not override a failed exact boundary.

## 7. Run the controlled comparison

Create one reusable evaluation setup and run it against both application
versions.

Hold fixed:

- The five dataset rows and version.
- Both deterministic scorers.
- LLM-judge rubric and rubric ID.
- Judge model.
- Release-policy definition.

Change only the declared application dimension. Use V1 as the baseline and V2
as the candidate.

In Weave, inspect:

- The overall evaluation summary.
- One normal case.
- The targeted unsafe case.
- The incomplete-evidence case.
- At least one deterministic scorer Call.
- At least one LLM-judge Call and its reasons.
- Application and evaluation properties.

Do not grade the project by the average alone. Explain which specific case
improved, whether anything regressed, and which uncertainty remains.

## 8. Set the human-in-the-loop policy

Based on the comparison, state:

- What may run automatically.
- What must go to a person.
- What must be blocked.
- Your confidence and approved scope.
- The next evidence needed before expanding automation.

You may record the decision in your project output, a Weave annotation, or a
traced decision record. The policy must be documented with the project.

## Hosted-call and cost warning

With five rows, two application versions, one application-model call per row,
and one judge call per row, the comparison uses at least **20 hosted model
calls**. Retries, tools, or multi-turn application behavior may increase that
number.

Run deterministic assertions before spending hosted calls. Use small synthetic
inputs and check available Serverless Inference credits before starting both
evaluation runs.

## Technical acceptance criteria

- [ ] The code executes successfully.
- [ ] V1 and V2 use the same structured interface.
- [ ] One declared application dimension changes.
- [ ] A nested Weave trace is inspectable.
- [ ] The dataset contains five complete, versioned cases.
- [ ] Two deterministic scorers return status and reason.
- [ ] Local pass, fail, and unknown assertions succeed.
- [ ] One live LLM judge applies a three-criterion rubric.
- [ ] V1 and V2 produce separate evaluation runs under one fixed contract.
- [ ] The unsafe sample does not silently pass.
- [ ] Insufficient evidence routes to review.
- [ ] No secrets or real private data appear in code or Weave.

A predetermined live judge verdict is not required, and the application does
not need to use every available tool. Focus on implementation correctness,
evaluation quality, and accurate interpretation of the behavior that was
actually recorded.

## Recommended final review order

Review the completed implementation in this order:

1. Use case, risk, and V1/V2 change.
2. Relevant application code and one nested trace.
3. Dataset and deterministic scorer assertions.
4. LLM-judge rubric and one judge Call.
5. V1/V2 Weave comparison.
6. Human-in-the-loop policy.
