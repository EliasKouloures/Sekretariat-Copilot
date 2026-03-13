# Pilot Checklist

Use this checklist to run a first pilot without confusion.

The goal is not to prove that AI can do everything.
The goal is to prove one useful, governable workflow.

---

## Before the Pilot

Confirm:

1. A named pilot owner exists.
2. One school office workflow is in scope.
3. One local machine is assigned.
4. IT knows where the app, model, and local database will live.
5. Staff understand that all outputs must be reviewed by a human.
6. Real sensitive material stays out until the fixture path is accepted.

---

## Good First Workflow Choices

Choose one:

- absence handling
- parent communication drafting
- typed phone-note handling
- digital PDF triage

Avoid doing all of them at once.

---

## Good First Technical Scope

Start with:

- local-only deployment
- `127.0.0.1` bind host
- one local text model
- text and digital PDF workflows first

Add image OCR later if needed.

---

## Questions the Pilot Should Answer

1. Does it save office time?
2. Do staff trust the outputs enough to use them as drafts?
3. Are the warnings and placeholders clear?
4. Does the local-first posture reduce governance friction?
5. Can IT support it without a major new stack?

---

## Success Signals

Look for:

- faster handling of routine admin messages
- fewer copy-paste mistakes
- more consistent tone in replies
- faster internal case summaries
- a clear path from demo to governed use

---

## Failure Signals

Stop and reassess if:

- staff expect auto-send
- the workflow expands too quickly
- OCR quality is too weak for the chosen documents
- the school tries to use it for grading or admissions
- governance questions are being deferred instead of answered

---

## Minimum Pilot Review Set

Use at least:

- one complete absence message
- one missing-information note
- one digital PDF
- one contradictory example
- one unsupported case

The fixture set in this repo already covers these patterns.

---

## Decision After the Pilot

At the end of the pilot, decide one of three paths:

1. Stop
   The workflow or trust model was not strong enough.
2. Continue locally
   The school wants a slightly wider pilot on the same local-first model.
3. Extend with support
   The school wants workflow adaptation, rollout design, staff training, or deeper implementation work.

---

## Next Docs

- [School Leader Brief](SCHOOL_LEADER_BRIEF.md)
- [IT Deployment Guide](IT_DEPLOYMENT.md)
- [Privacy Note](PRIVACY.md)
- [FAQ](FAQ.md)
