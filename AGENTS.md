# Agent instructions

This repository is a study path built with [StudyForge](https://github.com/Chamba-Lab/studyforge) (version in `studyforge.toml`). It is the single source of instructions for any AI agent; `CLAUDE.md` only imports it. It is also the StudyForge showcase: it must stay an exemplary application of the method.

## Start here (fresh session)
1. Read this file, `SYLLABUS.md` (plan, status, notes for the next labs) and `docs/lessons.md`.
2. Run `git status` and `git log --oneline -15` to see where the work stands.
3. If the StudyForge skill is installed, use it: `build` for the next ⬜ `pending` item in syllabus order (do not ask which), `feedback` when a learner reports on a lab, `review` to audit or upgrade.
4. Without the skill, follow the rules below and the method at https://github.com/Chamba-Lab/studyforge/tree/master/skills/studyforge.

## Context
- **Learner:** knows basic Python (functions, classes, modules) and has written few or no automated tests. Community course of [Chamba Lab](https://chambalab.org), Spanish-speaking.
- **Goal:** write and maintain automated tests with professional judgment; tests that fail for the right reason.
- **Stack:** Python 3.12+ (verified on 3.12 and 3.15), pytest 9.2.0, pytest-cov 7.1.0. Versions live in `requirements.txt` and are upgraded together.
- **Learner environment:** Windows first (PowerShell, then Bash); everything must also work on macOS and Linux.

## Working agreement
- Chat in the learner's language; lab content in Spanish (`language.content = "es"`, neutral Spanish, no local slang); code, identifiers, folders and commits in English.
- Decide and recommend; do not hand decisions back. Scope, depth and anything outward-facing are the maintainer's call.
- One lab at a time. Labs stay 🟨 `built` until a learner solved them and their feedback was applied; only then ✅ `done`.
- Report outcomes faithfully: what passed, what failed, what was not run.

## Repository rules
- Layout, names and IDs follow StudyForge (`labs/NN-block/NN-slug`, `project-<domain>` last in its block; IDs freeze once `built`).
- `master` is the clean template. Learners keep solutions in `solutions/<name>` or a fork; never commit solved starters here.
- Conventional Commits: `feat(lab-1.2): …`, `feat(project-1): …`, `fix(lab-…)`, `docs(syllabus): …`.
- Never commit secrets or `.env`. No byte-order marks. LF line endings (`.gitattributes`).
- Every claim in a lab was run on the pinned versions. `python tools/verify.py --lab <ID>` must pass before a lab is `built`.

## Stack specifics
- **One virtual environment** at the repository root (`.venv`, from `requirements.txt`). Each lab variant has its own `pyproject.toml` with only `[tool.pytest]` (native TOML configuration, pytest 9+) and `pythonpath = ["."]`; no packaging.
- **Projects are atomic:** `project-*/reference` declares its own dependencies in its `pyproject.toml` and does not rely on lab code.
- **Testing labs are turned around:** the production code is finished and the learner writes tests. Each challenge validates the learner's tests with a **mutant hunt** (`tests/test_mutant_hunt.py`): the learner's test file must pass against the real module and fail against each mutant in `tests/mutants/<id>/`. Starter test stubs call `pytest.skip("TODO …")`, so a starter is red only through the hunt, and each task turns its own mutants green (progressive check works).
- Run commands with `python -m pytest`, never bare `pytest` (it picks the active interpreter and puts the current folder on `sys.path` consistently).
- Verify a lab: activate the virtual environment, then `python tools/verify.py --lab <ID>`.

## Upgrading the stack
1. Read the pytest changelog and the deprecations page; check Python support.
2. Change `requirements.txt`, `SETUP.md`, `SYLLABUS.md`, this file and the CI matrix.
3. Run `python tools/verify.py` on every supported Python; re-check every claim that quotes the old version (outputs, messages).
4. Commit `chore: upgrade pytest to <version>`.

## Lessons
Stack-specific lessons live in `docs/lessons.md`; decisions in `docs/decisions.md`. Read both before building.
