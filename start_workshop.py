"""Secure first-run configuration and launcher for PatchPilot."""

from __future__ import annotations

import argparse
import getpass
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
ENV_PATH = ROOT / ".env"
WORKSHOP_PATH = ROOT / "workshop.py"
DEFAULT_PROJECT = "patchpilot-executive-masterclass"
DEFAULT_MODEL = "openai/gpt-oss-20b"
SAFE_SLUG = re.compile(r"^[A-Za-z0-9_.-]+$")
SAFE_MODEL = re.compile(r"^[A-Za-z0-9_./-]+$")


def parse_env(path: Path = ENV_PATH) -> dict[str, str]:
    """Read the four workshop settings without executing the file."""

    if not path.exists():
        return {}
    if path.is_symlink():
        raise ValueError(f"Refusing to read symlinked credential file: {path}")

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        if name in {
            "WANDB_API_KEY",
            "WANDB_ENTITY",
            "WANDB_PROJECT",
            "PATCHPILOT_JUDGE_MODEL",
        }:
            values[name] = value.strip().strip('"').strip("'")
    return values


def normalize_entity(value: str) -> str:
    """Accept a team slug, entity/project path, or wandb.ai URL."""

    candidate = value.strip()
    if "://" in candidate:
        parsed = urlparse(candidate)
        parts = [part for part in parsed.path.split("/") if part]
        candidate = parts[0] if parts else ""
    elif "/" in candidate:
        candidate = candidate.split("/", 1)[0]

    if not candidate or not SAFE_SLUG.fullmatch(candidate):
        raise ValueError(
            "Enter only a W&B username or team slug, such as acme-team."
        )
    return candidate


def validate_project(value: str) -> str:
    candidate = value.strip()
    if not candidate or not SAFE_SLUG.fullmatch(candidate):
        raise ValueError(
            "The project must contain only letters, numbers, dots, underscores, or hyphens."
        )
    return candidate


def validate_model(value: str) -> str:
    candidate = value.strip()
    if not candidate or not SAFE_MODEL.fullmatch(candidate):
        raise ValueError("The judge model ID contains unsupported characters.")
    return candidate


def validate_key(value: str) -> str:
    candidate = value.strip()
    if len(candidate) < 16 or any(character.isspace() for character in candidate):
        raise ValueError("The W&B API key appears incomplete.")
    return candidate


def prompt_until_valid(
    label: str,
    validator,
    *,
    default: str = "",
    hidden: bool = False,
) -> str:
    while True:
        suffix = f" [{default}]" if default else ""
        prompt = f"{label}{suffix}: "
        raw_value = getpass.getpass(prompt) if hidden else input(prompt)
        value = raw_value or default
        try:
            return validator(value)
        except ValueError as error:
            print(f"  {error}")


def configuration_ready(values: dict[str, str]) -> bool:
    try:
        validate_key(values.get("WANDB_API_KEY", ""))
        normalize_entity(values.get("WANDB_ENTITY", ""))
        validate_project(values.get("WANDB_PROJECT", ""))
        validate_model(values.get("PATCHPILOT_JUDGE_MODEL", ""))
    except ValueError:
        return False
    return True


def write_env(values: dict[str, str], path: Path = ENV_PATH) -> None:
    """Write the local credential file with owner-only permissions where supported."""

    if path.exists() and path.is_symlink():
        raise ValueError(f"Refusing to overwrite symlinked credential file: {path}")

    content = (
        "# Created locally by start_workshop.py. Never commit this file.\n"
        f"WANDB_API_KEY={values['WANDB_API_KEY']}\n"
        f"WANDB_ENTITY={values['WANDB_ENTITY']}\n"
        f"WANDB_PROJECT={values['WANDB_PROJECT']}\n"
        f"PATCHPILOT_JUDGE_MODEL={values['PATCHPILOT_JUDGE_MODEL']}\n"
    )
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    if os.name != "nt":
        path.chmod(0o600)


def configure(*, force: bool = False) -> dict[str, str]:
    existing = parse_env()
    if not force and configuration_ready(existing):
        values = {
            "WANDB_API_KEY": validate_key(existing["WANDB_API_KEY"]),
            "WANDB_ENTITY": normalize_entity(existing["WANDB_ENTITY"]),
            "WANDB_PROJECT": validate_project(existing["WANDB_PROJECT"]),
            "PATCHPILOT_JUDGE_MODEL": validate_model(
                existing["PATCHPILOT_JUDGE_MODEL"]
            ),
        }
        # Normalize the file and repair overly broad permissions from manual setup.
        write_env(values)
        return values

    if not sys.stdin.isatty():
        raise RuntimeError(
            "Interactive configuration requires a terminal. Run this command in Terminal or PowerShell."
        )

    print("\nPatchPilot first-time setup")
    print("Your API key is entered privately and saved only in the local .env file.")
    print("Find or create a key at https://wandb.ai/authorize\n")

    api_key = ""
    if not force:
        try:
            api_key = validate_key(existing.get("WANDB_API_KEY", ""))
            print("Existing local API key found (not displayed).")
        except ValueError:
            pass
    if not api_key:
        api_key = prompt_until_valid(
            "W&B API key (hidden)",
            validate_key,
            hidden=True,
        )
    entity = prompt_until_valid(
        "W&B username, team slug, or project URL",
        normalize_entity,
        default=existing.get("WANDB_ENTITY", ""),
    )
    project = prompt_until_valid(
        "W&B project",
        validate_project,
        default=existing.get("WANDB_PROJECT", DEFAULT_PROJECT) or DEFAULT_PROJECT,
    )
    model = prompt_until_valid(
        "Judge model",
        validate_model,
        default=existing.get("PATCHPILOT_JUDGE_MODEL", DEFAULT_MODEL) or DEFAULT_MODEL,
    )
    values = {
        "WANDB_API_KEY": api_key,
        "WANDB_ENTITY": entity,
        "WANDB_PROJECT": project,
        "PATCHPILOT_JUDGE_MODEL": model,
    }
    write_env(values)
    return values


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Configure PatchPilot securely and launch the participant notebook."
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Replace the current local workshop configuration.",
    )
    parser.add_argument(
        "--configure-only",
        action="store_true",
        help="Validate or create .env without launching Marimo.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Start without opening a browser automatically.",
    )
    arguments = parser.parse_args()

    try:
        values = configure(force=arguments.reset)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"\nSetup could not continue: {error}", file=sys.stderr)
        return 2

    print("\nConfiguration ready.")
    print(f"  Entity: {values['WANDB_ENTITY']}")
    print(f"  Project: {values['WANDB_PROJECT']}")
    print(f"  Judge: {values['PATCHPILOT_JUDGE_MODEL']}")
    print("  API key: saved privately (not displayed)")

    if arguments.configure_only:
        print("\nNext: uv run --locked python start_workshop.py")
        return 0

    if not WORKSHOP_PATH.is_file():
        print(f"Workshop notebook not found: {WORKSHOP_PATH}", file=sys.stderr)
        return 2

    print("\nStarting PatchPilot. Keep this terminal open during the workshop.")
    print("After the notebook opens, click Run workshop preflight.\n")
    command = [
        sys.executable,
        "-m",
        "marimo",
        "run",
        str(WORKSHOP_PATH),
        "--no-sandbox",
    ]
    if arguments.headless:
        command.append("--headless")
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            check=False,
        )
    except KeyboardInterrupt:
        print("\nWorkshop stopped.")
        return 130
    return int(completed.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
