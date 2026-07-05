"""
GitHub API client with authentication and rate limit handling.
"""
import os
import time
import requests
from datetime import datetime, timezone


class GitHubClient:
    """
    Thin wrapper around the GitHub REST API v3.
    Handles authentication, pagination, and rate limit back-off.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: str | None = None):
        token = token or os.getenv("GITHUB_TOKEN")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        else:
            print(
                "[warn] No GITHUB_TOKEN set — using unauthenticated API "
                "(60 req/hr limit). Set GITHUB_TOKEN for 5,000 req/hr."
            )

    # ------------------------------------------------------------------
    # Core request helper
    # ------------------------------------------------------------------

    def _get(self, path: str, params: dict | None = None) -> dict | list:
        url = f"{self.BASE_URL}{path}"
        resp = self.session.get(url, params=params, timeout=15)

        # Rate limit: wait and retry once
        if resp.status_code == 403 and "rate limit" in resp.text.lower():
            reset_ts = int(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            wait = max(reset_ts - int(time.time()), 1)
            print(f"[rate limit] Waiting {wait}s before retrying...")
            time.sleep(wait)
            resp = self.session.get(url, params=params, timeout=15)

        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Paginated list fetcher
    # ------------------------------------------------------------------

    def get_all(self, path: str, params: dict | None = None, max_pages: int = 10) -> list:
        """Fetch all pages of a list endpoint (up to max_pages)."""
        params = dict(params or {})
        params.setdefault("per_page", 100)
        results = []
        for page in range(1, max_pages + 1):
            params["page"] = page
            data = self._get(path, params)
            if not data:
                break
            results.extend(data)
            if len(data) < params["per_page"]:
                break
        return results

    # ------------------------------------------------------------------
    # Domain helpers
    # ------------------------------------------------------------------

    def get_releases(self, repo: str) -> list:
        """Return all releases for a repo, newest first."""
        return self.get_all(f"/repos/{repo}/releases")

    def get_merged_prs(self, repo: str, since: str) -> list:
        """Return merged PRs updated since `since` (ISO 8601 string)."""
        prs = self.get_all(
            f"/repos/{repo}/pulls",
            params={"state": "closed", "sort": "updated", "direction": "desc"},
        )
        return [
            pr for pr in prs
            if pr.get("merged_at") and pr["merged_at"] >= since
        ]

    def get_issues(self, repo: str, since: str, labels: str = "") -> list:
        """Return closed issues since `since`, optionally filtered by labels."""
        params = {"state": "closed", "since": since, "per_page": 100}
        if labels:
            params["labels"] = labels
        return self.get_all(f"/repos/{repo}/issues", params=params)

    def get_repo_info(self, repo: str) -> dict:
        return self._get(f"/repos/{repo}")

    # ------------------------------------------------------------------
    # Timestamp utility
    # ------------------------------------------------------------------

    @staticmethod
    def parse_dt(iso_str: str) -> datetime:
        """Parse a GitHub ISO 8601 timestamp to a UTC-aware datetime."""
        return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
