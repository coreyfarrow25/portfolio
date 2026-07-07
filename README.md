# Corey Farrow — Product Management Portfolio

## Start Here

Two things before you scroll:

→ **[DORA Metrics Dashboard](./dora-metrics-dashboard/)** — a working Python CLI that pulls all four DevOps performance metrics for any GitHub repo and classifies them against DORA's Elite/High/Medium/Low bands. The [README](./dora-metrics-dashboard/) documents proxy decisions the same way a PRD documents scope decisions.

→ **[GitHub Actions: Flaky Test Detection](./github-actions-case-study/)** — a full feature teardown + mini-PRD for a real gap in CI/CD tooling. RICE scoring, competitive benchmarks against BuildKite and CircleCI, and explicit tradeoff documentation.

**What I bring:** UVA Sociology (Organizations & Work) + two PM internships + a BeReal PM externship. My edge is reading the gap between how systems are designed and how people actually use them — then translating that into product decisions that can be scoped, prioritized, and shipped.

---

## Why Product Management

Sociology is the study of how systems shape human behavior — and how humans, in turn, reshape systems. My concentration at UVA is Global Economy, Organizations, and Work: how institutions are designed, how people move through them, and where the design breaks down.

Most technology is built by people who think about systems first and humans second. That produces tools that work technically but fail socially — enterprise software that nobody uses because it was designed around a process diagram instead of the actual way people work, consumer apps that grow fast and retain poorly because they optimized for engagement metrics instead of genuine value. The technical problem gets solved. The human problem doesn't.

I came to product management because it's the role where that gap is supposed to close. A PM is accountable for both: the system has to work, *and* it has to be something people actually want to use. Sociology trained me to look for the gap between what a system is designed to do and what people actually do inside it. That gap is usually where the real product problem lives.

My background in stakeholder management — coordinating state agencies, university partners, and long-term care administrators at Tellegacy; building district-wide engagement pipelines across 36 organizations at CBATES; restructuring operations at Panera — is the operational side of that same skill: understanding what different people need from a system, and building something that works for all of them simultaneously. Not compromise. Synthesis.

The emotional intelligence piece isn't soft. At Panera, diagnosing *why* the waste reduction initiative would or wouldn't stick required understanding the team's relationship to the process — not just redesigning the process. At BeReal, the most important product decision wasn't which feature to build; it was understanding what emotional state users are in when the notification fires, and designing for that state. The same data that tells you 40% of users post in the 2-minute window tells you something about trust and habit. You have to read both signals.

I want to build products that work for people — not just products that work. I'm drawn to tools that engineers and operators use every day, where the quality of the experience directly affects whether someone can do their job well. I'm also drawn to consumer products where emotional design isn't a veneer on top of the product but a structural feature of how it works. Both require the same underlying skill: understanding what people actually need, not just what they ask for.

---

## Internship Work

These two case studies cover real internship work — verified deliverables, real stakeholders, real outcomes. Neither is software product management, but both demonstrate the underlying PM skills (business case writing, stakeholder segmentation, system design, launch planning) in contexts where the decisions actually mattered.

---

### Tellegacy: Launching a Loneliness-Reduction Program at 25 Nursing Homes

> **PM Internship** · Jan 2026–Present · Program launch, grant strategy, operational infrastructure

**Problem:** Tellegacy had a proven intergenerational program model — trained student "Legacy Builders" conducting 10 structured sessions with nursing home residents, culminating in a bound Legacy Book. Scaling it to 25 North Dakota facilities required a funded business case, a facility recruitment pipeline, and a program infrastructure facilities could sustain independently after funding ended. None of those existed.

**What I owned:**
- Co-wrote the $187,500 CMP federal grant application: problem narrative, 12-month implementation plan, budget justification (audited the spreadsheet, benchmarked comparable approved budgets, documented every cost line with explicit calculation rather than round numbers), and sustainability appendix
- Built the grant intelligence database: 40+ federal and foundation programs tracked with focus tags, nursing home fit rating, award size benchmarks, deadline status, and strategy notes — designed as a filterable decision tool, not a list of links
- Built the stakeholder outreach database: 15+ ND healthcare associations and GWEP university partners researched, individual point-of-contact identified at each
- Flagged letters of participation as the critical dependency before the budget was finalized — facility commitments, not narrative quality, were the gate on grant approval

**Key decision:** Designed the program for train-the-trainer delivery from the start — so facilities could run Tellegacy after CMP funding ended at near-zero marginal cost (staff time + printing). The alternative, Tellegacy-staffed delivery at all 25 sites, would have collapsed when the grant period closed.

**Outcome:** $187,500 grant application submitted. Program scoped for up to 200 residents served (3–8 per facility × 25 facilities). Grant inventory tracking 40+ opportunities with deadlines and fit scores. Standardized toolkit designed to reduce administrative lead time for future site launches by ~20%.

