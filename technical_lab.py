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
"""Optional editable follow-up for the Agent Loop Workshop."""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import html
    from copy import deepcopy
    from pathlib import Path
    from typing import Any

    import marimo as mo
    import weave
    from dotenv import load_dotenv

    local_env = Path(__file__).with_name(".env")
    load_dotenv(local_env if local_env.exists() else None, override=True)
    import workshop_core as core

    return Any, core, deepcopy, html, mo, weave


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <style>
          :root { --ink:#111827; --muted:#64748b; --line:#d8dee8; --blue:#2563eb; --amber:#d97706; --mint:#0f9f86; --rose:#b84735; }
          .lab-page { padding:1.1rem 0 .7rem; color:var(--ink); }
          .lab-page h1 { font-size:2.5rem; line-height:1.05; margin:.45rem 0 1rem; }
          .lab-page h2 { font-size:1.7rem; line-height:1.15; margin:.35rem 0 .65rem; }
          .lab-page p { font-size:1.02rem; line-height:1.55; }
          .lab-kicker { color:var(--rose); font-size:.78rem; font-weight:850; letter-spacing:.09em; text-transform:uppercase; }
          .lab-rail { border-top:2px solid var(--line); border-bottom:2px solid var(--line); padding:.75rem 0; margin:1rem 0; color:var(--muted); font-weight:750; }
          .lab-panel { border-left:8px solid var(--blue); background:#f7f9fc; padding:1rem 1.15rem; margin:1rem 0; }
          .lab-panel.amber { border-color:var(--amber); }
          .lab-panel.mint { border-color:var(--mint); }
          .lab-panel.rose { border-color:var(--rose); }
          .lab-receipt { background:#eef8f5; border:1px solid #b9e2d9; padding:.9rem 1rem; margin:.9rem 0; }
          .lab-error { background:#fff2ef; border:1px solid #efc0b7; padding:.9rem 1rem; margin:.9rem 0; color:#842f23; }
          .lab-small { color:var(--muted); font-size:.91rem; }
          table { font-size:.92rem; }
        </style>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <header class="lab-page">
          <div class="lab-kicker">Optional technical lab · 45–60 minutes</div>
          <h1>Extend the Agent Loop with real code</h1>
          <p>Build on the BeeVerse case by adding a dataset row, a deterministic scorer, and PatchPilot Version 3—then compare V2 and V3 under one controlled evaluation contract.</p>
          <div class="lab-rail">EDIT → TRACE → EXTEND DATA → ADD A SCORER → EVALUATE → COMPARE</div>
          <div class="lab-panel amber"><b>Cost and variability</b><br>The preflight makes one hosted model call. Each five-row evaluation makes five live LLM-judge calls through W&amp;B Serverless Inference. The judge can vary; the Python gates remain deterministic.</div>
          <p class="lab-small">This notebook is intentionally editable. Credentials remain in the local <code>.env</code>; do not paste an API key into a cell, function input, trace attribute, dataset row, or prompt.</p>
        </header>
        """
    )
    return


@app.cell(hide_code=True)
def _(core):
    lab_config_status = core.configuration_status()
    return (lab_config_status,)


@app.cell(hide_code=True)
def _(lab_config_status, mo):
    lab_preflight_button = mo.ui.run_button(
        label="Verify W&B, Weave, and judge access",
        disabled=not lab_config_status["ready"],
    )
    lab_preflight_button
    return (lab_preflight_button,)


@app.cell(hide_code=True)
async def _(core, lab_preflight_button):
    lab_preflight_error = ""
    lab_preflight_receipt = None
    if lab_preflight_button.value:
        try:
            lab_preflight_receipt = await core.verify_workshop_connection()
        except Exception as error:
            lab_preflight_error = core.safe_error_text(error)
    return lab_preflight_error, lab_preflight_receipt


@app.cell(hide_code=True)
def _(
    core,
    html,
    lab_config_status,
    lab_preflight_error,
    lab_preflight_receipt,
    mo,
):
    _readiness = core.workshop_readiness(
        lab_config_status,
        preflight_receipt=lab_preflight_receipt,
        preflight_error=lab_preflight_error,
    )
    _missing = ", ".join(lab_config_status["missing"]) or "none"
    _invalid = "; ".join(lab_config_status["invalid"]) or "none"
    _connection_detail = ""
    if lab_preflight_receipt:
        _url = html.escape(lab_preflight_receipt["project_url"], quote=True)
        _connection_detail = (
            f'<div class="lab-receipt"><b>Notebook connection verified.</b> '
            f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
            "Open the project in Weave ↗</a><br>"
            '<span class="lab-small">Browser sign-in is separate from notebook '
            "authentication.</span></div>"
        )
    elif lab_preflight_error:
        _connection_detail = (
            f'<div class="lab-error"><b>Connection not verified.</b> '
            f"{html.escape(lab_preflight_error)}<br><b>Next step:</b> "
            f"{html.escape(core.connection_error_guidance(RuntimeError(lab_preflight_error)))}</div>"
        )
    mo.Html(
        f"""
        <section class="lab-page">
          <div class="lab-kicker">Preflight</div>
          <h2>{_readiness['title']}</h2>
          <div class="lab-panel {_readiness['tone']}">
            Entity: <code>{html.escape(lab_config_status['entity'])}</code><br>
            Project: <code>{html.escape(lab_config_status['project'])}</code><br>
            Judge: <code>{html.escape(lab_config_status['judge_model'])}</code><br>
            Missing: {html.escape(_missing)}<br>Invalid: {html.escape(_invalid)}
          </div>
          {_connection_detail}
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(lab_preflight_receipt):
    lab_connection_verified = lab_preflight_receipt is not None
    return (lab_connection_verified,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 1: create an editable traced application

    `LabPatchPilotAgent.predict` is the real function Weave evaluates. Change the
    Version 3 properties or add a field to its returned evidence, then rerun the
    cells below. The `@weave.op` decorator records its inputs, output, timing, and
    execution metadata as a Call.
    """)
    return


@app.cell
def _(Any, core, weave):
    class LabPatchPilotAgent(weave.Model):
        agent_version: str
        patch_strategy: str
        customer_boundary: str
        change_summary: str
        evidence_strategy: str = "as_observed"

        @weave.op(name="patchpilot_technical_lab_run_agent")
        async def predict(
            self,
            case_id: str,
            title: str,
            source_type: str,
            risk: str,
            scenario: str,
            request: dict[str, Any],
            expected_behavior: dict[str, Any],
        ) -> dict[str, Any]:
            del title, source_type, risk, scenario, expected_behavior
            return core.simulate_prepared_agent_output(
                self.model_dump(),
                case_id=case_id,
                request=request,
            )

    v3_agent = LabPatchPilotAgent(
        agent_version="v3",
        patch_strategy="tenant_scoped",
        customer_boundary="requesting_customer_only",
        change_summary="Collect explicit customer-boundary and retry evidence",
        evidence_strategy="active_safety_checks",
    )
    return (v3_agent,)


@app.cell(hide_code=True)
def _(mo, v3_agent):
    mo.md(f"""
    **Current V3 properties**

    | Property | Value |
    |---|---|
    | `agent_version` | `{v3_agent.agent_version}` |
    | `patch_strategy` | `{v3_agent.patch_strategy}` |
    | `customer_boundary` | `{v3_agent.customer_boundary}` |
    | `evidence_strategy` | `{v3_agent.evidence_strategy}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 2: add a fifth dataset case

    This case has customer-account evidence but lacks retry evidence. It is a
    deliberate coverage boundary, not a prose answer. Edit the request or expected
    behavior to test a different operational concern.
    """)
    return


@app.cell
def _(core):
    fifth_case = {
        "case_id": "partial_safety_evidence",
        "title": "Only part of the safety evidence was recorded",
        "source_type": "synthetic",
        "risk": "Evidence completeness",
        "scenario": (
            "BeeVerse records the affected customer accounts but does not exercise "
            "the retry path before the patch is reviewed."
        ),
        "request": {
            "requesting_customer_id": "honeycomb-books",
            "tickets": [
                {"ticket_id": "BV-601", "customer_id": "honeycomb-books"},
                {"ticket_id": "BV-602", "customer_id": "honeycomb-books"},
            ],
            "retry_count": 1,
            "observe_customer_accounts": True,
            "observe_retry_behavior": False,
        },
        "expected_behavior": {
            "allowed_customer_id": "honeycomb-books",
            "required_visible_checks": 3,
            "maximum_duplicate_audit_events": 0,
            "required_evidence": ["customer_accounts", "retry_behavior"],
        },
    }
    lab_rows = [*core.workshop_dataset_rows(), fifth_case]
    return (lab_rows,)


@app.cell(hide_code=True)
def _(core, lab_rows, mo):
    _titles = "\n".join(f"- **{row['title']}**" for row in lab_rows)
    mo.md(
        f"""
    ### Five-case technical-lab dataset

    {_titles}

    Fingerprint: `{core.dataset_fingerprint(lab_rows)}`
            """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 3: implement a deterministic scorer

    This scorer answers an exact question: did the recorded output contain every
    required category of safety evidence? It does not call an LLM. Edit the required
    fields or return shape to explore how scorer design affects the evaluation.
    """)
    return


@app.cell
def _(weave):
    def evidence_completeness_status(output, expected_behavior):
        required = set(expected_behavior.get("required_evidence", []))
        available = set()
        if output.get("customer_account_evidence_available"):
            available.add("customer_accounts")
        if output.get("retry_evidence_available"):
            available.add("retry_behavior")
        missing = sorted(required - available)
        return {
            "status": "fail" if missing else "pass",
            "reason": (
                f"Missing required evidence: {', '.join(missing)}."
                if missing
                else "All required safety evidence is present."
            ),
        }

    @weave.op(name="patchpilot_technical_lab_evidence_completeness_scorer")
    def evidence_completeness_scorer(output, expected_behavior):
        return evidence_completeness_status(output, expected_behavior)

    return evidence_completeness_scorer, evidence_completeness_status


@app.cell
def _(core, evidence_completeness_status, lab_rows):
    def lab_deterministic_results(application):
        rows = core.deterministic_case_results_for_application(lab_rows, application)
        expected_by_id = {row["case_id"]: row["expected_behavior"] for row in lab_rows}
        for row in rows:
            evidence_score = evidence_completeness_status(
                row["output"], expected_by_id[row["case_id"]]
            )
            row["scores"]["evidence_completeness"] = evidence_score
            statuses = [score["status"] for score in row["scores"].values()]
            row["gate"] = (
                "block"
                if "fail" in statuses
                else "review"
                if "unknown" in statuses
                else "pass"
            )
        return rows

    return (lab_deterministic_results,)


@app.cell(hide_code=True)
def _(core, lab_deterministic_results, mo, v3_agent):
    _v2_rows = {row["case_id"]: row for row in lab_deterministic_results(core.build_agent("v2"))}
    _v3_rows = {row["case_id"]: row for row in lab_deterministic_results(v3_agent)}
    _lines = ["| Case | V2 gate | V3 gate |", "|---|---:|---:|"]
    for _case_id, _v2 in _v2_rows.items():
        _lines.append(
            f"| {_v2['title']} | **{_v2['gate'].upper()}** | "
            f"**{_v3_rows[_case_id]['gate'].upper()}** |"
        )
    mo.vstack(
        [
            mo.md("### Deterministic preview—no model calls"),
            mo.md("\n".join(_lines)),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 4: evaluate V2 and V3 under one fixed contract

    Both runs below use the same five dataset rows, four deterministic scorers,
    judge model, and rubric. Only the application changes. Each button makes five
    live LLM-judge calls.
    """)
    return


@app.cell(hide_code=True)
def _(lab_connection_verified, mo):
    confirm_lab_calls = mo.ui.checkbox(
        label="I understand that each evaluation makes five live judge calls"
    )
    run_lab_v2_button = mo.ui.run_button(
        label="Run the technical-lab V2 baseline · 5 judge calls",
        disabled=not (lab_connection_verified and confirm_lab_calls.value),
    )
    mo.vstack([confirm_lab_calls, run_lab_v2_button])
    return confirm_lab_calls, run_lab_v2_button


@app.cell(hide_code=True)
async def _(core, evidence_completeness_scorer, lab_rows, run_lab_v2_button):
    lab_v2_error = ""
    lab_v2_evaluation = None
    if run_lab_v2_button.value:
        try:
            lab_v2_evaluation = await core.run_application_evaluation(
                core.build_agent("v2"),
                lab_rows,
                additional_scorers=[evidence_completeness_scorer],
                additional_scorer_ids=["evidence_completeness"],
                dataset_name="patchpilot-technical-lab-cases",
                dataset_description="Five editable BeeVerse technical-lab cases.",
                evaluation_name="patchpilot-technical-lab-v2-v3",
                evaluation_run_prefix="Technical Lab",
                scorer_set_version="technical-lab-scorers-v1",
                contract_id="technical-lab-v1",
                attribute_namespace="agent_loop_lab",
            )
        except Exception as error:
            lab_v2_error = core.safe_error_text(error)
    return lab_v2_error, lab_v2_evaluation


@app.cell(hide_code=True)
def _(confirm_lab_calls, lab_connection_verified, lab_v2_evaluation, mo):
    run_lab_v3_button = mo.ui.run_button(
        label="Run the technical-lab V3 candidate · 5 judge calls",
        disabled=not (
            lab_connection_verified
            and confirm_lab_calls.value
            and lab_v2_evaluation is not None
        ),
    )
    run_lab_v3_button
    return (run_lab_v3_button,)


@app.cell(hide_code=True)
async def _(
    core,
    evidence_completeness_scorer,
    lab_rows,
    run_lab_v3_button,
    v3_agent,
):
    lab_v3_error = ""
    lab_v3_evaluation = None
    if run_lab_v3_button.value:
        try:
            lab_v3_evaluation = await core.run_application_evaluation(
                v3_agent,
                lab_rows,
                additional_scorers=[evidence_completeness_scorer],
                additional_scorer_ids=["evidence_completeness"],
                dataset_name="patchpilot-technical-lab-cases",
                dataset_description="Five editable BeeVerse technical-lab cases.",
                evaluation_name="patchpilot-technical-lab-v2-v3",
                evaluation_run_prefix="Technical Lab",
                scorer_set_version="technical-lab-scorers-v1",
                contract_id="technical-lab-v1",
                attribute_namespace="agent_loop_lab",
            )
        except Exception as error:
            lab_v3_error = core.safe_error_text(error)
    return lab_v3_error, lab_v3_evaluation


@app.cell(hide_code=True)
def _(
    core,
    html,
    lab_v2_error,
    lab_v2_evaluation,
    lab_v3_error,
    lab_v3_evaluation,
    mo,
):
    _items = []
    if lab_v2_evaluation:
        _v2_url = html.escape(lab_v2_evaluation["evaluation_url"], quote=True)
        _items.append(
            mo.Html(
                f'<div class="lab-receipt"><b>V2 baseline complete.</b> '
                f'<a href="{_v2_url}" target="_blank" rel="noopener noreferrer">'
                "Open V2 in Weave ↗</a></div>"
            )
        )
    if lab_v2_error:
        _items.append(
            mo.Html(
                f'<div class="lab-error"><b>V2 did not complete.</b> '
                f"{html.escape(lab_v2_error)}</div>"
            )
        )
    if lab_v3_evaluation:
        _v3_url = html.escape(lab_v3_evaluation["evaluation_url"], quote=True)
        _items.append(
            mo.Html(
                f'<div class="lab-receipt"><b>V3 candidate complete.</b> '
                f'<a href="{_v3_url}" target="_blank" rel="noopener noreferrer">'
                "Open V3 and compare it with V2 in Weave ↗</a></div>"
            )
        )
        _comparison = core.compare_evaluations(lab_v2_evaluation, lab_v3_evaluation)
        _lines = [
            "| Case | V2 gate | V3 gate | V2 judge | V3 judge |",
            "|---|---:|---:|---:|---:|",
        ]
        for _row in _comparison:
            _lines.append(
                f"| {_row['case']} | {_row['v1_gate'].upper()} | "
                f"{_row['v2_gate'].upper()} | {_row['v1_judge'].upper()} | "
                f"{_row['v2_judge'].upper()} |"
            )
        _items.append(mo.md("\n".join(_lines)))
    if lab_v3_error:
        _items.append(
            mo.Html(
                f'<div class="lab-error"><b>V3 did not complete.</b> '
                f"{html.escape(lab_v3_error)}</div>"
            )
        )
    mo.vstack(_items) if _items else mo.md("")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Optional experiment: change the judge rubric

    Changing the rubric changes the evaluation contract. Do not compare a result
    scored with this rubric against the earlier contract. Rerun both V2 and V3, then
    compare those two new runs with each other.
    """)
    return


@app.cell
def _(core, deepcopy):
    revised_lab_rubric = deepcopy(core.load_rubric())
    revised_lab_rubric["rubric_id"] = "agent-quality-technical-lab-v2"
    revised_lab_rubric["name"] = "BeeVerse agent-quality technical-lab rubric"
    revised_lab_rubric["criteria"].append(
        {
            "id": "evidence_actionable",
            "label": (
                "The recorded evidence must be specific enough for a reviewer to "
                "verify customer isolation and retry behavior."
            ),
            "blocking": False,
        }
    )
    return (revised_lab_rubric,)


@app.cell(hide_code=True)
def _(lab_connection_verified, mo, revised_lab_rubric):
    confirm_revised_calls = mo.ui.checkbox(
        label="Run the revised rubric as a separate 10-call comparison"
    )
    run_revised_pair_button = mo.ui.run_button(
        label="Evaluate V2 and V3 with the revised rubric · 10 judge calls",
        disabled=not (lab_connection_verified and confirm_revised_calls.value),
    )
    mo.vstack(
        [
            mo.md(
                f"Revised contract: `{revised_lab_rubric['rubric_id']}` with "
                f"{len(revised_lab_rubric['criteria'])} criteria."
            ),
            confirm_revised_calls,
            run_revised_pair_button,
        ]
    )
    return (run_revised_pair_button,)


@app.cell(hide_code=True)
async def _(
    core,
    evidence_completeness_scorer,
    lab_rows,
    revised_lab_rubric,
    run_revised_pair_button,
    v3_agent,
):
    revised_pair_error = ""
    revised_v2_evaluation = None
    revised_v3_evaluation = None
    if run_revised_pair_button.value:
        _shared = {
            "additional_scorers": [evidence_completeness_scorer],
            "additional_scorer_ids": ["evidence_completeness"],
            "rubric": revised_lab_rubric,
            "dataset_name": "patchpilot-technical-lab-cases",
            "dataset_description": "Five editable BeeVerse technical-lab cases.",
            "evaluation_name": "patchpilot-technical-lab-rubric-v2",
            "evaluation_run_prefix": "Technical Lab Rubric V2",
            "scorer_set_version": "technical-lab-scorers-v1",
            "contract_id": "technical-lab-rubric-v2",
            "attribute_namespace": "agent_loop_lab",
        }
        try:
            revised_v2_evaluation = await core.run_application_evaluation(
                core.build_agent("v2"), lab_rows, **_shared
            )
            revised_v3_evaluation = await core.run_application_evaluation(
                v3_agent, lab_rows, **_shared
            )
        except Exception as error:
            revised_pair_error = core.safe_error_text(error)
    return revised_pair_error, revised_v2_evaluation, revised_v3_evaluation


@app.cell(hide_code=True)
def _(
    core,
    html,
    mo,
    revised_pair_error,
    revised_v2_evaluation,
    revised_v3_evaluation,
):
    if revised_v2_evaluation and revised_v3_evaluation:
        _comparison = core.compare_evaluations(
            revised_v2_evaluation, revised_v3_evaluation
        )
        _v3_url = html.escape(revised_v3_evaluation["evaluation_url"], quote=True)
        _lines = [
            "| Case | Revised V2 judge | Revised V3 judge |",
            "|---|---:|---:|",
        ]
        for _row in _comparison:
            _lines.append(
                f"| {_row['case']} | {_row['v1_judge'].upper()} | "
                f"{_row['v2_judge'].upper()} |"
            )
        _view = mo.vstack(
            [
                mo.Html(
                    f'<div class="lab-receipt"><b>Separate rubric experiment '
                    f'complete.</b> <a href="{_v3_url}" target="_blank" '
                    'rel="noopener noreferrer">Open the revised V3 run in Weave ↗</a></div>'
                ),
                mo.md("\n".join(_lines)),
            ]
        )
    elif revised_pair_error:
        _view = mo.Html(
            f'<div class="lab-error"><b>The revised-rubric comparison did not '
            f"complete.</b> {html.escape(revised_pair_error)}</div>"
        )
    else:
        _view = mo.md("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="lab-page">
          <div class="lab-kicker">What to take forward</div>
          <h2>One change, one explicit evaluation contract</h2>
          <p>The application, dataset, deterministic scorers, LLM judge, and rubric are all versioned evidence. Hold the contract fixed when comparing application changes. When the contract changes, rerun every candidate you intend to compare.</p>
          <div class="lab-panel mint"><b>Continue experimenting</b><br>Add a case from a sanitized incident, change the V3 evidence strategy, write another exact scorer, or revise one rubric criterion. Keep the experiment name and metadata honest about what changed.</div>
        </section>
        """
    )
    return


if __name__ == "__main__":
    app.run()
