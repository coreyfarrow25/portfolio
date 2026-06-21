# BeReal Feature Prioritization: RICE Framework Case Study

![Framework](https://img.shields.io/badge/Framework-RICE%20Scoring-6366f1)
![Deliverable](https://img.shields.io/badge/Deliverable-PRD%20%2B%20Pitch-f59e0b)
![Method](https://img.shields.io/badge/Method-User%20Research-10b981)
![Output](https://img.shields.io/badge/Output-Shipped%20Feature%20Spec-blue)

---

## Problem

BeReal had a strong engagement foundation: 40M MAUs, 25M DAUs, a 62.5% DAU:MAU ratio, and 70% of users posting daily — metrics most social apps can't approach. But its engagement loop had a structural ceiling: the daily notification drives a post, and that post is purely visual. You see what someone is doing. You don't know how they feel about it.

Compared to Snapchat, where streaks and reaction systems create ongoing social signals, BeReal posts generate a single burst of interaction and then go quiet. The question: could adding emotional context to posts deepen the social layer and improve retention — without breaking the "authentic, unfiltered" brand that drove 40% of users to post within the 2-minute window?

---

## What It Does

A full product development cycle for **Mood Prompt** — a one-tap mood selector that fires before the camera opens when the BeReal notification arrives. The mood tag appears beneath the photo in friends' feeds.

The work covers:

- **Competitive analysis** — Feature and sentiment comparison of BeReal's "Time to BeReal" notification vs. Snapchat's Snapstreaks, with qualitative review coding across 10 themes (~100 quotes per theme) to identify where each feature drives and loses engagement
- **RICE prioritization** — Scored 8 feature candidates across Reach, Impact, Confidence, and Effort; Mood Prompt scored 192 vs. the next closest at 98
- **PRD-Lite** — Problem statement, success metrics, MVP scope, non-goals, and open questions
- **User testing plan** — Designed a focus group guide (5-10 participant target), 12-question survey instrument (50-500+ participant target), and a test summary framework with pre-specified analysis criteria
- **Stakeholder pitch** — 5-minute pitch script with evidence pack, competitive benchmarks, and retention modeling

```
research/               → business snapshot, user journey map (5 stages)
competitive-analysis/   → benchmark tables, sentiment analysis docs, PM opportunity note
feature-development/    → RICE scoring, PRD-Lite, prototype flow map
user-testing/           → focus group plan, discussion guide, survey instrument, test summary
pitch/                  → evidence pack, pitch outline, speaker notes
```

---

## Product Decisions & Tradeoffs

**Why Mood Prompt scored highest across all 8 candidates.** The two strongest alternatives were Reaction Expansion (more emoji reactions on posts) and Location Tags. I eliminated Reaction Expansion on Confidence — Instagram's experience introducing reactions on top of Likes showed engagement fragmentation without depth gains; adding more reaction types risks the same outcome for BeReal. I eliminated Location Tags on Impact — BeReal's appeal is rooted in authenticity and implicit privacy; a location-sharing feature introduces a trust surface area that conflicts with the brand's core positioning. Mood Prompt had the cleanest path: it adds expressiveness without requiring new social graph features or trust-sensitive data.

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| **Mood Prompt** | **9** | **8** | **8** | **3** | **192** |
| Reaction Expansion | 8 | 7 | 7 | 4 | 98 |
| Location Tags | 7 | 6 | 6 | 5 | 50 |

**The PRD's most important non-goal: mandatory mood selection.** An early version of the feature required a mood selection before the camera would open. I cut this from scope because it inverts the psychology of BeReal's value proposition — BeReal works because the friction is removed once the notification fires. Adding a required gate before the camera opens adds a decision point that risks post abandonment. The correct scope is opt-in, with the mood selector appearing as a dismissible overlay. This trades data completeness (mandatory gives 100% mood data across all posts) for completion rate (opt-in risks sparse data but preserves the core post behavior). The decision: optimize for completion rate in v1, revisit in v2 once baseline adoption is established.

**Why a focus group over a quantitative A/B test.** The feature was pre-prototype, so there was no live build to test against. A focus group gives directional signal on the fundamental question — does emotional context add value to BeReal posts, or does it feel performative and off-brand? — faster than building a prototype. The tradeoff is low n and potential social desirability bias in group settings. The test plan documents this limitation explicitly and specifies a live A/B test as the required next step before any shipping decision.

**The competitive insight that shaped scope.** Sentiment coding of Snapchat Streaks reviews revealed a consistent pattern: users value the habit formation but resent the anxiety it creates ("I lost my 200-day streak because my phone died"). BeReal's product opportunity is emotional depth without streak-style pressure. This directly shaped the non-goals section of the PRD: no mood streaks, no mood-based notifications, no public mood history. The feature should add meaning to the daily post — not add another thing to maintain.

**Why BeReal's engagement baseline matters for the RICE inputs.** BeReal reached 5x the engagement rate of Instagram at its launch peak, and 40% of its users post within the 2-minute notification window. These aren't incidental metrics — they validate that users are willing to comply with the core behavior if the friction is structured correctly. Mood Prompt's Reach score (9) is grounded in this: a feature that fires at the moment of the notification has access to the behavior that's already working, not a new funnel to build.

**Success metrics chosen and why.** Primary: 30-day retention for users who post with Mood Prompt enabled vs. control. Secondary: daily completion rate (posts with mood tag / total notifications fired). Not tracked in v1: mood data trends — the feature is about giving users a way to express themselves, not about building a mood analytics product. Tracking mood trends creates a privacy surface area that isn't justified until the feature proves retention value.

---

## Tech

No code in this project — it is a pure product artifact. Tools used:

| Tool | Purpose |
|---|---|
| Excel / Google Sheets | RICE scoring matrix, feature candidate comparison |
| Word / Docs | PRD-Lite, focus group materials, survey instrument, pitch docs |
| User journey mapping | BeReal experience map across 5 stages |

---

## How to Read This

Start with `feature-development/RICE Scoring Table` to see the full prioritization rationale, then `PRD-Lite` for the feature spec. `user-testing/Test Summary` has the testing framework and pre-specified analysis criteria. The pitch materials synthesize all of the above into a 5-minute stakeholder-facing format.

---

**Data sources:** BeReal engagement metrics (40M MAU, 25M DAU, 62.5% DAU:MAU, 70% daily post rate, 40% 2-min post rate, 5x engagement benchmark) from *BeReal By The Numbers* project brief. Competitive sentiment data from qualitative coding of Snapchat Streaks user reviews across 10 engagement themes.
