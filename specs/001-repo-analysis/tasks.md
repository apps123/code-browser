# Tasks: Repository Analysis Readme Generation

**Input**: Design documents from `specs/001-repo-analysis/`  
**Prerequisites**: `plan.md` (required), `spec.md` (required for user stories)

**Tests**: The spec places strong emphasis on observability of outcomes and security posture, so this plan includes targeted tests for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions (relative to repo root)

## Path Conventions

- CLI entrypoints and orchestration: `cli/`, `lib/`
- Specs and feature docs: `specs/001-repo-analysis/`
- Tests: `tests/unit/`, `tests/integration/`, `tests/contract/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for the repository analysis CLI.

- [ ] T001 Create initial Python project structure for CLI in `cli/` and core library code in `lib/`
- [ ] T002 Initialize Python project metadata and dependencies in `pyproject.toml` using `typer`, `GitPython`, `PyGithub`, `requests`, `pydantic`, `pytest`, `pytest-cov`, and tooling dependencies
- [ ] T003 [P] Configure linting and formatting tools for Python (e.g., ruff/flake8, black) in `pyproject.toml` or config files under `.config/`
- [ ] T004 [P] Set up basic logging configuration for the CLI and library in `lib/logging_config.py`
- [ ] T005 Configure `pytest` and `pytest-cov` defaults (including coverage thresholds and test discovery) in `pyproject.toml` or `pytest.ini`
- [ ] T006 Document development setup and how to run the CLI and tests (including coverage) in `specs/001-repo-analysis/quickstart.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T007 Implement Git and GitHub client abstractions for cloning and repository metadata access in `lib/git_providers.py`
- [ ] T008 Implement configuration module to capture CLI options (org URL/ID, repo URL/ID, working folder, AI provider choice) and to select among supported local LLM providers in `lib/config.py`
- [ ] T009 Implement local AI assistant integration abstraction (e.g., Claude/Cursor/Copilot adapters) in `lib/ai_summarizer.py` honoring the configured provider choice
- [ ] T010 Implement security scanner orchestration abstraction for SAST, SCA, secrets, DAST, and IaC scanning in `lib/security_scanner.py`
- [ ] T011 Implement core data structures for repository analysis results, including security issues and AI readiness, in `lib/models.py`
- [ ] T012 [P] Create top-level CLI entrypoint that wires arguments to configuration and orchestration in `cli/repo_analysis_cli.py`
- [ ] T013 [P] Set up base unit test layout for core modules in `tests/unit/` and ensure test runner works

**Checkpoint**: Foundation ready – user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 – Scan all repositories in an organization (Priority: P1) 🎯 MVP

**Goal**: Allow a user to run the CLI against a GitHub/Enterprise GitHub organization and clone/update all accessible repositories from `main`, generating one folder per repository under `code-browser` with a populated README.

**Independent Test**: From a clean environment, run the CLI with an organization URL/ID and verify that each accessible repository under the organization has been cloned/updated and has a corresponding folder with a generated README under `code-browser/`.

### Tests for User Story 1

- [ ] T014 [P] [US1] Add integration test that runs an organization scan against a small fixture org and asserts cloned repositories and README files in `tests/integration/test_org_scan_basic.py`
- [ ] T015 [P] [US1] Add contract test for CLI arguments and help output for organization scans in `tests/contract/test_cli_org_args.py`

### Implementation for User Story 1

- [ ] T016 [US1] Implement organization-scope repository discovery and selection logic in `lib/org_discovery.py`
- [ ] T017 [US1] Implement orchestration to clone/update all organization repositories from `main` into a working folder in `lib/org_clone_orchestrator.py`
- [ ] T018 [US1] Implement per-repository folder creation under `code-browser/` with stable naming in `lib/repo_folder_manager.py`
- [ ] T019 [US1] Implement top-level organization scan command and flags in `cli/repo_analysis_cli.py`
- [ ] T020 [US1] Implement progress reporting and error aggregation for organization scans in `lib/progress_reporting.py`
- [ ] T021 [US1] Ensure idempotent behavior when re-running an organization scan (update instead of duplicate) in `lib/org_clone_orchestrator.py`

**Checkpoint**: Organization-level scanning produces folders and base READMEs for all accessible repositories under `code-browser/`.

---

## Phase 4: User Story 2 – Analyze a single repository (Priority: P1)

