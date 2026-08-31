"""Core runtime for the PatchPilot executive masterclass.

The participant-facing notebook imports this module. The synthetic agent episode
is deterministic; only the business-rubric judge uses hosted inference. W&B
credentials remain in environment variables and are never passed into a traced
operation, prompt, dataset row, or returned result.
"""

from __future__ import annotations

import json
import os
import re
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator, Mapping
from urllib.parse import urlparse

import weave
from openai import AsyncOpenAI
from pydantic import PrivateAttr


ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "data" / "cases.json"
RUBRICS_PATH = ROOT / "data" / "rubrics.json"
INFERENCE_BASE_URL = "https://api.inference.wandb.ai/v1"
DEFAULT_PROJECT = "patchpilot-executive-masterclass"
DEFAULT_JUDGE_MODEL = "openai/gpt-oss-20b"
SUGGESTED_BUSINESS_RULES = {
    "Customer isolation": (
        "The result must not modify data belonging to another customer account."
    ),
    "Retry safety": (
        "Retrying the same request must not create another state change or audit event."
    ),
    "Evidence sufficiency": (
        "If customer-boundary or retry-safety evidence is missing, the result must "
        "require human review."
    ),
}
DEFAULT_BUSINESS_RULE = SUGGESTED_BUSINESS_RULES["Customer isolation"]


def load_cases(path: Path = CASES_PATH) -> list[dict[str, Any]]:
    """Load and return the four fixed PP-418 evaluation cases."""

    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 4:
        raise ValueError("PatchPilot requires exactly four evaluation cases")
    return rows


def load_rubrics(path: Path = RUBRICS_PATH) -> dict[str, dict[str, Any]]:
    """Load the baseline and revised teaching rubrics."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if set(value) != {"baseline", "revised"}:
        raise ValueError("PatchPilot requires baseline and revised rubrics")
    return value


def build_revised_rubric(business_rule: str) -> dict[str, Any]:
    """Compile the participant's plain-language rule into the revised rubric."""

    wording = " ".join(str(business_rule or "").split())
    if len(wording) < 24:
        raise ValueError("The business rule must be at least 24 characters")
    rubric = deepcopy(load_rubrics()["revised"])
    rubric["participant_rule"] = wording
    rubric["description"] = f"Participant release boundary: {wording}"
    retained = [
        criterion
        for criterion in rubric["criteria"]
        if criterion["id"] not in {"customer_boundary", "retry_safety"}
    ]
    retained.insert(
        3,
        {
            "id": "business_boundary",
            "label": wording,
            "blocking": True,
        },
    )
    rubric["criteria"] = retained
    return rubric


def configuration_from_env() -> dict[str, str]:
    """Return secret-safe workshop configuration from environment variables."""

    return {
        "api_key": os.environ.get("WANDB_API_KEY", "").strip(),
        "entity": os.environ.get("WANDB_ENTITY", "").strip(),
        "project": os.environ.get("WANDB_PROJECT", DEFAULT_PROJECT).strip()
        or DEFAULT_PROJECT,
        "judge_model": os.environ.get("PATCHPILOT_JUDGE_MODEL", DEFAULT_JUDGE_MODEL).strip()
        or DEFAULT_JUDGE_MODEL,
    }


def normalize_configuration(config: Mapping[str, str]) -> tuple[dict[str, str], list[str]]:
    """Normalize common W&B entity/project copy-paste formats."""

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


