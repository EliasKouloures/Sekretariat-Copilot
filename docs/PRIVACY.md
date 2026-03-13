# Privacy Note

Sekretariat-Copilot is designed to support a local-first privacy posture.

It does not make legal guarantees by itself.
It gives schools a simpler technical starting point.

---

## Default Privacy Posture

By default:

- the app binds to `127.0.0.1`
- the model runs locally through a local host such as LM Studio
- uploaded files and raw pasted content are treated as transient working material in the app session
- the SQLite database stores derived case outputs and minimal audit metadata only
- raw source content is not logged by default
- the app never auto-sends emails or other communication

---

## What Is Stored

The app stores minimal operational metadata such as:

- timestamp
- task type
- duration
- confidence
- success or failure

It also stores derived outputs needed for the local workflow, such as:

- extracted facts
- case briefs
- reply variants
- clarifying questions

The goal is to preserve useful workflow results without creating unnecessary raw-data retention.

---

## What Is Not Logged by Default

By default, the app does not log:

- raw pasted source bodies
- raw uploaded file contents
- outbound messages, because none are sent automatically

This design supports data minimisation and easier internal explanation.

---

## Why This Matters

Many schools are more comfortable with a system that:

- runs on a school-controlled machine
- avoids default public cloud inference
- keeps the first pilot local
- limits retention
- keeps humans in the approval loop

That does not remove the need for policy, legal, or DPO review.
It does make the technical starting posture easier to explain and evaluate.

---

## What Schools Still Need To Decide

Each school still needs to define:

- lawful basis
- workflow scope
- retention period
- access rights
- device controls
- backup handling
- incident handling
- whether a DPIA is required

---

## Intranet Mode

Intranet mode is optional and off by default.

If a school enables LAN access, it should:

- restrict access to a trusted subnet
- review firewall controls
- confirm the model host is not exposed more broadly
- document who can access the service

For most first pilots, localhost-only is the better default.
