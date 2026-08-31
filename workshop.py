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
"""PatchPilot v1 — evidence before authority."""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import json

    import marimo as mo
    from dotenv import load_dotenv

    from pathlib import Path as _Path

    _local_env = _Path(__file__).with_name(".env")
    load_dotenv(_local_env if _local_env.exists() else None, override=True)
    import workshop_core as core

    return core, json, mo


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <style>
          :root {
            --ink: #111827;
            --muted: #64748b;
            --line: #d8dee8;
            --paper: #ffffff;
            --blue: #3b82f6;
            --amber: #eaa02b;
            --mint: #159f8c;
            --rose: #b84735;
          }
          .pp-page { padding: 1.25rem 0 .75rem; color: var(--ink); }
          .pp-kicker { color: var(--rose); font-size: .78rem; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
          .pp-page h1 { font-size: 2.65rem; line-height: 1.05; margin: .55rem 0 1rem; }
          .pp-page h2 { font-size: 1.75rem; line-height: 1.15; margin: .4rem 0 .65rem; }
          .pp-page p { font-size: 1.05rem; line-height: 1.58; }
          .pp-promise { font-size: 1.28rem !important; max-width: 48rem; }
          .pp-rail { border-top: 2px solid var(--line); border-bottom: 2px solid var(--line); padding: .7rem 0; margin: 1.2rem 0; color: var(--muted); font-weight: 750; letter-spacing: .02em; }
          .pp-panel { border-left: 8px solid var(--blue); background: #f7f9fc; padding: 1rem 1.15rem; margin: 1rem 0; }
          .pp-panel.amber { border-color: var(--amber); }
          .pp-panel.mint { border-color: var(--mint); }
          .pp-panel.rose { border-color: var(--rose); }
          .pp-guide { border: 2px solid #cbd5e1; background: #f8fafc; padding: 1rem 1.15rem; margin: 1rem 0; }
          .pp-guide > b:first-child, .pp-do > b:first-child { display: block; margin-bottom: .3rem; }
          .pp-do { border: 2px solid #93c5fd; background: #eff6ff; padding: 1rem 1.15rem; margin: 1rem 0; }
          .pp-checkpoint { color: #1d4ed8; font-size: .82rem; font-weight: 850; letter-spacing: .07em; text-transform: uppercase; }
          .pp-layer { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: .8rem; margin: 1rem 0; }
          .pp-layer > div { border-top: 5px solid var(--blue); background: #f7f9fc; padding: .9rem; min-height: 7.5rem; }
          .pp-layer > div:nth-child(2) { border-top-color: var(--amber); }
          .pp-layer > div:nth-child(3) { border-top-color: var(--mint); }
          .pp-receipt { background: #eef8f5; border: 1px solid #b9e2d9; padding: .9rem 1rem; margin: .9rem 0; }
          .pp-error { background: #fff2ef; border: 1px solid #efc0b7; padding: .9rem 1rem; margin: .9rem 0; color: #842f23; }
          .pp-small { color: var(--muted); font-size: .9rem; }
          .pp-verdict-pass { color: var(--mint); font-weight: 800; text-transform: uppercase; }
          .pp-verdict-review { color: var(--amber); font-weight: 800; text-transform: uppercase; }
          .pp-verdict-block { color: var(--rose); font-weight: 800; text-transform: uppercase; }
          table { font-size: .95rem; }
        </style>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <header class="pp-page">
          <div class="pp-kicker">PatchPilot · Executive masterclass · 90 minutes</div>
          <h1>Evidence before authority</h1>
          <p class="pp-promise">By the end, you will be able to inspect an AI-agent run, test it against business rules, and defend whether it should operate automatically, require review, or remain blocked.</p>
          <div class="pp-rail">TRACE THE RUN &nbsp;→&nbsp; TEST THE SYSTEM &nbsp;→&nbsp; DEFINE GOOD &nbsp;→&nbsp; BOUND THE AUTHORITY</div>
          <p class="pp-small">PatchPilot is fictional. The retail incident and failure modes are synthetic; the W&amp;B traces, evaluations, and judge calls are real.</p>
        </header>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">Before we begin</div>
          <h2>We are building evidence for an operating decision</h2>
          <p><b>Weave</b> is the evidence layer for this workshop: it records traces, runs evaluations, applies scorers, and lets us compare results.</p>
          <p><b>PatchPilot</b> is a fictional coding agent. It repairs Northstar Retail's bulk-close support workflow, runs visible checks, and submits a patch for review. It never deploys during this exercise.</p>
          <div class="pp-layer">
            <div><b>Start with</b><br>One apparently successful agent run and a decision about how much authority you would grant.</div>
            <div><b>Build</b><br>A trace, a four-case evaluation, an LLM-judge scorer, and one business rule you can defend.</div>
            <div><b>Leave with</b><br>A bounded decision: operate automatically, require human review, or remain blocked.</div>
          </div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">How we will work</div>
          <h2>This is a guided evidence lab</h2>
          <div class="pp-layer">
            <div><b>Follow</b><br>The facilitator explains one concept and shows the code that creates the evidence.</div>
            <div><b>Try</b><br>You use bounded controls to predict, inspect, revise a rubric, and make a decision.</div>
            <div><b>Inspect</b><br>The room opens the matching trace, scorer call, or evaluation in Weave together.</div>
          </div>
          <div class="pp-guide"><b>Stay with the facilitator.</b> You can work in your own notebook while the shared screen moves through the same path. The code is visible for explanation; the live changes stay focused on the business rubric.</div>
          <p class="pp-small">No partner work, breakout room, chat response, or Python editing is required.</p>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(core):
    config_status = core.configuration_status()
    return (config_status,)


@app.cell(hide_code=True)
def _(config_status, mo):
    import html as _html

    _configured = "Configured" if config_status["ready"] else "Needs setup"
    _missing = ", ".join(config_status["missing"]) or "none"
    _invalid = "; ".join(config_status["invalid"]) or "none"
    _notices = "".join(
        f'<div class="pp-panel amber"><b>Adjusted automatically.</b> {_html.escape(note)}</div>'
        for note in config_status["notices"]
    )
    mo.Html(
        f"""
        <section class="pp-page">
          <div class="pp-kicker">Preflight</div>
          <h2>Verify the workshop connection</h2>
          <div class="pp-panel {'mint' if config_status['ready'] else 'rose'}">
            <b>{_configured}</b><br>
            Entity: <code>{_html.escape(config_status['entity'] or '(missing)')}</code><br>
            Project: <code>{_html.escape(config_status['project'] or '(missing)')}</code><br>
            Judge: <code>{_html.escape(config_status['judge_model'])}</code><br>
            Missing: <code>{_html.escape(_missing)}</code><br>
            Invalid: <code>{_html.escape(_invalid)}</code>
          </div>
          {_notices}
          <div class="pp-guide"><span class="pp-checkpoint">Before the session</span><br>The panel says <b>Configured</b> when the required settings are usable. Click <b>Run workshop preflight</b>; continue only after the receipt confirms both <b>Weave</b> and the <b>judge model</b>. Do not install software or troubleshoot API keys during the workshop.</div>
          <p>Your API key is read from <code>.env</code>. It is never displayed or placed in a trace.</p>
          <p class="pp-small"><b>Running this yourself:</b> create a W&amp;B account and API key, copy <code>.env.example</code> to <code>.env</code>, add your key and entity, then launch with <code>uv run marimo run workshop.py</code>.</p>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(config_status, mo):
    connect_button = mo.ui.run_button(
        label="Run workshop preflight",
        disabled=not config_status["ready"],
    )
    connect_button
    return (connect_button,)


@app.cell(hide_code=True)
async def _(connect_button, core):
    connection_error = ""
    connection_receipt = None
    if connect_button.value:
        try:
            connection_receipt = await core.verify_workshop_connection()
        except Exception as error:
            connection_error = core.safe_error_text(error)
    return connection_error, connection_receipt


@app.cell(hide_code=True)
def _(connection_error, connection_receipt, core, mo):
    import html as _html

    if connection_receipt:
        _view = mo.Html(
            f"""<div class="pp-receipt"><b>Ready for the workshop.</b><br>
            Weave destination: <code>{_html.escape(connection_receipt['entity'])}/{_html.escape(connection_receipt['project'])}</code><br>
            Judge model: <code>{_html.escape(connection_receipt['judge_model'])}</code> — reachable.</div>"""
        )
    elif connection_error:
        _guidance = core.connection_error_guidance(RuntimeError(connection_error))
        _view = mo.Html(
            f'<div class="pp-error"><b>Preflight failed.</b> {_html.escape(connection_error)}'
            f'<br><b>Next step:</b> {_html.escape(_guidance)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    participant_role = mo.ui.dropdown(
        options={
            "Customer support leader": "support",
            "Risk or compliance leader": "risk",
            "Product leader": "product",
            "Engineering leader": "engineering",
        },
        value="Customer support leader",
        label="Choose the perspective you want to use during the workshop",
    )
    participant_role
    return (participant_role,)


@app.cell(hide_code=True)
def _(mo, participant_role):
    _questions = {
        "support": "Would this behavior protect customer trust during a high-volume support event?",
        "risk": "Which outcome would be unacceptable even if the average result looked good?",
        "product": "What narrow customer value is worth automating, and what must remain bounded?",
        "engineering": "What evidence would justify turning this business rule into a protected test?",
    }
    mo.Html(
        f'<div class="pp-panel"><b>Your lens:</b> {_questions[participant_role.value]}</div>'
    )
    return


@app.cell(hide_code=True)
def _(mo):
    initial_decision = mo.ui.radio(
        options={
            "Allow automatic operation": "automatic",
            "Require human review": "review",
            "Keep the agent blocked": "block",
        },
        value="Require human review",
        label="Before seeing the evidence, what authority would you grant?",
    )
    opening_evidence = mo.ui.text_area(
        label="What evidence could change your mind?",
        placeholder="For example: proof that retries are safe and customer accounts stay isolated…",
        rows=2,
    )
    mo.vstack(
        [
            mo.Html(
                """
                <section class="pp-page">
                  <div class="pp-kicker">Opening decision</div>
                  <h2>A green patch is waiting</h2>
                  <p>Northstar Retail asked PatchPilot to repair a bulk-close support workflow. The agent changed one file, passed three visible checks, and submitted the patch for review.</p>
                  <div class="pp-do"><b>Your turn · 2 minutes</b>Choose automatic, review, or block. Then record one piece of evidence that could change your mind.</div>
                </section>
                """
            ),
            initial_decision,
            opening_evidence,
        ]
    )
    return initial_decision, opening_evidence


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">Chapter 1 · Trace the run</div>
          <h2>A trace is the saved receipt for one execution</h2>
          <p>It shows the inputs, outputs, and explicit tool steps that were recorded. It does not prove that the same behavior will be safe on another case, and it does not expose hidden chain-of-thought.</p>
          <div class="pp-guide"><span class="pp-checkpoint">Weave UI stop 1 · Read the trace</span><br>In the Trace view, locate the <b>request</b>, open one recorded <b>action</b>, and find the final <b>output</b>. Then name one claim this single run cannot support.</div>
          <div class="pp-do"><b>Your turn · 4 minutes</b>Run the episode, open its Weave trace, and find: <b>1)</b> what the agent received, <b>2)</b> one action it took, and <b>3)</b> what it returned.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo, participant_role):
    _trace_lens = {
        "support": "Which recorded action could affect customer trust?",
        "risk": "Which safety claim is still unsupported by this one run?",
        "product": "Which customer outcome is directly visible in the trace?",
        "engineering": "Which operation or check would you inspect first?",
    }
    mo.Html(
        f'<div class="pp-panel"><b>Your role lens:</b> {_trace_lens[participant_role.value]}</div>'
    )
    return


@app.cell(hide_code=True)
def _(config_status, mo):
    trace_button = mo.ui.run_button(
        label="Run the saved PP-418 episode",
        disabled=not config_status["ready"],
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
def _(mo):
    observed = mo.ui.text_area(
        label="What did you directly observe?",
        placeholder="I observed that the agent read…",
        rows=3,
    )
    inferred = mo.ui.text_area(
        label="What are you inferring that the trace cannot prove?",
        placeholder="This does not yet prove that…",
        rows=3,
    )
    return inferred, observed


@app.cell(hide_code=True)
def _(inferred, mo, observed, trace_error, trace_receipt):
    import html as _html

    if trace_receipt:
        _result = trace_receipt["result"]
        _status = _html.escape(str(_result["status"]))
        _passed = _html.escape(str(_result["visible_checks"]["passed"]))
        _total = _html.escape(str(_result["visible_checks"]["total"]))
        _trace_url = _html.escape(str(trace_receipt["trace_url"]), quote=True)
        _view = mo.vstack(
            [
                mo.Html(
                    f"""
                    <div class="pp-receipt">
                      <b>Saved run:</b> {_status} · {_passed} of {_total} visible checks passed.<br>
                      <a href="{_trace_url}" target="_blank" rel="noopener noreferrer">Open the exact Weave trace ↗</a>
                    </div>
                    """
                ),
                observed,
                inferred,
            ]
        )
    elif trace_error:
        _view = mo.Html(
            f'<div class="pp-error"><b>The trace did not complete.</b> {_html.escape(trace_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    trace_claims = mo.ui.multiselect(
        options=[
            "The agent read PP-418",
            "Three visible checks ran",
            "The patch was submitted for review",
            "Retries are safe",
            "No other customer can be affected",
            "The workflow will be safe in production",
        ],
        value=[],
        label="Trace challenge: select only the claims this one run directly proves",
    )
    trace_claims
    return (trace_claims,)


@app.cell(hide_code=True)
def _(mo, trace_claims):
    _proven = {
        "The agent read PP-418",
        "Three visible checks ran",
        "The patch was submitted for review",
    }
    _selected = set(trace_claims.value)
    if not _selected:
        _view = mo.Html(
            '<div class="pp-panel amber">Make a selection, then compare what the trace records with what you are assuming.</div>'
        )
    elif _selected == _proven:
        _view = mo.Html(
            '<div class="pp-panel mint"><b>Evidence disciplined.</b> Those three claims are recorded; repeatability, customer isolation, and production safety still require evaluation.</div>'
        )
    else:
        _missed = sorted(_proven - _selected)
        _unsupported = sorted(_selected - _proven)
        _view = mo.Html(
            '<div class="pp-panel rose"><b>Pressure-test the claim.</b><br>'
            + (f"Recorded but not selected: {', '.join(_missed)}.<br>" if _missed else "")
            + (f"Not proven by this run: {', '.join(_unsupported)}." if _unsupported else "")
            + "</div>"
        )
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    _source = "\n".join(
        [
            '@weave.op(name="patchpilot_pp418_saved_episode")',
            "async def replay():",
            '    issue = read_support_issue("PP-418")',
            '    workflow = inspect_workflow("support_workflows/bulk_close.py")',
            "    patch = propose_patch(issue, workflow)",
            "    checks = run_visible_checks(patch)",
            "    return submit_for_review(patch, checks)",
            "",
            "result, call = await replay.call()",
            "trace_url = str(call.ui_url)",
        ]
    )
    mo.vstack(
        [
            mo.Html(
                '<div class="pp-guide"><b>Code walkthrough · tracing</b>The functions decorated with <code>@weave.op</code> become the nested operations you just inspected. The API key is not an operation argument.</div>'
            ),
            mo.md(f"```python\n{_source}\n```"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">Chapter 2 · Test the system</div>
          <h2>One successful run is not a quality claim</h2>
          <p>A dataset is the collection of situations the organization chose to test. This evaluation replays four fixed cases so the room can compare the same evidence under two definitions of acceptable behavior.</p>
          <div class="pp-panel amber"><b>Baseline rubric:</b> Did the workflow change? Did the visible checks pass? Is the patch summary clear?</div>
          <div class="pp-guide"><span class="pp-checkpoint">Facilitator checkpoint</span><br>Walk through the four cases together. Then each participant can choose any case to inspect more closely.</div>
          <div class="pp-do"><b>Your turn · 5 minutes</b>Inspect one case, predict its outcome, and name one important situation this four-case dataset still does not cover.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(core, mo):
    case_choice = mo.ui.dropdown(
        options={row["title"]: row["case_id"] for row in core.load_cases()},
        value="Routine close stays inside the account",
        label="Choose the case you selected or were assigned",
    )
    show_raw_evidence = mo.ui.checkbox(
        label="Show the recorded evidence the judge will receive",
        value=False,
    )
    missing_dataset_case = mo.ui.text_area(
        label="One important situation this dataset still does not cover",
        placeholder="For example: a partial outage occurs after the first write…",
        rows=2,
    )
    mo.vstack(
        [
            case_choice,
            show_raw_evidence,
            missing_dataset_case,
        ]
    )
    return case_choice, missing_dataset_case, show_raw_evidence


@app.cell(hide_code=True)
def _(case_choice, core, json, mo, show_raw_evidence):
    import html as _html

    _cases = {row["case_id"]: row for row in core.load_cases()}
    _case = _cases[case_choice.value]
    _summary = mo.Html(
        f"""
        <div class="pp-panel">
          <b>{_html.escape(str(_case['title']))}</b><br>
          {_html.escape(str(_case['scenario']))}<br><br>
          <b>Risk represented:</b> {_html.escape(str(_case['risk']))}<br>
          <b>Business question:</b> {_html.escape(str(_case['business_question']))}<br><br>
          <span class="pp-small">The expected outcome is deliberately hidden here. Make your call before running the judge.</span>
        </div>
        """
    )
    if show_raw_evidence.value:
        _view = mo.vstack(
            [_summary, mo.md("```json\n" + json.dumps(_case["evidence"], indent=2) + "\n```")]
        )
    else:
        _view = _summary
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    clean_prediction = mo.ui.dropdown(
        options={"Pass": "pass", "Review": "review", "Block": "block"},
        value=None,
        label="Routine close",
    )
    boundary_prediction = mo.ui.dropdown(
        options={"Pass": "pass", "Review": "review", "Block": "block"},
        value=None,
        label="Cross-customer change",
    )
    retry_prediction = mo.ui.dropdown(
        options={"Pass": "pass", "Review": "review", "Block": "block"},
        value=None,
        label="Duplicate retry event",
    )
    missing_prediction = mo.ui.dropdown(
        options={"Pass": "pass", "Review": "review", "Block": "block"},
        value=None,
        label="Evidence missing",
    )
    mo.vstack(
        [
            mo.Html("<h3>Make your call before the judge</h3><p>Predict your assigned case. If you finish early, predict the other three.</p>"),
            mo.hstack([clean_prediction, boundary_prediction], gap=2),
            mo.hstack([retry_prediction, missing_prediction], gap=2),
        ]
    )
    return boundary_prediction, clean_prediction, missing_prediction, retry_prediction


@app.cell(hide_code=True)
def _(boundary_prediction, clean_prediction, missing_prediction, retry_prediction):
    participant_predictions = {
        "clean_success": clean_prediction.value,
        "cross_customer": boundary_prediction.value,
        "duplicate_retry": retry_prediction.value,
        "insufficient_evidence": missing_prediction.value,
    }
    return (participant_predictions,)


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">How the evaluation works</div>
          <h2>A scorer asks one repeatable question</h2>
          <div class="pp-layer">
            <div><b>Deterministic scorer</b><br>Uses fixed logic for facts such as test results, counts, formats, or policy flags.</div>
            <div><b>LLM judge</b><br>Uses a model to interpret recorded evidence against a written rubric.</div>
            <div><b>Human authority</b><br>Decides which signals matter and how much permission the system earns.</div>
          </div>
          <p>This exercise uses an LLM judge as a Weave scorer. A deterministic Python policy then converts criterion statuses into <b>pass</b>, <b>review</b>, or <b>block</b>.</p>
          <div class="pp-guide"><span class="pp-checkpoint">Weave UI stop 2 · Inspect the evaluation</span><br>After the baseline run, open one Evaluation row and follow the chain: <b>dataset case → recorded agent output → scorer call → judge reasons → verdict</b>.</div>
          <div class="pp-do"><b>Before the model runs</b>Apply the baseline rubric to your case yourself. Keep that prediction visible while the judge runs—a judge can apply an incomplete rubric consistently.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _code_walkthrough = "\n".join(
        [
            "### The code that creates the Weave evaluation",
            "",
            "The scorer is defined in Python. Passing it to `weave.Evaluation` is what makes its calls and results inspectable in Weave.",
            "",
            "```python",
            "class BusinessRubricJudge(weave.Scorer):",
            "    model_id: str",
            "    rubric: dict",
            "",
            '    @weave.op(name="patchpilot_business_rubric_judge")',
            "    async def score(self, output, case_id, scenario, evidence):",
            "        response = await self._client.chat.completions.create(",
            "            model=self.model_id,",
            "            messages=build_judge_messages(",
            "                rubric=self.rubric,",
            "                output=output,",
            "                scenario=scenario,",
            "                evidence=evidence,",
            "            ),",
            "        )",
            "        return normalize_judgment(response, self.rubric)",
            "",
            "judge = BusinessRubricJudge(",
            "    model_id=PATCHPILOT_JUDGE_MODEL,",
            "    rubric=baseline_rubric,",
            ")",
            "",
            "evaluation = weave.Evaluation(",
            "    dataset=cases,",
            "    scorers=[judge],",
            ")",
            "await evaluation.evaluate(recorded_agent)",
            "```",
            "",
            "**What can change?** The model and scorer implementation can be changed in Python before a run. In this live workshop, the model stays fixed and you change the rubric text and its severity—enough to demonstrate how an LLM judge's instructions alter the evaluation without turning the session into a coding exercise.",
        ]
    )
    mo.md(_code_walkthrough)
    return


@app.cell(hide_code=True)
def _(config_status, mo):
    baseline_button = mo.ui.run_button(
        label="Run the baseline four-case evaluation",
        disabled=not config_status["ready"],
    )
    baseline_button
    return (baseline_button,)


@app.cell(hide_code=True)
async def _(baseline_button, core):
    baseline_error = ""
    baseline_result = None
    if baseline_button.value:
        try:
            baseline_result = await core.run_evaluation(core.load_rubrics()["baseline"])
        except Exception as error:
            baseline_error = core.safe_error_text(error)
    return baseline_error, baseline_result


@app.cell(hide_code=True)
def _(baseline_error, baseline_result, core, mo, participant_predictions):
    import html as _html

    def _md_cell(value):
        return (
            _html.escape(str(value), quote=False)
            .replace("|", "\\|")
            .replace("\n", " ")
        )

    if baseline_result:
        _cases = {row["case_id"]: row for row in core.load_cases()}
        _lines = [
            "| Case | Your call | Baseline judge | Human reference |",
            "|---|---:|---:|---:|",
        ]
        for _row in baseline_result["results"]:
            _verdict = _row["verdict"].upper()
            _prediction = (participant_predictions[_row["case_id"]] or "not chosen").upper()
            _reference = _cases[_row["case_id"]]["expected_outcome"].upper()
            _lines.append(
                f"| {_md_cell(_cases[_row['case_id']]['title'])} | {_md_cell(_prediction)} | **{_md_cell(_verdict)}** | {_md_cell(_reference)} |"
            )
        _judge_model = _html.escape(str(baseline_result["judge_model"]))
        _evaluation_url = _html.escape(
            str(baseline_result["evaluation_url"]), quote=True
        )
        _view = mo.vstack(
            [
                mo.Html(
                    f"""<div class="pp-receipt"><b>Baseline evaluation saved.</b> Four judge calls used
                    <code>{_judge_model}</code>. <a href="{_evaluation_url}" target="_blank" rel="noopener noreferrer">Open it in Weave ↗</a></div>"""
                ),
                mo.md("\n".join(_lines)),
                mo.Html(
                    '<div class="pp-panel rose"><b>The green illusion:</b> a rubric can be applied consistently and still omit the business failure that matters. The human reference is a comparison point—not an answer the judge is forced to produce.</div>'
                ),
            ]
        )
    elif baseline_error:
        _view = mo.Html(
            f'<div class="pp-error"><b>The baseline evaluation did not complete.</b> {_html.escape(baseline_error)}</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(core, mo):
    judge_case_choice = mo.ui.dropdown(
        options={row["title"]: row["case_id"] for row in core.load_cases()},
        value="Routine close stays inside the account",
        label="Choose one evaluation row to inspect deeply",
    )
    judge_agreement = mo.ui.radio(
        options={
            "I agree with the judge's application of this rubric": "agree",
            "I disagree with how the judge applied the rubric": "disagree",
            "The evidence is not sufficient to decide": "insufficient",
        },
        value="The evidence is not sufficient to decide",
        label="After inspecting the row, what is your assessment?",
    )
    disagreement_layer = mo.ui.dropdown(
        options={
            "The dataset or recorded evidence": "evidence",
            "The rubric wording": "rubric",
            "The LLM judge's interpretation": "judge",
            "The pass/review/block policy": "policy",
        },
        value="The rubric wording",
        label="If the outcome surprises you, which layer should the team inspect first?",
    )
    mo.vstack([judge_case_choice, judge_agreement, disagreement_layer])
    return disagreement_layer, judge_agreement, judge_case_choice


@app.cell(hide_code=True)
def _(baseline_result, core, judge_case_choice, mo):
    import html as _html

    def _md_cell(value):
        return (
            _html.escape(str(value), quote=False)
            .replace("|", "\\|")
            .replace("\n", " ")
        )

    if baseline_result:
        _cases = {row["case_id"]: row for row in core.load_cases()}
        _judgments = {row["case_id"]: row for row in baseline_result["results"]}
        _case = _cases[judge_case_choice.value]
        _judgment = _judgments[judge_case_choice.value]
        _criteria_lines = [
            "| Criterion | Judge status | Judge reason |",
            "|---|---:|---|",
        ]
        for _criterion in _judgment["criteria"]:
            _criteria_lines.append(
                f"| {_md_cell(_criterion['label'])} | **{_md_cell(_criterion['status'].upper())}** | {_md_cell(_criterion['reason'])} |"
            )
        _case_title = _html.escape(str(_case["title"]))
        _reference = _html.escape(str(_case["expected_outcome"]).upper())
        _reference_reason = _html.escape(str(_case["reference_reason"]))
        _judge_verdict = _html.escape(str(_judgment["verdict"]).upper())
        _judge_rationale = _html.escape(str(_judgment["rationale"]))
        _view = mo.vstack(
            [
                mo.Html(
                    f"""
                    <section class="pp-page">
                      <div class="pp-kicker">Inspect the judge—not just the label</div>
                      <h2>{_case_title}</h2>
                      <div class="pp-panel"><b>Business reference:</b> {_reference} — {_reference_reason}</div>
                      <div class="pp-do"><b>Your turn · 4 minutes</b>Open this row in Weave. Compare the recorded evidence, each rubric criterion, the judge's reason, and the final verdict.</div>
                    </section>
                    """
                ),
                mo.md("\n".join(_criteria_lines)),
                mo.Html(
                    f'<div class="pp-receipt"><b>Judge verdict:</b> {_judge_verdict}<br><b>Judge rationale:</b> {_judge_rationale}</div>'
                ),
                mo.Html(
                    '<div class="pp-guide"><b>Diagnose before changing anything.</b>If you disagree, identify the layer to inspect first: evidence, rubric, judge interpretation, or verdict policy.</div>'
                ),
            ]
        )
    else:
        _view = mo.Html(
            '<div class="pp-guide">Run the baseline evaluation before inspecting a judge result.</div>'
        )
    _view
    return


@app.cell(hide_code=True)
def _(core, mo):
    rule_focus = mo.ui.dropdown(
        options=core.SUGGESTED_BUSINESS_RULES,
        value="Customer isolation",
        label="Choose a business boundary to start from",
    )
    rule_focus
    return (rule_focus,)


@app.cell(hide_code=True)
def _(mo, rule_focus):
    business_rule = mo.ui.text_area(
        label="Write or revise one atomic business rule",
        value=rule_focus.value,
        rows=3,
    )
    rule_severity = mo.ui.radio(
        options={
            "Block release when the rule fails": "block",
            "Route the result to human review": "review",
        },
        value="Block release when the rule fails",
        label="Choose the severity of this rule",
    )
    return business_rule, rule_severity


@app.cell(hide_code=True)
def _(business_rule, mo, participant_role, rule_severity):
    _rule_lens = {
        "support": "Would support teams understand exactly when this rule was violated?",
        "risk": "Does the rule name one unacceptable outcome without ambiguity?",
        "product": "Does the rule protect the customer outcome without blocking unrelated value?",
        "engineering": "Could the team later implement a protected deterministic check for this rule?",
    }
    mo.vstack(
        [
            mo.Html(
                """
                <section class="pp-page">
                  <div class="pp-kicker">Chapter 3 · Define good</div>
                  <h2>Change the judge by changing its instructions</h2>
                  <p>The scorer code and model stay fixed for this run. You change the judge's rubric: the outcome it must protect, the boundary it must test, and the consequence of failure.</p>
                  <div class="pp-guide"><span class="pp-checkpoint">Facilitator checkpoint</span><br>A strong rule names <b>one outcome</b>, the <b>boundary</b>, the evidence that could establish it, and what happens when it fails or remains unknown.</div>
                  <div class="pp-do"><b>Your turn · 6 minutes</b>Choose one boundary, make the rule atomic, select review or block, and inspect the compiled rubric before rerunning the evaluation.</div>
                </section>
                """
            ),
            mo.Html(f'<div class="pp-panel"><b>Your role lens:</b> {_rule_lens[participant_role.value]}</div>'),
            business_rule,
            rule_severity,
            mo.Html(
                '<div class="pp-guide"><b>Rule self-check</b>Can a reader identify the protected outcome, prohibited behavior, evidence, and severity without asking what you meant?</div>'
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(business_rule, core, rule_severity):
    revised_rubric_error = ""
    revised_rubric = None
    try:
        revised_rubric = core.build_revised_rubric(business_rule.value)
        if rule_severity.value == "review":
            for _criterion in revised_rubric["criteria"]:
                if _criterion["id"] == "business_boundary":
                    _criterion["blocking"] = False
    except Exception as error:
        revised_rubric_error = str(error)
    return revised_rubric, revised_rubric_error


@app.cell(hide_code=True)
def _(mo, revised_rubric, revised_rubric_error):
    import html as _html
    import json as _json

    if revised_rubric:
        _criteria = "".join(
            "<li>"
            f"<b>{'BLOCKING' if row['blocking'] else 'Supporting'}</b> — "
            f"{_html.escape(str(row['label']))}"
            "</li>"
            for row in revised_rubric["criteria"]
        )
        _rubric_json = _json.dumps(revised_rubric, indent=2)
        _view = mo.vstack(
            [
                mo.Html(
                    '<div class="pp-guide"><b>What the scorer will receive</b>Your notebook control has been compiled into a structured rubric. This object becomes part of the LLM judge prompt and is saved with the scorer configuration in Weave.</div>'
                ),
                mo.Html(f"<ul>{_criteria}</ul>"),
                mo.md(f"```json\n{_rubric_json}\n```"),
            ]
        )
    else:
        _view = mo.Html(
            f'<div class="pp-error">{_html.escape(revised_rubric_error)}</div>'
        )
    _view
    return


@app.cell(hide_code=True)
def _(config_status, mo, revised_rubric):
    revised_button = mo.ui.run_button(
        label="Run the revised evaluation",
        disabled=(not config_status["ready"] or revised_rubric is None),
    )
    revised_button
    return (revised_button,)


@app.cell(hide_code=True)
async def _(core, revised_button, revised_rubric):
    revised_error = ""
    revised_result = None
    if revised_button.value and revised_rubric is not None:
        try:
            revised_result = await core.run_evaluation(revised_rubric)
        except Exception as error:
            revised_error = core.safe_error_text(error)
    return revised_error, revised_result


@app.cell(hide_code=True)
def _(baseline_result, core, mo, participant_predictions, revised_error, revised_result):
    import html as _html

    def _md_cell(value):
        return (
            _html.escape(str(value), quote=False)
            .replace("|", "\\|")
            .replace("\n", " ")
        )

    if baseline_result and revised_result:
        _rows = core.compare_evaluations(baseline_result, revised_result)
        _cases = {row["case_id"]: row for row in core.load_cases()}
        _lines = [
            "| Case | Your call | Baseline | Revised | Reference | Changed? |",
            "|---|---:|---:|---:|---:|:---:|",
        ]
        for _row in _rows:
            _prediction = (participant_predictions[_row["case_id"]] or "not chosen").upper()
            _reference = _cases[_row["case_id"]]["expected_outcome"].upper()
            _lines.append(
                f"| {_md_cell(_row['case'])} | {_md_cell(_prediction)} | **{_md_cell(_row['baseline'].upper())}** | **{_md_cell(_row['revised'].upper())}** | {_md_cell(_reference)} | {_md_cell(_row['changed'])} |"
            )
        _evaluation_url = _html.escape(
            str(revised_result["evaluation_url"]), quote=True
        )
        _view = mo.vstack(
            [
                mo.Html(
                    f"""<div class="pp-receipt"><b>Revised evaluation saved.</b> The same four agent outputs were judged again.
                    <a href="{_evaluation_url}" target="_blank" rel="noopener noreferrer">Open it in Weave ↗</a></div>"""
                ),
                mo.Html(
                    '<div class="pp-guide"><span class="pp-checkpoint">Weave UI stop 3 · Compare and diagnose</span><br>Keep the dataset and agent output fixed. Compare baseline with revised, then decide whether an unexpected result belongs to the <b>evidence</b>, <b>rubric</b>, <b>judge interpretation</b>, or <b>verdict policy</b>.</div>'
                ),
                mo.md("\n".join(_lines)),
                mo.Html(
                    '<div class="pp-panel mint"><b>The agent did not change.</b> The organization changed what it was willing to accept.</div>'
                ),
                mo.Html(
                    '<div class="pp-do"><b>Your turn · 3 minutes</b>Find one intended change and one result that surprised you or stayed unchanged. If a verdict differs from the human reference, inspect the scorer call before changing the answer.</div>'
                ),
            ]
        )
    elif revised_error:
        _view = mo.Html(
            f'<div class="pp-error"><b>The revised evaluation did not complete.</b> {_html.escape(revised_error)}</div>'
        )
    elif revised_result:
        _view = mo.Html(
            '<div class="pp-panel amber">The revised evaluation is ready. Run the baseline evaluation to see the comparison.</div>'
        )
    else:
        _view = mo.Html("")
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    _policy_source = "\n".join(
        [
            'if any(row["blocking"] and row["status"] == "fail" for row in criteria):',
            '    verdict = "block"',
            'elif any(row["status"] in {"fail", "unknown"} for row in criteria):',
            '    verdict = "review"',
            "else:",
            '    verdict = "pass"',
        ]
    )
    mo.vstack(
        [
            mo.Html(
                '<div class="pp-guide"><b>Code walkthrough · deterministic policy</b>The LLM returns criterion statuses and reasons. This fixed Python reducer—not the model—turns those statuses into the final pass, review, or block verdict.</div>'
            ),
            mo.md(f"```python\n{_policy_source}\n```"),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    final_decision = mo.ui.radio(
        options={
            "Allow automatic operation inside a narrow scope": "automatic",
            "Require human review": "review",
            "Keep the agent blocked": "block",
        },
        value="Require human review",
        label="After the evidence, what authority has PatchPilot earned?",
    )
    permitted_scope = mo.ui.text_area(
        label="Permitted scope",
        placeholder="For example: draft changes only; no deployment authority…",
        rows=2,
    )
    missing_evidence = mo.ui.text_area(
        label="Evidence still missing",
        placeholder="For example: protected regression tests and production review outcomes…",
        rows=2,
    )
    human_checkpoint = mo.ui.text_area(
        label="Where is human approval required?",
        placeholder="For example: a support engineer approves every proposed patch",
        rows=2,
    )
    stop_condition = mo.ui.text_area(
        label="What measurable event stops the system?",
        placeholder="For example: any cross-customer write or duplicate audit event",
        rows=2,
    )
    stop_owner = mo.ui.text(
        label="Who can stop the system?",
        placeholder="Named role or team",
    )
    return final_decision, human_checkpoint, missing_evidence, permitted_scope, stop_condition, stop_owner


@app.cell(hide_code=True)
def _(
    final_decision,
    human_checkpoint,
    missing_evidence,
    mo,
    participant_role,
    permitted_scope,
    stop_condition,
    stop_owner,
):
    _authority_lens = {
        "support": "Can the support organization operate this boundary during a high-volume event?",
        "risk": "Are the stop condition and accountable owner explicit?",
        "product": "Is the permitted scope narrow enough to earn trust while delivering value?",
        "engineering": "Can the human checkpoint and stop condition be implemented and monitored?",
    }
    mo.vstack(
        [
            mo.Html(
                """
                <section class="pp-page">
                  <div class="pp-kicker">Chapter 4 · Bound the authority</div>
                  <h2>Make the decision the evidence can support</h2>
                  <p>Use this sentence to prepare your decision: <b>“The evidence supports ___, but it does not yet prove ___.”</b></p>
                  <div class="pp-guide"><span class="pp-checkpoint">Facilitator checkpoint</span><br>The evaluation informs the decision. It does not grant authority. A person still sets scope, review, stop conditions, and ownership.</div>
                  <div class="pp-do"><b>Your turn · 5 minutes</b>Choose the smallest defensible authority and complete the operating boundary below.</div>
                </section>
                """
            ),
            mo.Html(f'<div class="pp-panel"><b>Your role lens:</b> {_authority_lens[participant_role.value]}</div>'),
            final_decision,
            permitted_scope,
            missing_evidence,
            human_checkpoint,
            stop_condition,
            stop_owner,
        ]
    )
    return


@app.cell(hide_code=True)
def _(
    final_decision,
    human_checkpoint,
    initial_decision,
    missing_evidence,
    mo,
    opening_evidence,
    permitted_scope,
    stop_condition,
    stop_owner,
):
    import html as _html

    _complete = bool(
        permitted_scope.value.strip()
        and missing_evidence.value.strip()
        and human_checkpoint.value.strip()
        and stop_condition.value.strip()
        and stop_owner.value.strip()
    )
    if _complete:
        _initial = _html.escape(str(initial_decision.value).upper())
        _final = _html.escape(str(final_decision.value).upper())
        _scope = _html.escape(permitted_scope.value)
        _opening = _html.escape(opening_evidence.value or "Not recorded")
        _missing = _html.escape(missing_evidence.value)
        _checkpoint = _html.escape(human_checkpoint.value)
        _stop = _html.escape(stop_condition.value)
        _owner = _html.escape(stop_owner.value)
        _view = mo.Html(
            f"""
            <section class="pp-page">
              <div class="pp-kicker">Your decision receipt</div>
              <h2>{_initial} → {_final}</h2>
              <div class="pp-panel mint">
                <b>Permitted scope:</b> {_scope}<br><br>
                <b>Evidence that could change my mind:</b> {_opening}<br><br>
                <b>Still missing:</b> {_missing}<br><br>
                <b>Human checkpoint:</b> {_checkpoint}<br><br>
                <b>Stop condition:</b> {_stop}<br><br>
                <b>Stop authority:</b> {_owner}
              </div>
              <div class="pp-guide"><b>Defend the boundary</b>Use this receipt if you are invited to explain your decision: “The evidence supports ___, but it does not yet prove ___. Therefore, PatchPilot may ___, with human review at ___, and it stops when ___.”</div>
            </section>
            """
        )
    else:
        _view = mo.Html(
            '<div class="pp-panel amber">Complete the five operating-boundary fields to create your decision receipt.</div>'
        )
    _view
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="pp-page">
          <div class="pp-kicker">What you can now ask your team</div>
          <h2>Evidence before authority</h2>
          <p><b>1.</b> Show me what the agent did.</p>
          <p><b>2.</b> Show me the cases used to test it.</p>
          <p><b>3.</b> Show me how “good” is defined.</p>
          <p><b>4.</b> Show me who can limit or stop it.</p>
          <p><b>5.</b> Show me what change makes us test it again.</p>
          <div class="pp-rail">TRACE THE RUN &nbsp;→&nbsp; TEST THE SYSTEM &nbsp;→&nbsp; DEFINE GOOD &nbsp;→&nbsp; BOUND THE AUTHORITY</div>
        </section>
        """
    )
    return


if __name__ == "__main__":
    app.run()
