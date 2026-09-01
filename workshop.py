# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#   "marimo>=0.21,<0.24",
#   "openai>=1.100,<3",
#   "pydantic>=2.10,<3",
#   "python-dotenv>=1.0,<2",
#   "weave>=0.52,<0.54",
# ]
#
# [tool.marimo.runtime]
# auto_instantiate = true
# on_cell_change = "autorun"
# ///
"""Agent Loop Workshop — trace, evaluate, and improve with W&B Weave."""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import html
    import inspect
    import json
    from pathlib import Path

    import marimo as mo
    from dotenv import load_dotenv

    local_env = Path(__file__).with_name(".env")
    load_dotenv(local_env if local_env.exists() else None, override=True)
    import workshop_core as core

    return core, html, inspect, json, mo


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <style>
          :root { --ink:#111827; --muted:#64748b; --line:#d8dee8; --blue:#2563eb; --amber:#d97706; --mint:#0f9f86; --rose:#b84735; }
          .loop-page { padding:1.2rem 0 .8rem; color:var(--ink); }
          .loop-page h1 { font-size:2.6rem; line-height:1.05; margin:.45rem 0 1rem; }
          .loop-page h2 { font-size:1.75rem; line-height:1.15; margin:.35rem 0 .65rem; }
          .loop-page p { font-size:1.03rem; line-height:1.56; }
          .loop-kicker { color:var(--rose); font-size:.78rem; font-weight:850; letter-spacing:.09em; text-transform:uppercase; }
          .loop-rail { border-top:2px solid var(--line); border-bottom:2px solid var(--line); padding:.75rem 0; margin:1.1rem 0; color:var(--muted); font-weight:750; }
          .loop-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin:1rem 0; }
          .loop-grid > div { border-top:5px solid var(--blue); background:#f7f9fc; padding:.9rem; min-height:6.7rem; }
          .loop-grid > div:nth-child(2) { border-top-color:var(--amber); }
          .loop-grid > div:nth-child(3) { border-top-color:var(--mint); }
          .loop-panel { border-left:8px solid var(--blue); background:#f7f9fc; padding:1rem 1.15rem; margin:1rem 0; }
          .loop-panel.amber { border-color:var(--amber); }
          .loop-panel.mint { border-color:var(--mint); }
          .loop-panel.rose { border-color:var(--rose); }
          .loop-do { border:2px solid #93c5fd; background:#eff6ff; padding:1rem 1.15rem; margin:1rem 0; }
          .loop-receipt { background:#eef8f5; border:1px solid #b9e2d9; padding:.9rem 1rem; margin:.9rem 0; }
          .loop-error { background:#fff2ef; border:1px solid #efc0b7; padding:.9rem 1rem; margin:.9rem 0; color:#842f23; }
          .loop-small { color:var(--muted); font-size:.91rem; }
          .loop-code { border:1px solid var(--line); background:#f8fafc; padding:.75rem 1rem; }
          table { font-size:.93rem; }
          @media (max-width:800px) { .loop-grid { grid-template-columns:1fr; } }
        </style>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <header class="loop-page">
          <div class="loop-kicker">Agent Loop Workshop · 90 minutes</div>
          <h1>Trace, evaluate, and improve an AI agent</h1>
          <p>Follow one PatchPilot coding agent from a green-looking patch to a measured improvement—and decide where a person should remain in the loop.</p>
          <div class="loop-rail">RUN → TRACE → BUILD A DATASET → EVALUATE → IMPROVE → COMPARE → DECIDE</div>
          <p><b>W&amp;B Weave</b> is an observability and evaluation platform that helps teams track, evaluate, and improve AI applications.</p>
          <p class="loop-small">PatchPilot and BeeVerse Market are fictional. The Weave traces, calls, dataset, evaluation runs, annotations, and live W&amp;B Inference judge calls are real.</p>
        </header>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">The use case</div>
          <h2>BeeVerse needs a safe fix before its seasonal sale</h2>
          <p>BeeVerse Market runs merchant-support software. Its bulk-close workflow is broken, and PatchPilot has prepared a one-file repair.</p>
          <div class="loop-grid">
            <div><b>What PatchPilot does</b><br>Reads the issue, inspects the workflow, proposes a code change, and runs checks.</div>
            <div><b>What could go wrong</b><br>A request for one merchant could change a ticket belonging to another merchant.</div>
            <div><b>What we decide</b><br>Allow automatic operation, require human review, or keep the agent blocked.</div>
          </div>
          <div class="loop-panel amber"><b>Production versus today</b><br>In a production workflow, the first part of this chain would also be live: a model would choose tools, inspect files, propose edits, and run tests. We have fixed that layer today so we can focus on evaluating the result.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(core):
    config_status = core.configuration_status()
    return (config_status,)


@app.cell(hide_code=True)
def _(config_status, core, html, mo, preflight_error, preflight_receipt):
    _readiness = core.workshop_readiness(
        config_status,
        preflight_receipt=preflight_receipt,
        preflight_error=preflight_error,
    )
    _missing = ", ".join(config_status["missing"]) or "none"
    _invalid = "; ".join(config_status["invalid"]) or "none"
    mo.Html(
        f"""
        <section class="loop-page">
          <div class="loop-kicker">Preflight</div>
          <h2>Verify the workshop connection</h2>
          <div class="loop-panel {_readiness['tone']}"><b>{_readiness['title']}</b><br>
          Entity: <code>{html.escape(config_status['entity'])}</code><br>
          Project: <code>{html.escape(config_status['project'])}</code><br>
          Judge: <code>{html.escape(config_status['judge_model'])}</code><br>
          Missing: {html.escape(_missing)}<br>Invalid: {html.escape(_invalid)}</div>
          <p class="loop-small">The API key remains in your local <code>.env</code>. It is never displayed or placed in a trace. Local setup and a verified notebook connection do not sign this browser into wandb.ai.</p>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(config_status, mo):
    preflight_button = mo.ui.run_button(
        label="Verify W&B, Weave, and judge access",
        disabled=not config_status["ready"],
    )
    preflight_button
    return (preflight_button,)


@app.cell(hide_code=True)
async def _(core, preflight_button):
    preflight_error = ""
    preflight_receipt = None
    if preflight_button.value:
        try:
            preflight_receipt = await core.verify_workshop_connection()
        except Exception as error:
            preflight_error = core.safe_error_text(error)
    return preflight_error, preflight_receipt


@app.cell(hide_code=True)
def _(core, html, mo, preflight_error, preflight_receipt):
    if preflight_receipt:
        _url = html.escape(preflight_receipt["project_url"], quote=True)
        _view = mo.Html(
            f'<div class="loop-receipt"><b>Notebook connection verified.</b> W&amp;B authentication, the Weave project, and the live LLM judge responded successfully.<br><a href="{_url}" target="_blank" rel="noopener noreferrer">Open the project in Weave ↗</a><br><span class="loop-small">You must be signed into wandb.ai in this browser to open private project links.</span></div>'
        )
    elif preflight_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>Preflight failed.</b> {html.escape(preflight_error)}<br><b>Next step:</b> {html.escape(core.connection_error_guidance(RuntimeError(preflight_error)))}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(preflight_receipt):
    connection_verified = preflight_receipt is not None
    return (connection_verified,)


@app.cell(hide_code=True)
def _(mo):
    participant_role = "cross_functional_reviewer"
    initial_decision = mo.ui.radio(
        options={
            "Allow automatic operation": "automatic",
            "Require human review": "review",
            "Keep the agent blocked": "block",
        },
        value="Require human review",
        label="Before seeing more evidence, what should happen?",
    )
    mo.vstack(
        [
            mo.Html(
                '<section class="loop-page"><div class="loop-kicker">Opening decision</div><h2>The visible checks passed. Is that enough?</h2><p>You are the cross-functional reviewer: connect the business requirement to the engineering evidence.</p><div class="loop-do"><b>Your turn · 1 minute</b><br>Make the initial human-in-the-loop decision before seeing more evidence.</div></section>'
            ),
            initial_decision,
        ]
    )
    return initial_decision, participant_role


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">Chapter 1 · Trace</div>
          <h2>Start with the receipt for one run</h2>
          <p>A <b>trace</b> is the end-to-end record of one run. It contains a hierarchy of <b>calls</b>: the tracked operations or steps inside that run.</p>
          <div class="loop-panel"><b>What to look for in Weave</b><br>Open the root call, expand its child calls, and inspect the inputs, outputs, query filter, timing, and the checks that were—and were not—run.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _markdown = "\n".join(
        [
            "### The actual tracing runtime",
            "",
            "**Read-only excerpt from `workshop_core.py`.** The run button below executes this implementation. Supporting operations are defined immediately above this excerpt in the source file.",
            "",
            "```python",
            '@weave.op(name="patchpilot_prepare_v1_patch")',
            "def prepare_patch(",
            "    issue: dict[str, Any], workflow: dict[str, Any]",
            ") -> dict[str, Any]:",
            "    return {",
            '        "agent_version": "v1",',
            '        "file": workflow["path"],',
            '        "query_filter": "ticket_id IN requested_ticket_ids",',
            '        "customer_constraint": "not included",',
            '        "summary": "Close the selected tickets and preserve the review step.",',
            '        "issue_id": issue["issue_id"],',
            "    }",
            "",
            '@weave.op(name="patchpilot_v1_agent_episode")',
            "async def run_episode() -> dict[str, Any]:",
            '    issue = read_issue("BV-418")',
            '    workflow = inspect_workflow("support_workflows/bulk_close.py")',
            "    patch = prepare_patch(issue, workflow)",
            "    checks = run_visible_checks(patch)",
            "    return submit(patch, checks)",
            "",
            "result, call = await run_episode.call()",
            "```",
            "",
            "`@weave.op` records each decorated function as a Call. Calling `.call()` returns both the application result and the root Call object used for the Weave link and annotations.",
        ]
    )
    mo.md(_markdown)
    return


@app.cell(hide_code=True)
def _(connection_verified, mo):
    trace_button = mo.ui.run_button(
        label="Run PatchPilot Version 1 and create the trace",
        disabled=not connection_verified,
    )
    trace_button
    return (trace_button,)


@app.cell(hide_code=True)
async def _(core, trace_button):
    trace_error = ""
    trace_receipt = None
    if trace_button.value:
        try:
            trace_receipt = await core.run_saved_episode()
        except Exception as error:
            trace_error = core.safe_error_text(error)
    return trace_error, trace_receipt


@app.cell(hide_code=True)
def _(html, mo, trace_error, trace_receipt):
    if trace_receipt:
        _url = html.escape(trace_receipt["trace_url"], quote=True)
        _view = mo.Html(
            f'<div class="loop-receipt"><b>Version 1 trace saved.</b> <a href="{_url}" target="_blank" rel="noopener noreferrer">Open the trace in Weave ↗</a><br><span class="loop-small">Find the input, the child calls, the query filter, and what the visible checks did not cover.</span></div>'
        )
    elif trace_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The trace did not complete.</b> {html.escape(trace_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo, trace_receipt):
    observed_risk = mo.ui.radio(
        options={
            "Customer isolation": "customer_isolation",
            "Retry safety": "retry_safety",
            "Missing evidence": "missing_evidence",
            "No material concern": "no_material_concern",
        },
        value="Customer isolation",
        label="What is the primary risk you observed?",
    )
    save_risk_button = mo.ui.run_button(
        label="Save this annotation to the trace",
        disabled=trace_receipt is None,
    )
    mo.vstack(
        [
            mo.Html(
                '<div class="loop-do"><b>Your turn · 1 minute</b><br>Select the risk supported by the trace. This becomes a structured human annotation attached to the root Call in Weave, and it guides the dataset case we build next.</div>'
            ),
            observed_risk,
            save_risk_button,
        ]
    )
    return observed_risk, save_risk_button


@app.cell(hide_code=True)
def _(core, observed_risk, save_risk_button, trace_receipt):
    risk_annotation_error = ""
    risk_annotation_receipt = None
    if save_risk_button.value and trace_receipt:
        try:
            risk_annotation_receipt = core.annotate_trace_risk(
                trace_receipt["call_id"], observed_risk.value
            )
        except Exception as error:
            risk_annotation_error = core.safe_error_text(error)
    return risk_annotation_error, risk_annotation_receipt


@app.cell(hide_code=True)
def _(html, mo, risk_annotation_error, risk_annotation_receipt):
    if risk_annotation_receipt:
        _view = mo.Html(
            '<div class="loop-receipt"><b>Annotation saved.</b> The human observation now sits beside the machine-generated trace.</div>'
        )
    elif risk_annotation_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The annotation was not saved.</b> {html.escape(risk_annotation_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">Chapter 2 · Dataset</div>
          <h2>One trace becomes a repeatable test</h2>
          <p>A <b>dataset</b> is a versioned collection of cases used to test behavior repeatedly. Historical cases preserve what actually happened. Synthetic cases deliberately probe boundaries that may be rare but costly.</p>
          <div class="loop-panel amber"><b>Why this matters for AI systems</b><br>A single successful run does not establish consistent behavior. The dataset lets us rerun the same business expectations after a model, prompt, tool, retrieval, skill, or code change.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    source_strategy = mo.ui.dropdown(
        options={
            "Synthetic edge case": "synthetic",
            "Sanitized pattern from a past incident": "sanitized_pattern",
        },
        value="Synthetic edge case",
        label="How would your team source this kind of case?",
    )
    boundary_shape = mo.ui.dropdown(
        options={
            "One ticket belongs to another customer": "one_foreign_ticket",
            "Two tickets belong to another customer": "two_foreign_tickets",
        },
        value="One ticket belongs to another customer",
        label="Mixed-customer test shape",
    )
    mo.vstack(
        [
            mo.Html(
                '<div class="loop-do"><b>Your turn · 2 minutes</b><br>Configure the customer-boundary case. You are changing structured test inputs—not writing an answer that disappears when the notebook closes.</div>'
            ),
            source_strategy,
            boundary_shape,
        ]
    )
    return boundary_shape, source_strategy


@app.cell(hide_code=True)
def _(boundary_shape, core, source_strategy):
    participant_case = core.build_participant_case(
        source_strategy=source_strategy.value,
        boundary_shape=boundary_shape.value,
    )
    dataset_rows = core.workshop_dataset_rows(participant_case)
    dataset_version = core.dataset_fingerprint(dataset_rows)
    return dataset_rows, dataset_version, participant_case


@app.cell(hide_code=True)
def _(dataset_rows, dataset_version, json, mo, participant_case):
    _titles = "\n".join(
        f"- **{row['title']}** — {row['risk']} ({row['source_type']})"
        for row in dataset_rows
    )
    mo.vstack(
        [
            mo.md(
                f"""
### Your four-case dataset

{_titles}

Dataset fingerprint: `{dataset_version}`
                """
            ),
            mo.accordion(
                {
                    "Inspect the structured participant case": mo.md(
                        f"```json\n{json.dumps(participant_case, indent=2)}\n```"
                    )
                }
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(connection_verified, mo):
    publish_dataset_button = mo.ui.run_button(
        label="Publish this dataset to Weave",
        disabled=not connection_verified,
    )
    publish_dataset_button
    return (publish_dataset_button,)


@app.cell(hide_code=True)
def _(core, dataset_rows, publish_dataset_button):
    dataset_error = ""
    dataset_receipt = None
    if publish_dataset_button.value:
        try:
            dataset_receipt = core.publish_workshop_dataset(dataset_rows)
        except Exception as error:
            dataset_error = core.safe_error_text(error)
    return dataset_error, dataset_receipt


@app.cell(hide_code=True)
def _(dataset_error, dataset_receipt, html, mo):
    if dataset_receipt:
        _url = html.escape(dataset_receipt["dataset_url"], quote=True)
        _view = mo.Html(
            f'<div class="loop-receipt"><b>Dataset published.</b> {dataset_receipt["row_count"]} cases · version <code>{dataset_receipt["fingerprint"]}</code> · <a href="{_url}" target="_blank" rel="noopener noreferrer">Open the dataset in Weave ↗</a></div>'
        )
    elif dataset_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The dataset was not published.</b> {html.escape(dataset_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">Chapter 3 · Evaluation</div>
          <h2>Define “good” before comparing versions</h2>
          <div class="loop-grid">
            <div><b>Scorer</b><br>A function or class that analyzes an output and returns one or more metrics.</div>
            <div><b>Evaluation</b><br>A reusable setup containing a dataset, scorers, and optional configuration.</div>
            <div><b>LLM judge</b><br>A model-powered scorer that applies written scoring criteria to recorded evidence.</div>
          </div>
          <p>A <b>rubric</b> is the written scoring criteria supplied to the judge. Each time we run the evaluation setup against an application version, Weave creates an <b>evaluation run</b>. The judge is one scorer inside that setup; it is not the human release decision.</p>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(core, mo):
    deterministic_scorers = mo.ui.multiselect(
        options={label: scorer_id for scorer_id, label in core.DETERMINISTIC_SCORER_LABELS.items()},
        value=list(core.DETERMINISTIC_SCORER_LABELS.values()),
        label="Custom Python scorers (deterministic logic)",
    )
    freeze_evaluation = mo.ui.checkbox(
        value=True,
        label="Use the same evaluation setup for both application versions",
    )
    mo.vstack(
        [
            mo.Html(
                '<div class="loop-do"><b>Your turn · 2 minutes</b><br>Review the three fixed checks and confirm the comparison contract. Keep all three selected for the shared workshop path.</div>'
            ),
            deterministic_scorers,
            freeze_evaluation,
        ]
    )
    return deterministic_scorers, freeze_evaluation


@app.cell(hide_code=True)
def _(core, json, mo):
    rubric = core.load_rubric()
    mo.accordion(
        {
            "See the fixed rubric used by the live LLM judge": mo.md(
                f"```json\n{json.dumps(rubric, indent=2)}\n```"
            )
        }
    )
    return (rubric,)


@app.cell(hide_code=True)
def _(core, inspect, mo):
    _python_scorer_source = "\n\n".join(
        [
            inspect.getsource(core._deterministic_status),
            inspect.getsource(core.customer_isolation_scorer),
        ]
    )
    _judge_source = inspect.getsource(core.BusinessRubricJudge)
    _evaluation_source = "\n\n".join(
        [
            inspect.getsource(core.run_application_evaluation),
            inspect.getsource(core.run_evaluation),
        ]
    )
    mo.vstack(
        [
            mo.md(
                """
### The actual scorer and evaluation runtime

These are **read-only sources loaded directly from `workshop_core.py`**, the
same implementation called by the evaluation buttons. The code is collapsed
by default so the shared discussion can stay focused; expand any section when
the room wants the technical detail.
                """
            ),
            mo.accordion(
                {
                    "Exact Python scorer implementation": mo.md(
                        f"```python\n{_python_scorer_source}\n```"
                    ),
                    "Exact live LLM-judge implementation": mo.md(
                        f"```python\n{_judge_source}\n```"
                    ),
                    "Exact evaluation setup and execution": mo.md(
                        f"```python\n{_evaluation_source}\n```"
                    ),
                }
            ),
            mo.md(
                "The function-based scorers use deterministic Python logic. "
                "`BusinessRubricJudge` is a class-based `weave.Scorer` that "
                "calls W&B Serverless Inference. `weave.Evaluation` combines "
                "the dataset and both scorer types, and `.evaluate.call()` "
                "creates the inspectable evaluation run."
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(deterministic_scorers):
    scorer_ids = list(deterministic_scorers.value)
    return (scorer_ids,)


@app.cell(hide_code=True)
def _(connection_verified, dataset_receipt, freeze_evaluation, mo, scorer_ids):
    evaluation_ready = bool(
        connection_verified
        and dataset_receipt
        and freeze_evaluation.value
        and scorer_ids
    )
    run_v1_evaluation_button = mo.ui.run_button(
        label="Run the Version 1 evaluation",
        disabled=not evaluation_ready,
    )
    run_v1_evaluation_button
    return evaluation_ready, run_v1_evaluation_button


@app.cell(hide_code=True)
async def _(core, dataset_rows, run_v1_evaluation_button, scorer_ids):
    v1_evaluation_error = ""
    v1_evaluation = None
    if run_v1_evaluation_button.value:
        try:
            v1_evaluation = await core.run_evaluation(
                "v1", dataset_rows, scorer_ids=scorer_ids
            )
        except Exception as error:
            v1_evaluation_error = core.safe_error_text(error)
    return v1_evaluation, v1_evaluation_error


@app.cell(hide_code=True)
def _(html, mo, v1_evaluation, v1_evaluation_error):
    if v1_evaluation:
        _judges = {row["case_id"]: row for row in v1_evaluation["judge_results"]}
        _lines = [
            "| Dataset case | Deterministic gate | Live LLM judge |",
            "|---|---:|---:|",
        ]
        for _row in v1_evaluation["deterministic_results"]:
            _judge = _judges.get(_row["case_id"], {}).get("verdict", "missing")
            _lines.append(
                f"| {_row['title']} | **{_row['gate'].upper()}** | **{str(_judge).upper()}** |"
            )
        _url = html.escape(v1_evaluation["evaluation_url"], quote=True)
        _view = mo.vstack(
            [
                mo.Html(
                    f'<div class="loop-receipt"><b>Version 1 evaluation run complete.</b> Three Python scorers with deterministic logic plus {v1_evaluation["judge_calls"]} live judge calls. <a href="{_url}" target="_blank" rel="noopener noreferrer">Open the evaluation run in Weave ↗</a></div>'
                ),
                mo.md("\n".join(_lines)),
                mo.Html(
                    '<div class="loop-panel rose"><b>Weave stop</b><br>Open the mixed-customer row. Follow the same case from input → Version 1 output → customer-isolation scorer → LLM-judge call. The deterministic failure is the reason Version 1 stays blocked for this case.</div>'
                ),
            ]
        )
    elif v1_evaluation_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The Version 1 evaluation run did not complete.</b> {html.escape(v1_evaluation_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">Chapter 4 · Improve</div>
          <h2>Change the agent—not the test</h2>
          <p>Version 1 and Version 2 are two development versions of the same PatchPilot application. Weave represents each version as a <code>weave.Model</code> so its configuration can be saved and compared. The only intended change is the customer boundary in the patch strategy.</p>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _markdown = "\n".join(
        [
            "### The prepared Version 1 → Version 2 change",
            "",
            "**Simplified patch logic—not a literal source-code diff.** The table below shows the exact `weave.Model` properties used by the runtime.",
            "",
            "```diff",
            " # Version 1",
            "-tickets = select(ticket_id in requested_ticket_ids)",
            "",
            " # Version 2",
            "+tickets = select(",
            "+    ticket_id in requested_ticket_ids",
            "+    and customer_id == requesting_customer_id",
            "+ )",
            "```",
            "",
            "| Property | Version 1 | Version 2 |",
            "|---|---|---|",
            "| `agent_version` | `v1` | `v2` |",
            "| `patch_strategy` | `ticket_ids_only` | `tenant_scoped` |",
            "| `customer_boundary` | `not_enforced` | `requesting_customer_only` |",
            "",
            "Held fixed: dataset fingerprint, three Python scorers, LLM-judge rubric, judge model, and human-in-the-loop policy.",
        ]
    )
    mo.md(_markdown)
    return


@app.cell(hide_code=True)
def _(evaluation_ready, mo, v1_evaluation):
    run_v2_evaluation_button = mo.ui.run_button(
        label="Run the Version 2 evaluation with the same setup",
        disabled=not (evaluation_ready and v1_evaluation),
    )
    run_v2_evaluation_button
    return (run_v2_evaluation_button,)


@app.cell(hide_code=True)
async def _(core, dataset_rows, run_v2_evaluation_button, scorer_ids):
    v2_evaluation_error = ""
    v2_evaluation = None
    if run_v2_evaluation_button.value:
        try:
            v2_evaluation = await core.run_evaluation(
                "v2", dataset_rows, scorer_ids=scorer_ids
            )
        except Exception as error:
            v2_evaluation_error = core.safe_error_text(error)
    return v2_evaluation, v2_evaluation_error


@app.cell(hide_code=True)
def _(core, html, mo, v1_evaluation, v2_evaluation, v2_evaluation_error):
    if v1_evaluation and v2_evaluation:
        _comparison = core.compare_evaluations(v1_evaluation, v2_evaluation)
        _lines = [
            "| Dataset case | V1 gate | V2 gate | V1 judge | V2 judge |",
            "|---|---:|---:|---:|---:|",
        ]
        for _row in _comparison:
            _lines.append(
                f"| {_row['case']} | **{_row['v1_gate'].upper()}** | **{_row['v2_gate'].upper()}** | {_row['v1_judge'].upper()} | {_row['v2_judge'].upper()} |"
            )
        _url = html.escape(
            core.evaluation_comparison_url(v1_evaluation, v2_evaluation),
            quote=True,
        )
        _view = mo.vstack(
            [
                mo.Html(
                    f'<div class="loop-receipt"><b>Version 2 evaluation run complete.</b> <a href="{_url}" target="_blank" rel="noopener noreferrer">Open the V1 baseline and V2 comparison in Weave ↗</a></div>'
                ),
                mo.md("\n".join(_lines)),
                mo.Html(
                    '<div class="loop-panel mint"><b>What changed?</b><br>The mixed-customer case moves from BLOCK to PASS in the deterministic gate. The missing-evidence case remains in human review. A live LLM judge may vary; inspect its reasons instead of treating variation as a hidden failure.</div>'
                ),
            ]
        )
    elif v2_evaluation_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The Version 2 evaluation run did not complete.</b> {html.escape(v2_evaluation_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo, v2_evaluation):
    final_decision = mo.ui.radio(
        options={
            "Allow automatic operation for bounded low-risk cases": "automatic",
            "Require human review": "review",
            "Keep the agent blocked": "block",
        },
        value="Require human review",
        label="After comparing both versions, what should happen?",
    )
    confidence = mo.ui.radio(
        options={"High": "high", "Medium": "medium", "Low": "low"},
        value="Medium",
        label="Confidence",
    )
    permitted_scope = mo.ui.radio(
        options={
            "Low-risk, single-customer cases": "bounded_cases",
            "This patch only": "this_patch",
            "No automatic operation": "no_automation",
        },
        value="No automatic operation",
        label="Approved scope",
    )
    reviewer = mo.ui.text(value="Workshop participant", label="Reviewer")
    save_decision_button = mo.ui.run_button(
        label="Save the human-in-the-loop decision",
        disabled=v2_evaluation is None,
    )
    mo.vstack(
        [
            mo.Html(
                '<section class="loop-page"><div class="loop-kicker">Chapter 5 · Decide</div><h2>Use evidence to set the human-in-the-loop boundary</h2><div class="loop-do"><b>Your turn · 2 minutes</b><br>Record the decision, confidence, and operating scope. These annotations persist in Weave.</div></section>'
            ),
            final_decision,
            confidence,
            permitted_scope,
            reviewer,
            save_decision_button,
        ]
    )
    return confidence, final_decision, permitted_scope, reviewer, save_decision_button


@app.cell(hide_code=True)
async def _(
    confidence,
    core,
    dataset_receipt,
    final_decision,
    initial_decision,
    participant_role,
    permitted_scope,
    reviewer,
    rubric,
    save_decision_button,
    scorer_ids,
    trace_receipt,
):
    decision_error = ""
    decision_receipt = None
    if save_decision_button.value and trace_receipt and dataset_receipt:
        try:
            decision_receipt = await core.record_human_review(
                {
                    "initial_decision": initial_decision.value,
                    "final_decision": final_decision.value,
                    "participant_role": participant_role,
                    "dataset_uri": dataset_receipt["uri"],
                    "scorer_ids": scorer_ids,
                    "rubric_id": rubric["rubric_id"],
                    "reviewed_versions": ["v1", "v2"],
                    "permitted_scope": permitted_scope.value,
                    "reviewer": reviewer.value,
                    "confidence": confidence.value,
                    "trace_call_id": trace_receipt["call_id"],
                }
            )
        except Exception as error:
            decision_error = core.safe_error_text(error)
    return decision_error, decision_receipt


@app.cell(hide_code=True)
def _(decision_error, decision_receipt, html, mo):
    if decision_receipt:
        _record_url = html.escape(decision_receipt["record_url"], quote=True)
        _annotation_note = (
            f'<br><span class="loop-small">Annotation warning: {html.escape(decision_receipt["annotation_error"])}</span>'
            if decision_receipt["annotation_error"]
            else ""
        )
        _view = mo.Html(
            f'<div class="loop-receipt"><b>Human-in-the-loop record saved.</b> <a href="{_record_url}" target="_blank" rel="noopener noreferrer">Open the review record in Weave ↗</a>{_annotation_note}</div>'
        )
    elif decision_error:
        _view = mo.Html(
            f'<div class="loop-error"><b>The decision was not saved.</b> {html.escape(decision_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="loop-page">
          <div class="loop-kicker">The Agent Loop</div>
          <h2>Every change creates a new evidence question</h2>
          <div class="loop-rail">TRACE → DATASET → SCORERS → EVALUATION → CHANGE → COMPARE → HUMAN-IN-THE-LOOP DECISION</div>
          <p><b>A trace</b> tells us what happened. <b>A dataset</b> makes the concern repeatable. <b>Scorers</b> turn expectations into measurements. <b>Evaluation runs</b> show whether a change helped. <b>Human review</b> determines how much responsibility the system is ready to receive.</p>
          <div class="loop-panel amber"><b>Where AI was used today</b><br>The LLM judge used W&amp;B Serverless Inference. PatchPilot V1 and V2, the three Python scorers, dataset assembly, and annotation policy were fixed so the central comparison remained reliable.</div>
          <p class="loop-small">Optional follow-up: change the judge rubric, add dataset cases, or replace the prepared PatchPilot versions with a live autonomous coding agent.</p>
        </section>
        """
    )
    return


if __name__ == "__main__":
    app.run()
