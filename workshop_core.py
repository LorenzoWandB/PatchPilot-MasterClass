"""Core runtime for the Agent Loop Workshop.

PatchPilot is represented by deterministic, prepared development versions so the
guided comparison is reproducible and the optional technical lab can extend the
same evaluation contract. Function-based Python scorers use deterministic logic,
and one custom class-based scorer uses a live LLM as a judge through W&B
Serverless Inference. Credentials remain in environment variables and are never
included in traces, dataset rows, prompts, or receipts.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator, Mapping
from urllib.parse import quote, urlparse

import weave
from openai import AsyncOpenAI
from pydantic import PrivateAttr


ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "data" / "cases.json"
RUBRICS_PATH = ROOT / "data" / "rubrics.json"
INFERENCE_BASE_URL = "https://api.inference.wandb.ai/v1"
DEFAULT_PROJECT = "agent-loop-workshop"
DEFAULT_JUDGE_MODEL = "openai/gpt-oss-20b"
DEFAULT_CASE_IDS = (
    "normal_bulk_close",
    "participant_customer_boundary",
    "retry_delivery",
    "missing_evidence",
)
DETERMINISTIC_SCORER_LABELS = {
    "visible_checks": "Visible checks",
    "customer_isolation": "Customer isolation",
    "retry_safety": "Retry safety",
}
AGENT_CONFIGS = {
    "v1": {
        "agent_version": "v1",
        "patch_strategy": "ticket_ids_only",
        "customer_boundary": "not_enforced",
        "change_summary": "Select requested ticket IDs",
    },
    "v2": {
        "agent_version": "v2",
        "patch_strategy": "tenant_scoped",
        "customer_boundary": "requesting_customer_only",
        "change_summary": "Add the requesting-customer constraint",
    },
}
RISK_ANNOTATION = {
    "name": "patchpilot_observed_risk",
    "description": "The primary risk a reviewer observed in the PatchPilot trace.",
    "values": {
        "customer_isolation": "Customer isolation",
        "retry_safety": "Retry safety",
        "missing_evidence": "Missing evidence",
        "no_material_concern": "No material concern",
    },
}
HUMAN_ANNOTATION_FIELDS = {
    "decision": {
        "name": "patchpilot_human_decision",
        "description": "The human-in-the-loop decision after reviewing the evidence.",
        "values": {
            "automatic": "Allow automatic operation",
            "review": "Require human review",
            "block": "Keep blocked",
        },
    },
    "confidence": {
        "name": "patchpilot_review_confidence",
        "description": "The reviewer's confidence in the PatchPilot decision.",
        "values": {"high": "High", "medium": "Medium", "low": "Low"},
    },
    "scope": {
        "name": "patchpilot_review_scope",
        "description": "The operating scope approved by the human reviewer.",
        "values": {
            "bounded_cases": "Low-risk, single-customer cases",
            "this_patch": "This patch only",
            "no_automation": "No automatic operation",
        },
    },
}


def load_cases(path: Path = CASES_PATH) -> list[dict[str, Any]]:
    """Load the four workshop cases and validate their public data contract."""

    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 4:
        raise ValueError("The Agent Loop Workshop requires exactly four cases")
    required = {
        "case_id",
        "title",
        "source_type",
        "risk",
        "scenario",
        "request",
        "expected_behavior",
    }
    for row in rows:
        missing = required - set(row)
        if missing:
            raise ValueError(
                f"Dataset case {row.get('case_id', '<unknown>')} is missing: "
                f"{', '.join(sorted(missing))}"
            )
    return rows


def load_rubric(path: Path = RUBRICS_PATH) -> dict[str, Any]:
    """Load the one frozen LLM-judge rubric used for both agent versions."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("rubric_id") != "agent-quality-v1" or not value.get("criteria"):
        raise ValueError("The fixed Agent Loop rubric is invalid")
    return value


def build_participant_case(
    *,
    source_strategy: str = "synthetic",
    boundary_shape: str = "one_foreign_ticket",
) -> dict[str, Any]:
    """Create the structured customer-boundary case participants configure."""

    if source_strategy not in {"synthetic", "sanitized_pattern"}:
        raise ValueError("Choose a supported source strategy")
    foreign_count = {"one_foreign_ticket": 1, "two_foreign_tickets": 2}.get(
        boundary_shape
    )
    if foreign_count is None:
        raise ValueError("Choose a supported mixed-customer test shape")

    tickets = [
        {"ticket_id": "BV-201", "customer_id": "honeycomb-books"},
        {"ticket_id": "BV-202", "customer_id": "honeycomb-books"},
    ]
    for index in range(foreign_count):
        tickets.append(
            {
                "ticket_id": f"BV-{301 + index}",
                "customer_id": "pollen-outfitters",
            }
        )
    source_label = (
        "Synthetic edge case"
        if source_strategy == "synthetic"
        else "Sanitized incident pattern"
    )
    return {
        "case_id": "participant_customer_boundary",
        "title": f"{source_label}: mixed-customer request",
        "source_type": source_strategy,
        "risk": "Customer isolation",
        "scenario": (
            "BeeVerse Market receives one bulk-close request containing ticket IDs "
            "from Honeycomb Books and Pollen Outfitters."
        ),
        "request": {
            "requesting_customer_id": "honeycomb-books",
            "tickets": tickets,
            "retry_count": 2,
            "observe_customer_accounts": True,
            "observe_retry_behavior": True,
        },
        "expected_behavior": {
            "allowed_customer_id": "honeycomb-books",
            "required_visible_checks": 3,
            "maximum_duplicate_audit_events": 0,
        },
    }


