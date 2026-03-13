# Sekretariat-Copilot

Free, local-first AI for school offices.

Turn messy parent emails, typed phone notes, screenshots, and PDFs into clean, review-ready admin outputs on a school-controlled machine.

This repo is public on purpose. It is both:

1. a free working tool for school administration workflows
2. a live proof-of-work for privacy-first AI product and deployment services

It is built for schools that want useful AI without defaulting to US cloud dependency, recurring token bills, or vague pilot theatre.

---

## What This Means for a School Office

School administration is full of repetitive work that still needs care:

- absence messages
- parent replies
- phone notes
- meeting summaries
- document triage
- copy-paste into legacy systems

Most of this work is not hard. It is just constant.

Sekretariat-Copilot helps staff turn messy inputs into a clean case pack:

- structured facts
- a short internal brief
- three subject line options
- three draft reply styles
- warnings where information is missing
- clarifying questions when the source is unclear

The point is simple:

**staff stay in control, the tool does the repetitive drafting work, and nothing is sent automatically.**

---

## Why Schools Care

Schools do not need another abstract AI promise.

They need a tool that:

- saves time in the office
- looks serious in front of leaders and governors
- is easy to explain to staff
- is easier to defend in privacy review
- does not create a new monthly inference bill

This project is designed around that reality.

It is narrow on purpose. That is a strength.

---

## Why This Is Different From a Generic AI Pilot

Many AI pilots fail because they start too wide.

They promise transformation. They deliver confusion.

Schools get:

- unclear use cases
- unclear ownership
- unclear privacy answers
- unclear costs
- unclear next steps

Sekretariat-Copilot avoids that trap.

It focuses on one practical category of work: school administration support.

That makes it easier to:

- trial safely
- show value quickly
- train staff simply
- review governance early
- decide what to scale later

---

## Why Local-First Matters in Europe

Many European schools are not comfortable sending routine school communications through external AI clouds by default.

That concern is reasonable.

If personal data is processed by a US-controlled cloud provider, schools may need to think carefully about:

- third-country transfer exposure
- vendor and sub-processor risk
- contractual safeguards
- supervisory guidance
- access by foreign authorities
- the practical meaning of the US CLOUD Act

This repo does not claim that every US vendor is automatically unlawful in every case.

It makes a narrower and more useful point:

**if you can keep routine drafting and extraction work on a school-controlled machine, you remove a large amount of avoidable cloud complexity from the start.**

That matters for trust.
That matters for procurement.
That matters for governance.

---

## Why the Cost Model Is Attractive

If you run this with local models:

- there are no per-token API fees
- there is no mandatory AI SaaS subscription
- there is no cost spike when staff use it more

There are still real costs:

- hardware
- setup
- maintenance
- support

But there is no default meter running every time someone drafts a reply.

---

## GDPR and EU AI Act Positioning

This repo is designed to be more governance-friendly.
It is not a magic compliance certificate.

The design supports sensible choices such as:

- local processing by default
- limited logging
- human review before use
- no auto-send
- clear warnings on low-confidence cases
- clear blocking of unsupported cases

This MVP is meant for:

- drafting
- summarising
- extracting facts
- generating clarifying questions

It is not meant for:

- grading
- admissions decisions
- behavioural monitoring
- automated disciplinary decisions

Schools still need their own review of:

- lawful basis
- retention
- access control
- staff guidance
- DPIA needs
- local and national education rules

In short:

**this tool is built to support a safer local-first posture, not to replace legal or policy review.**

---

## Who This Repo Is For

### School administrators

Use it to reduce repetitive writing and handling work without changing your whole system.

### Principals and school leaders

Use it to show a calm, credible AI direction that feels governable and useful.

### Teachers and pastoral staff

Use it where school policy allows support with parent communication drafts, meeting notes, or routine summaries.

### IT teams and data protection reviewers

Use it as an inspectable local-first starting point instead of a black-box SaaS claim.

### Organisations evaluating my services

Use it as proof that I can combine:

- AI workflow design
- product and UX thinking
- privacy-first architecture
- local deployment strategy
- technical implementation
- governance-aware documentation

---

## What School Staff Actually Get

For a typical case, the app returns:

- structured admin facts
- a concise internal case brief
- exactly three subject lines
- exactly three draft variants
- visible warnings
- clarifying questions when needed

The three reply styles always follow the same order:

1. Hemingway-style
2. Corporate
3. Educator-first

That consistency matters in office work.

---

## What It Does

- accepts pasted text, typed notes, images, and PDFs
- detects the likely workflow and lets staff override it
- extracts facts locally
- drafts clean copy-ready outputs
- flags missing or contradictory information
- exports text, JSON, and CSV
- stores only minimal local audit metadata by default

---

## What It Refuses to Do

- auto-send emails
- guess mandatory missing facts
- process multi-child cases in MVP
- pretend low-quality OCR is reliable
- support handwritten cursive
- behave like an autonomous decision-maker

That restraint is deliberate.

---

## How a School Administrator Uses It

