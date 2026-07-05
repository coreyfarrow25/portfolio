"""
DORA Metrics calculations using the GitHub API.

Metric definitions and data proxies
────────────────────────────────────
Deployment Frequency  — GitHub Releases per week (tagged releases = production deploys)
Lead Time for Changes — Median time from PR open → PR merge, for PRs in the lookback window
Change Failure Rate   — % of releases followed within 24 h by a bug/incident issue opened
MTTR                  — Median time from bug/incident issue open → close

Why these proxies?
  Not every team uses GitHub Releases for deploys or labels every incident issue.
  These proxies work reliably for repos that do follow those conventions (which is
  most well-maintained open-source and SaaS projects). The README explains where
  the proxies break down and what to wire in instead for internal repos.

DORA performance bands (2023 State of DevOps Report)
  Deployment Frequency  Elite ≥1/day  High ≥1/week  Medium ≥1/month  Low <1/month
  Lead Time             Elite <1hr    High <1day    Medium <1week    Low >1week
  Change Failure Rate   Elite 0-5%    High 6-15%   Medium 16-30%    Low >30%
  MTTR                  Elite <1hr    High <1day    Medium <1week    Low >1week
"""

from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import NamedTuple

from .github_client import GitHubClient


# ── DORA band thresholds ──────────────────────────────────────────────────────

def _deploy_band(per_week: float) -> str:
    if per_week >= 7:   return "Elite"
    if per_week >= 1:   return "High"
    if per_week >= 0.25: return "Medium"
    return "Low"

def _lead_time_band(hours: float) -> str:
    if hours < 1:    return "Elite"
    if hours < 24:   return "High"
    if hours < 168:  return "Medium"
    return "Low"

def _cfr_band(pct: float) -> str:
    if pct <= 5:  return "Elite"
    if pct <= 15: return "High"
    if pct <= 30: return "Medium"
    return "Low"

def _mttr_band(hours: float) -> str:
    if hours < 1:    return "Elite"
    if hours < 24:   return "High"
    if hours < 168:  return "Medium"
    return "Low"


# ── Result types ──────────────────────────────────────────────────────────────

class MetricResult(NamedTuple):
    value: float
    unit: str
    band: str
    label: str
    detail: str


# ── Main metrics class ────────────────────────────────────────────────────────