📁 [`tellegacy-pm-internship/`](./tellegacy-pm-internship/)

---

### CBATES / DFW Metro NAACP: Outreach System for a Youth STEAM Initiative

> **PM Internship** · Dec 2024–Feb 2025 · Stakeholder pipeline, communication system design, AI-assisted content generation

**Problem:** The annual DFW Metro NAACP Youth Gaming Expo needed to recruit volunteers, youth participants, and financial supporters across 36 organizations simultaneously — each requiring different messaging. One generic communication would fail all three audiences. And at a small org, writing 30+ tailored stakeholder messages by hand would take 15+ hours per project phase.

**What I owned:**
- Designed a three-variant stakeholder communication system: standard volunteer recruitment, D9 Greek org version with financial contribution ask (recognizing chapter funding pools as an available resource a generic letter leaves untapped), and school district participant outreach with a STEAM education framing
- Built a prompt-based AI workflow to generate 30+ tailored communications at scale: structured a brief template (recipient type, org name, relevant details, ask type) → used it to generate per-org messages → human review before send for tone and factual accuracy. Drafting time: 15 hours → under 2 hours per project phase
- Contributed to event-day logistics design: proposed wristband system (vs. re-verification at re-entry) to eliminate check-in bottleneck, designed shift structure across venue areas, pushed for two short pre-event Zoom huddles over a long briefing document to reduce volunteer no-show friction

**Outcome:** Gaming Expo executed February 1, 2025. 36 organizations engaged. Potential reach: 379,561+ students across Frisco ISD (65K), Lewisville ISD (49K), Plano ISD (49K), and 30+ other DFW-area school districts.

📁 [`cbates-pm-internship/`](./cbates-pm-internship/)

---

## Case Studies

### — Externship —

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

**So what:** A 3–5% lift in 30-day retention at BeReal's 25M DAU scale represents 750K–1.25M more retained users — a material metric for a product that was acquired for $537M and needed to demonstrate engagement depth, not just breadth.

📁 **Artifacts:** [`bereal-feature-prioritization/`](./bereal-feature-prioritization/)

---

### — Self-Directed Teardowns —

---

### GitHub Actions: Flaky Test Detection & Triage

> **Self-directed** · Mini-PRD for a real product gap in GitHub Actions

**Problem:** GitHub Actions has no memory across runs — a test that failed once and passed on re-run 40 times looks identical to a brand-new failure. Developers can't distinguish real regressions from flaky tests, so they re-run CI jobs reflexively before investigating. At scale this inflates DORA Lead Time, erodes CI trust, and accumulates invisible test debt tracked in wikis instead of the tool where the failures appear.

**Proposed feature:** A native "Flaky Tests" tab in GitHub Actions that parses JUnit XML artifacts (already output by Jest, pytest, JUnit, RSpec, Go test) to build per-test pass/fail history. Surfaces a ranked flaky test list, an acknowledgement mechanism, and an inline PR warning when failures match known flaky tests.

**Scoping rationale:**
- JUnit XML is the right v1 format: covers ~70% of Actions users with test steps, requires no changes to how teams write tests
- No auto-retry in v1 — automating re-runs hides test debt instead of surfacing it; visibility first
- Acknowledgement expires in 30 days to prevent tests from silently staying broken

**RICE score vs. alternatives:** 144 (vs. Workflow Cost Attribution at 59, Matrix Build Visualization at 80, Required Workflow Approvals at 90) — wins on Reach (JUnit XML is already common) and Impact (directly reduces Lead Time, a core DORA metric).

**So what:** A 20% reduction in re-run rate across repos that adopt JUnit XML upload would reclaim millions of CI compute minutes per week at GitHub's scale — a direct input into the developer productivity metrics GitHub surfaces to enterprise customers.

📁 **Full teardown:** [`github-actions-case-study/`](./github-actions-case-study/)

---

### B2B Workflow Teardown: Asana's Momentum Gap

> **Self-directed** · Competitive teardown of Jira / Linear / Asana + feature proposal

**Problem:** Asana, Jira, and Linear are all built around task creation and deadlines. None have a mechanism for detecting mid-execution stall before a task is already overdue. The notification model across all three is deadline-reactive: you learn something is late after it's late. By the time the alert fires, the sprint is already broken.

**Proposed feature — Workflow Health Signals:** A real-time stall detection layer that tracks activity signals at the task level (comments, subtask completion, status transitions) and surfaces a "Health" indicator before a task crosses its deadline. Flags at-risk tasks in a weekly digest for project owners; sends a lightweight in-app nudge to assignees.

**Scoping rationale:**
- Rules-based heuristic in v1, not ML — "your task hasn't had activity in 4 days" is interpretable; a confidence score isn't
- No automated status updates — automation hides the signal instead of surfacing it
- Nudge copy framed as "anything blocking you?" not "you haven't updated this" — will A/B test in beta

