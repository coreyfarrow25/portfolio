# DORA Metrics Dashboard: GitHub API → DevOps Performance Benchmarks

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![GitHub API](https://img.shields.io/badge/GitHub%20API-v3-181717?logo=github)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![DORA](https://img.shields.io/badge/Framework-DORA%20Metrics-6366f1)

---

## Problem

Engineering and DevOps teams use the four DORA metrics — Deployment Frequency, Lead Time for Changes, Change Failure Rate, and MTTR — to benchmark delivery performance. The [2023 State of DevOps Report](https://dora.dev/) found that elite-performing teams deploy 182× more frequently and recover from failures 2,604× faster than low performers. But most teams don't have visibility into where they sit — the metrics live across GitHub, Jira, PagerDuty, and incident logs, with no single view.

This tool pulls the four DORA metrics for any GitHub repo using the public GitHub API and renders them as a benchmarked dashboard, colored by DORA performance band.

---

## What It Does

```bash
python main.py expressjs/express --days 90
```

```
────────────────────────────────────────────────────────────
  DORA Metrics — expressjs/express  (90-day window)
────────────────────────────────────────────────────────────
  Deployment Frequency           2.4 deploys/week          [High]
    ↳ 31 releases in 90 days
  Lead Time for Changes          18.3 hours (median)       [High]
    ↳ Across 147 merged PRs
  Change Failure Rate            6.5 %                     [High]
    ↳ 2 of 31 releases had a bug opened within 24h
  Mean Time to Recovery          41.2 hours (median)       [Medium]
    ↳ Across 58 resolved issues
────────────────────────────────────────────────────────────
```

Also saves a color-coded 2×2 dashboard PNG to `output/dora_dashboard.png`.

**Data sources:**
| Metric | GitHub API endpoint | Proxy logic |
|---|---|---|
| Deployment Frequency | `/repos/{owner}/{repo}/releases` | Release count ÷ weeks in window |
| Lead Time | `/repos/{owner}/{repo}/pulls?state=closed` | PR open → merge timestamp (median) |
| Change Failure Rate | Releases + `/issues?labels=bug` | Bug issues opened within 24h of a release |
| MTTR | `/repos/{owner}/{repo}/issues?labels=bug` | Issue open → close timestamp (median) |

---

## Product Decisions & Tradeoffs

**Why GitHub Releases as the deployment proxy, not workflow runs or deployment events?**
GitHub's `/deployments` API requires repos to explicitly create deployment objects — most open-source and SaaS repos don't. Workflow runs would be more granular but require `actions` scope and produce too many false positives (every CI run would count). Releases are the most reliable signal across repos with no special configuration: a tagged release is intentional, reviewable, and close enough to "shipped to production" for benchmarking purposes. The README is explicit about this limitation so users don't misread the numbers.

**Why median instead of mean for Lead Time and MTTR?**
Both distributions are right-skewed — a few very long PRs or incidents would inflate the mean significantly. Median is more interpretable and matches how DORA recommends reporting. For a team dashboard you'd also want to show p75 and p90 to surface tail risk, which is in the v2 roadmap.

**Why fall back to all closed issues when no "bug" label exists?**
Many repos don't use a consistent labeling convention. Returning zero for MTTR when there are hundreds of resolved issues would be misleading. The fallback makes the tool useful out of the box for most repos, with a console note explaining which data was used. A stricter mode (`--strict-labels`) is in the roadmap.

**Why make the repo a CLI argument instead of a config file?**
The tool is designed to be run ad hoc against any repo — a config file would imply a persistent installation, which adds setup friction. The right interface for a one-off analysis is a single command. If this were embedded in a CI pipeline, the repo could be read from `$GITHUB_REPOSITORY` automatically, which the `--token` flag already supports via `GITHUB_TOKEN`.

**What these metrics can't tell you:**
- They use public GitHub data — internal deploy pipelines (Jenkins, Spinnaker, ArgoCD) aren't reflected
- Change Failure Rate is a conservative undercount: many bugs don't get a "bug" label, and many post-deploy issues get fixed silently in the next PR
- Lead Time from PR open ≠ lead time from first commit — PR open is a later and shorter window. True lead time requires commit-level data per PR (one additional API call per PR), which would burn rate limits on large repos. This is noted inline in the code.

**Scope decision I explicitly did not make:** I considered adding Jira integration to pull incident tickets for MTTR (since many teams track incidents in Jira, not GitHub Issues). I cut it from v1 because it would require OAuth and a different auth model, tripling setup complexity for a feature most users couldn't use. The right v2 path is a plugin architecture where data sources are swappable — see roadmap below.

---

## v2 Roadmap

| Feature | Rationale |
|---|---|
| Commit-level lead time | True lead time (first commit → deploy) requires fetching commits per PR — feasible but rate-limit-sensitive |
| p75 / p90 percentiles | Better tail risk visibility for Lead Time and MTTR |
| `--strict-labels` flag | Only use explicitly labeled bugs/incidents; return N/A otherwise |
| CSV export | `--csv` flag for teams who want to track trends over time |
| Multi-repo comparison | Compare DORA bands across a portfolio of repos in one chart |
| Plugin data sources | Swap GitHub Issues for PagerDuty or Jira for more accurate MTTR |

---

## Tech

```
dora-metrics-dashboard/
├── main.py                   # CLI entry point (argparse)
├── requirements.txt
├── .env.example              # GITHUB_TOKEN template
├── dora/
│   ├── github_client.py      # API wrapper: auth, pagination, rate limit back-off
│   ├── metrics.py            # DORA calculations + DORA band classification
│   └── visualize.py          # Matplotlib 2×2 dashboard
└── output/                   # Generated PNGs (gitignored)
```

| Dependency | Purpose |
|---|---|
| `requests` | GitHub REST API calls |
| `python-dotenv` | Load `GITHUB_TOKEN` from `.env` |
| `matplotlib` | Dashboard visualization |
| `numpy` | Percentile calculations |

---

## How to Run

```bash
# 1. Clone and install
git clone https://github.com/coreyfarrow25/portfolio
cd dora-metrics-dashboard
pip install -r requirements.txt

# 2. Set your GitHub token (optional but recommended)
cp .env.example .env
# Edit .env and add your token — generate at github.com/settings/tokens
# Scope needed: public_repo

# 3. Run against any public repo
python main.py expressjs/express
python main.py axios/axios --days 60
python main.py owner/repo --token ghp_yourtoken --out results/

# 4. Skip the chart and just print to console
python main.py expressjs/express --no-chart
```

The dashboard PNG is saved to `output/dora_dashboard.png` by default.

> Without a token you get 60 API requests/hour (unauthenticated). That's usually enough for one run on a mid-sized repo. Set `GITHUB_TOKEN` for 5,000/hour.
