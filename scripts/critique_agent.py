#!/usr/bin/env python3
"""
Critique Agent — reads DESIGN.md, explores the English Scorer codebase, and
produces a structured critique with prioritised suggestions.

Usage (from project root):
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...
    python3 scripts/critique_agent.py

    # Save the report to a file:
    python3 scripts/critique_agent.py > critique_report.md

Requirements:
    anthropic Python package  (pip install anthropic)
    ANTHROPIC_API_KEY environment variable
"""

import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit(
        "Error: 'anthropic' package not found.\n"
        "Install it with:  pip install anthropic"
    )

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def _safe_resolve(path: str) -> Path | None:
    """Resolve a project-relative path, rejecting traversal outside root."""
    target = (PROJECT_ROOT / path).resolve()
    try:
        target.relative_to(PROJECT_ROOT)
        return target
    except ValueError:
        return None


def read_file(path: str) -> str:
    target = _safe_resolve(path)
    if target is None:
        return f"Error: path outside project root: {path}"
    try:
        return target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error reading {path}: {e}"


def list_directory(path: str) -> str:
    target = _safe_resolve(path)
    if target is None:
        return f"Error: path outside project root: {path}"
    try:
        entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name))
        lines = [
            f"{'DIR ' if e.is_dir() else 'FILE'} {e.relative_to(PROJECT_ROOT)}"
            for e in entries
        ]
        return "\n".join(lines) or "(empty directory)"
    except FileNotFoundError:
        return f"Error: directory not found: {path}"
    except Exception as e:
        return f"Error: {e}"


def search_files(glob_pattern: str, search_term: str) -> str:
    results: list[str] = []
    try:
        for filepath in sorted(PROJECT_ROOT.glob(glob_pattern)):
            if not filepath.is_file():
                continue
            try:
                text = filepath.read_text(encoding="utf-8")
            except Exception:
                continue
            rel = filepath.relative_to(PROJECT_ROOT)
            for i, line in enumerate(text.splitlines(), 1):
                if search_term.lower() in line.lower():
                    results.append(f"{rel}:{i}: {line.strip()}")
                    if len(results) >= 60:
                        results.append("... (truncated at 60 results)")
                        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
    return "\n".join(results) if results else f"No matches for '{search_term}' in {glob_pattern}"


TOOL_HANDLERS = {
    "read_file": lambda inp: read_file(inp["path"]),
    "list_directory": lambda inp: list_directory(inp["path"]),
    "search_files": lambda inp: search_files(inp["glob_pattern"], inp["search_term"]),
}

TOOLS: list[dict] = [
    {
        "name": "read_file",
        "description": (
            "Read the full contents of a file. "
            "Path is relative to the project root (e.g. 'DESIGN.md', 'backend/app/main.py')."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path relative to the project root.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "list_directory",
        "description": (
            "List files and subdirectories inside a directory. "
            "Path is relative to the project root (e.g. '.' or 'backend/app/scoring')."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory path relative to the project root.",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "search_files",
        "description": (
            "Search for a term across files matching a glob pattern. "
            "Returns matching lines with file:line context (case-insensitive, max 60 results)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "glob_pattern": {
                    "type": "string",
                    "description": (
                        "Glob pattern from the project root, "
                        "e.g. 'backend/**/*.py' or 'frontend/src/**/*.jsx'."
                    ),
                },
                "search_term": {
                    "type": "string",
                    "description": "Term to search for (case-insensitive).",
                },
            },
            "required": ["glob_pattern", "search_term"],
        },
    },
]

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM = """\
You are a senior software architect reviewing the English Scorer web application.

Your task is to produce a thorough, honest critique comparing the actual codebase
against DESIGN.md.

Steps:
1. Read DESIGN.md in full to understand the goals, architecture, phases, and
   requirements.
2. Explore the project structure with list_directory, then read key source files
   in both the backend (FastAPI/Python) and frontend (React/Vite).
3. Compare the implementation against the design across: feature completeness,
   architecture decisions, code quality, testing coverage, and missing functionality.
4. Write a detailed critique report.

Report structure (use these headings in order):

## Executive Summary
One-paragraph overall assessment.

## Phase Completion
For each phase in DESIGN.md, state: Done / Partially done / Not started.
List what is complete and what remains.

## Feature Gaps
Specific features described in DESIGN.md that are missing or incomplete.
Reference the DESIGN.md section number and the relevant source path.

## Design Deviations
Where the implementation meaningfully differs from the design (note whether
each deviation is an improvement, a pragmatic shortcut, or a concern).

## Quality & Technical Observations
Code quality, test coverage, security, performance, error handling,
accessibility, and any technical debt worth noting.

## Prioritised Recommendations
Numbered list of actionable suggestions, highest impact first.
For each: what to do, why it matters, rough effort (low/medium/high).

Be specific — cite DESIGN.md section numbers and actual file paths throughout.\
"""

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def run() -> None:
    client = anthropic.Anthropic()

    messages: list[dict] = [
        {
            "role": "user",
            "content": (
                "Critique the English Scorer application against DESIGN.md. "
                "Read DESIGN.md and explore the codebase thoroughly, then produce "
                "a structured critique report with prioritised recommendations."
            ),
        }
    ]

    print("=" * 70, file=sys.stderr)
    print("English Scorer — Critique Agent", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(file=sys.stderr)

    turn = 0
    max_turns = 40

    while turn < max_turns:
        turn += 1

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=SYSTEM,
            tools=TOOLS,
            messages=messages,
        ) as stream:
            response = stream.get_final_message()

        # Final response — print and exit
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text" and block.text.strip():
                    print(block.text)
            break

        if response.stop_reason != "tool_use":
            # Unexpected stop — print whatever text we have and exit
            for block in response.content:
                if block.type == "text" and block.text.strip():
                    print(block.text)
            print(f"\n[Stopped: unexpected stop_reason={response.stop_reason}]", file=sys.stderr)
            break

        # Execute tool calls
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            handler = TOOL_HANDLERS.get(block.name)
            result = handler(block.input) if handler else f"Unknown tool: {block.name}"

            # Show progress on stderr so stdout stays clean for the report
            arg_preview = next(iter(block.input.values()), "") if block.input else ""
            print(f"  → {block.name}({arg_preview!r})", file=sys.stderr)

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})

    else:
        print(f"\n[Stopped: reached {max_turns}-turn limit]", file=sys.stderr)


if __name__ == "__main__":
    run()
