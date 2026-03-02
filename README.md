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

### Getting started (to be refined)

This repository does not yet define the full application stack or runtime. As the implementation lands, this section should be updated to include:

- **Tech stack** (e.g., framework, language, key libraries).
- **Setup instructions** (dependencies, environment variables, seeding data, etc.).
- **Common commands** (run dev server, tests, linters, formatters).

For now, treat this README as the living source of truth for how to work in this repo and keep it up to date as the codebase grows.

