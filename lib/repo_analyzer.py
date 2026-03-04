from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from git import Repo  # type: ignore[import-untyped]

from .models import RepositorySummary
from .security_scanner import SecurityScanner


@dataclass
class RepoAnalysis:
    summary: RepositorySummary
    contributors: List[str]
    tech_stack: List[str]
    code_coverage: Optional[float]
    has_readme: bool
    ci_badges: List[str]
    last_updated: Optional[datetime]
    open_issues: Optional[int]
    closed_issues: Optional[int]
    ai_tools: List[str]
    test_count: Optional[int]
    license_type: Optional[str] = None
    # Detected dependencies (e.g., "package==1.2.3" or "group:artifact:version")
    software_dependencies: List[str] = field(default_factory=list)
    # High-level system/runtime/infra requirements inferred from the repo
    system_dependencies: List[str] = field(default_factory=list)


class RepoAnalyzer:
    """
    Performs a lightweight analysis of a repository to collect signals needed
    for the generated README.
    """

    def __init__(self, security_scanner: Optional[SecurityScanner] = None) -> None:
        self._security_scanner = security_scanner or SecurityScanner()

    def analyze(self, full_name: str, local_path: Path) -> RepoAnalysis:
        scanned_at = datetime.utcnow()
        security_result = self._security_scanner.run_all(local_path)

        summary = RepositorySummary(
            full_name=full_name,
            local_path=local_path,
            scanned_at=scanned_at,
            total_security_issues=security_result.total_issues,
            ai_readiness=None,
        )

        contributors = self._infer_contributors(local_path)
        tech_stack = self._infer_tech_stack(local_path)
        code_coverage: Optional[float] = None  # left to external coverage tooling
        has_readme = (local_path / "README.md").exists()
        ci_badges: List[str] = []  # detection from README or CI config can be added later
        last_updated = self._infer_last_updated(local_path)
        open_issues: Optional[int] = None
        closed_issues: Optional[int] = None
        ai_tools: List[str] = []  # could be inferred from config files in future
        test_count = self._infer_test_count(local_path)
        license_type = self._infer_license_type(local_path)
        software_dependencies = self._infer_software_dependencies(local_path)
        system_dependencies = self._infer_system_dependencies(local_path, software_dependencies)

        # Simple heuristic for AI readiness based on tests and documentation presence.
        if test_count and test_count > 0 and has_readme:
            summary.ai_readiness = "Yes"
        elif test_count or has_readme:
            summary.ai_readiness = "Partial"
        else:
            summary.ai_readiness = "No"

        summary.license_type = license_type

        return RepoAnalysis(
            summary=summary,
            contributors=contributors,
            tech_stack=tech_stack,
            code_coverage=code_coverage,
            has_readme=has_readme,
            ci_badges=ci_badges,
            last_updated=last_updated,
            open_issues=open_issues,
            closed_issues=closed_issues,
            ai_tools=ai_tools,
            test_count=test_count,
            license_type=license_type,
            software_dependencies=software_dependencies,
            system_dependencies=system_dependencies,
        )

    def _infer_contributors(self, local_path: Path) -> List[str]:
        try:
            repo = Repo(str(local_path))
        except Exception:
            return []

        counts: Dict[str, int] = {}
        try:
            for commit in repo.iter_commits(max_count=100):
                name = commit.author.name or "Unknown"
                counts[name] = counts.get(name, 0) + 1
        except Exception:
            return []

        total = sum(counts.values()) or 1
        return [f"{name} [{(count/total)*100:.1f}%]" for name, count in counts.items()]

    def _infer_tech_stack(self, local_path: Path) -> List[str]:
        exts: Set[str] = set()
        for path in local_path.rglob("*"):
            if path.is_file():
                exts.add(path.suffix)
        mapping = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".go": "Go",
        }
        stack = {mapping[ext] for ext in exts if ext in mapping}
        return sorted(stack)

    def _infer_last_updated(self, local_path: Path) -> Optional[datetime]:
        try:
            repo = Repo(str(local_path))
            head_commit = next(iter(repo.iter_commits(max_count=1)), None)
            if head_commit is None:
                return None
            return datetime.utcfromtimestamp(head_commit.committed_date)
        except Exception:
            return None

    def _infer_test_count(self, local_path: Path) -> Optional[int]:
        tests_dir = local_path / "tests"
        if not tests_dir.exists():
            return None
        count = 0
        for path in tests_dir.rglob("test_*.py"):
            if path.is_file():
                count += 1
        return count or None

    def _infer_license_type(self, local_path: Path) -> Optional[str]:
        """
        Best-effort detection of the repository license type based on common
        license files in the repository root.
        """
        candidates = [
            "LICENSE",
            "LICENSE.txt",
            "LICENSE.md",
            "COPYING",
            "COPYING.txt",
            "COPYING.md",
        ]

        license_file: Optional[Path] = None
        for name in candidates:
            path = local_path / name
            if path.exists():
                license_file = path
                break

        if not license_file:
            return None

        try:
            text = license_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None

        lowered = text.lower()

        if "mit license" in lowered:
            return "MIT"
        if "apache license" in lowered:
            if "version 2.0" in lowered:
                return "Apache-2.0"
            return "Apache"
        if "gnu general public license" in lowered:
            if "lesser general public license" in lowered:
                return "LGPL"
            if "affero general public license" in lowered:
                return "AGPL"
            return "GPL"
        if "bsd license" in lowered or "redistribution and use in source and binary forms" in lowered:
            return "BSD"
        if "mozilla public license" in lowered:
            return "MPL"

        return "Custom / Unknown"

    # ---- Dependency inference helpers ----

    def _infer_software_dependencies(self, local_path: Path) -> List[str]:
        """
        Aggregate software dependencies detected from language-specific manifests.
        """
        deps: Set[str] = set()
        deps.update(self._infer_python_dependencies(local_path))
        deps.update(self._infer_java_dependencies(local_path))
        deps.update(self._infer_go_dependencies(local_path))
        return sorted(deps)

    def _infer_python_dependencies(self, local_path: Path) -> List[str]:
        deps: List[str] = []
        # requirements-style files
        for name in ("requirements.txt", "requirements-dev.txt"):
            path = local_path / name
            if path.exists():
                try:
                    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                        line = line.strip()
                        # Skip comments, includes, and option lines
                        if not line or line.startswith("#") or line.startswith("-"):
                            continue
                        deps.append(line)
                except Exception:
                    continue

        # pyproject.toml (PEP 621 / Poetry-style) – only use structured dependency fields
        pyproject = local_path / "pyproject.toml"
        if pyproject.exists():
            try:
                text = pyproject.read_text(encoding="utf-8", errors="ignore")
                toml_module = None
                try:
                    import tomllib as toml_module  # type: ignore[attr-defined]
                except Exception:
                    try:
                        import tomli as toml_module  # type: ignore[import-not-found]
                    except Exception:
                        toml_module = None

                if toml_module is not None:
                    data = toml_module.loads(text)
                    project = data.get("project", {}) or {}

                    # PEP 621 dependencies list
                    for entry in project.get("dependencies", []) or []:
                        if isinstance(entry, str) and entry.strip():
                            deps.append(entry.strip())

                    # Optional dependencies (e.g., dev extras)
                    opt = project.get("optional-dependencies", {}) or {}
                    if isinstance(opt, dict):
                        for extra_list in opt.values():
                            for entry in extra_list or []:
                                if isinstance(entry, str) and entry.strip():
                                    deps.append(entry.strip())

                    # Poetry-style [tool.poetry.dependencies]
                    tool = data.get("tool", {}) or {}
                    poetry = tool.get("poetry", {}) or {}
                    poetry_deps = poetry.get("dependencies", {}) or {}
                    if isinstance(poetry_deps, dict):
                        for name, spec in poetry_deps.items():
                            # Skip interpreter constraint
                            if name.lower() == "python":
                                continue
                            if isinstance(spec, str) and spec.strip():
                                deps.append(f"{name} {spec.strip()}")
                            elif isinstance(spec, dict):
                                version = spec.get("version")
                                if isinstance(version, str) and version.strip():
                                    deps.append(f"{name} {version.strip()}")
            except Exception:
                # Fall back silently if TOML parsing fails
                pass

        return deps

    def _infer_java_dependencies(self, local_path: Path) -> List[str]:
        deps: List[str] = []

        # Maven: pom.xml
        pom = local_path / "pom.xml"
        if pom.exists():
            try:
                import xml.etree.ElementTree as ET

                tree = ET.parse(str(pom))
                root = tree.getroot()
                # Handle namespaces by stripping them
                for dep in root.iter():
                    tag = dep.tag.split("}")[-1]
                    if tag != "dependency":
                        continue
                    group_id = None
                    artifact_id = None
                    version = None
                    for child in dep:
                        ctag = child.tag.split("}")[-1]
                        text = (child.text or "").strip()
                        if ctag == "groupId":
                            group_id = text
                        elif ctag == "artifactId":
                            artifact_id = text
                        elif ctag == "version":
                            version = text
                    if group_id and artifact_id:
                        if version:
                            deps.append(f"{group_id}:{artifact_id}:{version}")
                        else:
                            deps.append(f"{group_id}:{artifact_id}")
            except Exception:
                pass

        # Gradle: build.gradle / build.gradle.kts (very lightweight heuristic)
        for name in ("build.gradle", "build.gradle.kts"):
            gradle = local_path / name
            if not gradle.exists():
                continue
            try:
                for raw in gradle.read_text(encoding="utf-8", errors="ignore").splitlines():
                    line = raw.strip()
                    if not line or line.startswith("//"):
                        continue
                    if any(
                        line.startswith(prefix)
                        for prefix in ("implementation", "api", "compileOnly", "runtimeOnly")
                    ):
                        # Look for "group:artifact:version" inside quotes
                        quote = '"' if '"' in line else "'"
                        if quote in line:
                            try:
                                first = line.index(quote) + 1
                                second = line.index(quote, first)
                                coord = line[first:second]
                                if coord:
                                    deps.append(coord)
                            except ValueError:
                                continue
            except Exception:
                continue

        return deps

    def _infer_go_dependencies(self, local_path: Path) -> List[str]:
        deps: List[str] = []
        gomod = local_path / "go.mod"
        if not gomod.exists():
            return deps

        try:
            in_block = False
            for raw in gomod.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = raw.strip()
                if not line or line.startswith("//"):
                    continue
                if line.startswith("require ("):
                    in_block = True
                    continue
                if in_block and line.startswith(")"):
                    in_block = False
                    continue
                if line.startswith("require "):
                    # Single-line require
                    _, rest = line.split("require", 1)
                    parts = rest.strip().split()
                    if len(parts) >= 2:
                        deps.append(f"{parts[0]} {parts[1]}")
                    continue
                if in_block:
                    parts = line.split()
                    if len(parts) >= 2:
                        deps.append(f"{parts[0]} {parts[1]}")
        except Exception:
            return []

        return deps

    def _infer_system_dependencies(self, local_path: Path, software_dependencies: List[str]) -> List[str]:
        """
        Infer high-level system requirements and external infrastructure from
        project structure and declared dependencies.

        This intentionally provides approximate, human-readable guidance rather
        than a complete environment specification.
        """
        items: List[str] = []

        # Baseline environment assumptions – most modern repos can run on these.
        items.append("Operating systems: Linux, macOS, Windows (x86_64)")
        items.append("CPU: 2+ cores recommended for comfortable usage")
        items.append("Memory: 2+ GB RAM recommended (more for large repositories)")
        items.append("Disk: At least 1 GB free for repository clone and tooling")

        # Network requirements based on common Git hosting and HTTP usage.
        items.append(
            "Network: Outbound HTTPS access to Git hosting (e.g., GitHub or enterprise Git) and any remote APIs used by the code"
        )

        # Detect databases, caches, messaging systems, etc. from dependencies.
        infra: List[str] = []
        lower_deps = [d.lower() for d in software_dependencies]

        def _add_unique(label: str) -> None:
            if label not in infra:
                infra.append(label)

        # Python DB drivers / ORMs
        for dep in lower_deps:
            if "psycopg2" in dep or "asyncpg" in dep or "pg8000" in dep:
                _add_unique("Database: PostgreSQL")
            if ("mysqlclient" in dep) or ("pymysql" in dep):
                _add_unique("Database: MySQL / MariaDB")
            if "sqlserver" in dep or "pyodbc" in dep:
                _add_unique("Database: SQL Server (via ODBC)")
            if "pymongo" in dep or "mongoengine" in dep:
                _add_unique("Database: MongoDB")
            if "redis" in dep:
                _add_unique("Cache / Key-Value store: Redis")
            if "kafka" in dep:
                _add_unique("Messaging: Apache Kafka")
            if "rabbitmq" in dep or "pika" in dep:
                _add_unique("Messaging: RabbitMQ")
            if "celery" in dep:
                _add_unique("Background jobs: Celery (requires broker such as Redis or RabbitMQ)")
            if "boto3" in dep:
                _add_unique("Cloud: AWS services (via boto3)")

        # Java ecosystem hints
        for dep in lower_deps:
            if "spring-boot-starter-data-jpa" in dep:
                _add_unique("Database: Relational DB (via JPA/Hibernate)")
            if "spring-boot-starter-data-mongodb" in dep:
                _add_unique("Database: MongoDB")
            if "spring-boot-starter-data-redis" in dep:
                _add_unique("Cache / Key-Value store: Redis")
            if "spring-kafka" in dep:
                _add_unique("Messaging: Apache Kafka")
            if "spring-boot-starter-amqp" in dep:
                _add_unique("Messaging: AMQP (e.g., RabbitMQ)")

        # Go ecosystem hints
        for dep in lower_deps:
            if "github.com/lib/pq" in dep:
                _add_unique("Database: PostgreSQL")
            if "go-sql-driver/mysql" in dep:
                _add_unique("Database: MySQL / MariaDB")
            if "go.mongodb.org/mongo-driver" in dep or "mongo-go-driver" in dep:
                _add_unique("Database: MongoDB")
            if "github.com/redis" in dep or "go-redis" in dep:
                _add_unique("Cache / Key-Value store: Redis")
            if "segmentio/kafka-go" in dep:
                _add_unique("Messaging: Apache Kafka")

        # Very light-weight config/manifest scanning for infra keywords.
        config_dirs = ["config", "deploy", "k8s", ".github", ".config"]
        config_exts = {".yml", ".yaml", ".json", ".tf"}
        keywords = {
            "postgres": "Database: PostgreSQL",
            "mysql": "Database: MySQL / MariaDB",
            "mariadb": "Database: MySQL / MariaDB",
            "mongodb": "Database: MongoDB",
            "redis": "Cache / Key-Value store: Redis",
            "kafka": "Messaging: Apache Kafka",
            "rabbitmq": "Messaging: RabbitMQ",
            "sqs": "Messaging: AWS SQS",
            "sns": "Messaging: AWS SNS",
            "dynamodb": "Database: AWS DynamoDB",
            "elasticsearch": "Search: Elasticsearch / OpenSearch",
            "opensearch": "Search: OpenSearch",
            "memcached": "Cache: Memcached",
        }

        try:
            for path in local_path.rglob("*"):
                if not path.is_file():
                    continue
                if path.suffix in config_exts or any(part in config_dirs for part in path.parts):
                    try:
                        text = path.read_text(encoding="utf-8", errors="ignore").lower()
                    except Exception:
                        continue
                    for token, label in keywords.items():
                        if token in text:
                            _add_unique(label)
        except Exception:
            # Best-effort only; ignore scanning issues.
            pass

        items.extend(infra)
        return items


