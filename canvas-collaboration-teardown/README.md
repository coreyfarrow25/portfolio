# Canvas Collaboration Teardown: Presenter Awareness in Figma Spotlight and Miro Follow Mode

> **Self-directed** · Teardown of "follow the presenter" mechanics in two multiplayer canvas tools + mini-PRD + clickable concept prototype

📁 **Prototype:** [`prototype.html`](./prototype.html) — open it in a browser. It is a generic concept mockup, not Figma's or Miro's interface, and is not affiliated with either company.

---

## The Problem Worth Solving

Multiplayer canvas tools sell a social promise: a team can look at the same thing at the same time. The mechanism that delivers it in a walkthrough or workshop is *following*: one person drives, everyone else's view tracks theirs. Following is a small social contract between a presenter and a room, and both tools I looked at get one side of it wrong.

**Figma (Spotlight).** According to Figma's help center, a presenter starts a spotlight and viewers get a prompt and a few seconds to decline before their view switches. Only canvas actions are shared (not toolbar or sidebar actions), and the person being followed is **not notified** that someone is following. The presenter's only awareness signal is a cursor, and only if multiplayer cursors are on.

*The gap:* a presenter in a remote design review cannot tell how many people are actually following them. Someone who declined the prompt, someone who dropped out, and someone who never saw it all look the same. The presenter has to break the flow to ask "are you with me?"

**Miro (Bring everyone to me).** Per a Miro community feature thread (2020–2022), the feature pulls all participants to the facilitator's view, but facilitators say there is no one-click way to release everyone. Participants have to leave follow mode individually, and newcomers don't know what "following" means. The thread shows strong support and I found no official response on it.

*The gap:* the facilitator has the opposite problem. They have control but little release. The tool drags the whole group along when they want to split people into pairs or help one person in another frame.

**The shared root cause:** both tools treat following as a *view-sync feature*, not as a *social interaction with two parties who each need to know the state of it*. The presenter needs awareness; the follower needs clarity and an easy exit.

This is the same pattern as my other teardowns: the system works technically, and the human layer is where it breaks.

---

## What I Verified vs. What I Am Inferring

| Claim | Status | Source |
|---|---|---|
| Figma Spotlight: viewers get a prompt and a few seconds to decline | Verified | Figma Help Center, "Present to collaborators using spotlight" |
| Figma Spotlight: only canvas actions are shared, and the followed person isn't notified | Verified | Same page |
| Figma Spotlight: the presenter sees the follower's cursor only if multiplayer cursors are on | Verified | Same page |
| Miro: "Bring everyone to me" has no release-all, and followers can get stuck | Reported by users in a community thread dated 2020–2022. Miro may have changed this since. | Miro Community, "Toggle on/off the Bring all to me" |
| Presenters lose track of who is following | Hypothesis, inferred from the verified "not notified" behavior. I have no usage data. | — |
| Size of impact, adoption, session frequency | Unknown. I have no access to either company's data. | — |

Every RICE input below is my estimate, not a measured figure.

---

## Feature Proposal: Presenter Pulse (Figma Spotlight)

**What it is:** While a spotlight is active, the presenter sees a compact roster, "Following 4 of 7", with avatars split into *following* and *not following*. When someone leaves the spotlight, their avatar moves to the not-following group quietly. No pop-ups and no push notifications.

**What it changes for followers:** a small label in their view, "Visible to presenter", so the awareness is mutual and never covert.

**Why this and not more notifications:** a presenter mid-walkthrough is already managing audio, the canvas, and the room. Another toast competes for attention. A persistent, glanceable count gives the awareness without interrupting.

---

## RICE Prioritization

Formula: Reach × Impact × Confidence ÷ Effort, each scored 1–10. All inputs are estimates.

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| **Presenter Pulse (follower roster)** | **7** | **6** | **7** | **3** | **98** |
| "Ask everyone to follow" in one click | 6 | 4 | 6 | 2 | 72 |
| Async canvas walkthrough (record a spotlight path with voice) | 7 | 7 | 5 | 6 | 41 |
| Presenter pointer trails | 6 | 4 | 5 | 3 | 40 |

**Scoring rationale:**

