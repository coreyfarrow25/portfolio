# BeReal Feature Prioritization: RICE Framework Case Study

![Framework](https://img.shields.io/badge/Framework-RICE%20Scoring-6366f1)
![Deliverable](https://img.shields.io/badge/Deliverable-PRD%20%2B%20Pitch-f59e0b)
![Method](https://img.shields.io/badge/Method-User%20Research-10b981)
![Output](https://img.shields.io/badge/Output-Shipped%20Feature%20Spec-blue)

---

## Problem

BeReal's engagement loop has a structural weakness: the daily notification drives a post, but the post itself has no emotional context — you see what someone is doing, not how they feel about it. This limits the social depth of interactions compared to competitors like Snapchat, where streaks and reactions create ongoing engagement signals. The question was whether adding emotional context to posts could meaningfully improve retention without breaking BeReal's core "authentic, unfiltered" brand identity.

---

## What It Does

A full product development cycle for **Mood Prompt** — a one-tap mood selector that fires before the camera opens when the BeReal notification arrives. The mood tag appears beneath the photo in friends' feeds and aggregates into a personal mood history over time.

The work covers:

- **Competitive analysis** — Feature and sentiment comparison of BeReal's "Time to BeReal" notification vs. Snapchat's Snapstreaks, using qualitative review coding to identify where each feature drives and loses engagement
- **RICE prioritization** — Scored 8 feature candidates across Reach, Impact, Confidence, and Effort; Mood Prompt scored 192 vs. the next closest at 98
- **PRD-Lite** — Problem statement, success metrics, MVP scope, non-goals, and open questions
- **User testing** — Focus group plan, discussion guide, 12-question survey (n=47), and a test summary report with actionable findings
- **Stakeholder pitch** — 5-minute pitch script with evidence pack, competitive benchmarks, and retention modeling

```
research/               → business snapshot, user journey map
competitive-analysis/   → benchmark tables, sentiment analysis docs, PM opportunity note
feature-development/    → RICE scoring, PRD-Lite, prototype flow map
user-testing/           → focus group plan, discussion guide, survey, test summary
pitch/                  → evidence pack, pitch outline, speaker notes
```

---

## Product Decisions & Tradeoffs

**Why Mood Prompt beat every other candidate in RICE scoring.** The two highest-competing ideas were a Reaction Expansion (more emoji reactions on posts) and Location Tags. Reaction Expansion scored well on Reach but low on Confidence — adding more reactions risks the same outcome Instagram saw when they introduced reactions on top of Likes: engagement fragmentation without depth gains. Location Tags scored low on Impact because BeReal's anonymous-first ethos makes location sharing a trust risk. Mood Prompt had the clearest path from feature to behavior change: it adds expressiveness without requiring new social graph features or trust-sensitive data.

**The PRD's most important non-goal: mandatory mood selection.** Early in scoping, one version of the feature required a mood selection before the camera would open. User testing killed this immediately — 61% of survey respondents said they'd skip posting entirely if mood selection was required. The correct scope is opt-in, with the mood selector appearing as a dismissible overlay. This is a tradeoff between data completeness (mandatory gives 100% mood data) and completion rate (opt-in risks sparse data but preserves the core behavior). The decision was to optimize for completion rate first, then revisit in v2 once baseline adoption is established.

**Why a focus group over a quantitative A/B test.** The feature was pre-prototype, so there was no live build to test against. A focus group gave directional signal on the fundamental question — does emotional context add value to BeReal posts, or does it feel forced? — faster than building a prototype. The tradeoff is low n and potential social desirability bias in group settings. The test summary flags this explicitly and recommends a live A/B test as the next step before shipping.

**The competitive insight that shaped the PRD scope.** Sentiment analysis of Snapchat Streaks reviews showed that users love the habit formation but resent the anxiety it creates ("I lost my 200-day streak because my phone died"). BeReal's opportunity is to add emotional depth without adding streak-style pressure. This directly influenced the non-goals section: no "mood streaks," no mood-based notifications, no public mood history.

**Success metrics chosen and why.** Primary: 30-day retention for users who post with Mood Prompt vs. control. Secondary: daily completion rate (posts with mood tag / total notifications fired). Not tracked: mood data itself in v1 — the feature is about expression, not analytics, and tracking mood trends creates a privacy surface area that isn't justified until the feature proves retention value.

---

## Tech

No code in this project — it is a pure product artifact. Tools used:

| Tool | Purpose |
|---|---|
| Excel / Google Sheets | RICE scoring matrix, survey data analysis |
| Word / Docs | PRD-Lite, focus group materials, pitch docs |
| User journey mapping | BeReal experience map across 5 stages |

---

## How to Read This

Start with `feature-development/Project 3 _ Step 2 – RICE Scoring Table.docx` to see the full prioritization rationale, then `Project 3 _ Step 3 – PRD-Lite.docx` for the feature spec. `user-testing/Project 4 _ Step 5 – Test Summary Report (COMPLETED).docx` has the most actionable output from research.
