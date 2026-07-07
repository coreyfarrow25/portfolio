# GitHub Actions: Flaky Test Detection & Triage — Self-Directed Product Case Study

> **Type:** Self-directed feature teardown / mini-PRD
> **Target product:** GitHub Actions
> **Scope:** New native feature proposal
> **Framework:** RICE prioritization + success metrics

---

## Problem

Flaky tests — tests that fail non-deterministically without a real code regression — are one of the most expensive, invisible drains on engineering velocity. When a CI run fails on GitHub Actions, a developer has no way to know whether the failure is real or flaky. The only recourse is to re-run the job and hope. At scale, this behavior is nearly universal and deeply damaging:

- **Alert fatigue:** developers learn to distrust CI, so they re-run failures reflexively before investigating — sometimes two or three times per PR
- **Lead time inflation:** each re-run adds 5–30 minutes of idle wait, directly inflating the Lead Time for Changes DORA metric
- **Invisible debt:** flaky tests are tracked, if at all, in wikis, Slack threads, or by institutional memory — not in the tool where the failures appear

GitHub Actions has no native flaky test detection. Competing CI platforms (BuildKite, CircleCI, Buildkite) have shipped partial solutions, creating a gap in a core GitHub product surface that developers visit multiple times daily.

**The root cause isn't the flaky tests themselves — it's that GitHub Actions has no memory.** Every run is stateless from the product's perspective. A test that has failed on the first run and passed on re-run 40 times in the last 90 days looks identical to a test that just broke for the first time.

---

## Target User

**Primary:** Platform engineers and DevEx (Developer Experience) teams at companies with 20–500 engineers. They own CI configuration, manage test infrastructure, and field complaints about slow or unreliable pipelines. Flaky tests are their most common support ticket.

**Secondary:** Senior engineers and tech leads who review CI failures during code review. They lose the most time to re-run cycles and make the most noise when CI is unreliable.

**Not the primary user:** Individual contributors at small teams (<10 engineers). Flaky test problems exist there too, but the pain is diffuse enough that a dedicated tab doesn't justify the context switch. The right surface for them is an inline warning on the PR, not a separate management UI.

---

## Proposed Solution: GitHub Actions Flaky Tests Tab

A native "Flaky Tests" tab inside the GitHub Actions UI that surfaces historical pass/fail patterns per test, ranked by impact on CI reliability.

**How it works:**

Most test frameworks (Jest, pytest, JUnit, RSpec, Go test) can output results in JUnit XML format. GitHub Actions already accepts artifact uploads — the Flaky Tests feature would parse JUnit XML artifacts uploaded from test steps and build a per-test history over time.

**Core feature set (v1 MVP):**

1. **Flaky test detection** — A test is flagged as "potentially flaky" when it fails on the first attempt but passes on a re-run, OR when its pass rate over the last 90 days falls between 55–95% (consistently passing tests and consistently failing tests are not flaky — only the in-between range is)

2. **Ranked flaky test list** — A table showing test name, failure rate, number of affected PRs in the last 30 days, and the workflow/job where it appears. Sortable by failure rate and PR impact.

3. **Acknowledgement mechanism** — Engineers can mark a test as "acknowledged" (known flaky, being tracked) to reduce noise in CI failure views without removing the test. Acknowledgements expire after 30 days to prevent tests from staying silently broken.

4. **Inline PR warning** — When a PR's CI run has failures that match known flaky tests, show a dismissible banner: "1 of 3 test failures matches a known flaky test — consider re-running before investigating." Reduces re-run friction without automating re-runs.

5. **Workflow-level flakiness score** — An aggregate "reliability score" per workflow (% of runs in the last 30 days that passed on first attempt), visible on the Actions tab. Gives platform teams a single number to track over time.

**Out of scope for v1:**
- Automatic re-runs (reduces signal; teams need to know flaky tests exist, not have them hidden)
- Flakiness alerting / notifications (too noisy without first establishing baseline signal)
- Custom test runner support beyond JUnit XML (too much format fragmentation for MVP)

---

## RICE Prioritization

Scored against other GitHub Actions roadmap candidates (hypothetical):

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---|---|---|---|---|---|
| **Flaky Test Detection** | **8** | **9** | **8** | **4** | **144** |
| Workflow cost attribution | 6 | 7 | 7 | 5 | 59 |
| Matrix build visualization | 5 | 6 | 8 | 3 | 80 |
| Required workflow approvals | 4 | 5 | 9 | 2 | 90 |

