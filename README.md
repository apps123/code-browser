## Code Browser

**Code Browser** is a workspace for building a code exploration and navigation experience. This repository is currently in the early setup phase and is wired for AI-assisted development using Speckit-style workflows.

### Project goals

- **Fast understanding of codebases**: Make it easy to browse, search, and understand code structure.
- **High-quality contributions**: Enforce strong standards around tests, documentation, and security.
- **AI-first workflow**: Use specifications, plans, and constitutions to guide automated and human contributors.

### Repository structure (early stage)

- `.cursor/`: Cursor AI configuration and commands (e.g., `speckit.*` commands).
- `.specify/`: Templates and scripts for specifications, plans, tasks, and constitutions.
- `speckit.constitution`: Project constitution that defines contribution rules and expectations.
- (More application code and directories will be added as the implementation evolves.)

### Developer workflow

- **1. Start with a spec/plan**  
  Use the Speckit/Cursor commands (e.g., `speckit.specify`, `speckit.plan`) to write a spec and plan for non-trivial features before implementing them.

- **2. Keep PRs small**  
  Break work into **small, independently-valuable pull requests**, aiming to keep **most PRs under ~300 changed lines**. When a change must be larger (e.g., sweeping refactor), clearly justify it in the PR description.

- **3. Update documentation with each PR**  
  As part of every PR:
  - Update this `README` and/or other docs with key information needed for developers to understand and work with the changes (architecture shifts, setup steps, config, workflows, etc.).
  - Call out any breaking changes or new required knowledge.

- **4. Testing and coverage expectations**  
  - Add **comprehensive automated tests** (unit, integration, and/or end-to-end as appropriate) for all new or changed behavior.
  - Ensure the **overall project coverage is at least 98%** and that your PR does **not reduce coverage below this threshold**.
  - Run the test suite locally before opening or merging a PR.

- **5. Security expectations**  
  - Do **not introduce new security vulnerabilities** (e.g., injection, broken access control, secrets in code, insecure configuration).
  - When touching authentication, authorization, data handling, or external integrations, explicitly describe the security impact in the PR and how it is mitigated.

- **6. Git safety and cleanliness**  
  - Avoid destructive operations (force-push, history rewrites) unless explicitly required and agreed upon.
  - Keep commits focused and well-labeled; avoid mixing unrelated changes in a single PR.

### Project constitution

The full set of contribution rules lives in `speckit.constitution`. When in doubt about how to structure work, size PRs, or handle tests/docs/security, **defer to that constitution** and update it (in a separate, focused PR) if the rules need to evolve.

### Repository analysis CLI (001-repo-analysis)

This repo includes a Python-based CLI that can scan a GitHub or Enterprise GitHub organization (or a single repository), clone/update the code locally, and generate per-repository analysis folders under `code-browser/` with a standardized `README.md`.

Each generated README summarizes:

- **Scanned Date**
- **Summary** (contributors, tech stack, code coverage placeholder, total security issues, CI/CD badges, commit recency, issue counts, AI readiness, AI tools, license, number of tests)
- **Dependencies** (software/system – currently scaffolded as “Not available” until deeper integration)
- **Contribution** (key contributors and all contributors – currently scaffolded)
- **Architecture** (Mermaid diagram)
- **Code Organization** (Mermaid diagram)
- **Overall Code Flow and Functional Call Graph** (Mermaid diagram)
- **Features**, **Code Documentation**, **Tests** (initially scaffolded, ready to be enriched)

#### Tech stack

- **Language**: Python 3.11  
- **CLI framework**: `typer`  
- **Git / GitHub access**: `GitPython`, `PyGithub`  
- **Utilities**: `requests`, `pydantic`  
- **Testing & coverage**: `pytest`, `pytest-cov`  
- **Linting/formatting**: `ruff`, `black`, `mypy`  
- **Security tooling integration (planned)**: `bandit`, `pip-audit`/`safety`, `detect-secrets`, Trivy, Checkov

Dependencies are declared in `pyproject.toml`.

#### Setup

