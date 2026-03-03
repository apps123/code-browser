# Implementation Plan: Repository Analysis Readme Generation

**Branch**: `001-repo-analysis` | **Date**: 2026-03-02 | **Spec**: `specs/001-repo-analysis/spec.md`  
**Input**: Feature specification from `specs/001-repo-analysis/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

This feature adds a CLI-driven tool that, given either a GitHub/Enterprise GitHub organization URL/identifier or a single repository URL/identifier, clones or updates the corresponding repositories from their main branch into a working folder and creates one folder per repository under `code-browser`.  

Each repository folder will contain a generated `README.md` plus optional subfolders (Documentation, Features, Code Documentation, Tests) that together summarize repository health, ownership, tech stack, architecture, features, documentation, tests, and security posture, using a locally configured AI assistant for narrative summarization.

## Technical Context

**Language/Version**: Python 3.11  

**Primary Dependencies**:  
- CLI framework: `typer` (for a modern, well-typed CLI)  
- Git / GitHub access: `GitPython` (local git operations), `PyGithub` (GitHub/Enterprise GitHub API access)  
- HTTP / utilities: `requests`, `pydantic` (for typed configuration and data models)  
- Security scanning integration (invoked via subprocess/CLI where available):  
  - `bandit` (SAST for Python)  
  - `pip-audit` or `safety` (SCA / dependency vulnerability scanning)  
  - `detect-secrets` (secrets detection)  
  - External tools such as Trivy and Checkov for container and IaC scanning  

**Storage**: Local filesystem (repository working folder and `code-browser` directory for generated docs)  

**Testing**: `pytest` with `pytest-cov` (backed by `coverage.py`) for unit, integration, and contract tests  

**Target Platform**: Developer and CI environments on Unix-like systems (macOS/Linux)  

**Project Type**: CLI tool plus supporting library code  

**Performance Goals**: Complete a typical single-repository scan (including cloning, analysis, and README generation) in a few minutes for average-sized services; organization-wide scans should make steady, observable progress and avoid blocking other tooling.  

**Constraints**: Must be safe to run repeatedly, avoid destructive Git operations, and handle large organizations by processing repositories incrementally with clear progress and error reporting.  

**Scale/Scope**: Must handle organizations with at least low hundreds of repositories and repositories with typical monolith or multi-service layouts without manual per-repo configuration.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Constitution file not found at `.specify/memory/constitution.md`; applying default gates:
  - Keep the design as a single CLI-oriented tool within this repository.
  - Prefer simple, observable flows for cloning, analysis, and README generation.
  - Avoid unnecessary technology proliferation; reuse existing project tooling where practical.
  - Ensure security scanning and AI usage follow least-privilege and transparency principles.

All gates are currently satisfied at the planning level; revisit after detailing data model, contracts, and quickstart flows.

## Project Structure

### Documentation (this feature)

```text
specs/001-repo-analysis/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
cli/                      # Entry point(s) for the repository analysis CLI
lib/ or modules/          # Core analysis, summarization, and security scan orchestration
tools/ or scripts/        # Helper scripts for invoking scans in CI or batch mode

specs/
└── 001-repo-analysis/    # Feature documentation (spec, plan, research, data model, contracts, quickstart, tasks)

tests/
├── unit/                 # Unit tests for analysis and summarization logic
├── integration/          # End-to-end scans against sample or fixture repositories
└── contract/             # Contract-level tests for CLI arguments and outputs
```

**Structure Decision**: Treat this as a CLI-focused feature within the existing repository, with `cli/` hosting entry points, `lib/` (or equivalent modules) containing analysis logic, `tools/` for automation scripts, and all feature documentation under `specs/001-repo-analysis/`. The exact directories may be adapted to match the current repo layout while preserving this separation of concerns.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
