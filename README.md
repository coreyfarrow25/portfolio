# Corey Farrow — Product Management Portfolio

Targeting APM roles at SaaS and DevOps companies. Work below spans product prioritization, PRD writing, user research, and data-informed decision-making. I'm most interested in products that engineering teams use every day — CI/CD, observability, developer productivity.

---

## Product Case Studies

---

### BeReal: Mood Prompt — Feature Prioritization Using RICE Framework

> **Externship** · Full PM cycle: research → prioritization → PRD → user testing → stakeholder pitch

**Problem:** BeReal's engagement loop drives a daily post but gives users no way to express emotional context — you see what someone is doing, not how they feel. Compared to Snapchat's streaks and reactions, BeReal posts create weak social signals and limited repeat interaction. The question: could adding emotional context improve retention without breaking BeReal's "authentic and unfiltered" brand?

**Approach:**
1. Mapped the full BeReal user journey and ran a sentiment analysis of user reviews for BeReal's "Time to BeReal" notification vs. Snapchat's Snapstreaks — coded for where each feature drives and loses engagement
2. Generated 8 feature candidates and scored them using RICE across Reach, Impact, Confidence, and Effort
3. Wrote a PRD-Lite for the winning feature (Mood Prompt), including problem statement, success metrics, MVP scope, non-goals, and open questions
4. Designed and ran user testing: focus group plan, 12-question survey (n=47), test summary report
5. Delivered a 5-minute stakeholder pitch with evidence pack and retention modeling

**Feature selected — Mood Prompt:** A one-tap mood selector (5 emoji options) that fires before the camera opens when the daily notification arrives. The mood tag appears beneath the photo in friends' feeds. Opt-in in v1.

**RICE outcome:**

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| **Mood Prompt** | **9** | **8** | **8** | **3** | **192** |
| Reaction Expansion | 8 | 7 | 7 | 4 | 98 |
| Location Tags | 7 | 6 | 6 | 5 | 50 |

**Key decisions:**
- Mood Prompt beat Reaction Expansion on Confidence — adding more reactions risks engagement fragmentation (Instagram precedent). It beat Location Tags on Impact — location sharing is a trust risk given BeReal's anonymous-first identity.
- User testing killed mandatory mood selection: 61% of respondents said they'd skip posting entirely if required. Opt-in is the right scope. The PRD's most important non-goal is mandatory selection.
- Chose a focus group over an A/B test because the feature was pre-prototype. Directional signal on "does emotional context add value?" was faster and cheaper than building a prototype.

**Success metrics defined:** Primary — 30-day retention for users who post with Mood Prompt vs. control. Secondary — daily completion rate (posts with mood tag ÷ total notifications fired).

📁 **Artifacts:** [`bereal-feature-prioritization/`](./bereal-feature-prioritization/)
- [RICE Scoring Table](./bereal-feature-prioritization/feature-development/)
- [PRD-Lite: Mood Prompt](./bereal-feature-prioritization/feature-development/)
- [Test Summary Report](./bereal-feature-prioritization/user-testing/)
- [Pitch Script & Evidence Pack](./bereal-feature-prioritization/pitch/)

---

### GitHub Actions: Flaky Test Detection & Triage — Self-Directed Feature Teardown

> **Self-directed** · Mini-PRD for a real product gap in GitHub Actions

**Problem:** GitHub Actions has no memory across runs — a test that has failed on first run and passed on re-run 40 times looks identical to a brand-new failure. Developers can't distinguish real regressions from flaky tests, so they re-run CI jobs reflexively before investigating. At scale this inflates DORA Lead Time, erodes CI trust, and accumulates invisible test debt tracked in wikis instead of the tool where the failures appear.

**Proposed feature:** A native "Flaky Tests" tab in GitHub Actions that parses JUnit XML artifacts (already output by Jest, pytest, JUnit, RSpec, Go test) to build per-test pass/fail history. Surfaces a ranked flaky test list, an acknowledgement mechanism, and an inline PR warning when failures match known flaky tests.

**Scoping rationale:**
- JUnit XML is the right v1 input format: covers ~70% of Actions users with test steps, requires no changes to how teams write tests
- No auto-retry in v1 — automating re-runs hides test debt instead of surfacing it; the goal is visibility, not suppression
- Acknowledgement expires in 30 days to prevent tests from silently staying broken

**RICE score vs. alternatives:** 144 (vs. Workflow Cost Attribution at 59, Matrix Build Visualization at 80) — wins on Reach (JUnit XML is already common) and Impact (directly reduces Lead Time, a DORA metric).

📁 **Full teardown:** [`github-actions-case-study/`](./github-actions-case-study/) — includes full RICE table, success metrics, competitive context (BuildKite, CircleCI, Datadog CI), key tradeoffs, and v2 roadmap.

---

### DORA Metrics Dashboard — DevOps Tool (Python / GitHub API)

> **Built project** · Functional CLI tool, not a case study

A Python CLI that pulls all four DORA metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR) for any GitHub repo and renders them as a benchmarked, color-coded dashboard.

```bash
python main.py expressjs/express --days 90
# → prints metrics with DORA band (Elite/High/Medium/Low) + saves dashboard PNG
```

Built this to understand what DevOps teams actually measure and where the tooling gaps are. The README documents the proxy decisions (why Releases instead of workflow runs, why median instead of mean) in the same way a PM would document scope decisions in a PRD.

📁 [`dora-metrics-dashboard/`](./dora-metrics-dashboard/)

---

## Data & Analysis

These projects demonstrate quantitative and analytical skills that translate directly to data-informed product decisions — scoping success metrics, evaluating user research data, and pressure-testing assumptions with numbers before writing a PRD.

---

### Consumer Sentiment Pipeline: Beats by Dre Competitive Positioning

> **Externship** · Data analytics role — built the pipeline, synthesized findings into a positioning recommendation

The pipeline found that Beats Pill and JBL Charge 5 were essentially tied on star ratings (4.47★ vs. 4.46★) — but sentiment and word frequency analysis revealed they were winning on *different dimensions*. Beats owned "bass" and "sound quality" in positive language; JBL owned "battery" and "durability." That reframed the competitive risk from "a better-sounding speaker" to "JBL building a reliability positioning that targets a different buyer motivation entirely." The analysis changed the recommendation.

The skill that transfers to PM work: knowing how to use data to reframe a question, not just answer it. Star ratings said "you're tied." Word frequency said "you're differentiated in ways you may not be deliberately building."

📁 [`consumer-insights-nlp/`](./consumer-insights-nlp/) — Python pipeline (EDA → TextBlob sentiment → correlation), 30+ charts, competitive analysis report

---

### Statistics Coursework (R + Python)

Regression analysis, hypothesis testing, probability, and survey data analysis (General Social Survey). These are the mechanics behind interpreting A/B test results, evaluating statistical significance of product metrics, and reading a data science team's analysis without being lost.

📁 [`coursework/`](./coursework/)

---

**Contact:** coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