*Presenter Pulse:* Reach 7 because anyone running a live review or workshop hits this; it is not relevant to solo work. Impact 6 because it removes a recurring interruption but doesn't unlock a new capability. Confidence 7 because the "not notified" behavior is documented and the Miro thread shows the same family of problem from the facilitator's side, but I have no data on how often it actually derails sessions. Effort 3 because the presence data already exists (Spotlight must know who is following to sync views); the work is UI and a privacy setting.

*One-click ask everyone:* cheap, but it solves how people get *into* a spotlight, not whether the presenter knows the state afterward.

*Async walkthrough:* the biggest potential impact, because it changes how teams review. It also has the lowest confidence and highest effort: it is a new content type with storage, playback, and permissions.

*Pointer trails:* helps followers track the presenter's attention, but doesn't address presenter awareness.

---

## PRD-Lite: Presenter Pulse

**Problem statement:** In a live Spotlight session, the presenter cannot see who is following. Presenters either interrupt the flow to check, or present without knowing whether the room is with them.

**Success metrics (no baseline exists, so step one is instrumenting one):**
- *Primary:* repeat Spotlight use per presenter within 30 days. If presenters trust the mode more, they should use it again.
- *Secondary:* stop-and-restart rate inside a session, as a proxy for "I lost the room"; share of presenters who open the roster at least once per session.
- *Guardrails:* admin opt-out rate; support tickets or feedback about feeling monitored. If these rise, the privacy tradeoff below is not working.

**MVP scope:**
- Persistent "Following N of M" indicator for the presenter during an active spotlight
- Hover/click opens the roster: following vs. not following
- Followers see a "Visible to presenter" label
- Org-level setting to turn the roster off (default on)

**Non-goals (explicitly out of v1):**
- No attention tracking, gaze, or "where did people look" analytics
- No history or logging of who followed and for how long
- No notifications or toasts when someone leaves
- No changes to the existing consent model: viewers can still decline or leave at any time

**Key tradeoffs documented:**
- *Awareness vs. surveillance.* Figma's current design makes following feel private: the followed person isn't notified. Changing that is a real product decision, not a free upgrade. A crit with students or a review with senior stakeholders can feel monitored. Mitigations: ephemeral roster (no history), mutual visibility label, and an admin switch. If guardrail metrics move the wrong way, the fallback is an aggregate count only, with no names.
- *Persistent indicator vs. notifications.* A glanceable count respects the presenter's attention. Toasts do not.
- *Opt-out vs. opt-in at the org level.* Default on gives the feature a chance to prove itself; I would test both in a staged rollout.

**Open questions:**
- How many followers can the roster show before it needs to collapse? Large all-hands style sessions may need only the count.
- Should followers be able to hide their presence from the presenter while still following? Probably not in v1, since it undermines the point, but it is the first thing a privacy review would raise.
- Does the Miro facilitator problem (release everyone, split into groups) belong in the same feature, or is it a separate workshop-mode proposal?

---

## What a Prototype Should Test

The clickable prototype ([`prototype.html`](./prototype.html)) lets you toggle between current behavior (presenter sees nothing) and the proposal (presenter sees the roster), and simulate people declining or leaving. The research questions it is designed for:

1. Does a persistent count read as helpful, or as surveillance? (Show to 5–8 people who run design reviews and 5–8 who attend them.)
2. Does the "Visible to presenter" label change whether followers choose to stay in?
3. At what room size does the roster become noise?

I have not run this research. The prototype is the stimulus for it, not evidence for the proposal.

---

## Why This Matters Beyond Canvas Tools

Any collaborative product that offers "come look at this with me" has the same two-party problem: the person guiding needs awareness, the person following needs agency and a clear exit. Screen-share, live co-editing, and shared whiteboards all trade on it. The tools that get the social contract right will make synchronous collaboration feel less like a performance and more like a conversation.

---

**Sources:**
- Figma Help Center, "Present to collaborators using spotlight": https://help.figma.com/hc/en-us/articles/360040322673-Present-to-collaborators-using-spotlight
- Miro Community, "Toggle on/off the Bring all to me": https://community.miro.com/ideas/toggle-onoff-the-bring-all-to-me-2055

**Contact:** coreyfarrow25@gmail.com
