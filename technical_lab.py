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
# on_cell_change = "autorun"
# ///
"""Standalone technical Agent Loop Workshop with a live, bounded AI agent."""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import html
    import json
    from copy import deepcopy
    from pathlib import Path
    from typing import Any

    import marimo as mo
    import weave
    from dotenv import load_dotenv

    local_env = Path(__file__).with_name(".env")
    load_dotenv(local_env if local_env.exists() else None, override=True)
    import technical_lab_core as lab
    import workshop_core as core

    return Any, core, deepcopy, html, json, lab, mo, weave


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <style>
          :root { --ink:#111827; --muted:#64748b; --line:#d8dee8; --blue:#2563eb; --amber:#d97706; --mint:#0f9f86; --rose:#b84735; }
          .lab-page { padding:1.1rem 0 .7rem; color:var(--ink); }
          .lab-page h1 { font-size:2.5rem; line-height:1.05; margin:.45rem 0 1rem; }
          .lab-page h2 { font-size:1.7rem; line-height:1.15; margin:.35rem 0 .65rem; }
          .lab-page h3 { font-size:1.25rem; margin:.35rem 0 .55rem; }
          .lab-page p, .lab-page li { font-size:1.01rem; line-height:1.55; }
          .lab-kicker { color:var(--rose); font-size:.78rem; font-weight:850; letter-spacing:.09em; text-transform:uppercase; }
          .lab-rail { border-top:2px solid var(--line); border-bottom:2px solid var(--line); padding:.75rem 0; margin:1rem 0; color:var(--muted); font-weight:750; }
          .lab-panel { border-left:8px solid var(--blue); background:#f7f9fc; padding:1rem 1.15rem; margin:1rem 0; }
          .lab-panel.amber { border-color:var(--amber); }
          .lab-panel.mint { border-color:var(--mint); }
          .lab-panel.rose { border-color:var(--rose); }
          .lab-do { border:2px solid #bfd2f5; background:#f7faff; padding:.9rem 1rem; margin:.9rem 0; }
          .lab-receipt { background:#eef8f5; border:1px solid #b9e2d9; padding:.9rem 1rem; margin:.9rem 0; }
          .lab-error { background:#fff2ef; border:1px solid #efc0b7; padding:.9rem 1rem; margin:.9rem 0; color:#842f23; }
          .lab-small { color:var(--muted); font-size:.91rem; }
          table { font-size:.91rem; }
        </style>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <header class="lab-page">
          <div class="lab-kicker">Standalone technical workshop · 90 minutes</div>
          <h1>Build, trace, and improve a live AI agent</h1>
          <p>PatchPilot is a bounded coding agent for BeeVerse Market. You will inspect a weak live-agent trace, add safety evidence tools, extend the evaluation dataset, write a deterministic scorer, compare two agent policies in W&amp;B Weave, and make a release decision.</p>
          <div class="lab-rail">OBSERVE → HYPOTHESIZE → BUILD → TRACE → EVALUATE → COMPARE → DECIDE</div>
          <div class="lab-panel amber"><b>Cost and variability</b><br>The core path makes 21 hosted model calls: one baseline agent call, ten agent calls across two evaluations, and ten LLM-judge calls. Live tool selection and judge verdicts can vary; uncertainty is recorded instead of hidden. If V3 skips both participant-built safety tools, one clearly labeled optional retry adds one model call.</div>
          <p class="lab-small">This is the single technical workshop. Four focused Python editors are embedded directly in the lab; notebook plumbing stays out of the participant path. Credentials stay in the local <code>.env</code>; never paste an API key into an editor, trace, dataset row, tool argument, or prompt.</p>
        </header>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html(
        """
        <section class="lab-page">
          <div class="lab-kicker">Start here · 0–10 minutes</div>
          <h2>The two loops you are learning</h2>
          <div class="lab-panel"><b>Inner agent loop</b><br>Model chooses tools → validated dispatcher runs safe tools → evidence becomes the agent output → Weave records the call tree.</div>
          <div class="lab-panel mint"><b>Outer improvement loop</b><br>Trace reveals a weakness → dataset captures it → scorers make the expectation executable → the fixed evaluation contract compares agent policies → a human decides.</div>
          <h3>By the end, you can</h3>
          <ul>
            <li>Read a nested agent trace and distinguish model intent from tool evidence.</li>
            <li>Turn a trace-derived failure into a dataset case and deterministic scorer.</li>
            <li>Compare live applications while holding the evaluation contract fixed.</li>
            <li>Handle missing tools, malformed calls, and model variability without silently passing.</li>
          </ul>
          <div class="lab-panel amber"><b>Safety boundary</b><br>The model can call only three in-memory workshop functions. It cannot run a shell, edit files, access credentials, or operate BeeVerse systems.</div>
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    _loop_code = mo.ui.code_editor(
        value="""response = await model.choose_tools(prompt, tools=allowlist)

for call in response.tool_calls:
    arguments = validate_json(call.arguments)
    handler = registered_handlers.get(call.name)
    receipts[call.name] = handler(request, application, arguments)

output = assemble_agent_output(receipts)
# Weave traces the agent, inference, tools, scorers, and judge.""",
        language="python",
        disabled=True,
        min_height=220,
        max_height=320,
        label="Bounded agent-loop sketch",
    )
    mo.accordion({"Inspect the bounded agent loop": _loop_code})
    return


@app.cell(hide_code=True)
def _(core):
    lab_config_status = core.configuration_status()
    return (lab_config_status,)


@app.cell(hide_code=True)
def _(lab_config_status, mo):
    lab_preflight_button = mo.ui.run_button(
        label="Verify W&B and Weave access · no model call",
        disabled=not lab_config_status["ready"],
    )
    lab_preflight_button
    return (lab_preflight_button,)


@app.cell(hide_code=True)
async def _(core, lab, lab_preflight_button):
    lab_preflight_error = ""
    lab_preflight_receipt = None
    if lab_preflight_button.value:
        try:
            lab_preflight_receipt = await lab.verify_technical_connection()
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
    if not lab_config_status["ready"]:
        _title, _tone = "Setup incomplete", "rose"
    elif lab_preflight_receipt:
        _title, _tone = "W&B and Weave connection verified", "mint"
    elif lab_preflight_error:
        _title, _tone = "Connection not verified", "rose"
    else:
        _title, _tone = "Local setup found—connection not tested", "amber"
    _missing = ", ".join(lab_config_status["missing"]) or "none"
    _invalid = "; ".join(lab_config_status["invalid"]) or "none"
    _detail = ""
    if lab_preflight_receipt:
        _url = html.escape(lab_preflight_receipt["project_url"], quote=True)
        _detail = (
            '<div class="lab-receipt"><b>Weave is ready.</b> '
            f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
            "Open the project in Weave ↗</a><br>"
            '<span class="lab-small">The next exercise tests live model access '
            "with the first counted agent call.</span></div>"
        )
    elif lab_preflight_error:
        _safe = lab_preflight_error
        _detail = (
            '<div class="lab-error"><b>Connection failed.</b> '
            f"{html.escape(_safe)}<br><b>Next step:</b> "
            f"{html.escape(core.connection_error_guidance(RuntimeError(_safe)))}</div>"
        )
    mo.Html(
        f"""
        <section class="lab-page">
          <div class="lab-kicker">Preflight</div>
          <h2>{_title}</h2>
          <div class="lab-panel {_tone}">
            Entity: <code>{html.escape(lab_config_status['entity'])}</code><br>
            Project: <code>{html.escape(lab_config_status['project'])}</code><br>
            Agent and judge model: <code>{html.escape(lab_config_status['judge_model'])}</code><br>
            Missing: {html.escape(_missing)}<br>Invalid: {html.escape(_invalid)}
          </div>
          {_detail}
        </section>
        """
    )
    return


@app.cell(hide_code=True)
def _(lab_preflight_receipt):
    lab_connection_verified = lab_preflight_receipt is not None
    return (lab_connection_verified,)


@app.cell(hide_code=True)
def _(core, lab, lab_config_status):
    baseline_case = next(
        row
        for row in core.workshop_dataset_rows()
        if row["case_id"] == "missing_evidence"
    )
    baseline_v2_agent = lab.build_live_agent(
        "v2", model_id=lab_config_status["judge_model"]
    )
    return baseline_case, baseline_v2_agent


@app.cell(hide_code=True)
def _(mo):
    confirm_baseline_call = mo.ui.checkbox(
        label="Run one live V2 planning and tool-selection call"
    )
    return (confirm_baseline_call,)


@app.cell(hide_code=True)
def _(confirm_baseline_call, lab_connection_verified, mo):
    run_baseline_button = mo.ui.run_button(
        label="Run V2 on the missing-evidence case · 1 model call",
        disabled=not (lab_connection_verified and confirm_baseline_call.value),
    )
    mo.vstack(
        [
            mo.Html(
                """
                <section class="lab-page">
                  <div class="lab-kicker">Observe · 10–20 minutes</div>
                  <h2>Run the weak policy before changing anything</h2>
                  <p>V2 can prepare the tenant-scoped patch, but it has no active safety-evidence tools. The live model decides which available function to request. Weave records the model call, tool execution, and assembled output.</p>
                  <div class="lab-do"><b>Your turn</b><br>Run the case, then open its trace. Model access is verified by this real agent call—not by a throwaway preflight prompt.</div>
                </section>
                """
            ),
            confirm_baseline_call,
            run_baseline_button,
        ]
    )
    return (run_baseline_button,)


@app.cell(hide_code=True)
async def _(baseline_case, baseline_v2_agent, core, lab, run_baseline_button):
    baseline_error = ""
    baseline_trace = None
    if run_baseline_button.value:
        try:
            baseline_trace = await lab.run_single_case_trace(
                baseline_v2_agent, baseline_case
            )
        except Exception as error:
            baseline_error = core.safe_error_text(error)
    return baseline_error, baseline_trace


@app.cell(hide_code=True)
def _(core, html, baseline_error, baseline_trace, mo):
    if baseline_trace:
        _url = html.escape(baseline_trace["trace_url"], quote=True)
        _result = baseline_trace["result"]
        _tools = ", ".join(_result.get("executed_tools", [])) or "none"
        _view = mo.Html(
            f'<div class="lab-receipt"><b>Live V2 trace complete.</b> '
            f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
            f'Open the nested trace in Weave ↗</a><br>Executed tools: '
            f'<code>{html.escape(_tools)}</code><br>Customer evidence: '
            f'<b>{html.escape(str(_result.get("customer_account_evidence_available")))}</b> · '
            f'Retry evidence: <b>{html.escape(str(_result.get("retry_evidence_available")))}</b></div>'
        )
    elif baseline_error:
        _safe = baseline_error
        _view = mo.Html(
            f'<div class="lab-error"><b>The live V2 trace did not complete.</b> '
            f'{html.escape(_safe)}<br><b>Next step:</b> '
            f'{html.escape(core.connection_error_guidance(RuntimeError(_safe)))}</div>'
        )
    else:
        _view = mo.md("")
    _view
    return


@app.cell(hide_code=True)
def _(baseline_trace, mo):
    failure_hypothesis = mo.ui.text(
        value="V2 cannot actively collect missing customer-boundary and retry evidence.",
        label="Failure hypothesis",
        full_width=True,
    )
    predicted_metric = mo.ui.dropdown(
        options={
            "Evidence completeness should improve": "evidence_completeness",
            "Customer isolation should improve": "customer_isolation",
            "Retry safety should improve": "retry_safety",
        },
        value="Evidence completeness should improve",
        label="Metric you expect to move",
    )
    mo.vstack(
        [
            mo.Html(
                """
                <section class="lab-page">
                  <div class="lab-kicker">Hypothesize · 20–30 minutes</div>
                  <h2>Turn the trace into an engineering claim</h2>
                  <div class="lab-do"><b>Weave trace hunt</b><br>Find the parent agent Call, the automatically traced inference Call, the requested function name, the executed tool Call, the final output, latency, and token usage. Then write the smallest change you expect to improve one measurable result.</div>
                </section>
                """
            ),
            failure_hypothesis,
            predicted_metric,
            mo.md(
                "Trace ready—record your hypothesis before coding."
                if baseline_trace
                else "Run the baseline trace first so the hypothesis is evidence-based."
            ),
        ]
    )
    return failure_hypothesis, predicted_metric


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 1: capture the failure as a dataset case

    The new row requires customer-account and retry evidence but deliberately
    supplies only passive customer-account evidence. Edit the Python literal in
    the focused editor; the lab parses literals only and never executes this text.
    Replace both TODOs so the case captures the boundary revealed by the trace.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    fifth_case_default_source = '''fifth_case = {
    "case_id": "TODO",
    "title": "Only part of the safety evidence was recorded",
    "source_type": "synthetic",
    "risk": "Evidence completeness",
    "scenario": "Customer evidence exists, but the retry path was not exercised.",
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
        "required_evidence": [],  # TODO: require both evidence categories
    },
}'''
    _editor = mo.ui.code_editor(
        value=fifth_case_default_source,
        language="python",
        min_height=500,
        max_height=680,
        label="Your Python: add the fifth evaluation case",
    )
    fifth_case_form = _editor.form(submit_button_label="Check dataset case")
    fifth_case_form
    return fifth_case_default_source, fifth_case_form


@app.cell(hide_code=True)
def _(core, fifth_case_default_source, fifth_case_form, lab):
    fifth_case_error = ""
    try:
        fifth_case = lab.parse_literal_assignment(
            fifth_case_form.value or fifth_case_default_source,
            "fifth_case",
            dict,
        )
    except ValueError as error:
        fifth_case = {}
        fifth_case_error = str(error)
    lab_rows = [*core.workshop_dataset_rows()]
    if fifth_case:
        lab_rows.append(fifth_case)
    return fifth_case, fifth_case_error, lab_rows


@app.cell(hide_code=True)
def _(fifth_case, lab):
    fifth_case_check = lab.validate_fifth_case(fifth_case)
    return (fifth_case_check,)


@app.cell(hide_code=True)
def _(core, fifth_case_check, fifth_case_error, lab_rows, mo):
    _lines = ["| Dataset checkpoint | Result |", "|---|---:|"]
    for _check in fifth_case_check["checks"]:
        _lines.append(
            f"| {_check['check']} | {'PASS' if _check['passed'] else 'FIX'} |"
        )
    _titles = "\n".join(f"- **{row['title']}**" for row in lab_rows)
    _parse_result = (
        mo.Html(f'<div class="lab-error"><b>Fix the Python literal</b><br>{fifth_case_error}</div>')
        if fifth_case_error
        else mo.Html('<div class="lab-receipt"><b>Literal parsed safely.</b> No participant text was executed.</div>')
    )
    mo.vstack(
        [
            _parse_result,
            mo.md("### Dataset checkpoint"),
            mo.md("\n".join(_lines)),
            mo.md(
                f"### Five-case evaluation dataset\n\n{_titles}\n\n"
                f"Fingerprint: `{core.dataset_fingerprint(lab_rows)}`"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 2: implement the bounded tool dispatcher

    The model returns requested function names and JSON arguments; your Python
    decides what actually executes. Complete the TODOs so the dispatcher records
    intent, enforces the allowlist, rejects duplicates, contains malformed JSON,
    and calls only registered handlers. Five fixtures exercise the safety boundary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    dispatcher_default_source = '''def dispatch_tool_calls(
    tool_calls,
    allowed_tool_names,
    handlers,
    request,
    application,
):
    requested_tools = []
    receipts = {}
    invalid_tool_calls = []

    if not tool_calls:
        invalid_tool_calls.append("no_tool_calls_returned")

    for call in tool_calls:
        name = str(call.get("name", ""))
        requested_tools.append(name or "<missing-name>")

        # TODO 1: reject names outside allowed_tool_names.
        # Record: unknown_tool:<name>, then continue.

        # TODO 2: reject a duplicate name already in receipts.
        # Record: duplicate_tool:<name>, then continue.

        handler = handlers.get(name)
        # TODO 3: reject a missing handler.
        # Record: unregistered_tool:<name>, then continue.

        # TODO 4: parse call["arguments"] with json.loads.
        # Require an empty dict, execute the handler, and store its receipt.
        # Contain ValueError/TypeError as invalid_arguments:<name>.

    return {
        "requested_tools": requested_tools,
        "receipts": receipts,
        "invalid_tool_calls": invalid_tool_calls,
    }'''
    _editor = mo.ui.code_editor(
        value=dispatcher_default_source,
        language="python",
        min_height=660,
        max_height=820,
        label="Your Python: complete dispatch_tool_calls",
    )
    dispatcher_form = _editor.form(submit_button_label="Run dispatcher fixtures")
    mo.vstack(
        [
            mo.Html(
                '<div class="lab-do"><b>Contract</b><br>Return '
                '<code>requested_tools</code>, <code>receipts</code>, and '
                '<code>invalid_tool_calls</code>. Never execute an unknown, '
                'duplicate, unregistered, or malformed call.</div>'
            ),
            dispatcher_form,
        ]
    )
    return dispatcher_default_source, dispatcher_form


@app.cell(hide_code=True)
def _(dispatcher_default_source, dispatcher_form, json, lab):
    dispatcher_compile_error = ""
    try:
        _compiled = lab.compile_participant_functions(
            dispatcher_form.value or dispatcher_default_source,
            ["dispatch_tool_calls"],
            allowed_globals={"json": json},
        )
        participant_dispatcher = _compiled["dispatch_tool_calls"]
    except ValueError as error:
        dispatcher_compile_error = str(error)

        def participant_dispatcher(*_args):
            return {
                "requested_tools": [],
                "receipts": {},
                "invalid_tool_calls": ["dispatcher_not_loaded"],
            }

    dispatcher_check = lab.validate_dispatcher(participant_dispatcher)
    return dispatcher_check, dispatcher_compile_error, participant_dispatcher


@app.cell(hide_code=True)
def _(dispatcher_check, dispatcher_compile_error, html, mo):
    _lines = ["| Dispatcher fixture | Result | Detail |", "|---|---:|---|"]
    for _row in dispatcher_check["rows"]:
        _lines.append(
            f"| {_row['fixture']} | {'PASS' if _row['passed'] else 'FIX'} | "
            f"{_row['detail']} |"
        )
    _status = (
        mo.Html(
            '<div class="lab-error"><b>Dispatcher did not compile</b><br>'
            f'{html.escape(dispatcher_compile_error)}</div>'
        )
        if dispatcher_compile_error
        else mo.Html(
            '<div class="lab-receipt"><b>Dispatcher loaded.</b> '
            'Behavior—not syntax—is graded by the fixtures.</div>'
        )
    )
    mo.vstack([_status, mo.md("### Dispatcher checkpoint"), mo.md("\n".join(_lines))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 3: implement two traced safety tools

    Write the functions V3 can use to actively collect customer-boundary and
    retry evidence. They receive only the in-memory request and application
    configuration. The fixture deliberately includes a ticket from another
    customer, so a correct tool must honor the tenant-scoped patch strategy.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    safety_tools_default_source = '''def inspect_customer_boundary(request, application, arguments):
    # TODO: apply the application's patch_strategy to request["tickets"].
    # Return explicit evidence and the sorted unique affected customer IDs.
    return {}


def exercise_retry_path(request, application, arguments):
    # TODO: actively exercise at least two deliveries.
    # Return explicit retry evidence and zero duplicate audit events.
    return {}'''
    _editor = mo.ui.code_editor(
        value=safety_tools_default_source,
        language="python",
        min_height=300,
        max_height=460,
        label="Your Python: implement the V3 safety tools",
    )
    safety_tools_form = _editor.form(submit_button_label="Run safety-tool fixtures")
    safety_tools_form
    return safety_tools_default_source, safety_tools_form


@app.cell(hide_code=True)
def _(lab, safety_tools_default_source, safety_tools_form, weave):
    safety_tools_compile_error = ""
    try:
        _compiled = lab.compile_participant_functions(
            safety_tools_form.value or safety_tools_default_source,
            ["inspect_customer_boundary", "exercise_retry_path"],
        )
        participant_inspect_tool = _compiled["inspect_customer_boundary"]
        participant_retry_tool = _compiled["exercise_retry_path"]
    except ValueError as error:
        safety_tools_compile_error = str(error)

        def participant_inspect_tool(request, application, arguments):
            del request, application, arguments
            return {}

        def participant_retry_tool(request, application, arguments):
            del request, application, arguments
            return {}

    @weave.op(name="patchpilot_technical_inspect_customer_boundary_tool")
    def inspect_customer_boundary_tool(request, application, arguments):
        return participant_inspect_tool(request, application, arguments)

    @weave.op(name="patchpilot_technical_exercise_retry_path_tool")
    def exercise_retry_path_tool(request, application, arguments):
        return participant_retry_tool(request, application, arguments)

    v3_tool_handlers = {
        **lab.default_tool_handlers(),
        lab.CUSTOMER_BOUNDARY_TOOL: inspect_customer_boundary_tool,
        lab.RETRY_PATH_TOOL: exercise_retry_path_tool,
    }
    safety_tools_check = lab.validate_safety_tools(
        participant_inspect_tool,
        participant_retry_tool,
    )
    tool_registry_check = lab.validate_tool_registry(v3_tool_handlers)
    return (
        safety_tools_check,
        safety_tools_compile_error,
        tool_registry_check,
        v3_tool_handlers,
    )


@app.cell(hide_code=True)
def _(
    html,
    mo,
    safety_tools_check,
    safety_tools_compile_error,
    tool_registry_check,
):
    _lines = ["| Safety-tool fixture | Result |", "|---|---:|"]
    for _check in safety_tools_check["checks"]:
        _lines.append(
            f"| {_check['check']} | {'PASS' if _check['passed'] else 'FIX'} |"
        )
    for _check in tool_registry_check["checks"]:
        _lines.append(
            f"| Registry: {_check['check']} | {'PASS' if _check['passed'] else 'FIX'} |"
        )
    _error = safety_tools_compile_error or safety_tools_check.get("error", "")
    _status = (
        mo.Html(
            '<div class="lab-error"><b>Safety tools need attention</b><br>'
            f'{html.escape(_error)}</div>'
        )
        if _error
        else mo.Html(
            '<div class="lab-receipt"><b>Safety tools loaded.</b> '
            'The fixtures below determine whether their evidence is usable.</div>'
        )
    )
    mo.vstack([_status, mo.md("### Safety-tool checkpoint"), mo.md("\n".join(_lines))])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Exercise 4: implement the evidence-completeness scorer

    Turn the trace-derived expectation into executable evaluation logic. A
    missing output field is **unknown** because the system cannot prove whether
    evidence exists; an explicit `False` is a **failure**. Complete both TODO
    branches and satisfy the pass/fail/unknown fixtures without a model call.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    scorer_default_source = '''def evidence_completeness_status(output, expected_behavior):
    required = set(expected_behavior.get("required_evidence", []))
    if not required:
        return {
            "status": "pass",
            "reason": "No additional evidence categories are required.",
        }

    field_by_category = {
        "customer_accounts": "customer_account_evidence_available",
        "retry_behavior": "retry_evidence_available",
    }
    missing_fields = sorted(
        category
        for category in required
        if field_by_category.get(category) not in output
    )
    if missing_fields:
        # TODO 1: return UNKNOWN and name the fields that were not returned.
        return {"status": "todo", "reason": "TODO"}

    unavailable = sorted(
        category
        for category in required
        if not output.get(field_by_category[category])
    )
    # TODO 2: explicit unavailable evidence is FAIL; otherwise PASS.
    return {"status": "todo", "reason": "TODO"}

# End of exercise scaffold.'''
    _editor = mo.ui.code_editor(
        value=scorer_default_source,
        language="python",
        min_height=560,
        max_height=720,
        label="Your Python: complete evidence_completeness_status",
    )
    scorer_form = _editor.form(submit_button_label="Run scorer fixtures")
    scorer_form
    return scorer_default_source, scorer_form


@app.cell(hide_code=True)
def _(lab, scorer_default_source, scorer_form, weave):
    scorer_compile_error = ""
    try:
        _compiled = lab.compile_participant_functions(
            scorer_form.value or scorer_default_source,
            ["evidence_completeness_status"],
        )
        evidence_completeness_status = _compiled["evidence_completeness_status"]
    except ValueError as error:
        scorer_compile_error = str(error)

        def evidence_completeness_status(output, expected_behavior):
            del output, expected_behavior
            return {"status": "unknown", "reason": "Scorer did not compile."}

    @weave.op(name="patchpilot_technical_evidence_completeness_scorer")
    def evidence_completeness_scorer(output, expected_behavior):
        return evidence_completeness_status(output, expected_behavior)

    evidence_scorer_check = lab.validate_evidence_scorer(
        evidence_completeness_status
    )
    return (
        evidence_completeness_scorer,
        evidence_completeness_status,
        evidence_scorer_check,
        scorer_compile_error,
    )


@app.cell(hide_code=True)
def _(evidence_scorer_check, html, mo, scorer_compile_error):
    _lines = [
        "| Scorer fixture | Expected | Actual | Result |",
        "|---|---:|---:|---:|",
    ]
    for _row in evidence_scorer_check["rows"]:
        _lines.append(
            f"| {_row['fixture']} | {_row['expected'].upper()} | "
            f"{_row['actual'].upper()} | {'PASS' if _row['passed'] else 'FIX'} |"
        )
    _status = (
        mo.Html(
            '<div class="lab-error"><b>Scorer did not compile</b><br>'
            f'{html.escape(scorer_compile_error)}</div>'
        )
        if scorer_compile_error
        else mo.Html(
            '<div class="lab-receipt"><b>Scorer loaded.</b> '
            'The fixtures verify its semantics below.</div>'
        )
    )
    mo.vstack([_status, mo.md("### Scorer checkpoint"), mo.md("\n".join(_lines))])
    return


@app.cell(hide_code=True)
def _(
    evidence_completeness_status,
    lab,
    lab_config_status,
    participant_dispatcher,
    v3_tool_handlers,
):
    evaluation_v2_agent = lab.build_live_agent(
        "v2",
        model_id=lab_config_status["judge_model"],
        dispatcher=participant_dispatcher,
    )
    evaluation_v3_agent = lab.build_live_agent(
        "v3",
        model_id=lab_config_status["judge_model"],
        handlers=v3_tool_handlers,
        dispatcher=participant_dispatcher,
    )
    lab_result_compiler = lab.make_result_compiler(
        {"evidence_completeness": evidence_completeness_status}
    )
    return evaluation_v2_agent, evaluation_v3_agent, lab_result_compiler


@app.cell(hide_code=True)
def _(
    dispatcher_check,
    evidence_completeness_status,
    evidence_scorer_check,
    fifth_case_check,
    lab,
    lab_rows,
    mo,
    safety_tools_check,
):
    _ready = all(
        check["valid"]
        for check in (
            fifth_case_check,
            dispatcher_check,
            safety_tools_check,
            evidence_scorer_check,
        )
    )
    hypothesis_preview = (
        lab.deterministic_hypothesis_preview(
            lab_rows, evidence_completeness_status
        )
        if _ready
        else []
    )
    if _ready:
        _lines = [
            "| Case | Expected V2 gate | Target V3 gate |",
            "|---|---:|---:|",
        ]
        for _row in hypothesis_preview:
            _lines.append(
                f"| {_row['case']} | {_row['v2_gate'].upper()} | "
                f"{_row['v3_gate'].upper()} |"
            )
        _content = mo.vstack(
            [
                mo.md("### Hypothesis preview—no model calls"),
                mo.md(
                    "This table is the expected result if the live model requests "
                    "every available tool. The evaluation below measures what it "
                    "actually does."
                ),
                mo.md("\n".join(_lines)),
            ]
        )
    else:
        _content = mo.Html(
            '<div class="lab-panel amber"><b>Hypothesis preview locked</b><br>'
            'Pass the four local coding checkpoints to compile a meaningful '
            'V2-versus-V3 prediction.</div>'
        )
    _content
    return (hypothesis_preview,)


@app.cell(hide_code=True)
def _(
    dispatcher_check,
    evidence_scorer_check,
    fifth_case_check,
    safety_tools_check,
    tool_registry_check,
):
    all_lab_checkpoints_pass = (
        fifth_case_check["valid"]
        and dispatcher_check["valid"]
        and safety_tools_check["valid"]
        and evidence_scorer_check["valid"]
        and tool_registry_check["valid"]
    )
    return (all_lab_checkpoints_pass,)


@app.cell(hide_code=True)
def _(mo):
    confirm_evaluation_calls = mo.ui.checkbox(
        label="Each evaluation makes 5 agent calls and 5 judge calls"
    )
    return (confirm_evaluation_calls,)


@app.cell(hide_code=True)
def _(
    all_lab_checkpoints_pass,
    confirm_evaluation_calls,
    lab_connection_verified,
    mo,
):
    run_live_v2_button = mo.ui.run_button(
        label="Evaluate live V2 baseline · 10 model calls",
        disabled=not (
            lab_connection_verified
            and all_lab_checkpoints_pass
            and confirm_evaluation_calls.value
        ),
    )
    mo.vstack(
        [
            mo.Html(
                """
                <section class="lab-page">
                  <div class="lab-kicker">Evaluate · 65–80 minutes</div>
                  <h2>Compare two live agents under one contract</h2>
                  <p>Both runs use your dispatcher, the same five rows, four deterministic scorers, live judge model, rubric, patch strategy, and human-review policy. Only the available agent toolset changes.</p>
                  <div class="lab-do"><b>Before running</b><br>Confirm all four coding checkpoints pass. Predict which cases could still vary if the live model chooses not to request a safety tool.</div>
                </section>
                """
            ),
            mo.md(
                "**All local checkpoints pass.**"
                if all_lab_checkpoints_pass
                else "**Finish the dataset, dispatcher, tools, and scorer before spending calls.**"
            ),
            confirm_evaluation_calls,
            run_live_v2_button,
        ]
    )
    return (run_live_v2_button,)


@app.cell(hide_code=True)
async def _(
    core,
    evidence_completeness_scorer,
    evaluation_v2_agent,
    lab,
    lab_result_compiler,
    lab_rows,
    run_live_v2_button,
):
    live_v2_error = ""
    live_v2_evaluation = None
    if run_live_v2_button.value:
        try:
            live_v2_evaluation = await lab.run_technical_evaluation(
                evaluation_v2_agent,
                lab_rows,
                additional_scorers=[evidence_completeness_scorer],
                additional_scorer_ids=["evidence_completeness"],
                dataset_name=lab.TECHNICAL_DATASET_NAME,
                dataset_description=(
                    "Five BeeVerse cases for the standalone live-agent technical lab."
                ),
                evaluation_name=lab.TECHNICAL_EVALUATION_NAME,
                evaluation_run_prefix="Technical Live Agent",
                scorer_set_version="technical-live-scorers-v1",
                changed_dimension="agent_toolset",
                contract_id=lab.TECHNICAL_CONTRACT_ID,
                attribute_namespace="agent_loop_technical",
                result_compiler=lab_result_compiler,
            )
        except Exception as error:
            live_v2_error = core.safe_error_text(error)
    return live_v2_error, live_v2_evaluation


@app.cell(hide_code=True)
def _(
    confirm_evaluation_calls,
    lab_connection_verified,
    live_v2_evaluation,
    mo,
):
    run_live_v3_button = mo.ui.run_button(
        label="Evaluate live V3 candidate · 10 model calls",
        disabled=not (
            lab_connection_verified
            and confirm_evaluation_calls.value
            and live_v2_evaluation is not None
        ),
    )
    run_live_v3_button
    return (run_live_v3_button,)


@app.cell(hide_code=True)
async def _(
    core,
    evidence_completeness_scorer,
    evaluation_v3_agent,
    lab,
    lab_result_compiler,
    lab_rows,
    run_live_v3_button,
):
    live_v3_error = ""
    live_v3_evaluation = None
    if run_live_v3_button.value:
        try:
            live_v3_evaluation = await lab.run_technical_evaluation(
                evaluation_v3_agent,
                lab_rows,
                additional_scorers=[evidence_completeness_scorer],
                additional_scorer_ids=["evidence_completeness"],
                dataset_name=lab.TECHNICAL_DATASET_NAME,
                dataset_description=(
                    "Five BeeVerse cases for the standalone live-agent technical lab."
                ),
                evaluation_name=lab.TECHNICAL_EVALUATION_NAME,
                evaluation_run_prefix="Technical Live Agent",
                scorer_set_version="technical-live-scorers-v1",
                changed_dimension="agent_toolset",
                contract_id=lab.TECHNICAL_CONTRACT_ID,
                attribute_namespace="agent_loop_technical",
                result_compiler=lab_result_compiler,
            )
        except Exception as error:
            live_v3_error = core.safe_error_text(error)
    return live_v3_error, live_v3_evaluation


@app.cell(hide_code=True)
def _(
    html,
    lab,
    live_v2_error,
    live_v2_evaluation,
    live_v3_error,
    live_v3_evaluation,
    mo,
):
    _items = []
    if live_v2_evaluation:
        _url = html.escape(live_v2_evaluation["evaluation_url"], quote=True)
        _items.append(
            mo.Html(
                f'<div class="lab-receipt"><b>Live V2 evaluation complete.</b> '
                f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
                "Open V2 in Weave ↗</a></div>"
            )
        )
    if live_v2_error:
        _items.append(
            mo.Html(
                f'<div class="lab-error"><b>Live V2 did not complete.</b> '
                f"{html.escape(live_v2_error)}</div>"
            )
        )
    if live_v3_evaluation:
        _url = html.escape(
            lab.evaluation_comparison_url(
                live_v2_evaluation,
                live_v3_evaluation,
            ),
            quote=True,
        )
        _items.append(
            mo.Html(
                f'<div class="lab-receipt"><b>Live V3 evaluation complete.</b> '
                f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
                "Open the V2 baseline and V3 comparison in Weave ↗</a><br>"
                '<span class="lab-small">A newly completed Weave result can take '
                "10–20 seconds to become available. Reload once if the detail "
                "panel says Call not ready.</span></div>"
            )
        )
        _comparison = lab.compare_live_evaluations(
            live_v2_evaluation, live_v3_evaluation
        )
        _usage = lab.live_safety_tool_usage(live_v3_evaluation)
        if _usage["used"]:
            _used = ", ".join(_usage["used_tools"])
            _items.append(
                mo.Html(
                    '<div class="lab-panel mint"><b>The live agent used participant-built '
                    f"safety evidence.</b><br>Executed safety tools: <code>{html.escape(_used)}</code>. "
                    "Open the comparison and inspect the corresponding nested Calls.</div>"
                )
            )
        else:
            _items.append(
                mo.Html(
                    '<div class="lab-panel amber"><b>The tools existed, but this live agent '
                    "did not use them.</b><br>This is evidence—not a failed coding exercise. "
                    "Keep the result in human review, inspect requested versus executed tools, "
                    "and use the optional one-case retry below if time permits.</div>"
                )
            )
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
        _tool_lines = [
            "| Case | V2 executed tools | V3 executed tools |",
            "|---|---|---|",
        ]
        for _row in _comparison:
            _tool_lines.append(
                f"| {_row['case']} | `{_row['v2_tools']}` | `{_row['v3_tools']}` |"
            )
        _items.extend([mo.md("\n".join(_lines)), mo.md("\n".join(_tool_lines))])
    if live_v3_error:
        _items.append(
            mo.Html(
                f'<div class="lab-error"><b>Live V3 did not complete.</b> '
                f"{html.escape(live_v3_error)}</div>"
            )
        )
    mo.vstack(_items) if _items else mo.md("")
    return


@app.cell(hide_code=True)
def _(mo):
    confirm_v3_retry = mo.ui.checkbox(
        label="Retry one V3 evidence case · 1 model call"
    )
    return (confirm_v3_retry,)


@app.cell(hide_code=True)
def _(confirm_v3_retry, lab, live_v3_evaluation, mo):
    _usage = lab.live_safety_tool_usage(live_v3_evaluation)
    _show_retry = live_v3_evaluation is not None and not _usage["used"]
    run_v3_retry_button = mo.ui.run_button(
        label="Retry V3 on the partial-evidence case · 1 model call",
        disabled=not (_show_retry and confirm_v3_retry.value),
    )
    if _show_retry:
        _retry_view = mo.vstack(
            [
                mo.Html(
                    '<div class="lab-do"><b>Optional resilience path</b><br>Retry one '
                    "representative case. The model still chooses its tools, so a second skip "
                    "is a valid result and should remain in human review.</div>"
                ),
                confirm_v3_retry,
                run_v3_retry_button,
            ]
        )
    else:
        _retry_view = mo.md("")
    _retry_view
    return (run_v3_retry_button,)


@app.cell(hide_code=True)
async def _(core, evaluation_v3_agent, lab, lab_rows, run_v3_retry_button):
    v3_retry_error = ""
    v3_retry_trace = None
    if run_v3_retry_button.value:
        try:
            _case = next(
                row for row in lab_rows if row["case_id"] == "partial_safety_evidence"
            )
            v3_retry_trace = await lab.run_single_case_trace(
                evaluation_v3_agent,
                _case,
            )
        except Exception as error:
            v3_retry_error = core.safe_error_text(error)
    return v3_retry_error, v3_retry_trace


@app.cell(hide_code=True)
def _(core, html, lab, mo, v3_retry_error, v3_retry_trace):
    if v3_retry_trace:
        _url = html.escape(v3_retry_trace["trace_url"], quote=True)
        _result = v3_retry_trace["result"]
        _tools = [str(value) for value in _result.get("executed_tools", [])]
        _usage = lab.live_safety_tool_usage(
            {"deterministic_results": [{"output": _result}]}
        )
        _tool_text = ", ".join(_tools) or "none"
        if _usage["used"]:
            _message = (
                "The retry used participant-built safety evidence. Inspect the nested "
                "tool Calls before making the release decision."
            )
            _tone = "mint"
        else:
            _message = (
                "The retry also skipped both safety tools. Treat that repeat behavior "
                "as evidence for human review or Hold."
            )
            _tone = "amber"
        _view = mo.Html(
            f'<div class="lab-panel {_tone}"><b>Optional V3 retry complete.</b> '
            f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
            f'Open the retry trace in Weave ↗</a><br>Executed tools: '
            f'<code>{html.escape(_tool_text)}</code><br>{html.escape(_message)}</div>'
        )
    elif v3_retry_error:
        _safe = v3_retry_error
        _view = mo.Html(
            '<div class="lab-error"><b>The optional V3 retry did not complete.</b> '
            f"{html.escape(_safe)}</div>"
        )
    else:
        _view = mo.md("")
    _view
    return


@app.cell(hide_code=True)
def _(live_v3_evaluation, mo):
    final_decision = mo.ui.radio(
        options={
            "Ship": "Ship",
            "Ship with guardrails": "Ship with guardrails",
            "Hold": "Hold",
        },
        value="Ship with guardrails",
        label="Release decision",
    )
    decision_confidence = mo.ui.radio(
        options={"High": "High", "Medium": "Medium", "Low": "Low"},
        value="Medium",
        label="Confidence",
    )
    remaining_risk = mo.ui.dropdown(
        options={
            "Live model variability": "Live variability",
            "Missing evidence": "Missing evidence",
            "Judge disagreement": "Judge disagreement",
            "No material remaining risk": "None",
        },
        value="Live model variability",
        label="Primary remaining risk",
    )
    save_technical_decision_button = mo.ui.run_button(
        label="Save the decision and Weave annotations",
        disabled=live_v3_evaluation is None,
    )
    mo.vstack(
        [
            mo.Html(
                """
                <section class="lab-page">
                  <div class="lab-kicker">Compare and decide · 80–90 minutes</div>
                  <h2>Set the operating boundary from evidence</h2>
                  <div class="lab-do"><b>Weave comparison hunt</b><br>Verify the dataset fingerprint and contract ID match; inspect one deterministic scorer Call and one judge Call; compare requested versus executed tools; find one agreement or disagreement; then record the release decision on the V3 evaluation.</div>
                </section>
                """
            ),
            final_decision,
            decision_confidence,
            remaining_risk,
            save_technical_decision_button,
        ]
    )
    return (
        decision_confidence,
        final_decision,
        remaining_risk,
        save_technical_decision_button,
    )


@app.cell(hide_code=True)
async def _(
    core,
    decision_confidence,
    final_decision,
    lab,
    lab_rows,
    live_v2_evaluation,
    live_v3_evaluation,
    remaining_risk,
    save_technical_decision_button,
):
    technical_decision_error = ""
    technical_decision_receipt = None
    if save_technical_decision_button.value and live_v2_evaluation and live_v3_evaluation:
        try:
            technical_decision_receipt = await lab.record_technical_decision(
                target_call_id=live_v3_evaluation["evaluation_call_id"],
                decision=final_decision.value,
                confidence=decision_confidence.value,
                remaining_risk=remaining_risk.value,
                dataset_fingerprint=core.dataset_fingerprint(lab_rows),
                compared_call_ids=[
                    live_v2_evaluation["evaluation_call_id"],
                    live_v3_evaluation["evaluation_call_id"],
                ],
            )
        except Exception as error:
            technical_decision_error = core.safe_error_text(error)
    return technical_decision_error, technical_decision_receipt


@app.cell(hide_code=True)
def _(html, mo, technical_decision_error, technical_decision_receipt):
    if technical_decision_receipt:
        _url = html.escape(technical_decision_receipt["record_url"], quote=True)
        _view = mo.Html(
            f'<div class="lab-receipt"><b>Technical decision saved.</b> '
            f'<a href="{_url}" target="_blank" rel="noopener noreferrer">'
            "Open the review record in Weave ↗</a></div>"
        )
    elif technical_decision_error:
        _view = mo.Html(
            f'<div class="lab-error"><b>The decision was not saved.</b> '
            f"{html.escape(technical_decision_error)}</div>"
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
          <h2>A tool is a capability; a trace is evidence</h2>
          <p>Adding a tool does not prove that a live model will request it, use it correctly, or produce enough evidence. A trustworthy improvement loop records the actual call tree, tests the actual output, compares applications under one declared contract, and leaves the final operating boundary with a human.</p>
          <div class="lab-panel mint"><b>Take-home extension</b><br>Change one judge criterion and rescore both live applications under a separately named contract. A full rerun adds 20 hosted calls—ten agent calls and ten judge calls—and must never be compared directly with the earlier contract.</div>
        </section>
        """
    )
    return


if __name__ == "__main__":
    app.run()
