from __future__ import annotations

from typing import List

from .git_providers import GitHubProvider, RepoRef


def discover_org_repos(provider: GitHubProvider, org_identifier: str) => List[RepoRef]:
    """
    Discover repositories for an organization given either a URL or an org name.
    """
    if "/" in org_identifier:
        org_name = org_identifier.rstrip("/").split("/")[-1]
    else:
        org_name = org_identifier
    return provider.get_organization_repos(org_name)