**Reach (8/10):** JUnit XML output is supported by nearly every major test framework and is already a common artifact upload pattern in GitHub Actions. Adoption doesn't require changing how teams write or run tests — only uploading the existing output file. Estimated 60–70% of Actions users with test steps would be able to use this without any workflow changes.

**Impact (9/10):** Flaky tests are the most-cited reason developers distrust CI. Reducing re-run cycles directly improves DORA's Lead Time metric. The inline PR warning addresses the highest-friction moment (deciding whether to investigate or re-run) in a developer's daily workflow.

**Confidence (8/10):** The problem is well-documented (Google SRE, the DORA research program, and internal eng blogs from Netflix, Spotify, and Airbnb all name flaky tests as a top reliability issue). Competitive analogues exist (BuildKite's Flaky Tests feature, CircleCI's Flaky Test Management). JUnit XML parsing is solved infrastructure.

**Effort (4/10 — high effort):** Requires: a JUnit XML parser, per-test history storage with a retention policy, a new UI tab in the Actions interface, PR integration for the inline warning, and an acknowledgement data model. This is a medium-large engineering investment — estimated 2–3 quarters for a small team. The high impact justifies it.

---

## Success Metrics

**Primary (ship/no-ship):**
- **Re-run rate reduction:** % decrease in manual job re-runs per PR within 60 days of feature launch. Target: −20% for repos that adopt JUnit XML upload.
- **Flaky test acknowledgement rate:** % of detected flaky tests that get acknowledged within 7 days. Proxy for whether teams are engaging with the feature vs. ignoring it. Target: >40% within 30 days of first detection.

**Secondary (health indicators):**
- JUnit XML artifact upload rate (adoption vector — are teams uploading the required file?)
- Avg Lead Time for Changes (DORA) for repos using the feature vs. control group
- Inline warning dismissal rate on PRs (too high = warning is noise; too low = warning isn't being seen)

**What I'm explicitly not tracking as a success metric:** raw flaky test count. Surfaces more tests doesn't mean the feature is working — teams might just have more visibility into pre-existing debt. The behavior change is what matters: fewer re-runs, more acknowledged tests, lower lead time.

---

## Key Tradeoffs Documented

**JUnit XML as the only input format.** This is the right MVP scoping decision — JUnit XML has the broadest framework support — but it excludes teams using custom test runners, TAP format, or test frameworks without XML output (some Go and Rust testing setups). The honest tradeoff: we pick up 70% of users cleanly and explicitly defer the rest. The wrong move is to try to parse 10 different formats in v1 and do all of them poorly.

**Acknowledgement mechanism risks test debt.** If "acknowledge" becomes a way to stop being reminded about flaky tests without fixing them, the feature becomes a debt accumulation tool. The 30-day expiry is the mitigation, but it's imperfect — a sufficiently low-friction renewal will get clicked without thought. A v2 improvement: require a linked GitHub Issue when acknowledging, so the debt is tracked in the backlog, not just dismissed.

**No automatic re-runs.** The tempting product direction here is to auto-retry flaky tests. BuildKite offers this. I scoped it out because it creates a perverse incentive: if CI automatically hides flaky failures, teams have less reason to fix them. The goal is visibility and triage, not suppression. This is a values-level product decision, not just a scope decision.

---

## Competitive Context

| Product | Feature | Gap |
|---|---|---|
| BuildKite | Flaky Tests tab (native) | Enterprise-only; requires BuildKite CI migration |
| CircleCI | Flaky Test Management | Requires CircleCI-specific test metadata; not portable |
| GitHub Actions | None | Only product with the reach to address this at industry scale |
| Datadog CI Visibility | Flaky test detection | Requires Datadog agent; adds cost and vendor dependency |

GitHub's advantage isn't the feature — it's the distribution. GitHub Actions already has the test run data, the PR context, and the developer's daily workflow. The Flaky Tests feature requires no new integrations, no new vendor relationships, and no migration. That's the product moat.

---

## v2 Roadmap

| Feature | Why deferred |
|---|---|
| Auto-retry on known flaky tests | Risk of masking debt; needs adoption data first |
| Flaky test alerting (email/Slack) | Too noisy without first establishing baseline signal |
| Custom format support (TAP, etc.) | Fragmentation risk; solve the 70% first |
| Cross-repo flakiness trends | Useful for platform teams at large orgs; needs org-level UI surface |
| Linked Issue requirement for acknowledgement | Reduces debt risk; adds friction that may hurt adoption in v1 |