**Goal**: Allow a user to target a single repository and generate or refresh its folder and README under `code-browser/` without touching other repositories.

**Independent Test**: From a clean environment or with existing cloned repos, run the CLI with a single repository URL/ID and verify that only that repository is cloned/updated and that its folder and README under `code-browser/` are created or refreshed.

### Tests for User Story 2

- [ ] T022 [P] [US2] Add integration test that runs a single-repository scan and asserts that only the target repo folder and README are modified in `tests/integration/test_single_repo_scan.py`
- [ ] T023 [P] [US2] Add contract test for CLI arguments and help output for single-repository scans in `tests/contract/test_cli_repo_args.py`

### Implementation for User Story 2

- [ ] T024 [P] [US2] Implement repository-targeted cloning/updating logic shared between org and single-repo flows in `lib/repo_clone.py`
- [ ] T025 [US2] Implement single-repo scan command and flags in `cli/repo_analysis_cli.py`
- [ ] T026 [US2] Ensure single-repo scans correctly reuse and update existing `code-browser/` folders and READMEs in `lib/repo_folder_manager.py`

**Checkpoint**: Single-repo scanning is independently usable and does not affect unrelated repositories.

---

## Phase 5: User Story 3 – Review repository health and architecture (Priority: P2)

**Goal**: Generate rich per-repository READMEs that summarize health metrics, tech stack, contributors, security issues, and architecture/code-flow diagrams.

**Independent Test**: For a scanned repository, open its generated README and verify that Summary, Dependencies, Contribution, Architecture, Code Organization, Overall Code Flow, Features, Code Documentation, Tests, and security metrics are populated or explicitly marked as unavailable.

### Tests for User Story 3

- [ ] T027 [P] [US3] Add snapshot-style test that validates required README sections and basic structure in `tests/unit/test_readme_structure.py`
- [ ] T028 [P] [US3] Add integration test that runs a scan over a fixture repo and checks for expected Mermaid diagrams and metrics in `tests/integration/test_readme_content.py`

### Implementation for User Story 3

- [ ] T029 [P] [US3] Implement repository analysis pipeline to collect contributors, tech stack, tests, coverage, CI/CD badges, issues, license, and commit recency in `lib/repo_analyzer.py`
- [ ] T048 [US3] Implement software dependency detection for Python repositories by parsing common manifests (`requirements.txt`, `pyproject.toml`, `setup.cfg`, `Pipfile`) in `lib/repo_analyzer.py` and surfacing results to the Dependencies section
- [ ] T049 [US3] Implement software dependency detection for Java repositories by parsing build descriptors (`pom.xml`, `build.gradle`, `build.gradle.kts`) in `lib/repo_analyzer.py` and surfacing results to the Dependencies section
- [ ] T050 [US3] Implement software dependency detection for Go repositories by parsing `go.mod` (and related Go module metadata) in `lib/repo_analyzer.py` and surfacing results to the Dependencies section
- [ ] T051 [US3] Extend README renderer to list detected software dependencies (name and version range where available) and clearly separate them from system dependencies in `lib/readme_renderer.py`
- [ ] T030 [P] [US3] Integrate security scanner orchestration results (SAST, SCA, secrets, DAST, IaC) into a unified “total number of identified security issues” count in `lib/security_scanner.py`
- [ ] T031 [P] [US3] Implement AI-powered summarization layer to generate narrative sections (Summary, Features, Code Documentation, etc.) via `lib/ai_summarizer.py`
- [ ] T032 [US3] Implement architecture, code organization, and code-flow Mermaid diagram generation helpers in `lib/diagram_generator.py`
- [ ] T033 [US3] Implement README renderer that assembles all metrics, summaries, and diagrams into `code-browser/<repo-name>/README.md` in `lib/readme_renderer.py`
- [ ] T034 [US3] Ensure missing data (e.g., no issues, no tests) is represented as “Not available” rather than causing failures in `lib/readme_renderer.py`
- [ ] T035 [US3] Design and document behavior for large organizations and long-running scans (e.g., progress visibility, partial completion) in `specs/001-repo-analysis/quickstart.md`
- [ ] T047 [US3] Implement license detection from repository root license files and surface it in README summaries in `lib/repo_analyzer.py`, `lib/models.py`, and `lib/readme_renderer.py`

**Checkpoint**: Generated READMEs provide a comprehensive, human-readable summary of repository health and architecture.

---