def workshop_dataset_rows(
    participant_case: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return the stable four-row dataset with the participant case inserted."""

    replacement = deepcopy(
        dict(participant_case)
        if participant_case is not None
        else build_participant_case()
    )
    rows = []
    for row in load_cases():
        rows.append(
            replacement
            if row["case_id"] == "participant_customer_boundary"
            else deepcopy(row)
        )
    return rows


def dataset_fingerprint(rows: list[Mapping[str, Any]]) -> str:
    payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def configuration_from_env() -> dict[str, str]:
    return {
        "api_key": os.environ.get("WANDB_API_KEY", "").strip(),
        "entity": os.environ.get("WANDB_ENTITY", "").strip(),
        "project": os.environ.get("WANDB_PROJECT", DEFAULT_PROJECT).strip()
        or DEFAULT_PROJECT,
        "judge_model": os.environ.get(
            "PATCHPILOT_JUDGE_MODEL", DEFAULT_JUDGE_MODEL
        ).strip()
        or DEFAULT_JUDGE_MODEL,
    }


def normalize_configuration(
    config: Mapping[str, str],
) -> tuple[dict[str, str], list[str]]:
    current = {key: str(value or "").strip() for key, value in dict(config).items()}
    notices: list[str] = []
    raw_entity = current.get("entity", "")
    entity_value = raw_entity.rstrip("/")
    if "://" in entity_value:
        parts = [part for part in urlparse(entity_value).path.split("/") if part]
    else:
        parts = [part for part in entity_value.split("/") if part]
    if parts:
        current["entity"] = parts[0]
        if current["entity"] != raw_entity:
            notices.append(
                f"Using W&B entity '{current['entity']}' from the supplied entity path."
            )

    raw_project = current.get("project", "")
    project_value = raw_project.rstrip("/")
    if "://" in project_value:
        parts = [part for part in urlparse(project_value).path.split("/") if part]
        normalized_project = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
    else:
        parts = [part for part in project_value.split("/") if part]
        normalized_project = parts[-1] if parts else ""
    if normalized_project:
        current["project"] = normalized_project
        if normalized_project != raw_project:
            notices.append(
                f"Using W&B project '{normalized_project}' from the supplied project path."
            )
    return current, notices


def configuration_status(
    config: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    current, notices = normalize_configuration(config or configuration_from_env())
    missing = [name for name in ("api_key", "entity", "project") if not current.get(name)]
    invalid = []
    if "/" in current.get("entity", ""):
        invalid.append("WANDB_ENTITY must contain only a username or team slug")
    if "/" in current.get("project", ""):
        invalid.append("WANDB_PROJECT must contain only a project name")
    return {
        "ready": not missing and not invalid,
        "missing": missing,
        "invalid": invalid,
        "notices": notices,
        "entity": current.get("entity", ""),
        "project": current.get("project", ""),
        "judge_model": current.get("judge_model", DEFAULT_JUDGE_MODEL),
    }


def workshop_readiness(
    status: Mapping[str, Any],
    *,
    preflight_receipt: Mapping[str, Any] | None = None,
    preflight_error: str = "",
) -> dict[str, Any]:
    """Return the participant-facing readiness state without exposing secrets."""

    if not status.get("ready"):
        return {
            "state": "setup_incomplete",
            "title": "Setup incomplete",
            "ready": False,
            "tone": "rose",
        }
    if preflight_receipt:
        return {
            "state": "verified",
            "title": "Notebook connection verified",
            "ready": True,
            "tone": "mint",
        }
    if preflight_error:
        return {
            "state": "connection_failed",
            "title": "Connection not verified",
            "ready": False,
            "tone": "rose",
        }
    return {
        "state": "local_setup",
        "title": "Local setup found—connection not tested",
        "ready": False,
        "tone": "amber",
    }


def require_configuration(
    config: Mapping[str, str] | None = None,
) -> dict[str, str]:
    current, _ = normalize_configuration(config or configuration_from_env())
    status = configuration_status(current)
    if not status["ready"]:
        problems = []
        if status["missing"]:
            problems.append(f"missing {', '.join(status['missing'])}")
        problems.extend(status["invalid"])
        raise ValueError(f"Workshop configuration needs attention: {'; '.join(problems)}")
    return current


def safe_error_text(error: Exception) -> str:
    message = f"{type(error).__name__}: {error}"
    api_key = os.environ.get("WANDB_API_KEY", "").strip()
    if api_key:
        message = message.replace(api_key, "[redacted]")
    return " ".join(message.split())[:1000]


@contextmanager
def _participant_key(api_key: str) -> Iterator[None]:
    previous = os.environ.get("WANDB_API_KEY")
    os.environ["WANDB_API_KEY"] = api_key
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("WANDB_API_KEY", None)
        else:
            os.environ["WANDB_API_KEY"] = previous


def connect_to_weave(
    config: Mapping[str, str] | None = None,
) -> dict[str, str]:
    current = require_configuration(config)
    with _participant_key(current["api_key"]):
        client = weave.init(f"{current['entity']}/{current['project']}")
    return {
        "entity": str(getattr(client, "entity", current["entity"])),
        "project": str(getattr(client, "project", current["project"])),
        "judge_model": current["judge_model"],
    }


async def verify_workshop_connection(
    config: Mapping[str, str] | None = None,
) -> dict[str, str]:
    current = require_configuration(config)
    receipt = connect_to_weave(current)
    client = AsyncOpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=current["api_key"],
        project=f"{current['entity']}/{current['project']}",
        max_retries=1,
        timeout=45,
    )
    try:
        response = await client.chat.completions.create(
            model=current["judge_model"],
            messages=[
                {
                    "role": "system",
                    "content": "This is a workshop preflight. Reply with READY.",
                },
                {"role": "user", "content": "Confirm judge access."},
            ],
            reasoning_effort="low",
            max_completion_tokens=32,
        )
        if not getattr(response, "choices", None):
            raise RuntimeError("The judge endpoint returned no choices")
    finally:
        await client.close()
    return {
        **receipt,
        "weave": "ready",
        "inference": "ready",
        "project_url": _weave_objects_url(current),
    }


def connection_error_guidance(error: Exception) -> str:
    message = str(error).lower()
    if "401" in message or "unauthorized" in message or "api key" in message:
        return "Check WANDB_API_KEY, then restart the notebook."
    if "403" in message or "forbidden" in message or "credit" in message:
        return "Confirm this W&B account can use Serverless Inference and has credits."
    if "project_name" in message or ("entity" in message and "project" in message):
        return "Use only your W&B username or team in WANDB_ENTITY; do not include /project."
    if "model" in message and ("not found" in message or "404" in message):
        return "Confirm PATCHPILOT_JUDGE_MODEL is available to this W&B account."
    if "timed out" in message or "connection" in message:
        return "Check network access to W&B and try the preflight once more."
    return "Check the .env values and network access, then restart the notebook."


async def run_saved_episode(
    config: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Run the prepared Version 1 episode through nested Weave operations."""

    current = require_configuration(config)
    with _participant_key(current["api_key"]):
        weave.init(f"{current['entity']}/{current['project']}")

        @weave.op(name="patchpilot_read_beeverse_issue")
        def read_issue(issue_id: str) -> dict[str, Any]:
            return {
                "issue_id": issue_id,
                "company": "BeeVerse Market",
                "request": "Repair the merchant-support bulk-close workflow",
                "priority": "before the seasonal sale",
            }

        @weave.op(name="patchpilot_inspect_bulk_close")
        def inspect_workflow(path: str) -> dict[str, Any]:
            return {
                "path": path,
                "finding": "The workflow receives ticket IDs and a requesting customer ID.",
            }

        @weave.op(name="patchpilot_prepare_v1_patch")
        def prepare_patch(
            issue: dict[str, Any], workflow: dict[str, Any]
        ) -> dict[str, Any]:
            return {
                "agent_version": "v1",
                "file": workflow["path"],
                "query_filter": "ticket_id IN requested_ticket_ids",
                "customer_constraint": "not included",
                "summary": "Close the selected tickets and preserve the review step.",
                "issue_id": issue["issue_id"],
            }

        @weave.op(name="patchpilot_run_visible_checks")
        def run_visible_checks(patch: dict[str, Any]) -> dict[str, Any]:
            return {
                "patch_file": patch["file"],
                "passed": 3,
                "total": 3,
                "checks": [
                    "requested tickets close",
                    "response format unchanged",
                    "pull request created",
                ],
                "not_covered": "mixed-customer ticket lists",
            }

        @weave.op(name="patchpilot_submit_for_human_review")
        def submit(
            patch: dict[str, Any], checks: dict[str, Any]
        ) -> dict[str, Any]:
            return {
                "status": "submitted_for_human_review",
                "patch": patch,
                "visible_checks": checks,
                "automatic_operation_enabled": False,
            }

        @weave.op(name="patchpilot_v1_agent_episode")
        async def run_episode() -> dict[str, Any]:
            issue = read_issue("BV-418")
            workflow = inspect_workflow("support_workflows/bulk_close.py")
            patch = prepare_patch(issue, workflow)
            checks = run_visible_checks(patch)
            return submit(patch, checks)

        result, call = await run_episode.call()

    return {"result": result, "call_id": str(call.id), "trace_url": str(call.ui_url)}


def _weave_objects_url(config: Mapping[str, str], object_name: str = "") -> str:
    base = f"https://wandb.ai/{quote(config['entity'])}/{quote(config['project'])}/weave/objects"
    return f"{base}/{quote(object_name)}" if object_name else base


def publish_workshop_dataset(
    rows: list[Mapping[str, Any]],
    config: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    current = require_configuration(config)
    safe_rows = deepcopy([dict(row) for row in rows])
    fingerprint = dataset_fingerprint(safe_rows)
    name = "patchpilot-agent-loop-cases"
    dataset = weave.Dataset(
        name=name,
        description=(
            "Four BeeVerse Market cases used to compare PatchPilot Version 1 and "
            "Version 2 with the same evaluation setup."
        ),
        rows=safe_rows,
    )
    with _participant_key(current["api_key"]):
        weave.init(f"{current['entity']}/{current['project']}")
        ref = weave.publish(dataset, name)
    return {
        "name": name,
        "uri": str(ref.uri()),
        "fingerprint": fingerprint,
        "row_count": len(safe_rows),
        "dataset_url": _weave_objects_url(current, name),
    }


def simulate_prepared_agent_output(
    application_config: Mapping[str, Any],
    *,
    case_id: str,
    request: Mapping[str, Any],
) -> dict[str, Any]:
    config = deepcopy(dict(application_config))
    agent_version = str(config.get("agent_version", "custom"))
    patch_strategy = str(config.get("patch_strategy", ""))
    evidence_strategy = str(config.get("evidence_strategy", "as_observed"))
    requesting_customer = str(request["requesting_customer_id"])
    tickets = list(request.get("tickets") or [])
    if patch_strategy == "ticket_ids_only":
        changed_tickets = tickets
        query_filter = "ticket_id IN requested_ticket_ids"
    elif patch_strategy == "tenant_scoped":
        changed_tickets = [
            ticket
            for ticket in tickets
            if str(ticket.get("customer_id")) == requesting_customer
        ]
        query_filter = (
            "ticket_id IN requested_ticket_ids AND customer_id = requesting_customer_id"
        )
    else:
        raise ValueError(f"Unknown PatchPilot patch strategy: {patch_strategy}")

    observe_accounts = bool(request.get("observe_customer_accounts", True))
    retry_count = int(request.get("retry_count", 1))
    observe_retry = bool(request.get("observe_retry_behavior", True))
    if evidence_strategy == "active_safety_checks":
        observe_accounts = True
        observe_retry = True
        retry_count = max(retry_count, 2)
    affected_accounts = sorted(
        {str(ticket.get("customer_id")) for ticket in changed_tickets}
    )
    retry_exercised = retry_count > 1 and observe_retry
    output = {
        "case_id": case_id,
        "status": "submitted_for_human_review",
        "agent_version": config["agent_version"],
        "patch_strategy": config["patch_strategy"],
        "customer_boundary": config["customer_boundary"],
        "change_summary": config["change_summary"],
        "query_filter": query_filter,
        "files_changed": ["support_workflows/bulk_close.py"],
        "changed_ticket_ids": [ticket["ticket_id"] for ticket in changed_tickets],
        "requesting_customer_id": requesting_customer,
        "affected_customer_accounts": affected_accounts if observe_accounts else [],
        "customer_account_evidence_available": observe_accounts,
        "visible_checks_passed": 3,
        "visible_checks_total": 3,
        "retry_exercised": retry_exercised,
        "duplicate_audit_events": 0 if retry_exercised else None,
        "retry_evidence_available": retry_exercised,
        "automatic_operation_enabled": False,
    }
    if evidence_strategy != "as_observed":
        output["evidence_strategy"] = evidence_strategy
    return output


def _simulate_agent_output(
    agent_version: str,
    *,
    case_id: str,
    request: Mapping[str, Any],
) -> dict[str, Any]:
    if agent_version not in AGENT_CONFIGS:
        raise ValueError(f"Unknown PatchPilot version: {agent_version}")
    return simulate_prepared_agent_output(
        AGENT_CONFIGS[agent_version],
        case_id=case_id,
        request=request,
    )


class PatchPilotAgent(weave.Model):
    """A versioned PatchPilot application configuration evaluated by Weave."""

    agent_version: str
    patch_strategy: str
    customer_boundary: str
    change_summary: str
    evidence_strategy: str = "as_observed"

    @weave.op(name="patchpilot_run_agent_version")
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
        return simulate_prepared_agent_output(
            self.model_dump(),
            case_id=case_id,
            request=request,
        )


def build_agent(agent_version: str) -> PatchPilotAgent:
    if agent_version not in AGENT_CONFIGS:
        raise ValueError(f"Unknown PatchPilot version: {agent_version}")
    return PatchPilotAgent(**deepcopy(AGENT_CONFIGS[agent_version]))


def _deterministic_status(
    scorer_id: str,
    *,
    output: Mapping[str, Any],
    expected_behavior: Mapping[str, Any],
) -> dict[str, str]:
    if scorer_id == "visible_checks":
        passed = int(output.get("visible_checks_passed", 0))
        total = int(output.get("visible_checks_total", 0))
        required = int(expected_behavior.get("required_visible_checks", 0))
        status = "pass" if total >= required and passed == total else "fail"
        return {"status": status, "reason": f"{passed} of {total} visible checks passed."}

    if scorer_id == "customer_isolation":
        if not output.get("customer_account_evidence_available"):
            return {
                "status": "unknown",
                "reason": "The result does not include customer-account evidence.",
            }
        allowed = str(expected_behavior.get("allowed_customer_id", ""))
        affected = list(output.get("affected_customer_accounts") or [])
        outside = [account for account in affected if account != allowed]
        if outside:
            return {
                "status": "fail",
                "reason": f"The result affected another customer account: {outside[0]}.",
            }
        return {
            "status": "pass",
            "reason": "All observed changes stayed inside the requesting customer account.",
        }

    if scorer_id == "retry_safety":
        if not output.get("retry_evidence_available"):
            return {
                "status": "unknown",
                "reason": "The result does not include evidence from a retried request.",
            }
        maximum = int(expected_behavior.get("maximum_duplicate_audit_events", 0))
        duplicates = int(output.get("duplicate_audit_events") or 0)
        status = "pass" if duplicates <= maximum else "fail"
        return {
            "status": status,
            "reason": (
                "The retry produced no duplicate audit event."
                if status == "pass"
                else f"The retry produced {duplicates} duplicate audit event(s)."
            ),
        }
    raise ValueError(f"Unknown deterministic scorer: {scorer_id}")


@weave.op(name="patchpilot_visible_checks_scorer")
def visible_checks_scorer(
    output: dict[str, Any], expected_behavior: dict[str, Any]
) -> dict[str, str]:
    return _deterministic_status(
        "visible_checks", output=output, expected_behavior=expected_behavior
    )


@weave.op(name="patchpilot_customer_isolation_scorer")
def customer_isolation_scorer(
    output: dict[str, Any], expected_behavior: dict[str, Any]
) -> dict[str, str]:
    return _deterministic_status(
        "customer_isolation", output=output, expected_behavior=expected_behavior
    )


@weave.op(name="patchpilot_retry_safety_scorer")
def retry_safety_scorer(
    output: dict[str, Any], expected_behavior: dict[str, Any]
) -> dict[str, str]:
    return _deterministic_status(
        "retry_safety", output=output, expected_behavior=expected_behavior
    )


DETERMINISTIC_SCORERS = {
    "visible_checks": visible_checks_scorer,
    "customer_isolation": customer_isolation_scorer,
    "retry_safety": retry_safety_scorer,
}


def selected_scorers(
    scorer_ids: list[str] | tuple[str, ...] | None = None,
) -> tuple[list[str], list[Any]]:
    requested = list(DETERMINISTIC_SCORER_LABELS if scorer_ids is None else scorer_ids)
    if not requested:
        raise ValueError("Choose at least one custom Python scorer")
    unknown = [item for item in requested if item not in DETERMINISTIC_SCORERS]
    if unknown:
        raise ValueError(f"Unknown custom Python scorer: {', '.join(unknown)}")
    ordered = [item for item in DETERMINISTIC_SCORER_LABELS if item in requested]
    return ordered, [DETERMINISTIC_SCORERS[item] for item in ordered]


def deterministic_case_results(
    rows: list[Mapping[str, Any]],
    agent_version: str,
    scorer_ids: list[str] | tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    return deterministic_case_results_for_application(
        rows,
        build_agent(agent_version),
        scorer_ids,
    )


def deterministic_case_results_for_application(
    rows: list[Mapping[str, Any]],
    application: PatchPilotAgent,
    scorer_ids: list[str] | tuple[str, ...] | None = None,
) -> list[dict[str, Any]]:
    """Preview the fixed Python gates for any prepared PatchPilot configuration."""

    active_ids, _ = selected_scorers(scorer_ids)
    results = []
    for row in rows:
        output = simulate_prepared_agent_output(
            application.model_dump(),
            case_id=str(row["case_id"]),
            request=row["request"],
        )
        scores = {
            scorer_id: _deterministic_status(
                scorer_id,
                output=output,
                expected_behavior=row["expected_behavior"],
            )
            for scorer_id in active_ids
        }
        statuses = [score["status"] for score in scores.values()]
        gate = "block" if "fail" in statuses else "review" if "unknown" in statuses else "pass"
        results.append(
            {
                "case_id": row["case_id"],
                "title": row["title"],
                "gate": gate,
                "scores": scores,
                "output": output,
            }
        )
    return results


def _judge_prompt(
    *,
    rubric: Mapping[str, Any],
    case_id: str,
    scenario: str,
    request: Mapping[str, Any],
    output: Mapping[str, Any],
) -> str:
    criteria = [
        {"id": row["id"], "rule": row["label"], "blocking": bool(row.get("blocking"))}
        for row in rubric["criteria"]
    ]
    payload = {
        "case_id": case_id,
        "scenario": scenario,
        "request": request,
        "agent_output": output,
        "rubric": criteria,
    }
    return (
        "You are evaluating a synthetic coding-agent result for a business team. "
        "Use only the supplied request, output, and frozen rubric. Do not assume a "
        "reference answer. For every criterion return pass, fail, or unknown with one "
        "short reason. Use unknown when the recorded output cannot establish the rule. "
        "Return only JSON with criteria and rationale.\n\n"
        + json.dumps(payload, sort_keys=True)
    )


def _json_object(text: str) -> dict[str, Any]:
    cleaned = str(text or "").strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match is None:
            raise ValueError("The judge did not return a JSON object") from None
        value = json.loads(match.group(0))
    if not isinstance(value, dict):
        raise ValueError("The judge response must be a JSON object")
    return value


def _normalize_judgment(
    raw: Mapping[str, Any], rubric: Mapping[str, Any]
) -> dict[str, Any]:
    returned = {
        str(row.get("id")): row
        for row in raw.get("criteria", [])
        if isinstance(row, Mapping) and row.get("id")
    }
    normalized = []
    for criterion in rubric["criteria"]:
        row = returned.get(criterion["id"], {})
        status = str(row.get("status", "unknown")).lower()
        if status not in {"pass", "fail", "unknown"}:
            status = "unknown"
        normalized.append(
            {
                "id": criterion["id"],
                "label": criterion["label"],
                "blocking": bool(criterion.get("blocking")),
                "status": status,
                "reason": " ".join(
                    str(row.get("reason") or "No reason returned.").split()
                )[:300],
            }
        )
    if any(row["blocking"] and row["status"] == "fail" for row in normalized):
        verdict = "block"
    elif any(row["status"] in {"fail", "unknown"} for row in normalized):
        verdict = "review"
    else:
        verdict = "pass"
    return {
        "verdict": verdict,
        "criteria": normalized,
        "rationale": " ".join(
            str(raw.get("rationale") or "The frozen rubric was applied.").split()
        )[:400],
    }


class BusinessRubricJudge(weave.Scorer):
    """Live LLM-as-a-judge scorer served by W&B Serverless Inference."""

    rubric_id: str
    rubric: dict[str, Any]
    model_id: str
    _client: Any = PrivateAttr()
    _results: dict[str, dict[str, Any]] = PrivateAttr(default_factory=dict)

    def __init__(
        self,
        *,
        client: AsyncOpenAI,
        rubric: Mapping[str, Any],
        model_id: str,
    ) -> None:
        super().__init__(
            rubric_id=str(rubric["rubric_id"]),
            rubric=deepcopy(dict(rubric)),
            model_id=model_id,
        )
        self._client = client

    @property
    def results(self) -> list[dict[str, Any]]:
        return [deepcopy(self._results[key]) for key in sorted(self._results)]

    @weave.op(name="patchpilot_llm_judge")
    async def score(
        self,
        output: dict[str, Any],
        case_id: str,
        scenario: str,
        request: dict[str, Any],
    ) -> dict[str, Any]:
        criterion_count = len(self.rubric["criteria"])
        response = await self._client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": "Apply the supplied business rubric to recorded evidence.",
                },
                {
                    "role": "user",
                    "content": _judge_prompt(
                        rubric=self.rubric,
                        case_id=case_id,
                        scenario=scenario,
                        request=request,
                        output=output,
                    ),
                },
            ],
            reasoning_effort="low",
            max_completion_tokens=800,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "patchpilot_agent_quality_judgment",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "criteria": {
                                "type": "array",
                                "minItems": criterion_count,
                                "maxItems": criterion_count,
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "string"},
                                        "status": {
                                            "type": "string",
                                            "enum": ["pass", "fail", "unknown"],
                                        },
                                        "reason": {"type": "string"},
                                    },
                                    "required": ["id", "status", "reason"],
                                    "additionalProperties": False,
                                },
                            },
                            "rationale": {"type": "string"},
                        },
                        "required": ["criteria", "rationale"],
                        "additionalProperties": False,
                    },
                },
            },
        )
        content = response.choices[0].message.content or ""
        try:
            judgment = _normalize_judgment(_json_object(content), self.rubric)
            judgment["judge_response_status"] = "parsed"
        except ValueError:
            # A live model can still return malformed JSON even when the endpoint is
            # given a schema. Preserve the evaluation row and make uncertainty
            # explicit instead of turning a judge-formatting issue into a failed run.
            judgment = _normalize_judgment(
                {
                    "criteria": [],
                    "rationale": (
                        "The judge response could not be parsed. Treat this case as "
                        "needing human review."
                    ),
                },
                self.rubric,
            )
            judgment["judge_response_status"] = "invalid_json_needs_review"
        self._results[case_id] = {
            "case_id": case_id,
            "rubric_id": self.rubric_id,
            **judgment,
        }
        return judgment

    @weave.op(name="patchpilot_llm_judge_summary")
    def summarize(
        self, score_rows: list[dict[str, Any]]
    ) -> dict[str, float | int]:
        rows = [row for row in score_rows if isinstance(row, dict)]
        total = len(rows)
        if not total:
            return {"cases": 0, "pass_rate": 0.0, "review_rate": 0.0, "block_rate": 0.0}
        return {
            "cases": total,
            "pass_rate": sum(row.get("verdict") == "pass" for row in rows) / total,
            "review_rate": sum(row.get("verdict") == "review" for row in rows) / total,
            "block_rate": sum(row.get("verdict") == "block" for row in rows) / total,
        }


