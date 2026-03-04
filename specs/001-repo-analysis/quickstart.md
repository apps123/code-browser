# Quickstart: Repository Analysis Readme Generation

This guide explains how to set up the environment, run the repository analysis CLI, and execute tests with coverage for the `001-repo-analysis` feature.

## Prerequisites

- Python 3.11 installed
- Git installed and configured with access to your GitHub or Enterprise GitHub organization

## Setup

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # on macOS/Linux
```

2. Install the project in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

This will install the CLI and libraries defined in `pyproject.toml`, including:

- `typer` for the CLI
- `GitPython` and `PyGithub` for Git/GitHub access
- `pydantic`, `requests` and related utilities
- `pytest` and `pytest-cov` for testing and coverage

## Running the CLI

After installation, the CLI entrypoint `repo-analysis` will be available.

### Scan a GitHub organization

```bash
repo-analysis org-scan --org-url https://github.com/your-org
```

This command is expected to:

- Discover accessible repositories for the organization
- Clone or update them from their `main` branch
- Create or update one folder per repository under `code-browser/`
- Generate a `README.md` in each folder with summary information

On a typical developer laptop, an organization scan for up to ~100 small-to-medium repositories should generally complete within about 60 minutes, with progress logs indicating which repositories have been processed.

### Scan a single repository

```bash
repo-analysis repo-scan --repo-url https://github.com/your-org/your-repo
```

This command is expected to:

- Clone or update only the specified repository from `main`
- Create or update the corresponding folder under `code-browser/`
- Generate or refresh that repository’s `README.md`

For a typical single service-sized repository, the scan (clone/update + analysis + README generation) is expected to complete within a few minutes, depending on network and scanner performance.

## Running Tests and Coverage

To run the test suite with coverage:

```bash
pytest
```

By default, `pytest` is configured (via `pyproject.toml`) to:

- Run unit tests from `tests/unit/`
- Run integration tests from `tests/integration/`
- Run contract tests from `tests/contract/`
- Collect coverage for the `cli/` and `lib/` packages and report missing lines

You can also generate an HTML coverage report if desired by extending `pytest` options locally.

### Validating Success Criteria

To validate the high-level success criteria:

- **SC-001/SC-002**: Time representative org and single-repo scans and confirm they fall within expected ranges or that progress logs clearly indicate long-running work.
- **SC-003**: Have technical stakeholders review a sample of generated READMEs and confirm they can understand purpose, tech stack, architecture, and test posture without opening the code.
- **SC-004**: Spot-check that generated READMEs contain all required sections and that missing data is explicitly marked as “Not available”.
- **SC-005**: Where coverage tools are configured, compare reported coverage in CI and any coverage metrics you surface in analysis to ensure they are broadly consistent.
- **SC-006**: For portfolio reviews or onboarding exercises, compare time spent with and without the tool to ensure it materially reduces manual survey effort.

