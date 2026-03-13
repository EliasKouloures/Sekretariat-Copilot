# IT Deployment Guide

This guide is for school IT teams and technical operators.

It assumes you are comfortable with normal software setup, but not necessarily with local AI tooling yet.

If you are a school leader, administrator, or educator, start with the main [README](../README.md) instead.

---

## What You Are Deploying

You are deploying:

- a Python web app
- a local SQLite database
- a local model host
- one or more local AI models

You are not deploying:

- a managed SaaS platform
- an autonomous agent
- an email-sending bot
- a grading or admissions system

---

## Recommended First Deployment Profile

Use this for the first pilot:

- one dedicated Mac or Windows PC
- one named operator account
- LM Studio running locally
- app bound to `127.0.0.1`
- no intranet mode
- synthetic fixtures first
- real school data only after internal acceptance

This is the safest and simplest starting point.

---

## Technical Stack

- Python 3.12, 3.13, or 3.14
- Streamlit UI
- OpenAI Python SDK pointed at a local OpenAI-compatible endpoint
- LM Studio as the default local model host
- SQLite for local metadata and derived outputs
- PyMuPDF for direct PDF extraction
- Pillow for image preprocessing

---

## Before You Start

Confirm:

1. The pilot machine is patched.
2. Disk encryption is enabled.
3. Access is limited to named staff.
4. You know where `config.toml` and the SQLite file will live.
5. You have decided whether the first rollout is:
   - text only
   - text plus digital PDFs
   - text plus PDFs plus image OCR

For most schools, start with text and digital PDFs.

---

## Get the Repo

Clone the repository:

```bash
git clone https://github.com/EliasKouloures/Sekretariat-Copilot.git
cd Sekretariat-Copilot
```

If your school does not use Git yet, download the repository as a ZIP and unpack it on the pilot machine.

---

## LM Studio Setup

LM Studio is the reference backend for this repo.

### Why LM Studio

- easy desktop UI
- Apple Silicon friendly
- OpenAI-compatible local server
- good beginner path for local models
- works offline after model download

### Install LM Studio

1. Download LM Studio from the official site.
2. Install the correct build.
   - On Mac, use Apple Silicon / arm64.
3. Open the app.

### Choose a Model

On a 16 GB Apple Silicon machine:

- start with a small instruct model for text workflows
- add a vision-capable model only if you need image OCR

Practical advice:

- text-first gives the best first impression
- digital PDFs do not require a vision model if direct text extraction works
- vision models need more memory and more care

### Start the Local Server

In LM Studio:

1. Load the model.
2. Open the `Developer` tab.
3. Start the local server.
4. Confirm the endpoint is `http://127.0.0.1:1234/v1`.

That is the default backend target for this app.

---

## macOS Reference Install

From the repo root:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp config.example.toml config.toml
```

If `python3` does not work, try:

```bash
python --version
python -m venv .venv
```

If `sekretariat-copilot` is not found later, run:

```bash
.venv/bin/sekretariat-copilot
```

---

## Windows Reference Install

See the full [Windows setup guide](WINDOWS_SETUP.md) for the cleanest path.

Fast path:

```powershell
py --version
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item config.example.toml config.toml
```

If `py -3` does not exist, use:

```powershell
python -m venv .venv
```

If the launcher is not found, use:

```powershell
.venv\Scripts\sekretariat-copilot.exe
```

---

## Configure the App

Copy the example file first:

```bash
cp config.example.toml config.toml
```

Important fields:

- `provider_name`
  - default is `lm_studio`
- `base_url`
  - usually `http://127.0.0.1:1234/v1`
- `model_id`
  - must match the model actually loaded in LM Studio
- `supports_vision`
  - `false` for text-only use
  - `true` only if a working local vision model is loaded
- `bind_host`
  - keep `127.0.0.1` for the first deployment
- `database_path`
  - choose according to school policy and local backup rules

---

## Run the App

```bash
sekretariat-copilot
```

Then open:

```text
http://127.0.0.1:8501
```

If needed, run the launcher directly:

```bash
.venv/bin/sekretariat-copilot
```

---

## First Verification

Check:

1. The top status pill shows the backend is reachable.
2. The configured `model_id` matches the loaded model.
3. The diagnostics section shows no unexpected backend errors.
4. `Process locally` works with synthetic fixtures.

Recommended first fixtures:

- `fixtures/text/absence_full.txt`
- `fixtures/notes/note_missing_dates.txt`
- `fixtures/pdfs/pdf_absence_direct.pdf`
- `fixtures/images/image_absence_clear.png`

Use the image fixture only if `supports_vision = true`.

---

## Pilot Sequence

Use this order:

1. Synthetic fixtures
2. Low-sensitivity internal examples
3. Real office material under local policy

Train staff on:

- when to use the tool
- when not to use it
- how to review outputs
- how to recognise low-confidence or blocked cases

---

## Security and Governance Checklist

Before real use, confirm:

1. Disk encryption is enabled.
   - FileVault on macOS
   - BitLocker on Windows
2. Staff use named accounts.
3. Automatic screen lock is enabled.
4. The workflow scope is documented.
5. Retention for the SQLite database is defined.
6. Human review is mandatory before any communication leaves the system.
7. The school has checked whether a DPIA is needed.
8. Staff know which data may and may not be entered.

---

## GDPR and AI Act Notes for IT Leads

This tool is positioned as a human-in-the-loop drafting and extraction assistant.

That means:

- no automated decisions
- no auto-send
- no grading
- no behavioural monitoring
- no admissions automation

Review at minimum:

- purpose
- lawful basis
- data categories
- access rights
- retention
- device controls
- incident path
- local staff instructions

Do not treat the local-first design as a substitute for internal review.
Treat it as a better starting posture.

---

## Intranet Mode

This app can be exposed on a trusted local network, but that should be a second step.

For the first pilot:

- keep `bind_host = "127.0.0.1"`
- keep the model host local
- do not expose the service beyond the pilot machine

If you later enable LAN access:

- restrict it to a trusted subnet
- document who can reach it
- confirm the model host is not exposed more broadly
- review firewall and reverse proxy controls

---

## Troubleshooting Shortcuts

### The backend is unavailable

- make sure LM Studio is open
- make sure a model is loaded
- make sure the local server is running
- confirm `base_url` and `model_id` in `config.toml`

### PDFs work but screenshots do not

- you likely do not have a vision-capable model loaded
- set `supports_vision = false` and start with text or digital PDFs

### The machine feels slow

- use a smaller model
- keep OCR disabled at first
- begin with text-only workflows

### `python3.12` is missing

That is normal on many systems.
Use `python3` if it exists.

### `sekretariat-copilot` is not found

Activate the virtual environment first, or run the launcher directly from `.venv`.

For more, see the [Troubleshooting guide](TROUBLESHOOTING.md).

---

## Verification Commands

```bash
ruff check .
mypy app core services
pytest
```

---

## Related Docs

- [Main README](../README.md)
- [Windows setup guide](WINDOWS_SETUP.md)
- [Privacy note](PRIVACY.md)
- [Troubleshooting guide](TROUBLESHOOTING.md)
- [Demo runbook](DEMO_RUNBOOK.md)