No prompt engineering is needed.

1. Open the app in a browser on the local machine.
2. Paste a message, type a note, or upload a file.
3. Leave workflow detection on auto, or choose a workflow.
4. Click `Process locally`.
5. Review the facts, brief, subjects, and drafts.
6. Edit if needed.
7. Copy the final text into email or the school system.
8. Click `Reset case`.

That is the whole loop.

---

## What a Good First Pilot Looks Like

Start small.

Use the repo to test one narrow promise:

**Can this save the school office time on repetitive drafting without creating new trust problems?**

Recommended first checks:

1. Test the synthetic absence fixture.
2. Test a typed note with missing dates.
3. Test a digital PDF.
4. Keep image OCR as a second step.
5. Keep real school data out until the fixture path feels solid.

This is how you avoid pilot purgatory.

---

## Why This Repo Is Free

I am giving this away for free because the repo itself is useful.

It helps schools and organisations:

- evaluate a real local-first AI workflow
- understand what a calm, governable AI product can look like
- test a narrow use case before buying something large

It also shows how I work:

- from idea to product
- from policy concern to system design
- from UX to implementation
- from GitHub proof to deployable demo

The software is free.
The deeper value is in adaptation, rollout, training, and institution-ready implementation.

---

## For IT Departments

If you are technical, start here:

- [IT deployment guide](docs/IT_DEPLOYMENT.md)
- [Windows setup guide](docs/WINDOWS_SETUP.md)
- [Privacy note](docs/PRIVACY.md)
- [Troubleshooting guide](docs/TROUBLESHOOTING.md)
- [Demo runbook](docs/DEMO_RUNBOOK.md)

Short version:

- the app is a local Streamlit web app
- the backend is LM Studio by default
- the model runs locally
- the app binds to `127.0.0.1` by default
- local SQLite stores derived outputs and minimal audit metadata

If you are not the IT lead, you can stop here and hand the repo to your technical team.

---

## LM Studio in Plain Terms

LM Studio is the recommended local model host for this repo.

Why:

- it gives schools a visible desktop app
- it runs well on Apple Silicon
- it exposes an OpenAI-compatible local endpoint
- it is easier for non-AI specialists than building an inference stack from scratch

The app talks to LM Studio through `http://127.0.0.1:1234/v1`.

That keeps the app portable.
If a school later wants a different OpenAI-compatible local backend, the service layer is already designed for that.

Full setup instructions are in the [IT deployment guide](docs/IT_DEPLOYMENT.md).

---

## Repository Layout

- `app/` Streamlit UI, styles, launcher, and copy helpers
- `core/` typed models, config, storage, and text utilities
- `services/` analysis, ingestion, output generation, export, backend, and orchestration
- `prompts/` prompt templates
- `fixtures/` synthetic regression fixtures and demo material
- `tests/` automated tests
- `docs/` PRD, deployment notes, privacy note, troubleshooting, and demo runbook

---

## Developer Checks

```bash
ruff check .
mypy app core services
pytest
```

Run the app:

```bash
sekretariat-copilot
```

---

## If You Want to Work With Me

This repo is a free public deliverable.
It is also a signal.

If you want help turning local-first AI into something your school or organisation can actually use, I can support work such as:

- workflow discovery
- school-specific prompt and policy design
- privacy-first rollout planning
- local deployment setup
- stakeholder demos
- training for administrators and educators
- proof-of-concept to production pathway design

---

## Further Reading

- [EU AI Act official text (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [EU AI Act summary (EUR-Lex)](https://eur-lex.europa.eu/EN/legal-content/summary/rules-for-trustworthy-artificial-intelligence-in-the-eu.html)
- [GDPR official text (EUR-Lex)](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [GDPR summary (EUR-Lex)](https://eur-lex.europa.eu/EN/legal-content/summary/general-data-protection-regulation-gdpr.html)
- [EDPS 2024 Microsoft 365 decision summary](https://www.edps.europa.eu/press-publications/press-news/press-releases/2024/european-commissions-use-microsoft-365-infringes-data-protection-law-eu-institutions-and-bodies)
- [EDPS 2025 follow-up on Commission compliance](https://www.edps.europa.eu/press-publications/press-news/press-releases/2025/european-commission-brings-use-microsoft-365-compliance-data-protection-rules-eu-institutions-and-bodies_en)
- [US DOJ CLOUD Act resources](https://www.justice.gov/dag/cloudact)
- [LM Studio docs](https://lmstudio.ai/docs/)
- [LM Studio local server docs](https://lmstudio.ai/docs/developer/core/server)
- [LM Studio offline operation docs](https://lmstudio.ai/docs/app/offline)

---

## Bottom Line

If your school wants a first serious step into AI without defaulting to cloud dependency, subscription creep, and governance chaos, this repo is a practical place to start.

It is not a full school platform.
It is not legal advice.
It is not auto-pilot.

It is a focused local-first administrative sidecar designed to save staff time while keeping people, oversight, and trust in the loop.
