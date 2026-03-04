# Project Constitution

This constitution defines non‑negotiable principles for specifications, plans, and tasks in this repository.

## 1. Security and Privacy

- **SEC-001 (MUST)**: Features that access source code or repositories MUST consider security posture explicitly.
- **SEC-002 (MUST)**: Where security scanning is described (for example, FR‑020), specifications and tasks MUST name the security categories covered (SAST, SCA, secrets, DAST, IaC) and ensure there is at least one task implementing or integrating each category.
- **SEC-003 (SHOULD)**: When concrete tools are known (for example, Bandit, pip-audit, Trivy, Checkov, Gitleaks), they SHOULD be documented in the plan or tasks to make security behavior auditable.

## 2. Testing and Quality

- **TEST-001 (MUST)**: Every functional requirement MUST be testable via at least one task, and success criteria (SC‑XXX) MUST have at least one test or validation task referencing them.
- **TEST-002 (MUST)**: For CLI behavior and critical flows, there MUST be both unit-level and integration or contract tests.
- **TEST-003 (SHOULD)**: Tasks that introduce complex behavior SHOULD include or reference tests that exercise edge cases and failure modes.

## 3. Documentation and Traceability

- **DOC-001 (MUST)**: Specs MUST clearly state functional requirements (FR‑XXX) and success criteria (SC‑XXX).
- **DOC-002 (MUST)**: Tasks that implement requirements SHOULD reference the FR/SC IDs they cover or support.
- **DOC-003 (SHOULD)**: Plans SHOULD describe architecture, stack, and phase structure consistent with the spec and tasks.

## 4. Safety and Non‑Destructive Operation

- **SAFE-001 (MUST)**: Tools described in this repository MUST avoid destructive operations on user repositories by default (for example, no force pushes, no history rewrites).
- **SAFE-002 (MUST)**: Long‑running operations MUST provide progress visibility and avoid leaving the system in an inconsistent state on failure where reasonably possible.