def evaluation_properties(
    *,
    agent_version: str,
    rows: list[Mapping[str, Any]],
    scorer_ids: list[str],
    rubric: Mapping[str, Any],
    judge_model: str,
) -> dict[str, Any]:
    if agent_version not in AGENT_CONFIGS:
        raise ValueError(f"Unknown PatchPilot version: {agent_version}")
    return evaluation_properties_for_application(
        application=build_agent(agent_version),
        rows=rows,
        scorer_ids=scorer_ids,
        rubric=rubric,
        judge_model=judge_model,
    )


def evaluation_properties_for_application(
    *,
    application: PatchPilotAgent,
    rows: list[Mapping[str, Any]],
    scorer_ids: list[str],
    rubric: Mapping[str, Any],
    judge_model: str,
    dataset_name: str = "patchpilot-agent-loop-cases",
    scorer_set_version: str = "agent-loop-scorers-v1",
    release_policy: str = "human-in-the-loop-v1",
    changed_dimension: str = "agent_version",
    contract_id: str = "guided-agent-loop-v1",
) -> dict[str, Any]:
    """Build inspectable comparison metadata for a prepared application."""

    config = application.model_dump()
    return {
        "agent_version": config["agent_version"],
        "patch_strategy": config["patch_strategy"],
        "customer_boundary": config["customer_boundary"],
        "change_summary": config["change_summary"],
        "evidence_strategy": config.get("evidence_strategy", "as_observed"),
        "changed_dimension": changed_dimension,
        "evaluation_contract": contract_id,
        "dataset_name": dataset_name,
        "dataset_fingerprint": dataset_fingerprint(rows),
        "dataset_case_ids": [str(row["case_id"]) for row in rows],
        "deterministic_scorer_ids": list(scorer_ids),
        "scorer_set_version": scorer_set_version,
        "rubric_id": str(rubric["rubric_id"]),
        "judge_model": judge_model,
        "release_policy": release_policy,
    }