## Phase 6: User Story 4 – Drill into detailed documentation per repository (Priority: P3)

**Goal**: Support optional subfolders (`Documentation`, `Features`, `Code Documentation`, `Tests`) per repository for deeper markdown content, referenced from the main README.

**Independent Test**: For a scanned repository, create or edit markdown files in the optional subfolders and verify that the main README references these locations and that scans do not overwrite user-authored content.

### Tests for User Story 4

- [ ] T036 [P] [US4] Add integration test ensuring that existing markdown files in `Documentation/`, `Features/`, `Code Documentation/`, and `Tests/` are preserved across scans in `tests/integration/test_repo_subfolders_preserved.py`

### Implementation for User Story 4

- [ ] T037 [US4] Implement creation and management of optional subfolders under each repository folder in `lib/repo_folder_manager.py`
- [ ] T038 [US4] Update README renderer to include stable links or references to optional subfolders in `lib/readme_renderer.py`
- [ ] T039 [US4] Ensure scan logic never overwrites user-authored markdown files in subfolders in `lib/repo_folder_manager.py`

**Checkpoint**: Users can extend generated summaries with deeper markdown content without breaking the automated scans.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T040 [P] Add CLI help, usage examples, and error messages polish in `cli/repo_analysis_cli.py`
- [ ] T041 Refine logging, progress reporting, and failure diagnostics across modules in `lib/`
- [ ] T042 [P] Add additional unit tests for AI summarization edge cases and error handling in `tests/unit/test_ai_summarizer.py`
- [ ] T043 [P] Add additional unit tests for security scanner orchestration and mapping in `tests/unit/test_security_scanner.py`
- [ ] T044 Add tasks or documentation updates to ensure success criteria (SC-001–SC-006) are explicitly considered in test design and quickstart flows in `specs/001-repo-analysis/quickstart.md`
- [ ] T045 Update feature documentation and examples in `specs/001-repo-analysis/quickstart.md`
- [ ] T046 Run end-to-end validation of quickstart flows described in `specs/001-repo-analysis/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies – can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion – BLOCKS all user stories.
- **User Stories (Phases 3–6)**: All depend on Foundational phase completion.
  - User Story 1 (P1) should be implemented first as the MVP.
  - User Stories 2–4 can proceed in parallel once User Story 1’s core orchestration is stable.
- **Polish (Phase 7)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Setup and Foundational phases; no dependencies on other stories.
- **User Story 2 (P1)**: Depends on Setup and Foundational phases; reuses clone and folder management primitives from US1.
- **User Story 3 (P2)**: Depends on Setup and Foundational phases; reuses clone, analysis, and folder management primitives from US1/US2.
- **User Story 4 (P3)**: Depends on Setup and Foundational phases; reuses folder management and README rendering from prior stories.

### Within Each User Story

- Tests (if included) SHOULD be written and verified before full implementation.
- Core data models and abstractions before orchestration code.
- Orchestration before CLI wiring and documentation.
- Story completion should be independently demonstrable and testable.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel.
- Foundational tasks marked [P] can run in parallel within Phase 2.
- After Foundational completion, work on US1–US4 can be split across different team members, with care to avoid conflicts in shared modules.
- Tests marked [P] across integration and unit layers can be developed and executed in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL – blocks all stories).
3. Complete Phase 3: User Story 1 (organization-wide scanning and basic README generation).
4. **STOP and VALIDATE**: Run integration tests for US1 and confirm that organization scans behave correctly and are idempotent.
5. Demo or adopt US1 flow as the initial MVP.

### Incremental Delivery

1. After MVP, add User Story 2 (single-repo scans) and validate independently.
2. Add User Story 3 (rich repository health and architecture READMEs) and validate independently.
3. Add User Story 4 (optional subfolder deep dives) and validate independently.
4. Apply Phase 7 polish tasks across the whole feature.

### Parallel Team Strategy

With multiple developers:

1. Collaborate on Setup and Foundational phases.
2. Assign stories once the foundation is stable, for example:
   - Developer A: US1 (org scans and orchestration).
   - Developer B: US2 (single-repo scans).
   - Developer C: US3 (analysis, security, and README rendering).
   - Developer D: US4 (subfolders and documentation extensions).
3. Coordinate on shared modules (`lib/repo_folder_manager.py`, `lib/readme_renderer.py`, `cli/repo_analysis_cli.py`) to avoid conflicts and keep interfaces stable.