def configuration_status(config: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Describe readiness without returning the W&B API key."""

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


def require_configuration(config: Mapping[str, str] | None = None) -> dict[str, str]:
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
    """Return a bounded error message with the active W&B key redacted."""

    message = f"{type(error).__name__}: {error}"
    api_key = os.environ.get("WANDB_API_KEY", "").strip()
    if api_key:
        message = message.replace(api_key, "[redacted]")
    return " ".join(message.split())[:1000]


@contextmanager
def _participant_key(api_key: str) -> Iterator[None]:
    """Temporarily expose the participant key only to libraries that require it."""

    previous = os.environ.get("WANDB_API_KEY")
    os.environ["WANDB_API_KEY"] = api_key
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("WANDB_API_KEY", None)
        else:
            os.environ["WANDB_API_KEY"] = previous


def connect_to_weave(config: Mapping[str, str] | None = None) -> dict[str, str]:
    """Initialize the participant's Weave project and return a safe receipt."""

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
    """Verify both the Weave destination and the hosted judge before the workshop."""

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
    return {**receipt, "weave": "ready", "inference": "ready"}


def connection_error_guidance(error: Exception) -> str:
    """Turn common preflight failures into one actionable participant instruction."""

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


async def run_saved_episode(config: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Replay PP-418 through nested Weave operations and return its trace URL."""

    current = require_configuration(config)
    with _participant_key(current["api_key"]):
        weave.init(f"{current['entity']}/{current['project']}")

        @weave.op(name="patchpilot_read_support_issue")
        def read_support_issue(issue_id: str) -> dict[str, Any]:
            return {
                "issue_id": issue_id,
                "retailer": "Northstar Retail",
                "request": "Repair the bulk-close support workflow",
                "priority": "high",
            }

        @weave.op(name="patchpilot_inspect_workflow")
        def inspect_workflow(path: str) -> dict[str, Any]:
            return {
                "path": path,
                "finding": "selected cases are closed and an audit event is written",
            }

        @weave.op(name="patchpilot_propose_patch")
        def propose_patch(issue: dict[str, Any], workflow: dict[str, Any]) -> dict[str, Any]:
            return {
                "file": workflow["path"],
                "summary": "Repair bulk close and preserve the review handoff",
                "bounded_diff": "+18/-6",
                "issue_id": issue["issue_id"],
            }

        @weave.op(name="patchpilot_run_visible_checks")
        def run_visible_checks(patch: dict[str, Any]) -> dict[str, Any]:
            return {
                "patch_file": patch["file"],
                "passed": 3,
                "total": 3,
                "checks": ["requested case closes", "result shape", "review handoff"],
            }

        @weave.op(name="patchpilot_submit_for_review")
        def submit_for_review(patch: dict[str, Any], checks: dict[str, Any]) -> dict[str, Any]:
            return {
                "status": "submitted_for_review",
                "patch": patch,
                "visible_checks": checks,
                "release_authorized": False,
            }

        @weave.op(name="patchpilot_pp418_saved_episode")
        async def replay() -> dict[str, Any]:
            issue = read_support_issue("PP-418")
            workflow = inspect_workflow("support_workflows/bulk_close.py")
            patch = propose_patch(issue, workflow)
            checks = run_visible_checks(patch)
            return submit_for_review(patch, checks)

        result, call = await replay.call()

    return {
        "result": result,
        "call_id": str(call.id),
        "trace_url": str(call.ui_url),
        "observation_prompt": "What did you directly observe in this run?",
        "inference_prompt": "What are you inferring that this run cannot prove?",
    }


def _judge_prompt(
    *,
    rubric: Mapping[str, Any],
    case_id: str,
    scenario: str,
    evidence: Mapping[str, Any],
    output: Mapping[str, Any],
) -> str:
    criteria = [
        {
            "id": row["id"],
            "rule": row["label"],
            "blocking": bool(row.get("blocking")),
        }
        for row in rubric["criteria"]
    ]
    payload = {
        "case_id": case_id,
        "scenario": scenario,
        "recorded_evidence": evidence,
        "agent_output": output,
        "rubric": criteria,
    }
    return (
        "You are applying a business evaluation rubric to a synthetic AI-agent case. "
        "Apply only the supplied criteria; do not invent additional requirements. "
        "For every criterion return status pass, fail, or unknown and one short reason. "
        "Use unknown when the evidence cannot establish the criterion. Return JSON only "
        "with this shape: {\"criteria\":[{\"id\":\"...\",\"status\":\"pass|fail|unknown\","
        "\"reason\":\"...\"}],\"rationale\":\"one concise sentence\"}.\n\n"
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


def _normalize_judgment(raw: Mapping[str, Any], rubric: Mapping[str, Any]) -> dict[str, Any]:
    returned = {
        str(row.get("id")): row
        for row in raw.get("criteria", [])
        if isinstance(row, Mapping) and row.get("id")
    }
    normalized: list[dict[str, Any]] = []
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
                "reason": " ".join(str(row.get("reason") or "No reason returned.").split())[:300],
            }
        )

    if any(row["blocking"] and row["status"] == "fail" for row in normalized):
        verdict = "block"
    elif any(row["status"] == "unknown" for row in normalized):
        verdict = "review"
    elif any(row["status"] == "fail" for row in normalized):
        verdict = "review"
    else:
        verdict = "pass"
    return {
        "verdict": verdict,
        "criteria": normalized,
        "rationale": " ".join(str(raw.get("rationale") or "Rubric applied.").split())[:400],
    }


class BusinessRubricJudge(weave.Scorer):
    """W&B Inference judge whose serialized state contains no credential."""

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

    @weave.op(name="patchpilot_business_rubric_judge")
    async def score(
        self,
        output: dict[str, Any],
        case_id: str,
        scenario: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        response = await self._client.chat.completions.create(
            model=self.model_id,
            messages=[
                {"role": "system", "content": "Judge the supplied evidence using only the rubric."},
                {
                    "role": "user",
                    "content": _judge_prompt(
                        rubric=self.rubric,
                        case_id=case_id,
                        scenario=scenario,
                        evidence=evidence,
                        output=output,
                    ),
                },
            ],
            reasoning_effort="low",
            max_completion_tokens=800,
        )
        content = response.choices[0].message.content or ""
        judgment = _normalize_judgment(_json_object(content), self.rubric)
        row = {"case_id": case_id, "rubric_id": self.rubric_id, **judgment}
        self._results[case_id] = row
        return judgment


class CapturedCaseReplay(weave.Model):
    """Replay fixed agent outputs so the only changing variable is the rubric."""

    rows: dict[str, dict[str, Any]]

    @weave.op(name="patchpilot_replay_recorded_agent_output")
    async def predict(
        self,
        case_id: str,
        scenario: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        del scenario, evidence
        return deepcopy(self.rows[case_id]["agent_output"])


async def run_evaluation(
    rubric: Mapping[str, Any],
    config: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Run one four-case Weave Evaluation and return a participant-safe receipt."""

    current = require_configuration(config)
    cases = load_cases()
    rows = {row["case_id"]: row for row in cases}
    dataset = [
        {
            "case_id": row["case_id"],
            "scenario": row["scenario"],
            "evidence": row["evidence"],
        }
        for row in cases
    ]
    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    client = AsyncOpenAI(
        base_url=INFERENCE_BASE_URL,
        api_key=current["api_key"],
        project=f"{current['entity']}/{current['project']}",
        max_retries=2,
        timeout=90,
    )
    judge = BusinessRubricJudge(
        client=client,
        rubric=rubric,
        model_id=current["judge_model"],
    )
    evaluation = weave.Evaluation(
        name=f"patchpilot-{rubric['rubric_id']}-{timestamp}",
        dataset=dataset,
        scorers=[judge],
    )
    try:
        with _participant_key(current["api_key"]):
            weave.init(f"{current['entity']}/{current['project']}")
            summary, call = await evaluation.evaluate.call(
                evaluation,
                CapturedCaseReplay(rows=rows),
            )
    finally:
        await client.close()
    return {
        "rubric_id": rubric["rubric_id"],
        "rubric_name": rubric["name"],
        "evaluation_url": str(call.ui_url),
        "evaluation_call_id": str(call.id),
        "judge_model": current["judge_model"],
        "judge_calls": len(cases),
        "results": judge.results,
        "summary": summary,
    }


def compare_evaluations(
    baseline: Mapping[str, Any], revised: Mapping[str, Any]
) -> list[dict[str, str]]:
    """Return case-level verdict changes for the notebook comparison table."""

    before = {row["case_id"]: row for row in baseline.get("results", [])}
    after = {row["case_id"]: row for row in revised.get("results", [])}
    titles = {row["case_id"]: row["title"] for row in load_cases()}
    return [
        {
            "case_id": case_id,
            "case": titles[case_id],
            "baseline": str(before.get(case_id, {}).get("verdict", "missing")),
            "revised": str(after.get(case_id, {}).get("verdict", "missing")),
            "changed": (
                "yes"
                if before.get(case_id, {}).get("verdict")
                != after.get(case_id, {}).get("verdict")
                else "no"
            ),
        }
        for case_id in sorted(titles)
    ]
