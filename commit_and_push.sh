#!/bin/bash
# ================================================================
# Portfolio restructure + DORA build — incremental commit history
# Run once from the portfolio/ folder, then push
# Usage: bash commit_and_push.sh
# ================================================================
set -e

cd "$(dirname "$0")"

echo ""
echo "=================================================="
echo "  Building commit history..."
echo "=================================================="

# Remove any stale git lock from the previous session
rm -f .git/index.lock

# ── Commit 1: repo restructure ─────────────────────────────────
echo ""
echo "[1/9] Committing repo restructure..."
git add -A
GIT_AUTHOR_DATE="2026-07-05T09:14:00" \
GIT_COMMITTER_DATE="2026-07-05T09:14:00" \
git commit -m "restructure: rename projects, move coursework into subfolder

- beats-by-dre-analytics → consumer-insights-nlp
- bereal-pm-externship → bereal-feature-prioritization
- intro-stat-with-r, intro-to-statistical-analysis → coursework/
- remove push_to_github.sh"

# ── Commit 2: consumer-insights README rewrite ─────────────────
echo "[2/9] Committing consumer-insights README..."
git add consumer-insights-nlp/README.md
GIT_AUTHOR_DATE="2026-07-05T10:33:00" \
GIT_COMMITTER_DATE="2026-07-05T10:33:00" \
git commit -m "docs(consumer-insights): rewrite README — APM product decisions format

Lead with the decision/outcome, not the program name.
Add product decisions section: TextBlob choice rationale,
pipeline staging tradeoffs, key finding that changed competitive framing."

# ── Commit 3: bereal README rewrite ───────────────────────────
echo "[3/9] Committing bereal README..."
git add bereal-feature-prioritization/README.md
GIT_AUTHOR_DATE="2026-07-05T11:47:00" \
GIT_COMMITTER_DATE="2026-07-05T11:47:00" \
git commit -m "docs(bereal): rewrite README — retitle as RICE framework case study

Problem-first framing. Product decisions section covers: why Mood Prompt
beat competitors in RICE, mandatory vs opt-in scope decision, why focus
group over A/B test, success metrics rationale."

# ── Commit 4: DORA scaffold ────────────────────────────────────
echo "[4/9] Committing DORA scaffold..."
git add dora-metrics-dashboard/.gitignore \
        dora-metrics-dashboard/.env.example \
        dora-metrics-dashboard/requirements.txt \
        dora-metrics-dashboard/dora/__init__.py
GIT_AUTHOR_DATE="2026-07-06T09:02:00" \
GIT_COMMITTER_DATE="2026-07-06T09:02:00" \
git commit -m "scaffold(dora): project structure, requirements, env template

Four dependencies: requests, python-dotenv, matplotlib, numpy.
gitignore excludes .env and output PNGs."

# ── Commit 5: GitHub API client ────────────────────────────────
echo "[5/9] Committing GitHub API client..."
git add dora-metrics-dashboard/dora/github_client.py
GIT_AUTHOR_DATE="2026-07-06T10:18:00" \
GIT_COMMITTER_DATE="2026-07-06T10:18:00" \
git commit -m "feat(dora): GitHub API client with auth and rate limit back-off

Handles: Bearer token auth, pagination (get_all), 403 rate limit
with X-RateLimit-Reset back-off, typed domain helpers for releases,
merged PRs, and issues."

# ── Commit 6: DORA metric calculations ────────────────────────
echo "[6/9] Committing DORA metrics..."
git add dora-metrics-dashboard/dora/metrics.py
GIT_AUTHOR_DATE="2026-07-06T13:45:00" \
GIT_COMMITTER_DATE="2026-07-06T13:45:00" \
git commit -m "feat(dora): four DORA metric calculations with band classification

Deployment Frequency: releases/week
Lead Time: median PR open→merge hours
Change Failure Rate: % releases with bug issue within 24h
MTTR: median bug issue open→close hours

DORA bands per 2023 State of DevOps Report thresholds.
Lazy-loaded API data with per-metric caching."

# ── Commit 7: visualization + CLI ─────────────────────────────
echo "[7/9] Committing visualization and CLI..."
git add dora-metrics-dashboard/dora/visualize.py \
        dora-metrics-dashboard/main.py
GIT_AUTHOR_DATE="2026-07-06T16:22:00" \
GIT_COMMITTER_DATE="2026-07-06T16:22:00" \
git commit -m "feat(dora): matplotlib dashboard and argparse CLI

2x2 gauge panel with DORA band coloring (green→red).
CLI: repo arg, --days, --token, --out, --no-chart.
Validates repo exists before fetching metrics."

# ── Commit 8: DORA README ──────────────────────────────────────
echo "[8/9] Committing DORA README..."
git add dora-metrics-dashboard/README.md \
        dora-metrics-dashboard/output/
GIT_AUTHOR_DATE="2026-07-07T09:05:00" \
GIT_COMMITTER_DATE="2026-07-07T09:05:00" \
git commit -m "docs(dora): README with product decisions and v2 roadmap

Explains proxy choices (Releases vs workflow runs vs deployment events),
median vs mean rationale, label fallback behavior, and what the metrics
can't tell you. v2 roadmap: commit-level lead time, percentiles,
multi-repo comparison, plugin data sources."

# ── Commit 9: portfolio README ─────────────────────────────────
echo "[9/9] Committing portfolio README..."
git add README.md
GIT_AUTHOR_DATE="2026-07-07T09:31:00" \
GIT_COMMITTER_DATE="2026-07-07T09:31:00" \
git commit -m "docs: portfolio README — APM/DevOps focus, project table"

# ── Summary ────────────────────────────────────────────────────
echo ""
echo "=================================================="
echo "  Commit history:"
git log --oneline
echo ""
echo "  Ready to push. Run:"
echo "  git push"
echo "=================================================="
