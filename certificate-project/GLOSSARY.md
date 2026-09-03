# Beginner Glossary

These definitions use the terms from the Agent Loop Workshop and W&B Weave.
They are written for readers who do not need to implement the system in code.

## AI agent

An application that uses a model, instructions, and often tools to pursue a
goal. An agent may take several steps, use the result of one step in the next,
and decide what action to take.

## AI application

The complete system being evaluated. It may include a model, prompt,
retrieval, tools, business rules, and application code. Changing the
application does not always mean changing the underlying model.

## Model

The machine-learning system that produces a prediction or response. A language
model predicts and generates text, but the surrounding application decides
what context, instructions, and tools it receives.

## Instructions or prompt

The text that tells a model what task to perform, what information to use, and
how to format or constrain its response.

## Tool

A function or external capability an agent can use, such as searching a
knowledge base, reading an order, updating a ticket, or running a test.

## Op

A versioned function tracked by Weave. Decorating a Python function with
`@weave.op` lets Weave record its executions, inputs, outputs, timing, and
relationships to other tracked functions.

## Call

One recorded execution of an Op. If the same Op runs ten times, Weave records
ten Calls.

## Trace

The end-to-end record of one application run. A trace connects the root Call
to the Calls nested inside it so a reviewer can inspect what happened, in what
order, and with which inputs and outputs.

## Evidence

The recorded facts needed to evaluate a result. Evidence may include inputs,
outputs, tool results, source IDs, policy versions, validation results, or
other trace fields. A scorer cannot reliably check information the system did
not record.

## Feedback

Information attached to a Call after or during review. Feedback can include a
reaction, comment, correction, score, or structured annotation.

## Annotation

Structured human feedback attached to a Call. An annotation uses defined
fields or allowed choices so observations can be searched, compared, and used
consistently.

## Dataset

A collection of examples used to test an AI application. In this project, a
dataset is evaluation data—not training data. Each row describes a situation,
the input, expected behavior, risk, and evidence needed for scoring.

## Historical case

An evaluation example based on something that happened previously. Private or
sensitive information should be removed before the case is used.

## Synthetic case

An evaluation example created deliberately rather than copied from a real
event. Synthetic cases are useful for testing rare, dangerous, or not-yet-seen
conditions.

## Expected behavior

A clear description of what the application should do for a dataset case. It
is broader than an exact expected sentence; it may specify an action, safety
boundary, required evidence, or escalation.

## Scorer

Logic that examines an application output and returns one or more evaluation
metrics. A scorer can also use fields from the corresponding dataset row.

## Deterministic scorer

An exact rule that returns the same result when given the same evidence. It is
appropriate for requirements such as matching IDs, enforcing a limit,
checking a date, or confirming that required fields are present.

## LLM judge

A model-powered scorer that applies written criteria to an application result
and returns a verdict, score, explanation, or combination of these. It is
useful for nuanced questions, but its output may vary and should not replace
exact checks for hard safety boundaries.

## Rubric

The written criteria supplied to a judge. A useful rubric states what each
criterion means, which evidence the judge may use, and what counts as passing,
failing, or having insufficient information.

## Evaluation

The reusable test blueprint. In Weave, an Evaluation combines a dataset with
one or more scorers and optional configuration.

## Evaluation run

One execution of an Evaluation against an application version. Running the
same Evaluation against Version 1 and Version 2 creates two evaluation runs
that can be compared.

## Evaluation contract

The parts of the test that stay fixed during a controlled comparison: dataset,
scorers, rubric, judge model, and input/output expectations. Holding them fixed
helps isolate the effect of the application change.

## Baseline and candidate

The baseline is the starting application version. The candidate is the version
being considered as an improvement. Calling something a baseline does not mean
it is safe or approved.

## Version

A recorded state of an application or evaluation object. Versions make it
possible to identify what changed and reproduce an earlier result.

## Model drift

A change in model behavior or quality over time. Drift can become visible when
the model, incoming data, user behavior, connected tools, or operating
environment changes. Repeating evaluations and monitoring production behavior
can reveal whether performance has moved away from the expected level.

## Human in the loop

An operating policy that requires a person in defined situations. It does not
necessarily mean reviewing every action. A person may be required only when
evidence is missing, confidence is low, risk is high, or a safety boundary
fails.

## Pass, fail, and unknown

Statuses returned by the deterministic scorers in this project:

- **Pass:** The available evidence satisfies the exact rule.
- **Fail:** The available evidence violates the exact rule.
- **Unknown:** The scorer lacks evidence needed to decide.

Unknown should not be treated as pass.

## Pass, review, and block

The case-routing outcomes used in this project:

- **Pass:** The tested requirements are satisfied under the available
  evidence.
- **Review:** A person is needed because evidence is missing or judgment
  remains uncertain.
- **Block:** A tested safety or policy boundary failed.

Passing an evaluation case means the application passed that case and those
checks. It is not proof that the application is safe in every possible
situation.

## Useful W&B Weave references

- [What is Weave?](https://docs.wandb.ai/weave/concepts/what-is-weave)
- [Scoring overview](https://docs.wandb.ai/weave/guides/evaluation/scorers)
- [Evaluations overview](https://docs.wandb.ai/weave/guides/core-types/evaluations)
- [Feedback and annotations](https://docs.wandb.ai/weave/guides/tracking/feedback)
