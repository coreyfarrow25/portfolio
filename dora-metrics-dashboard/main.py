#!/usr/bin/env python3
"""
DORA Metrics Dashboard — CLI entry point.

Usage:
    python main.py expressjs/express
    python main.py expressjs/express --days 60
    python main.py expressjs/express --token ghp_... --out results/
"""
import argparse
import os
import sys

from dotenv import load_dotenv

from dora.github_client import GitHubClient
from dora.metrics import DoraMetrics
from dora.visualize import generate_dashboard

load_dotenv()


def print_results(results: list, repo: str, days: int) -> None:
    bar = "─" * 60
    print(f"\n{bar}")
    print(f"  DORA Metrics — {repo}  ({days}-day window)")
    print(bar)
    for r in results:
        band_pad = f"[{r.band}]".ljust(10)
        print(f"  {r.label:<30} {str(r.value) + ' ' + r.unit:<25} {band_pad}")
        print(f"    ↳ {r.detail}")
    print(bar + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="DORA Metrics Dashboard — GitHub API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py expressjs/express
  python main.py expressjs/express --days 60
  python main.py your-org/your-repo --token ghp_... --out results/

Authentication:
  Set GITHUB_TOKEN in your environment or .env file.
  Without a token you get 60 requests/hr (usually enough for one run).
        """,
    )
    parser.add_argument("repo", help="GitHub repo in owner/repo format")
    parser.add_argument("--days", type=int, default=90,
                        help="Lookback window in days (default: 90)")
    parser.add_argument("--token", default=None,
                        help="GitHub personal access token (overrides GITHUB_TOKEN env var)")
    parser.add_argument("--out", default="output",
                        help="Output directory for the dashboard PNG (default: output/)")
    parser.add_argument("--no-chart", action="store_true",
                        help="Print metrics to console only, skip chart generation")
    args = parser.parse_args()

    if "/" not in args.repo:
        print(f"[error] repo must be in owner/repo format, got: {args.repo}")
        sys.exit(1)

    print(f"\nFetching DORA metrics for {args.repo} ({args.days}-day window)...")

    client = GitHubClient(token=args.token)

    # Validate repo exists
    try:
        info = client.get_repo_info(args.repo)
        print(f"Repo: {info['full_name']} — ⭐ {info['stargazers_count']:,} stars")
    except Exception as e:
        print(f"[error] Could not fetch repo info: {e}")
        sys.exit(1)

    metrics = DoraMetrics(client, args.repo, days=args.days)
    results = metrics.all()

    print_results(results, args.repo, args.days)

    if not args.no_chart:
        out_path = generate_dashboard(metrics, args.repo, out_dir=args.out)
        print(f"Dashboard saved → {out_path}\n")


if __name__ == "__main__":
    main()
