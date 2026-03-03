from __future__ import annotations

from pathlib import Path


def architecture_diagram(repo_path: Path) -> str:
    """
    Return a Mermaid diagram describing high-level architecture.
    """
    return """```mermaid
graph TD
  A[Client] --> B[Service]
  B --> C[Database]
```"""


def code_organization_diagram(repo_path: Path) -> str:
    """
    Return a Mermaid diagram describing code organization.
    """
    return """```mermaid
graph TD
  src --> models
  src --> services
  src --> cli
```"""


def call_graph_diagram(repo_path: Path) -> str:
    """
    Return a Mermaid diagram describing overall code flow / call graph.
    """
    return """```mermaid
graph TD
  CLI --> Orchestrator
  Orchestrator --> Analyzer
  Analyzer --> Renderer
```"""

