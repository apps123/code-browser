# Feature Specification: Repository Analysis Readme Generation

**Feature Branch**: `001-repo-analysis`  
**Created**: 2026-03-02  
**Status**: In review  
**Input**: User description: "The software program should clone one or many GitHub repositories and generate per-repository folders under code-browser, each with a structured README and optional subpages summarizing repository health, architecture, features, documentation, and tests."

## Clarifications

### Session 2026-03-02

- Q: What is the primary user interface for triggering scans and providing GitHub / Enterprise GitHub organization or repository URLs? → A: Command-line interface (CLI) with flags/arguments.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Scan all repositories in an organization (Priority: P1)

An engineering leader wants an at-a-glance understanding of all repositories in a GitHub organization, including activity, code quality signals, documentation health, and AI readiness, without manually inspecting each repo.

**Why this priority**: This provides the highest leverage view of the engineering portfolio and is the primary value of the tool for planning, governance, and modernization decisions.

**Independent Test**: Trigger a scan for a GitHub organization and verify that a folder is created for each repository under `code-browser`, each containing a populated README with the required sections and metrics.

**Acceptance Scenarios**:

1. **Given** a valid GitHub organization name and access to its repositories, **When** the user runs an organization scan, **Then** all accessible repositories in that organization are cloned using their main branch and represented as folders under `code-browser` with generated READMEs.
2. **Given** an organization with some repositories already cloned locally, **When** the user runs an organization scan again, **Then** existing repositories are updated from main and their READMEs are regenerated without creating duplicate folders.

---

### User Story 2 - Analyze a single repository (Priority: P1)

An engineer or product owner wants a concise, standardized summary of a specific repository’s ownership, tech stack, architecture, features, documentation, and tests.

**Why this priority**: Individual repository analysis is a common entry point for understanding unfamiliar codebases and supports onboarding and due diligence.

**Independent Test**: Trigger a scan for a single repository and verify that only that repository is cloned or updated from main and that its folder and README are created or refreshed under `code-browser`.

**Acceptance Scenarios**:

1. **Given** a valid repository identifier, **When** the user runs a single-repository scan, **Then** only that repository is cloned or refreshed from its main branch and a corresponding folder and README are produced under `code-browser`.
2. **Given** that a repository folder already exists under `code-browser`, **When** the user rescans that same repository, **Then** the README content is updated to reflect the latest metrics and activity while preserving the folder naming convention.

---

### User Story 3 - Review repository health and architecture (Priority: P2)

An architect or technical lead wants to quickly understand how a repository is structured, which services or components it uses, and how code flows through the system, including Cloud services and integration points.

**Why this priority**: Architecture and flow views are essential for impact analysis, refactoring, and planning AI enablement or cloud migrations.

**Independent Test**: Open a generated README for a repository and verify that it contains architecture, code organization, and overall code flow sections represented as Mermaid diagrams, plus clearly labeled sections for dependencies, features, and tests.

**Acceptance Scenarios**:

1. **Given** a repository that uses cloud services or external systems, **When** its README is generated, **Then** the Architecture section includes a Mermaid diagram that calls out key cloud services and software stacks (including those in Google Cloud and AWS where applicable).
2. **Given** a repository with multiple modules or components, **When** its README is generated, **Then** the Code Organization and Overall Code Flow sections each include Mermaid diagrams that capture the main components and functional call graph at a high level.

---

### User Story 4 - Drill into detailed documentation per repository (Priority: P3)

A documentation owner or platform engineer wants to extend or refine the automatically generated summaries with deeper details on documentation, features, code documentation, and tests in separate markdown pages.

**Why this priority**: Separate markdown files enable richer, curated documentation without cluttering the main summary while keeping a consistent structure across repositories.

**Independent Test**: For a scanned repository, verify that a user can add or update markdown files in optional subfolders (Documentation, Features, Code Documentation, Tests) and that these are discoverable from the main README.

**Acceptance Scenarios**:

1. **Given** a repository folder under `code-browser`, **When** a user creates or updates markdown files in `Documentation`, `Features`, `Code Documentation`, or `Tests` subfolders, **Then** the main README references these subfolders as locations for deeper content.
2. **Given** a scan has completed, **When** a user inspects the repository folder, **Then** they can see the main README plus any existing subfolders for additional markdown content without breaking the folder naming convention.

---

### Edge Cases

- What happens when the GitHub organization or repository name does not exist or cannot be accessed due to permissions?  
  - The system should fail gracefully, clearly indicate which repositories could not be scanned, and still generate summaries for any repositories that were successfully accessed.
