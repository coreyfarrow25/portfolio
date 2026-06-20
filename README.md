# Corey Farrow — Product Management Portfolio

## Why Product Management

Sociology is the study of how systems shape human behavior — and how humans, in turn, reshape systems. My concentration at UVA is Global Economy, Organizations, and Work: how institutions are designed, how people move through them, and where the design breaks down.

Most technology is built by people who think about systems first and humans second. That produces tools that work technically but fail socially — enterprise software that nobody uses because it was designed around a process diagram instead of the actual way people work, consumer apps that grow fast and retain poorly because they optimized for engagement metrics instead of genuine value. The technical problem gets solved. The human problem doesn't.

I came to product management because it's the role where that gap is supposed to close. A PM is accountable for both: the system has to work, *and* it has to be something people actually want to use. Sociology trained me to look for the gap between what a system is designed to do and what people actually do inside it. That gap is usually where the real product problem lives.

My background in stakeholder management — coordinating state agencies, university partners, and long-term care administrators at Tellegacy; building district-wide engagement pipelines across 36 organizations at CBATES; restructuring operations at Panera — is the operational side of that same skill: understanding what different people need from a system, and building something that works for all of them simultaneously. Not compromise. Synthesis.

The emotional intelligence piece isn't soft. At Panera, diagnosing *why* the waste reduction initiative would or wouldn't stick required understanding the team's relationship to the process — not just redesigning the process. At BeReal, the most important product decision wasn't which feature to build; it was understanding what emotional state users are in when the notification fires, and designing for that state. The same data that tells you 40% of users post in the 2-minute window tells you something about trust and habit. You have to read both signals.

I want to build products that work for people — not just products that work. I'm drawn to tools that engineers and operators use every day, where the quality of the experience directly affects whether someone can do their job well. I'm also drawn to consumer products where emotional design isn't a veneer on top of the product but a structural feature of how it works. Both require the same underlying skill: understanding what people actually need, not just what they ask for.

---

## Product Case Studies

---

### BeReal: Mood Prompt — Feature Prioritization Using RICE Framework

> **Externship** · Full PM cycle: research → prioritization → PRD → user testing plan → stakeholder pitch

**Problem:** BeReal had strong engagement metrics — 40M MAUs, 25M DAUs, 62.5% DAU:MAU, 70% of users posting daily — but its posts generated one burst of social interaction and went quiet. You could see what someone was doing; you had no signal about how they felt. Compared to Snapchat's streaks and reaction systems, BeReal's social layer was thin. The question: could adding emotional context improve retention without breaking the "authentic, unfiltered" brand that drove 40% of users to post within the 2-minute window?

**Approach:**
1. Mapped the full BeReal user journey across 5 stages; coded sentiment across 10 themes (~100 quotes per theme) for BeReal's notification mechanic vs. Snapchat Streaks
2. Generated 8 feature candidates and scored each using RICE
3. Wrote a PRD-Lite for the winning feature (Mood Prompt): problem statement, success metrics, MVP scope, non-goals, open questions
4. Designed a user testing plan: focus group guide (5-10 participants), 12-question survey instrument, pre-specified analysis framework
5. Delivered a 5-minute stakeholder pitch with evidence pack, competitive benchmarks, and retention modeling

**Feature selected — Mood Prompt:** A one-tap mood selector (5 emoji options) that fires as a dismissible overlay before the camera opens when the daily notification arrives. Opt-in in v1.

**RICE outcome:**

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| **Mood Prompt** | **9** | **8** | **8** | **3** | **192** |
| Reaction Expansion | 8 | 7 | 7 | 4 | 98 |
| Location Tags | 7 | 6 | 6 | 5 | 50 |

**Key decisions:**
- Eliminated Reaction Expansion on Confidence — Instagram's move from Likes to Reactions showed engagement fragmentation, not depth gains. Eliminated Location Tags on Impact — location sharing is a trust risk in a product built on authenticity.
- Scoped Mood Prompt as opt-in after identifying that mandatory mood selection before the camera opens risks post abandonment — it adds a decision gate to a behavior that works precisely because it's frictionless.
- Chose focus group over A/B test because the feature was pre-prototype. The right first question was whether emotional context feels authentic or forced, not which version converts better.

📁 **Artifacts:** [`bereal-feature-prioritization/`](./bereal-feature-prioritization/)

---

### B2B Workflow Teardown: Asana's Momentum Gap — Self-Directed Feature Teardown

> **Self-directed** · Competitive teardown of Jira / Linear / Asana + feature proposal

**Problem:** Asana, Jira, and Linear are all built around task creation and deadlines. None have a mechanism for detecting mid-execution stall before a task is already overdue. The notification model across all three is deadline-reactive: you learn something is late after it's late. By the time the alert fires, the sprint is already broken. PMs managing cross-functional work don't know which tasks need attention until the damage is done.

**Proposed feature — Workflow Health Signals:** A real-time stall detection layer that tracks activity signals at the task level (comments, subtask completion, status transitions) and surfaces a "Health" indicator before a task crosses its deadline. Flags at-risk tasks in a weekly digest for project owners; sends a lightweight in-app nudge to assignees.

**Scoping rationale:**
- Rules-based heuristic in v1, not ML — "your task hasn't had activity in 4 days" is interpretable; a confidence score isn't
- No automated status updates — automation hides the signal instead of surfacing it
- Nudge copy framed as "anything blocking you?" not "you haven't updated this" — will A/B test in beta

**RICE score vs. alternatives:** 141 (vs. Smart Status Auto-Update at 112, OKR Linking at 42, AI Task Summarizer at 80) — wins on Impact (stall is the root cause of missed sprint commitments) and Reach (affects every PM and EM, not a niche workflow).

