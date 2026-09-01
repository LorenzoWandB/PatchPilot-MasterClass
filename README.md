# Agent Loop Workshop

**Trace, Evaluate, and Improve an AI Agent with W&B Weave**

This is a guided 90-minute workshop for mixed technical and non-technical
audiences. It follows one fictional coding agent, PatchPilot, through a complete
improvement loop:

> Run → trace → build a dataset → evaluate → improve → compare → decide

The business scenario is fictional. The W&B Weave traces, calls, dataset,
evaluation runs, annotations, and W&B Serverless Inference judge calls are real.

## The scenario

BeeVerse Market runs merchant-support software. A broken bulk-close workflow
needs to be repaired before its seasonal sale. PatchPilot prepares a one-file
change and passes three visible checks, but its first patch selects tickets only
by ticket ID. A mixed-customer request can therefore change a ticket belonging
to another merchant.

Participants:

1. Run PatchPilot Version 1 and inspect its trace.
2. Annotate the customer-isolation risk in Weave.
3. Configure and publish a structured dataset case.
4. Define one fixed evaluation setup with three Python scorers and one live LLM
   judge.
5. Create the Version 1 evaluation run.
6. Inspect the prepared Version 2 customer-boundary fix.
7. Create the Version 2 evaluation run with the exact same setup.
8. Compare both runs and save a human-in-the-loop decision.

## Workshop terminology

- **W&B Weave:** an observability and evaluation platform that helps teams
  track, evaluate, and improve AI applications.
- **Trace:** the end-to-end record of one run, containing a hierarchy of calls.
- **Call:** one tracked operation or step inside a trace. `@weave.op` records a
  function as a call, including its inputs, outputs, and execution metadata.
- **Dataset:** a versioned collection of test examples used for repeated
  evaluation and comparison.
- **Scorer:** a function or class that analyzes an output and returns one or
  more metrics.
- **Evaluation:** the reusable setup that combines a dataset, scorers, and
  optional configuration.
- **Evaluation run:** one execution of that evaluation setup against an
  application version.
- **LLM judge:** a model-powered scorer that applies written scoring criteria.
- **Rubric:** the written scoring criteria supplied to the judge.
- **Annotation:** structured human feedback attached to a Weave call.
- **Baseline:** the reference evaluation run used for comparison; it is not an
  automatic production recommendation.

## What is fixed and what uses AI

The workshop uses two prepared, deterministic versions of the same PatchPilot
agent. That keeps the live comparison reliable.

The evaluation setup contains:

- Three custom function-based Python scorers whose logic is deterministic:
  visible checks, customer isolation, and retry safety.
- One custom class-based scorer that uses an LLM as a judge through W&B
  Serverless Inference.
- One frozen dataset, scorer set, judge rubric, judge model, and review policy.

The small preflight also makes one hosted model call to verify access. The
preflight result is not used in the evaluation.

In production, the first half of the workflow could also be live: a model could
choose tools, inspect files, propose edits, and run tests. The workshop fixes
that layer so the room can focus on evaluation evidence.

## What participants create

- One Version 1 trace containing nested calls recorded by `@weave.op`.
- One observed-risk annotation attached to that trace.
- One four-row, versioned Weave dataset containing a participant-configured
  customer-boundary case.
- One Version 1 evaluation run and one Version 2 evaluation run created from
  the same evaluation setup.
- Four live judge calls per evaluation run.
- Three final human annotations plus one complete human-in-the-loop review
  record.

No participant edits Python during the main path. Technical attendees can read
the code examples while everyone else uses labeled controls and follows the
facilitator.

## Prerequisites

- A W&B account and API key.
- Access to W&B Serverless Inference and available credits.
- [`uv`](https://docs.astral.sh/uv/).
- Network access to W&B and Weave.
- A browser session signed into `wandb.ai` with access to the selected project.

The API key authenticates the notebook. It does not sign the browser into
`wandb.ai`, so both checks are required.

The notebook uses three explicit readiness states:

- **Setup incomplete:** a required local value is missing or invalid.
- **Local setup found—connection not tested:** the local values exist, but no
  service has been contacted yet.
- **Notebook connection verified:** W&B authentication, the Weave project, and
  the Serverless Inference judge all responded successfully.

After verification, use **Open the project in Weave** to confirm that the
browser is also signed in. Browser access cannot be proven by the API preflight.

## Start the workshop

Clone the repository, enter the folder, and run the guided launcher:

```bash
git clone https://github.com/LorenzoWandB/PatchPilot-MasterClass.git
cd PatchPilot-MasterClass
uv run --locked python start_workshop.py
```

On the first run, the launcher privately asks for:

- A W&B API key.
- A W&B username or team slug.
- The project name, which defaults to `agent-loop-workshop`.
- The judge model, which defaults to `openai/gpt-oss-20b`.

The launcher saves these values in a local `.env` file with owner-only
permissions where supported. `.env` is ignored by Git. Later runs reuse the
local settings.

To replace the local configuration:

```bash
uv run --locked python start_workshop.py --reset
```

Manual setup is also available by copying `.env.example` to `.env`.

## Optional technical lab

The guided workshop remains the default. Technical attendees can later open an
editable 45–60 minute follow-up with one command:

```bash
uv run --locked python start_workshop.py --technical
```

The technical lab uses the same BeeVerse scenario and W&B project, but distinct
dataset and evaluation names. Participants edit a real `@weave.op` application,
add a fifth dataset row and deterministic scorer, create PatchPilot V3, and
compare V2 with V3 under a fixed evaluation contract. An optional final exercise
changes the judge rubric and correctly reruns both application versions under a
separately named contract.

The lab opens with `marimo edit`, while the main workshop continues to open as a
read-only `marimo run` application. In the editor, click **Run all** in the
bottom-right once to initialize the lab. Each five-row evaluation makes five
live judge calls; the optional revised-rubric pair makes ten additional calls.

## Workshop control contract

The comparison is intentionally controlled:

| Held fixed | Changed |
| --- | --- |
| Dataset contents and fingerprint | PatchPilot agent version |
| Three custom Python scorers with deterministic logic | Patch strategy |
| LLM-judge rubric | Customer-boundary behavior |
| Judge model | Agent metadata shown in Weave |
| Human-in-the-loop policy | Agent output for affected cases |

Version 1 uses `ticket_ids_only`. Version 2 uses `tenant_scoped` and adds the
requesting-customer constraint.

The expected deterministic story is:

| Case | Version 1 | Version 2 |
| --- | --- | --- |
| Normal bulk close | Pass | Pass |
| Participant mixed-customer case | Block | Pass |
| Retried delivery | Pass | Pass |
| Missing evidence | Human review | Human review |

The LLM judge is live and may vary. The workshop requests structured JSON; if a
model response is malformed, that row is preserved as **needs human review**
instead of failing the evaluation. Participants inspect its rubric, evidence,
criteria, and reasons in Weave.

## Local verification

```bash
uv run --locked marimo check workshop.py technical_lab.py
```

This validates both notebooks without making a W&B or model call.

## Public package contents

The public participant repository needs only:

```text
agent-loop-workshop/
├── .env.example
├── .gitignore
├── README.md
├── data/
│   ├── cases.json
│   └── rubrics.json
├── pyproject.toml
├── start_workshop.py
├── technical_lab.py
├── uv.lock
├── workshop.py
└── workshop_core.py
```

Facilitator notes, decks, tests, caches, generated previews, and local
credentials are not required by participants.
