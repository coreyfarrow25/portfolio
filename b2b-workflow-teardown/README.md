# B2B Workflow Teardown: Asana's Momentum Gap

> **Self-directed** · Competitive teardown + feature proposal targeting the B2B work-management category (Asana, Jira, Linear)

---

## The Problem Worth Solving

Asana is excellent at task *creation*. You open it on Monday, build out a project, assign owners, set due dates — and everything looks organized. Then Wednesday arrives, and you have no idea which of those tasks are actually moving.

The core tension: **Asana's information architecture is optimized for planning, not for detecting mid-execution stall.** The "My Tasks" view tells you what's assigned to you. The project timeline tells you what's due when. Neither tells a PM which tasks are quietly at risk before they're already late.

By the time a task shows up red in Asana, the sprint has already broken. What's missing is a signal for *when a task is about to stall* — not *that it's already overdue*.

This is a structurally different problem than "better reminders." Reminders fire at a point in time. Stall signals fire based on *behavioral patterns* — a task hasn't had a comment in 4 days, its subtasks are untouched, its status hasn't moved from "In Progress." Those are leading indicators. Asana has the data to surface them. It doesn't.

---

## Competitive Landscape

| Dimension | Asana | Jira | Linear |
|---|---|---|---|
| Task creation UX | ⭐ Best in class | Heavy, form-based | Fast, keyboard-first |
| Mid-sprint visibility | Due date only | Due date + burndown chart | Cycle progress bar |
| Stall detection | None | None | None |
| Notification model | Due-date triggered | Status-change triggered | Activity-change triggered |
| Primary user | Cross-functional teams | Engineering orgs | Engineering teams |

**Key observation:** All three tools use *deadline-reactive* notifications. None use *activity-predictive* signals. This is a category-wide gap, not an Asana-specific miss — which means the team that solves it first creates a durable retention advantage.

**Why Asana is the right v1 target:** Asana's core user is a non-technical PM coordinating cross-functional work. They're the person most harmed by late stall signals — they're managing dependencies across 4+ workstreams and don't have the tribal knowledge to know which tasks have silent owners. They also have the most to gain from visibility that doesn't require them to manually audit every ticket.

---

## Feature Proposal: Workflow Health Signals

**What it does:** A real-time stall detection layer that tracks task-level activity signals — comments posted, subtasks completed, status transitions, file attachments — and surfaces a "Health" indicator at both the task and project level. Tasks that cross a low-activity threshold relative to their time-to-due-date get a "Needs Attention" flag *before* they're overdue.

**The experience:**
- Project view gains a **"Health" column** — color-coded (on track / watch / stall risk)
- Flagged tasks surface in a weekly **"At-Risk Digest"** sent to the project owner on Monday morning
- Individual assignees get a single in-app nudge: *"You haven't updated [Task] in 4 days — anything blocking you?"*
- PMs can set the sensitivity threshold per project (aggressive / standard / minimal)

**What it doesn't do (v1 non-goals):**
- No automated status updates — the goal is visibility, not automation that hides the signal
- No ML-based predictions in v1 — the heuristic (activity gap × time remaining) is interpretable and doesn't require training data
- No cross-project roll-up — project-level health is sufficient; portfolio health is a v2 problem

---

## RICE Prioritization

Feature candidates considered against Workflow Health Signals:

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| **Workflow Health Signals** | **9** | **9** | **7** | **4** | **141** |
| Smart Status Auto-Update (PR → ticket) | 7 | 6 | 8 | 3 | 112 |
| OKR / Goal Linking | 6 | 7 | 5 | 5 | 42 |
| AI Task Summarizer | 8 | 5 | 6 | 3 | 80 |

**Scoring rationale:**

*Workflow Health Signals:* Reach 9 — affects every PM and EM using Asana, not a niche workflow. Impact 9 — stall is the root cause of missed sprint commitments, which is the #1 friction point cited in B2B project management NPS surveys. Confidence 7 — activity-based heuristics are well-validated in academic PM literature (we know what stall patterns look like); the risk is user sensitivity to "surveillance-feeling" nudges. Effort 4 — requires activity-tracking infrastructure and a new notification type, but no ML in v1.

*Smart Status Auto-Update:* Wins on Confidence and Effort — straightforward integration with GitHub/GitLab webhooks. Loses on Impact — this is a reporting convenience, not a workflow change. It tells you what already happened faster; it doesn't prevent stall.

*OKR Linking:* Strategic but hard to confidence-score. OKR adoption is inconsistent even within companies that want it. A feature that depends on consistent OKR hygiene to work has low Confidence in the enterprise mid-market.

---

## PRD-Lite: Workflow Health Signals

**Problem statement:** Asana PMs learn about task stall after it has already impacted the sprint. There is no leading indicator in the current product that a task is trending toward late without already being overdue.

**Success metric (primary):** Reduction in "overdue task rate" (tasks that hit their due date with no update in the prior 7 days) for projects where Health Signals is enabled, vs. control. Target: 20% reduction at 90 days.

**Secondary metrics:**
- Weekly At-Risk Digest open rate (target: >40% — a digest nobody reads doesn't change behavior)
- "Needs Attention" nudge response rate (user updates task within 24h — target: >55%)
- Net Promoter contribution from PM/EM segment (NPS surveys already segment by role)

**MVP scope:**
- Health score heuristic: (last comment age + last status change age + subtask completion %) weighted against days-to-due-date
- Health column in List and Board views
- Monday At-Risk Digest email (opt-in default: on)
- Single in-app nudge to assignee when task crosses "stall risk" threshold
- Sensitivity toggle at project level (3 settings)

**Key tradeoffs documented:**
- *Heuristic vs. ML:* A rules-based heuristic is explainable ("your task hasn't had activity in 4 days") where an ML score is a black box. PMs who receive a "stall risk" flag need to understand *why* to act on it. Heuristic wins in v1.
- *Push vs. pull:* Default opt-in for the digest, but individual nudges are opt-out. Forcing the digest opt-out risks the digest becoming invisible; forcing nudge opt-in risks users resenting the tool. Different defaults for different signal types is intentional.
- *Surveillance perception risk:* The nudge to the assignee must be framed as supportive ("anything blocking you?") not accusatory ("you haven't updated this"). Copy matters. Will A/B test two framings in beta.

**Open questions for v1 scoping:**
- What's the right activity gap threshold to avoid alert fatigue? (hypothesis: 4 days for tasks with <7 days remaining, 7 days for tasks with >7 days remaining — to be validated in beta)
- Should the Health column be visible to all project members or only to the project owner?

---

## Why This Matters for the Category

The B2B project management market is in a consolidation phase. Asana, Monday, Notion, and ClickUp are all converging on similar task-creation and timeline features. The next competitive moat isn't "more features" — it's making the tool feel like a PM who actually watches your work and tells you what to do next.

Workflow Health Signals is a bet that the PM-as-intel-hub is the right product metaphor for Asana's next phase. The tool shouldn't just be a database of tasks. It should make PMs smarter about where their attention needs to go before the sprint is already broken.

That's a product positioning shift, not just a feature. And it's grounded in the actual behavior pattern that causes projects to fail: not bad planning, but invisible stall.

---

**Contact:** coreyfarrow25@gmail.com · [LinkedIn](https://linkedin.com/in/coreyfarrowjr)
