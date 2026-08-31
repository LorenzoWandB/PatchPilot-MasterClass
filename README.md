# PatchPilot: Evidence Before Authority

PatchPilot is a guided 90-minute workshop for learning how to inspect an
AI-agent run, evaluate its behavior across cases, and decide whether it should
operate automatically, require human review, or remain blocked.

The retail incident and agent behavior are synthetic. The W&B Weave traces,
evaluations, and W&B Serverless Inference judge calls are real and are saved to
the W&B project each participant configures.

## Before the session

Each participant needs:

- a W&B account and [personal API key](https://wandb.ai/authorize);
- a W&B username or team where they may create a project;
- W&B Serverless Inference access with available credits;
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed;
- access to W&B, Weave, and W&B Serverless Inference on their network; and
- a browser signed in to `wandb.ai` with access to the same W&B destination.

No GPU, separate Python installation, Python editing, or Docker setup is
required. `uv` installs the compatible Python version and locked workshop
dependencies when needed.

## Easiest start

Download this repository as a ZIP and extract it, or clone it. Open Terminal or
PowerShell in the extracted workshop folder and run one command:

```bash
uv run --locked python start_workshop.py
```

On the first run, the launcher asks for:

1. **W&B API key:** input is hidden. Create or copy it from
   <https://wandb.ai/authorize>.
2. **W&B destination:** paste a username, team slug, `entity/project` path, or
   full W&B project URL. The launcher safely extracts the entity.
3. **Project and judge model:** press Enter to accept the workshop defaults.

The values are validated and saved only in the Git-ignored local `.env` file.
The API key is not printed. Later runs reuse the same local setup, so the same
command starts the workshop immediately.

Keep the terminal open while the workshop runs. Open the local URL it prints,
then click **Run workshop preflight**. Continue only when the receipt says
**Connected** and confirms judge-model access.

Run this full check at least one business day before the session. It catches
credential, permission, credit, model-access, and network problems while there
is still time to resolve them.

## Browser sign-in is separate

The API key authorizes the notebook to create traces and evaluations. It does
not sign the browser into `wandb.ai`. Before the session, sign in to W&B in the
browser you will use and open the configured project once. Otherwise, the
notebook can run successfully while **Open in Weave** links show a login page or
private-project 404.

## Reconfigure or use manual setup

To replace the saved destination, model, or API key:

```bash
uv run --locked python start_workshop.py --reset
```

For manual setup only, copy `.env.example` to `.env`, fill in the four values,
then run:

```bash
uv run --locked python start_workshop.py
```

Never commit `.env` or paste an API key into the notebook.

## If setup does not complete

| What you see | What to check |
| --- | --- |
| `uv: command not found` | Install `uv` from the official link above, reopen the terminal, and rerun the command. |
| API/authentication error | Replace the key with `--reset`; do not share the key with the facilitator or in Zoom. |
| Entity/project permission error | Use a W&B username or team where your account may create a project. |
| Judge access, credit, or network error | Confirm Serverless Inference access and credits, and that the network permits W&B services. |
| Weave link opens login or 404 | Sign in to `wandb.ai` in that browser and confirm project access. |

If an individual machine is not ready during the live session, that participant
can still follow the facilitator's shared notebook and Weave screen and make
the same decisions privately. No pairing, breakout room, chat poll, or Python
editing is required.

## Workshop flow

The session is facilitator-led. Participants follow one shared path, use bounded
notebook controls, and inspect the matching evidence in Weave:

1. Run and inspect one traced episode.
2. Choose a dataset case and predict its result.
3. Read the custom `weave.Scorer` and `weave.Evaluation` wiring.
4. Run the baseline LLM judge and inspect one scorer call.
5. Change one business rubric rule and its review/block severity.
6. Inspect the compiled rubric, rerun the same cases, and compare.
7. Record the smallest operating authority the evidence supports.

## What one complete run creates

- One small preflight inference call.
- One deterministic saved-agent trace.
- One baseline evaluation over four synthetic cases.
- One revised evaluation over the same cases.
- Eight hosted LLM-judge calls across the two evaluations.
- One local operating-boundary decision receipt.

## Security and data flow

- `.env` is ignored by Git. The launcher refuses symlinked credential files and
  applies owner-only file permissions where the operating system supports them.
- API-key input is hidden. The key is used only for W&B authentication and is
  not placed in a trace, dataset row, judge prompt, notebook receipt, or launcher
  output.
- The notebook sends the synthetic cases, recorded synthetic evidence, agent
  outputs, rubric, and participant-written business rule to W&B/Weave and the
  configured W&B-hosted judge.
- Opening notes, dataset-gap notes, perspective choice, and the final decision
  receipt remain local to the notebook.
- Do not enter confidential, personal, production, or customer information into
  any workshop field.
- The notebook does not execute shell commands, upload local files, deploy code,
  or grant the synthetic agent production authority.

## Included files

```text
.
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── start_workshop.py
├── uv.lock
├── workshop.py
├── workshop_core.py
└── data/
    ├── cases.json
    └── rubrics.json
```

This public package intentionally excludes facilitator materials, slide decks,
development tests, private Git history, local environments, and generated
workshop state.
