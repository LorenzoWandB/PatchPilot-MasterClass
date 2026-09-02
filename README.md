# Agent Loop Workshop

**Trace, Evaluate, and Improve an AI Agent with W&B Weave**

This is a guided 90-minute workshop for mixed technical and non-technical
audiences. It follows one fictional coding agent, PatchPilot, through a complete
improvement loop:

> Run → trace → build a dataset → evaluate → improve → compare → decide

The business scenario is fictional. The W&B Weave traces, calls, dataset,
evaluation runs, annotations, and W&B Serverless Inference judge calls are real.

The guided path follows one repeatable interaction pattern throughout:

> Create it in the notebook → open it in Weave → inspect the evidence → use it
> to create the next artifact

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

Every successful creation step displays a numbered receipt and a direct Weave
link. The opening policy and final structured choices are saved in the final
review record; there are no disposable free-text reflection boxes.

## Prepare before the workshop

### 1. Create a W&B account and API key

1. [Create or sign in to a W&B account](https://wandb.ai/site).
2. Open **Profile → User Settings → API Keys**.
3. Select **Create new API key**.
4. Copy the complete key immediately and store it securely. W&B displays the
   full key only once. See the
   [current W&B API-key instructions](https://docs.wandb.ai/models/quickstart).

Keep the key ready, but do not send it through email, chat, or Zoom.

### 2. Open a terminal

- **macOS:** press `Command + Space`, type `Terminal`, and press Enter.
- **Windows:** open the Start menu, search for `PowerShell`, and open it.

### 3. Install `uv`

On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close and reopen the terminal after installation. These commands come from the
[official `uv` installation guide](https://docs.astral.sh/uv/getting-started/installation/).

You also need access to W&B Serverless Inference and available credits, network
access to W&B and Weave, and a browser signed into `wandb.ai`.

## Start the main guided workshop

Clone the repository, enter the folder, and run the guided launcher:

```bash
git clone https://github.com/LorenzoWandB/PatchPilot-MasterClass.git
cd PatchPilot-MasterClass
uv run --locked python start_workshop.py
```

If `git` is unavailable, open this repository in GitHub, select **Code →
Download ZIP**, unzip it, and open a terminal in the extracted
`PatchPilot-MasterClass` folder. Then run only the final command above.

On the first run, the launcher privately asks for:

- A W&B API key.
- A W&B username or team slug.
- The project name, which defaults to `agent-loop-workshop`.
- The judge model, which defaults to `openai/gpt-oss-20b`.

The launcher saves these values in a local `.env` file with owner-only
permissions where supported. `.env` is ignored by Git. Later runs reuse the
local settings. The notebook server listens only on `127.0.0.1` and uses a
random Marimo session token; the one-command launcher opens the authenticated
local URL automatically.

The API key authenticates the notebook but does not sign the browser into
`wandb.ai`. The notebook therefore shows three readiness states:

- **Setup incomplete:** a required local value is missing or invalid.
- **Local setup found—connection not tested:** the local values exist, but no
  service has been contacted yet.
- **Notebook connection verified:** W&B authentication, the Weave project, and
  the Serverless Inference judge all responded successfully.

After verification, use **Open the project in Weave** to confirm that the
browser is also signed in. Browser access cannot be proven by the API preflight.

To replace the local configuration:

```bash
uv run --locked python start_workshop.py --reset
```

Manual setup is also available by copying `.env.example` to `.env`.

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

## Optional standalone technical workshop

The repository also contains one consolidated, interactive 90-minute workshop for
Python developers. It stands on its own; participants do not need to complete
the guided workshop first. Open it with:

```bash
uv run --locked python start_workshop.py --technical
```

The technical workshop teaches two connected loops. In the inner loop, a live
model selects from an allowlist of in-memory Python tools and Weave records the
model call, validated tool execution, and output as a nested trace. In the outer
loop, participants turn a trace-derived failure into a dataset case and scorer,
add two safety-evidence tools to PatchPilot V3, evaluate V2 and V3 under one
fixed contract, compare the actual tool behavior, and save a human release
decision in Weave.

The notebook opens as a rendered workshop app—there is no **Run all** step and no
wall of notebook implementation cells. Four focused in-app Python editors ask
participants to complete a dataset case, bounded tool dispatcher, two traced
safety tools, and a deterministic scorer. Visible fixtures gate hosted calls,
and the participant-authored dispatcher, tools, and scorer are used by the live
V2/V3 comparison. There is no separate technical or solution notebook.

The four **Validate … locally** buttons compile or parse the participant's
current editor content and display an explicit fixture count immediately below
the button. These checks do not call a model or create a Weave artifact. The
later live trace and evaluation actions are the points that create Weave Calls
and evaluation runs.

The core path makes 21 hosted model calls per participant:

- One live V2 baseline agent call.
- Five live agent calls and five live judge calls for the V2 evaluation.
- Five live agent calls and five live judge calls for the V3 evaluation.

If the live V3 agent skips both optional safety tools, the notebook offers one
clearly labeled retry. Choosing it adds one agent call, for a maximum of 22 calls
on the core path.

The W&B and Weave preflight does not make a model call. A take-home full rerun
with a revised rubric adds 20 calls and must use a separately named evaluation
contract.

## Security and data handling

- The repository contains fictional BeeVerse cases only. Running the notebooks
  sends the selected synthetic case inputs, application outputs, traces,
  annotations, evaluation results, and model prompts/responses to the W&B
  project configured by the participant. Do not replace workshop fixtures with
  customer data, credentials, or other sensitive information.
- The API key remains in the local `.env` file. It is not displayed, included
  in operation inputs, stored in dataset rows, or passed to the model. The
  launcher refuses a symlinked credential file and uses owner-only permissions
  where the operating system supports them.
- Both workshop apps bind to the local loopback interface and require a random
  session token. They are not exposed as network services by the launcher.
- The technical workshop validates editor input, permits only function
  definitions and a small Python/JSON surface, and exposes no import, file,
  shell, credential, or network primitive. Those editors still execute the
  participant's Python in the local notebook process; use code you wrote or
  understand. They are not a hardened sandbox for untrusted third-party code.
- Model-requested tool names and arguments are untrusted. A deterministic
  allowlist and registered-handler check decide what runs, and all workshop
  tools operate only on in-memory fictional data. No repository is patched and
  nothing is deployed.
- Hosted inference consumes the participant's W&B credits. The notebooks show
  the call count before evaluation and require explicit confirmation before the
  high-call steps.

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
├── technical_lab_core.py
├── uv.lock
├── workshop.py
└── workshop_core.py
```

Facilitator notes, decks, tests, caches, generated previews, and local
credentials are not required by participants.
