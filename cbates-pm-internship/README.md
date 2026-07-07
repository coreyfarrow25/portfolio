# CBATES / DFW Metro NAACP: Stakeholder Communication System for a Youth STEAM Initiative

> **PM Internship** · Dec 2024–Feb 2025 · Outreach system design, stakeholder pipeline, AI-assisted content generation
>
> *Note: This case study covers outreach operations and communication system design, not software product management. The PM-transferable skills — audience segmentation, message architecture, pipeline design, process automation — are the point.*

---

## The Problem

The DFW Metro NAACP's annual Youth Gaming Expo and Tournament is a STEAM-focused community event designed to connect young people with technology, education, and career pathways through competitive gaming. The 2025 event (February 1, Denton Civic Center) needed to recruit across three distinct stakeholder groups simultaneously:

- **Volunteers** — event-day staff to manage check-in, floor operations, food, and shift coverage
- **Participants** — youth from DFW-area school districts (potential reach: 379,561+ students across Frisco ISD [65,000], Lewisville ISD [49,205], Plano ISD [49,000], and 30+ other districts)
- **Financial supporters** — D9 Greek organizations and community groups with chapter funding pools

Each audience required fundamentally different messaging. A single generic "help us" communication would fail all three.

The secondary problem: at a small community organization, a three-audience outreach campaign across 36 organizations would typically require 15+ hours of drafting per project phase — individually customizing emails, letters, and follow-ups for each recipient type. That wasn't sustainable for a team with limited staff bandwidth.

---

## What I Owned

### 1. Stakeholder Communication Architecture

Designed a multi-variant communication system rather than a single outreach template. The core insight was that each audience had a different "what's in it for me" — and conflating them would weaken the ask for all three.

**Volunteer recruitment:**
- Standard version: community members and general organizations → lead with mission ("celebration of innovation, diversity, and STEAM"), logistics (6AM–6PM, 2-hour shifts), and a clear call to action (SignUpGenius link)
- D9 Greek organization version: recognized that Greek chapters have chapter discretionary funds and respond to both volunteer and financial asks → added a donation request with explicit framing ("your generosity in time, money, or both ensures the success of this event")

**Participant outreach (school districts):**
- Drafted participant letters targeting school district coordinators, framing the Gaming Expo as an educational and career-pathway opportunity for students — a different value proposition than the volunteer pitch
- Coordinated contact research for 36 organizations across the DFW area, identifying the right point of contact at each (District Coordinators, C-level executives) rather than sending to generic school office emails

**Event communications:**
- Wrote social media copy (Instagram/community channels) calibrated for community shareability — concise, emoji-forward, specific date/location, hashtag strategy
- Drafted two pre-event huddle text sequences for confirmed volunteers (sent 1/25 and 1/29): short, actionable, with Zoom link and a "simple instructions" framing to reduce volunteer dropout from pre-event anxiety

### 2. AI-Assisted Content Generation Workflow

With 36 organizations across three audience types, the drafting problem was real. I designed a prompt-based workflow using AI to generate tailored stakeholder communications at scale — giving each message the specificity of a hand-drafted letter without the per-message time investment.

**What this looked like in practice:**
- Built a structured brief template: recipient type, organization name, relevant details (size, chapter, district enrollment), ask type (volunteer / financial / participant), tone calibration
- Used this brief to generate 30+ tailored stakeholder communications, each customized to the specific organization and audience segment
- Result: drafting time reduced from ~15 hours per project phase to under 2 hours — a 7x reduction in content production time while maintaining per-message specificity

**The judgment call:** The temptation in this workflow is to over-automate — generate and send without review. I kept human review as a required step before every communication went out, specifically for tone (community organizations are sensitive to impersonal outreach) and factual accuracy (wrong district name or enrollment number in a participant letter would damage the relationship). Automation handled volume; judgment handled quality.

### 3. Event Logistics Infrastructure

Volunteering at a gaming event for hundreds of youth requires operational structure that most community events underplan. I contributed to the event-day logistics design:

- Designed shift structure and coverage allocation across venue areas (check-in, floor circumference, food area, swag room, bathroom monitoring)
- Proposed the wristband system to distinguish participants who have exited and re-entered, eliminating the need to re-verify credentials at re-entry and reducing check-in bottleneck
- Coordinated with the sign-up system to ensure shift handoffs were documented (not just informally communicated)
- Pushed for pre-event huddles (short Zoom calls with volunteers, 1/25 and 1/29) rather than a long briefing document — recognizing that volunteers for community events are time-poor and will disengage from complex instructions

---

## Key Decisions & Tradeoffs

**Two volunteer letters instead of one.** The easier path was one generic letter for all organizations. The decision to split into two variants (standard + D9 with financial ask) required more upfront drafting but significantly increased conversion potential for the Greek org segment — an audience with available chapter funds that a generic volunteer letter would leave on the table.

**AI assistance with mandatory human review.** The risk in AI-generated stakeholder communications is brand/tone inconsistency — a community organization that receives something that "reads like a form letter" will disengage. The solution wasn't less automation; it was a structured review step that checked tone, specificity, and factual accuracy before send. This preserved the time savings while protecting relationship quality.

**Wristband system over re-check-in.** The default at community events is to re-verify all participants on re-entry. For a high-traffic youth event, this creates a bottleneck that both slows operations and creates friction for attendees. The wristband system moves verification to initial check-in, costs under $20 in materials, and reduces re-entry time to near zero. Simple operational decision with disproportionate impact on the attendee experience.

**Pre-event huddles over a briefing document.** Volunteer no-show rates at community events correlate with pre-event communication quality — not information volume. Two short Zoom huddles with a "simple instructions" framing gave volunteers confidence without overwhelming them. A long PDF briefing would have been read by fewer people and retained by fewer still.

---

## Outcome

- Youth Gaming Expo executed on February 1, 2025 at Denton Civic Center
- 36 organizations engaged across the DFW outreach pipeline through district-wide stakeholder coordination
- Potential participant reach: 379,561+ students across DFW-area school districts
- AI-assisted communication workflow: 30+ tailored stakeholder communications generated, drafting time reduced from ~15 hours to under 2 hours per project phase
- Multi-variant volunteer and participant communication system designed and deployed across general community, D9 Greek, and school district segments

**The PM parallel:** The core PM skill demonstrated here is stakeholder segmentation and message architecture — recognizing that different audiences have different jobs-to-be-done and designing a communication system that speaks to each without diluting the others. The AI workflow is a microcosm of a PM's relationship with automation: the judgment about when to automate, what guardrails to keep, and where human review is non-negotiable is more important than the automation itself.

---

**Contact:** coreyfarrow25@gmail.com · [LinkedIn](https://www.linkedin.com/in/coreyfarrow/)
