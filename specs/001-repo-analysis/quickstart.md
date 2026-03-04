# Quickstart: Repository Analysis Readme Generation

This quickstart explains how to set up the project, run organization‑wide and single‑repository scans, interpret the generated READMEs, and validate that the implementation meets the success criteria **SC‑001–SC‑006** from `spec.md`.

## 1. Prerequisites

- **Python**: 3.11+
- **Git**: Installed and configured with access to the target GitHub / Enterprise GitHub org or repo.
- **Network**: Outbound HTTPS access to GitHub (or your enterprise GitHub) and any security tools you enable.
- **Environment variables / credentials**:
  - A GitHub personal access token or equivalent credential (scopes sufficient for cloning and reading metadata), typically provided via environment variable (for example, `GITHUB_TOKEN`) or CI secret.

Recommended machine profile (aligns with SC‑001/SC‑002):

- CPU: ≥ 4 vCPUs
- Memory: ≥ 8 GB RAM
- Disk: ≥ 20 GB free for clones and analysis

## 2. Local Development Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -e .[dev]
```

Run tests to confirm the baseline:

```bash
pytest
```

This exercises:

- Unit tests in `tests/unit/` (including analysis, summarization, and security orchestration).
- Integration tests in `tests/integration/` (organization and single‑repo scans, README content).
- Contract tests in `tests/contract/` (CLI argument behavior and outputs).

## 3. Running an Organization Scan (US1)

The main CLI entry point is exposed as the `repo-analysis` script (see `pyproject.toml`) and wired to `cli/repo_analysis_cli.py`.

Example: scan all repositories in an organization:

```bash
export GITHUB_TOKEN=...  # or configure via your preferred mechanism

repo-analysis org \
  --org-name your-org-name \
  --working-dir ./work \
  --code-browser-root ./code-browser
```

Expected behavior (maps to **FR‑001–FR‑004**, **SC‑001**):

- All accessible repositories under `your-org-name` are cloned or updated from their main branch into `./work`.
- For each repository, a folder is created (or reused) under `./code-browser/` with a generated `README.md`.
- If you re‑run the command, existing repositories are updated in place and their READMEs regenerated without duplicate folders (idempotent behavior).
- Progress and any errors are reported via the CLI (supporting FR‑017 and SC‑001).

## 4. Running a Single‑Repository Scan (US2)

Example: scan a single repository:

```bash
repo-analysis repo \
  --repo \"owner/name\" \
  --working-dir ./work \
  --code-browser-root ./code-browser
```

Expected behavior (maps to **FR‑002–FR‑004**, **SC‑002**):

- Only the specified repository is cloned or updated from its main branch.
- Exactly one folder `./code-browser/owner__name/` is created or refreshed.
- Re‑running the command refreshes the README and updates metrics without affecting other repositories.

## 5. Interpreting Generated READMEs (US3)

For each repository folder under `code-browser/`, open `README.md`. It includes:

- **Scanned Date** (FR‑005)
- **Summary** section (FR‑006) with:
  - Contributor diversity (top contributors with approximate percentages)
  - Tech stack (languages/frameworks)
  - Code coverage (if available)
  - Total number of identified security issues
  - Documentation quality of the repository’s own README
  - CI/CD badges
  - Commit recency
  - Open/closed issues (if issue tracking enabled)
  - AI readiness (Yes/No/Partial)
  - AI tool support
  - License type
  - Number of tests available
- **Dependencies** (FR‑007):
  - Software dependencies (e.g., from `requirements.txt`, `pyproject.toml`, `pom.xml`, `build.gradle`, `go.mod`)
  - System dependencies (OS/CPU/memory/disk expectations, network access, and inferred infra components such as databases, caches, or messaging systems)
- **Contribution** (FR‑008)
- **Architecture**, **Code Organization**, **Overall Code Flow** sections with Mermaid diagrams (FR‑009–FR‑011)
- **Features**, **Code Documentation**, **Tests** sections (FR‑012–FR‑014)
- Links or references to optional subfolders (`Documentation`, `Features`, `Code Documentation`, `Tests`) when present (FR‑015, US4).

Repositories with missing data (for example, no tests or no issues) will explicitly say **“Not available”** instead of failing the scan (FR‑005–FR‑007, FR‑013–FR‑014).

## 6. Optional Deep‑Dive Documentation (US4)

Under each repository folder in `code-browser/`, you may create:

- `Documentation/` – deeper architectural or operational docs
- `Features/` – detailed feature descriptions
- `Code Documentation/` – design notes, code walkthroughs
- `Tests/` – test strategy and additional testing notes

The scan logic:

- Will **not overwrite** user-authored files in these subfolders.
- Will keep references in the main README so readers can discover deeper content.

## 7. Security Scanning and Metrics

Security behavior (FR‑006, FR‑020) is orchestrated via `lib/security_scanner.py` and driven by configuration and the tooling choices described in `plan.md`. At a high level:

- The scanner abstraction can invoke tools for:
  - SAST (e.g., Bandit)
  - SCA / dependency vulnerability scanning (e.g., pip‑audit or safety)
  - Secrets detection (e.g., detect‑secrets or Gitleaks)
  - DAST / container / runtime checks (e.g., Trivy)
  - IaC scanning (e.g., Checkov or similar)
- `lib/repo_analyzer.py` and `lib/readme_renderer.py` together:
  - Aggregate findings into a **“Total number of identified security issues”** metric.
  - Ensure missing or unavailable scanner data results in clear “Not available” signals, not failures.

When configuring or running scans in CI:

- Ensure the security tools you want are installed and available in the PATH.
- Use environment variables or CI secrets to provide any necessary credentials without hard‑coding them.

## 8. Validating Success Criteria (SC‑001–SC‑006)

Use the following to validate the measurable outcomes:

- **SC‑001 (org scan coverage & timeliness)**:
  - Run an organization scan for an org with up to ~100 repositories.
  - Confirm that at least 95% of accessible repositories receive a `code-browser/<repo>/README.md`.
  - Measure time from start to completion; ensure it is ≤ 30 minutes on a machine meeting the recommended profile.

- **SC‑002 (single‑repo responsiveness)**:
  - Run a single‑repository scan for a repo of average size (up to ~3000 source files / 1 GB).
  - Confirm README generation completes within 5 minutes on the reference machine.

- **SC‑003 (stakeholder satisfaction)**:
  - Have technical stakeholders review generated READMEs.
  - Confirm that at least 80% report that they can understand the repository’s purpose, tech stack, architecture, and test posture without opening the code immediately.

- **SC‑004 (coverage & completeness)**:
  - Spot‑check a sample of generated READMEs.
  - Ensure at least 90% include all required sections with either meaningful content or explicit “Not available” markers.

- **SC‑005 (test metrics accuracy)**:
  - For repositories with recognizable test suites, compare:
    - Reported number of tests
    - Any captured coverage percentage
  - Verify values are within ±10% of manually derived metrics.

- **SC‑006 (time‑to‑insight reduction)**:
  - For a representative portfolio review or onboarding scenario, measure:
    - Time to gather repository insights **before** adopting this tool.
    - Time to gather the same insights **after** using generated READMEs.
  - Confirm at least a 30% reduction in median time.

## 9. Next Steps

- Use `/speckit.implement` and `tasks.md` as the execution checklist.
- Extend `quickstart.md` over time with concrete examples of CI integration, security tool configuration, and organization‑specific workflows as the feature matures.

