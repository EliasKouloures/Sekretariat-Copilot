# FAQ

## Is this a cloud AI service?

No.

The default path is local-first:

- local web app
- local model host
- local machine by default

That means a school can evaluate the workflow without defaulting to public cloud inference.

## Does it send messages automatically?

No.

The app never auto-sends communication.
Staff review, edit, and copy the output themselves.

## Does it replace the school information system?

No.

It is a sidecar.
It helps with drafting, summarising, and extraction work around existing systems.

## Is this legally compliant?

No repo can promise that on its own.

This project is designed to be more governance-friendly through local processing, limited logging, and human review.
Each school still needs its own legal, policy, and data protection review.

## Why mention the US CLOUD Act and European concerns?

Because many European schools want to reduce avoidable cloud risk when a local path exists.

The point is not that every foreign service is automatically unlawful.
The point is that local-first often creates a cleaner starting posture.

## Why LM Studio?

Because it is one of the easiest ways for non-AI specialists to run a local model through an OpenAI-compatible endpoint.

It is especially practical for small pilots on Apple Silicon machines.

## Can this run on Windows?

Yes.

The same repo supports Windows.
See the [Windows Setup Guide](WINDOWS_SETUP.md).

## Does it work offline?

Yes, after the local models are downloaded.

The app can run fully offline on one machine if the model is already installed locally.

## Can it handle screenshots and scanned PDFs?

Sometimes, yes.

The app supports image and PDF workflows, but image OCR depends on the local model and input quality.
Digital PDFs are the easiest file path because the app tries direct text extraction first.

## Does it support handwriting?

No.

Handwritten cursive is out of scope for the MVP.

## Can it process multi-child messages?

No.

Those are blocked in the MVP because they raise ambiguity risk.

## Who should use this repo first?

- school leaders who want a calm, credible AI pilot story
- school offices who want to test one useful workflow
- IT teams who want an inspectable local-first architecture

## Where should a school start?

Start here:

1. [School Leader Brief](SCHOOL_LEADER_BRIEF.md)
2. [Pilot Checklist](PILOT_CHECKLIST.md)
3. [IT Deployment Guide](IT_DEPLOYMENT.md)