**RICE score vs. alternatives:** 141 (vs. Smart Status Auto-Update at 112, OKR Linking at 42, AI Task Summarizer at 80) — wins on Impact (stall is the root cause of missed sprint commitments) and Reach (affects every PM and EM, not a niche workflow).

**So what:** A 20% reduction in overdue task rate would shift Asana's enterprise renewal conversation from "seat stickiness" to "sprint outcome improvement" — a stronger ROI argument against Notion and Linear in competitive deals.

📁 **Full teardown:** [`b2b-workflow-teardown/`](./b2b-workflow-teardown/)

---

### Consumer Growth Teardown: Instagram's Authenticity Problem

> **Self-directed** · Growth loop analysis + feature proposal targeting social retention at consumer scale

**Problem:** Instagram's posting rate among casual users is declining while passive consumption grows. The platform is bifurcating into creators and audience — eroding the social reciprocity that drives long-term retention. BeReal's 62.5% DAU:MAU ratio (vs. Instagram's estimated 30-35%) and 70% daily post rate demonstrate that demand for casual authentic sharing is strong. The friction is Instagram's performance mechanics: algorithmic ranking, public like counts, and follower signals make posting feel high-stakes.

**Proposed feature — Real Circle:** A separate tab within Instagram with four structural constraints: visible only to Close Friends (max 50), chronological order only, like counts visible to poster only, one post per day. Leverages Instagram's existing Close Friends infrastructure without requiring users to rebuild a social graph elsewhere.

**Key decisions:**
- Tab, not separate app — Threads proved that splitting off a feature doesn't transfer the social graph
- One post per day is structural, not arbitrary — the daily cap removes the "which post is best?" decision; without it, performance anxiety returns
- No ads in v1 — Real Circle only works if users perceive it as architecturally distinct from the main feed

**RICE score vs. alternatives:** 121 (vs. Remove Public Like Counts at 93, Chronological Friends Feed at 74).

**So what:** Reactivating even 10% of Instagram's lapsed casual posters would add hundreds of millions of additional posts per week, directly addressing the DAU/MAU compression Meta reports quarterly and restoring the reciprocal social graph activity that drives long-term retention over passive consumption.

📁 **Full teardown:** [`consumer-growth-teardown/`](./consumer-growth-teardown/)

---

## Built Tools

---

### DORA Metrics Dashboard — Python / GitHub API

> **Built project** · Functional CLI tool

A Python CLI that pulls all four DORA metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR) for any GitHub repo and renders them as a benchmarked, color-coded dashboard.

```bash
python main.py expressjs/express --days 90
# → prints metrics with DORA band (Elite/High/Medium/Low) + saves dashboard PNG
```

Built this to understand what DevOps teams actually measure and where the tooling gaps are. The README documents the proxy decisions (why Releases instead of workflow runs, why median instead of mean) in the same way a PM would document scope decisions in a PRD.

**So what:** Running this against any public repo surfaces DORA band classification in under 30 seconds — useful for benchmarking a team's pipeline health before a product review or scoping a DevOps tooling conversation.

📁 [`dora-metrics-dashboard/`](./dora-metrics-dashboard/)

---

## Technical Skills

---

### Consumer Sentiment Pipeline: Beats by Dre Competitive Positioning

> **Externship** · Data analytics role — built the pipeline, synthesized findings into a positioning recommendation

Analyzed 5,127 Amazon reviews across 5 headphone brands. Sound quality averaged 4.47★ for Beats Pill — essentially tied with JBL Charge 5 at 4.46★. But sentiment and word frequency analysis told a different story: Beats owned "bass" and "sound quality" in positive review language; JBL owned "battery" and "durability." The competitive risk wasn't a better-sounding speaker — it was JBL building a reliability positioning that targets a different buyer motivation entirely.

A separate survey (n=4,979) found that 53% of respondents were unlikely to purchase despite the strong satisfaction scores — a gap between product quality and purchase intent that the review analysis helped explain: Beats wins the listening experience but hasn't closed the "will it last?" objection that drives the final purchase decision.

The skill that transfers to PM work: using data to reframe the question, not just answer it. Star ratings said "you're tied." Deeper analysis said "you're differentiated in ways you may not be deliberately building."

*(5,127 Amazon reviews · r = +0.83 polarity-to-rating correlation · 30 charts)*

📁 [`consumer-insights-nlp/`](./consumer-insights-nlp/)

---

### Statistics Coursework (R + Python)

Regression analysis, hypothesis testing, probability, and survey data analysis (General Social Survey). These are the mechanics behind interpreting A/B test results, evaluating statistical significance of product metrics, and reading a data team's analysis without getting lost.

📁 [`coursework/`](./coursework/)

---

**Contact:** coreyfarrow25@gmail.com · [LinkedIn](https://www.linkedin.com/in/coreyfarrow/)