- Install Python 3.11 and Git.
- (Recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

- Install the project in editable mode with dev dependencies:

```bash
pip install -e ".[dev]"
```

- Set your GitHub credentials (for GitHub.com or Enterprise) via environment variables:

```bash
export GITHUB_TOKEN=your_token_here
# Optional, for Enterprise:
export GITHUB_BASE_URL=https://github.your-company.com/api/v3
```

#### Quickstart examples

- **Scan all repositories in an organization**:

```bash
repo-analysis org-scan --org-url https://github.com/your-org
```

This will:

- Discover accessible repositories for `your-org`
- Clone or update each repository from its `main` branch into a working folder (default: `./work`)
- Create/update one folder per repository under `code-browser/owner__name/`
- Generate or refresh a structured `README.md` in each folder

- **Scan a single repository**:

```bash
repo-analysis repo-scan --repo-url https://github.com/your-org/your-repo
```

This will:

- Clone or update only `your-org/your-repo` from `main` into the working folder
- Create or update `code-browser/your-org__your-repo/README.md` with the analysis summary

The CLI also supports `--workdir` to override the working folder and `--ai-provider` to select which locally-integrated AI assistant to use for summarization once those integrations are configured.

#### Running tests and coverage

Run the full test suite (unit, integration, contract) with coverage:

```bash
pytest
```

By default, `pytest` is configured via `pyproject.toml` to:

- Discover tests under `tests/unit/`, `tests/integration/`, and `tests/contract/`
- Collect coverage for the `cli/` and `lib/` packages and report missing lines

You can layer on additional options (e.g., `-k`, `-m`, or HTML coverage reports) as needed.

#### Enabling security scanning

To have the generated READMEs include a real **“Total number of security issues”** count, you can wire in external security tools. The `SecurityScanner` class in `lib/security_scanner.py` is set up to call:

- `bandit` (SAST)  
- `pip-audit` (SCA for `requirements.txt`)  
- `detect-secrets` (secrets detection)

**Step 1 – Install the tools** (locally or in CI):

```bash
pip install bandit pip-audit detect-secrets
```

**Step 2 – (Optional) Control which scanners run** via environment variables:

```bash
export REPO_ANALYSIS_ENABLE_BANDIT=true
export REPO_ANALYSIS_ENABLE_PIP_AUDIT=true
export REPO_ANALYSIS_ENABLE_DETECT_SECRETS=true
```

Set any of these to `false` to disable that scanner.

**Step 3 – Run scans as usual**:

```bash
export GITHUB_TOKEN=your_token_here
repo-analysis org-scan --org-url https://github.com/your-org
```

For each repository:

- The tool clones/updates the repo into the working folder.
- `SecurityScanner` invokes the enabled tools against the local clone.
- Findings are aggregated into structured `SecurityIssue` entries and the **total count** is surfaced in `code-browser/<repo>/README.md` under the Summary section as “Total number of security issues”.

#### Feature summary

At this stage, the repository analysis CLI supports:

- **Organization-wide scans**: Clone/update all accessible repos in an org and generate per-repo analysis READMEs.
- **Single-repository scans**: Clone/update an individual repo and generate its analysis README.
- **Standardized README structure**: Consistent sections and Mermaid diagrams for architecture, code organization, and call graphs.
- **Security issue counting (scaffolded)**: A unified “total number of security issues” metric, ready to be backed by concrete security scanners.
- **AI readiness & tooling (heuristic)**: Basic signals (tests, README presence) feeding an AI readiness flag, and pluggable AI summarizer abstraction ready for local tools like Claude, Cursor, or Copilot.
- **Extensible per-repo docs**: Support for `Documentation/`, `Features/`, `Code Documentation/`, and `Tests/` subfolders under each `code-browser` repo folder, allowing deeper manual documentation without breaking automated scans.

### License and responsibility

This project is licensed under the **MIT License** (see `LICENSE`).

By using this tool, you acknowledge that:

- The author and any companies the author works for are **not liable** for any data loss, data corruption, data exfiltration, security compromise, or other damage resulting from use of the tool.
- It is **entirely the responsibility** of you and/or your organization to:
  - Decide where and how to run the tool.
  - Protect your repositories, credentials, and infrastructure.
  - Put appropriate security controls, monitoring, and backups in place.

If you are not comfortable accepting this responsibility, you should **not use** this tool.