📁 **Full teardown:** [`b2b-workflow-teardown/`](./b2b-workflow-teardown/) — competitive landscape, full RICE table, PRD-Lite, success metrics, key tradeoffs, v2 roadmap.

---

### Consumer Growth Teardown: Instagram's Authenticity Problem — Self-Directed Feature Teardown

> **Self-directed** · Growth loop analysis + feature proposal targeting social retention at consumer scale

**Problem:** Instagram's posting rate among casual users is declining while passive consumption grows. The platform is bifurcating into creators and audience — eroding the social reciprocity that drives long-term retention. BeReal's 62.5% DAU:MAU ratio (vs. Instagram's estimated 30-35%) and 70% daily post rate demonstrate that demand for casual authentic sharing is strong. The friction isn't desire — it's Instagram's performance mechanics: algorithmic ranking, public like counts, and follower signals make posting feel high-stakes.

**Proposed feature — Real Circle:** A separate tab within Instagram — not a new app — with four structural constraints: visible only to Close Friends (max 50), chronological order only, like counts visible to poster only, one post per day. Leverages Instagram's existing Close Friends infrastructure without requiring users to rebuild a social graph elsewhere.

**Key decisions:**
- Tab, not separate app — Threads proved that splitting off a feature doesn't transfer the social graph
- One post per day is structural, not arbitrary — the daily cap removes the "which post is best?" decision; without it, performance anxiety returns
- No ads in v1 — Real Circle only works if users perceive it as architecturally distinct from the main feed

**RICE score vs. alternatives:** 121 (vs. Remove Public Like Counts at 93, Chronological Friends Feed at 74) — wins on Reach (builds on existing Close Friends behavior) and Impact (targets posting frequency among lapsed users, the metric that drives reciprocity and retention).

📁 **Full teardown:** [`consumer-growth-teardown/`](./consumer-growth-teardown/) — growth loop analysis, RICE table, PRD-Lite, competitive context (BeReal, Snapchat, Threads).

---

### GitHub Actions: Flaky Test Detection & Triage — Self-Directed Feature Teardown

> **Self-directed** · Mini-PRD for a real product gap in GitHub Actions

**Problem:** GitHub Actions has no memory across runs — a test that failed once and passed on re-run 40 times looks identical to a brand-new failure. Developers can't distinguish real regressions from flaky tests, so they re-run CI jobs reflexively before investigating. At scale this inflates DORA Lead Time, erodes CI trust, and accumulates invisible test debt tracked in wikis instead of the tool where the failures appear.

**Proposed feature:** A native "Flaky Tests" tab in GitHub Actions that parses JUnit XML artifacts (already output by Jest, pytest, JUnit, RSpec, Go test) to build per-test pass/fail history. Surfaces a ranked flaky test list, an acknowledgement mechanism, and an inline PR warning when failures match known flaky tests.

**Scoping rationale:**
- JUnit XML is the right v1 format: covers ~70% of Actions users with test steps, requires no changes to how teams write tests
- No auto-retry in v1 — automating re-runs hides test debt instead of surfacing it; visibility first
- Acknowledgement expires in 30 days to prevent tests from silently staying broken

**RICE score vs. alternatives:** 144 (vs. Workflow Cost Attribution at 59, Matrix Build Visualization at 80) — wins on Reach (JUnit XML is already common) and Impact (directly reduces Lead Time, a core DORA metric).

📁 **Full teardown:** [`github-actions-case-study/`](./github-actions-case-study/)

---

## Technical Skills

These projects demonstrate the quantitative and analytical work that underlies data-informed product decisions — scoping success metrics, evaluating user research data, and pressure-testing assumptions before writing a PRD.

---

### DORA Metrics Dashboard — DevOps Tool (Python / GitHub API)

> **Built project** · Functional CLI tool

A Python CLI that pulls all four DORA metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR) for any GitHub repo and renders them as a benchmarked, color-coded dashboard.

```bash
python main.py expressjs/express --days 90
# → prints metrics with DORA band (Elite/High/Medium/Low) + saves dashboard PNG
```

Built this to understand what DevOps teams actually measure and where the tooling gaps are. The README documents the proxy decisions (why Releases instead of workflow runs, why median instead of mean) in the same way a PM would document scope decisions in a PRD.

📁 [`dora-metrics-dashboard/`](./dora-metrics-dashboard/)

---

### Consumer Sentiment Pipeline: Beats by Dre Competitive Positioning

> **Externship** · Data analytics role — built the pipeline, synthesized findings into a positioning recommendation

Analyzed 5,127 Amazon reviews across 5 headphone brands. Sound quality scored 4.47/5 — strong. But 53% of respondents said they were unlikely to purchase. That gap between product satisfaction and purchase intent is a sociological phenomenon: Beats is winning the listening experience but losing the purchase decision.

Word frequency analysis confirmed: Beats owned "bass" and "sound quality" in positive language; JBL owned "battery" and "durability." The competitive risk wasn't a better-sounding speaker — it was JBL building a reliability positioning that targets a fundamentally different buyer motivation.

The skill that transfers to PM work: using data to reframe the question, not just answer it. Star ratings said "you're tied." Deeper analysis said "you're differentiated in ways you may not be deliberately building."

*(5,127 reviews · r = +0.83 polarity-rating correlation · 30 charts)*

📁 [`consumer-insights-nlp/`](./consumer-insights-nlp/)

---

### Statistics Coursework (R + Python)

Regression analysis, hypothesis testing, probability, and survey data analysis (General Social Survey). These are the mechanics behind interpreting A/B test results, evaluating statistical significance of product metrics, and reading a data team's analysis without getting lost.

📁 [`coursework/`](./coursework/)

---

**Contact:** coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