async def run_application_evaluation(
    application: PatchPilotAgent,
    rows: list[Mapping[str, Any]],
    config: Mapping[str, str] | None = None,
    *,
    scorer_ids: list[str] | tuple[str, ...] | None = None,
    additional_scorers: list[Any] | tuple[Any, ...] = (),
    additional_scorer_ids: list[str] | tuple[str, ...] = (),
    rubric: Mapping[str, Any] | None = None,
    dataset_name: str = "patchpilot-agent-loop-cases",
    dataset_description: str = "The fixed Agent Loop Workshop dataset.",
    evaluation_name: str = "patchpilot-agent-version-comparison",
    evaluation_description: str = (
        "One reusable evaluation setup: dataset, scorers, LLM-judge rubric, "
        "judge model, and policy stay fixed while the application changes."
    ),
    evaluation_run_prefix: str = "PatchPilot",
    scorer_set_version: str = "agent-loop-scorers-v1",
    release_policy: str = "human-in-the-loop-v1",
    changed_dimension: str = "agent_version",
    contract_id: str = "guided-agent-loop-v1",
    attribute_namespace: str = "agent_loop",
) -> dict[str, Any]:
    """Evaluate any prepared PatchPilot model with an explicit experiment contract."""

    current = require_configuration(config)
    safe_rows = deepcopy([dict(row) for row in rows])
    active_ids, deterministic_scorers = selected_scorers(scorer_ids)
    extra_scorers = list(additional_scorers)
    extra_ids = [str(value) for value in additional_scorer_ids]
    if len(extra_scorers) != len(extra_ids):
        raise ValueError(
            "Provide one additional_scorer_id for each additional scorer"
        )
    active_rubric = deepcopy(dict(rubric)) if rubric is not None else load_rubric()
    if not active_rubric.get("rubric_id") or not active_rubric.get("criteria"):
        raise ValueError("The evaluation rubric needs an ID and at least one criterion")
    properties = evaluation_properties_for_application(
        application=application,
        rows=safe_rows,
        scorer_ids=[*active_ids, *extra_ids],
        rubric=active_rubric,
        judge_model=current["judge_model"],
        dataset_name=dataset_name,
        scorer_set_version=scorer_set_version,
        release_policy=release_policy,
        changed_dimension=changed_dimension,
        contract_id=contract_id,
    )
    client = AsyncOpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=current["api_key"],
        project=f"{current['entity']}/{current['project']}",
        max_retries=2,
        timeout=90,
    )
    judge = BusinessRubricJudge(
        client=client,
        rubric=active_rubric,
        model_id=current["judge_model"],
    )
    dataset = weave.Dataset(
        name=dataset_name,
        description=dataset_description,
        rows=safe_rows,
    )
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    evaluation = weave.Evaluation(
        name=evaluation_name,
        description=evaluation_description,
        dataset=dataset,
        scorers=[*deterministic_scorers, *extra_scorers, judge],
        metadata=properties,
        evaluation_name=(
            f"{evaluation_run_prefix} {application.agent_version.upper()} "
            f"evaluation run · {timestamp}"
        ),
    )
    try:
        with _participant_key(current["api_key"]):
            weave.init(f"{current['entity']}/{current['project']}")
            with weave.attributes(
                {f"{attribute_namespace}.{key}": value for key, value in properties.items()}
            ):
                summary, call = await evaluation.evaluate.call(
                    evaluation,
                    application,
                )
    finally:
        await client.close()
    return {
        "agent_version": application.agent_version,
        "evaluation_url": str(call.ui_url),
        "evaluation_call_id": str(call.id),
        "judge_model": current["judge_model"],
        "judge_calls": len(safe_rows),
        "case_ids": [str(row["case_id"]) for row in safe_rows],
        "scorer_ids": [*active_ids, *extra_ids],
        "comparison_properties": properties,
        "deterministic_results": deterministic_case_results(
            safe_rows, application, active_ids
        ),
        "judge_results": judge.results,
        "summary": summary,
    }