- How does the system handle repositories without certain data sources (for example, no issues, no tests, or missing CI configuration)?  
  - The system should explicitly indicate “Not available” or similar wording for each missing metric rather than failing the scan.
- How does the system behave when there are a very large number of repositories in an organization?  
  - The system should process repositories in a way that can be monitored (for example, progress information) and should ensure that partial progress is still reflected in generated folders and READMEs if the scan is interrupted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support scanning by GitHub organization, cloning or updating all accessible repositories for that organization into a configurable working folder, using each repository’s main branch as the source of truth.
- **FR-002**: The system MUST support scanning a single specified GitHub repository, cloning or updating only that repository into the working folder, using its main branch.
- **FR-003**: The system MUST expose options for the user to provide either (a) a GitHub or Enterprise GitHub organization URL or identifier, or (b) a single repository URL or identifier, and MUST use these inputs to determine which repositories to act on.
- **FR-004**: For every scanned repository, the system MUST create (or reuse and update) exactly one corresponding folder under the `code-browser` directory, with a stable and predictable naming convention per repository.
- **FR-005**: For each repository folder under `code-browser`, the system MUST generate a `README.md` that contains, at minimum, the following sections:
  - Scanned Date
  - Summary
  - Dependencies
  - Contribution
  - Architecture (with a Mermaid diagram)
  - Code Organization (with a Mermaid diagram)
  - Overall Code Flow and Functional Call Graph (with a Mermaid diagram)
  - Features
  - Code Documentation
  - Tests
- **FR-006**: Within the **Summary** section of each generated `README.md`, the system MUST include structured information for:
  - Contributor diversity (e.g., top contributors with approximate contribution percentages)
  - Tech stack used (key languages, packages, and libraries)
  - Code coverage (expressed as a percentage where measurable)
  - Total number of identified security issues
  - Whether the repository’s own `README.md` is well documented (Yes/No/Partial, based on observable signals)
  - Presence and type of CI/CD badges
  - Commit recency (last updated date for the repository)
  - Number of open issues (where issue tracking is enabled in the repository)
  - Number of closed issues (where issue tracking is enabled)
  - AI readiness (Yes/No/Partial, based on observable signals such as tests, modularity, documentation, and code quality indicators)
  - AI tool support (e.g., whether the repository already references or is configured for tools such as Claude, Cursor, Speckit, Kiro)
  - License type (e.g., MIT, Apache, or other)
  - Number of tests available (count of identifiable automated tests).
- **FR-007**: Within the **Dependencies** section of each `README.md`, the system MUST summarize:
  - Software dependencies (e.g., major framework and library dependencies by name and version range)
  - System dependencies (e.g., databases, message brokers, external services, or runtime environments the code expects).
- **FR-008**: Within the **Contribution** section of each `README.md`, the system MUST list:
  - Key contributors who together account for approximately 60% of contributions in combination
  - A complete list of contributors or a clearly summarized list that allows identifying all contributors.
- **FR-009**: Within the **Architecture** section of each `README.md`, the system MUST include a high-level Mermaid diagram that highlights key components, services, and, where detectable, cloud services or software stacks, explicitly calling out Google Cloud and AWS services when they are used.
- **FR-010**: Within the **Code Organization** section, the system MUST include a Mermaid diagram that conveys the primary modules, layers, or components of the repository and how they are organized in the codebase.
- **FR-011**: Within the **Overall Code Flow and Functional Call Graph** section, the system MUST include a Mermaid diagram that describes the main execution paths and interactions between major functions, modules, or services at a high level.
- **FR-012**: Within the **Features** section, the system MUST list the top features supported by the repository as concise one-line descriptions and, where possible, include an approximate date or release context for when each feature became available.
- **FR-013**: Within the **Code Documentation** section, the system MUST summarize the presence and extent of in-code documentation (for example, Javadocs, PyDocs, docstrings, or similar) and link or point to any major documentation sources within the repository.
- **FR-014**: Within the **Tests** section, the system MUST:
  - Summarize the types of tests that exist (unit, integration, end-to-end, etc.)
  - Call out possible missing tests or coverage gaps where they are reasonably detectable
  - Summarize available tests and their approximate scope.