class DoraMetrics:
    """Compute all four DORA metrics for a given GitHub repo."""

    def __init__(self, client: GitHubClient, repo: str, days: int = 90):
        self.client = client
        self.repo = repo
        self.days = days
        self._since_dt = datetime.now(timezone.utc) - timedelta(days=days)
        self._since_iso = self._since_dt.isoformat()
        self._weeks = days / 7

        # Cached API results (lazy-loaded)
        self._releases: list | None = None
        self._prs: list | None = None
        self._bug_issues: list | None = None

    # ── Data accessors ────────────────────────────────────────────────────────

    def _get_releases(self) -> list:
        if self._releases is None:
            all_releases = self.client.get_releases(self.repo)
            parse = self.client.parse_dt
            self._releases = [
                r for r in all_releases
                if r.get("published_at") and parse(r["published_at"]) >= self._since_dt
            ]
        return self._releases

    def _get_prs(self) -> list:
        if self._prs is None:
            self._prs = self.client.get_merged_prs(self.repo, self._since_iso)
        return self._prs

    def _get_bug_issues(self) -> list:
        if self._bug_issues is None:
            # Try "bug" label first; fall back to all closed issues if none found
            issues = self.client.get_issues(self.repo, self._since_iso, labels="bug")
            if not issues:
                issues = self.client.get_issues(self.repo, self._since_iso)
            self._bug_issues = [i for i in issues if "pull_request" not in i]
        return self._bug_issues

    # ── Metric 1: Deployment Frequency ───────────────────────────────────────

    def deployment_frequency(self) -> MetricResult:
        """
        Releases per week in the lookback window.
        Proxy: GitHub Releases (tagged releases ≈ production deployments).
        """
        releases = self._get_releases()
        per_week = len(releases) / self._weeks
        band = _deploy_band(per_week)
        return MetricResult(
            value=round(per_week, 2),
            unit="deploys/week",
            band=band,
            label="Deployment Frequency",
            detail=f"{len(releases)} releases in {self.days} days",
        )

    # ── Metric 2: Lead Time for Changes ──────────────────────────────────────

    def lead_time_for_changes(self) -> MetricResult:
        """
        Median hours from PR open to PR merge, for PRs merged in the lookback window.
        Proxy: PR open timestamp → merge timestamp (best available without commit-level data).
        Note: true lead time is from first commit to deploy; PR open is a conservative proxy.
        """
        prs = self._get_prs()
        parse = self.client.parse_dt

        durations = []
        for pr in prs:
            if pr.get("created_at") and pr.get("merged_at"):
                created = parse(pr["created_at"])
                merged = parse(pr["merged_at"])
                durations.append((merged - created).total_seconds() / 3600)

        if not durations:
            return MetricResult(0, "hours", "N/A", "Lead Time for Changes",
                                "No merged PRs found in window")

        durations.sort()
        median = durations[len(durations) // 2]
        band = _lead_time_band(median)
        return MetricResult(
            value=round(median, 1),
            unit="hours (median)",
            band=band,
            label="Lead Time for Changes",
            detail=f"Across {len(durations)} merged PRs",
        )

    # ── Metric 3: Change Failure Rate ─────────────────────────────────────────

    def change_failure_rate(self) -> MetricResult:
        """
        % of releases followed within 24 h by a bug issue being opened.
        Proxy: bug-labeled issues opened within 24 h of a release publish date.
        """
        releases = self._get_releases()
        bug_issues = self._get_bug_issues()

        if not releases:
            return MetricResult(0, "%", "N/A", "Change Failure Rate",
                                "No releases in window")

        parse = self.client.parse_dt
        failed = 0
        for release in releases:
            release_dt = parse(release["published_at"])
            window_end = release_dt + timedelta(hours=24)
            for issue in bug_issues:
                if issue.get("created_at"):
                    created = parse(issue["created_at"])
                    if release_dt <= created <= window_end:
                        failed += 1
                        break  # one failure per release is enough

        rate = (failed / len(releases)) * 100
        band = _cfr_band(rate)
        return MetricResult(
            value=round(rate, 1),
            unit="%",
            band=band,
            label="Change Failure Rate",
            detail=f"{failed} of {len(releases)} releases had a bug opened within 24h",
        )

    # ── Metric 4: Mean Time to Recovery ──────────────────────────────────────

    def mttr(self) -> MetricResult:
        """
        Median hours from bug issue open to close.
        Proxy: closed bug/incident issues in the lookback window.
        """
        bug_issues = self._get_bug_issues()
        parse = self.client.parse_dt

        durations = []
        for issue in bug_issues:
            if issue.get("created_at") and issue.get("closed_at"):
                opened = parse(issue["created_at"])
                closed = parse(issue["closed_at"])
                durations.append((closed - opened).total_seconds() / 3600)

        if not durations:
            return MetricResult(0, "hours", "N/A", "MTTR",
                                "No closed bug issues found in window")

        durations.sort()
        median = durations[len(durations) // 2]
        band = _mttr_band(median)
        return MetricResult(
            value=round(median, 1),
            unit="hours (median)",
            band=band,
            label="Mean Time to Recovery",
            detail=f"Across {len(durations)} resolved issues",
        )

    # ── All metrics ───────────────────────────────────────────────────────────

    def all(self) -> list[MetricResult]:
        return [
            self.deployment_frequency(),
            self.lead_time_for_changes(),
            self.change_failure_rate(),
            self.mttr(),
        ]