async def run_evaluation(
    agent_version: str,
    rows: list[Mapping[str, Any]],
    config: Mapping[str, str] | None = None,
    *,
    scorer_ids: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Compatibility wrapper for the guided Version 1 and Version 2 comparison."""

    if agent_version not in AGENT_CONFIGS:
        raise ValueError(f"Unknown PatchPilot version: {agent_version}")
    return await run_application_evaluation(
        build_agent(agent_version),
        rows,
        config,
        scorer_ids=scorer_ids,
        evaluation_description=(
            "One reusable evaluation setup: the dataset, three custom Python scorers "
            "with deterministic logic, LLM-judge rubric, judge model, and policy "
            "stay fixed. Only the PatchPilot application version changes."
        ),
    )


def compare_evaluations(
    version_one: Mapping[str, Any], version_two: Mapping[str, Any]
) -> list[dict[str, str]]:
    before_gate = {
        row["case_id"]: row for row in version_one.get("deterministic_results", [])
    }
    after_gate = {
        row["case_id"]: row for row in version_two.get("deterministic_results", [])
    }
    before_judge = {
        row["case_id"]: row for row in version_one.get("judge_results", [])
    }
    after_judge = {
        row["case_id"]: row for row in version_two.get("judge_results", [])
    }
    rows = []
    for case_id in version_one.get("case_ids", []):
        before = before_gate[case_id]
        after = after_gate[case_id]
        rows.append(
            {
                "case_id": case_id,
                "case": str(before["title"]),
                "v1_gate": str(before["gate"]),
                "v2_gate": str(after["gate"]),
                "v1_judge": str(before_judge.get(case_id, {}).get("verdict", "missing")),
                "v2_judge": str(after_judge.get(case_id, {}).get("verdict", "missing")),
                "agent_changed": "yes" if before["output"] != after["output"] else "no",
            }
        )
    return rows


def _add_annotation(
    client: Any,
    *,
    target_call_id: str,
    config: Mapping[str, Any],
    value: str,
) -> dict[str, str]:
    allowed = list(config["values"].values())
    if value not in allowed:
        raise ValueError("Invalid annotation value")
    spec = weave.AnnotationSpec(
        name=str(config["name"]),
        description=str(config["description"]),
        field_schema={"type": "string", "enum": allowed},
        unique_among_creators=True,
    )
    spec_ref = weave.publish(spec, str(config["name"]))
    annotation_uri = str(spec_ref.uri())
    target_call = client.get_call(target_call_id)
    feedback_id = target_call.feedback.add(
        feedback_type=f"wandb.annotation.{config['name']}",
        payload={"value": value},
        annotation_ref=annotation_uri,
    )
    return {
        "feedback_id": feedback_id,
        "annotation_ref": annotation_uri,
        "target_url": str(target_call.ui_url),
    }


def annotate_trace_risk(
    trace_call_id: str,
    risk_code: str,
    config: Mapping[str, str] | None = None,
) -> dict[str, str]:
    current = require_configuration(config)
    if risk_code not in RISK_ANNOTATION["values"]:
        raise ValueError("Choose a valid observed risk")
    value = RISK_ANNOTATION["values"][risk_code]
    with _participant_key(current["api_key"]):
        client = weave.init(f"{current['entity']}/{current['project']}")
        return _add_annotation(
            client,
            target_call_id=trace_call_id,
            config=RISK_ANNOTATION,
            value=value,
        )


def human_annotation_values(decision: Mapping[str, Any]) -> dict[str, str]:
    source_values = {
        "decision": decision.get("final_decision"),
        "confidence": decision.get("confidence"),
        "scope": decision.get("permitted_scope"),
    }
    translated = {}
    for field, source_value in source_values.items():
        values = HUMAN_ANNOTATION_FIELDS[field]["values"]
        if source_value not in values:
            raise ValueError(f"Invalid human annotation value for {field}")
        translated[field] = values[source_value]
    return translated


async def record_human_review(
    decision: Mapping[str, Any],
    config: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    current = require_configuration(config)
    payload = deepcopy(dict(decision))
    required = {
        "initial_decision",
        "final_decision",
        "participant_role",
        "dataset_uri",
        "scorer_ids",
        "rubric_id",
        "reviewed_versions",
        "permitted_scope",
        "reviewer",
        "confidence",
        "trace_call_id",
    }
    missing = sorted(key for key in required if not payload.get(key))
    if missing:
        raise ValueError(f"Complete the human review record: {', '.join(missing)}")

    with _participant_key(current["api_key"]):
        client = weave.init(f"{current['entity']}/{current['project']}")
        annotation_values = human_annotation_values(payload)
        payload["annotations"] = annotation_values

        @weave.op(name="patchpilot_human_in_the_loop_record")
        async def save_review(review: dict[str, Any]) -> dict[str, Any]:
            return {
                **review,
                "record_type": "human_in_the_loop_review",
                "recorded_at": datetime.now(UTC).isoformat(),
            }

        saved, call = await save_review.call(payload)
        receipts = {}
        annotation_error = ""
        try:
            for field, value in annotation_values.items():
                receipts[field] = _add_annotation(
                    client,
                    target_call_id=str(payload["trace_call_id"]),
                    config=HUMAN_ANNOTATION_FIELDS[field],
                    value=value,
                )
        except Exception as error:
            annotation_error = safe_error_text(error)
    return {
        "record": saved,
        "call_id": str(call.id),
        "record_url": str(call.ui_url),
        "annotation_receipts": receipts,
        "annotation_error": annotation_error,
    }