- **FR-015**: For each repository folder under `code-browser`, the system MUST support (and not overwrite) optional subfolders such as `Documentation`, `Features`, `Code Documentation`, and `Tests`, where additional markdown files can be stored for deeper narratives on those topics.
- **FR-016**: The system MUST ensure that repeated scans of the same organization or repository keep the folder structure stable while updating metrics, diagrams, and summaries to reflect the most recent state of the code and repository activity.
- **FR-017**: The system MUST provide clear feedback when a scan completes, including which repositories were successfully processed and which, if any, failed or were skipped.
- **FR-018**: For all narrative and summary content required in this specification (including summaries, metrics explanations, architecture descriptions, feature one-liners, and similar prose), the system MUST delegate the summarization work to a locally available AI assistant or LLM integration (for example, Claude, Cursor, Copilot, or similar) selected by the user or by project configuration, rather than hard-coding a specific provider.
- **FR-019**: The system MUST allow the user or project configuration to choose which installed LLM integration is used for summarization and MUST be able to operate without change if a different supported local AI assistant is selected in the future.
- **FR-020**: Where security analysis is performed to derive the “Total number of identified security issues” and related insights, the system MUST, where applicable to the repository and environment, cover checks aligned with established categories such as OWASP-style application risks, STRIDE-style threat modeling perspectives, static application security testing (SAST), software composition analysis (SCA), secrets detection, dynamic application security testing (DAST), and infrastructure-as-code (IaC) scanning.
- **FR-021**: The primary way to trigger organization-wide and single-repository scans MUST be a command-line interface (CLI) that accepts flags or arguments for GitHub or Enterprise GitHub organization URLs/identifiers and repository URLs/identifiers, consistent with the input options described in **FR-003**.

### Key Entities *(include if feature involves data)*

- **Organization Scan Request**: Represents a request to analyze all repositories under a given GitHub organization, including parameters such as organization identifier, working folder, and date/time of the scan.
- **Repository**: Represents a single GitHub repository, including its name, default branch, activity metadata, issue tracking status, license, and links to local clone location under `code-browser`.
- **Repository Summary**: Represents the structured summary for a repository that is surfaced in the generated `README.md`, including summary metrics, architecture views, dependencies, features, documentation, and tests.
- **Contributor**: Represents an individual or bot account that has contributed to a repository, including contribution counts and approximate percentage contribution.
- **Dependency**: Represents a software or system dependency identified as part of the analysis, including its name and category (library, framework, service, database, etc.).
- **Analysis Run**: Represents a single execution of the scanning process (organization-wide or single-repository), including start time, end time, scope, outcome per repository, and any notable warnings or failures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For organizations with up to **100** repositories, at least **95%** of accessible repositories complete scanning successfully in a single run, producing a corresponding folder and README under `code-browser` within **30 minutes** on a typical CI or developer workstation.
- **SC-002**: For a single-repository scan on an average-sized service (for example, up to **3000 source files** and **1 GB** of repository data), users can obtain a generated or refreshed README and folder under `code-browser` within **5 minutes** on a typical CI or developer workstation.
- **SC-003**: In user reviews, at least 80% of technical stakeholders report that the generated README provides enough information to understand the repository’s purpose, tech stack, architecture, and test posture without needing to open the code immediately.
- **SC-004**: At least 90% of generated READMEs include all required sections (Summary, Dependencies, Contribution, Architecture, Code Organization, Overall Code Flow, Features, Code Documentation, Tests) populated with meaningful content or clearly labeled as “Not available” where data cannot be determined.
- **SC-005**: For repositories with recognizable test suites, the reported number of tests and code coverage percentage is within an acceptable variance (for example, ±10%) when compared with manually derived values.
- **SC-006**: After adopting this tool, teams report at least a **30% reduction** in median time spent manually surveying repositories for planning or onboarding purposes (measured by comparing the average time to prepare a portfolio review or onboarding summary for a set of repositories before and after introducing the tool).

For the purposes of SC‑001 and SC‑002, a “typical CI or developer workstation” is assumed to be a machine with at least **4 vCPUs**, **8 GB RAM**, and **20 GB** of free disk space available for cloning and analysis work.

## Assumptions

- The system has appropriate access (credentials and permissions) to clone and analyze the specified GitHub organization and repositories.
- The `code-browser` directory is available and writable as the root location for generated per-repository folders and READMEs.
- Standard repository signals (such as commit history, issues, pull requests, tests, documentation files, and configuration files) are sufficient to derive approximate metrics and qualitative assessments such as AI readiness and documentation quality.
- Not all repositories will expose every metric (for example, some may not use built-in issue tracking or may lack explicit test or coverage configuration); in those cases, the tool will clearly indicate missing or indeterminable data rather than failing the scan.
