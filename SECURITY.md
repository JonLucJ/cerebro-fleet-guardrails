# Security Policy

## Scope
This repo ships a model **guardrail** (Ollama `SYSTEM`-layer) and two **lawful ebook
tools**. The threat model is small but specific:

- **Guardrail leaks** — a model emitting DRM-circumvention code/instructions. These are
  defense-in-depth failures, not capability failures: there is **no DRM-break binary on the
  box** (`pdf-merge` has no `--decrypt`, no breaker tool exists), so a bad model answer
  cannot actually break protection.
- **Over-refusal** — the guardrail blocking legitimate work. This is treated as a bug
  (see the project's guiding principle) and is a hard-gated CI failure.
- **Self-hosted CI runner** — the live probe runs on a private GB10 box. The workflow
  restricts `live-verify` to `push`/`workflow_dispatch` and never runs it on `pull_request`,
  so a fork's PR cannot execute code on the runner.

## Reporting
Email **jonathan.justinien@gmail.com** with a minimal reproduction:
- For a guardrail leak: the exact prompt + the model response (and which model/tag).
- For over-refusal: the legitimate prompt that was refused.
- For a tooling vuln (e.g. SSRF/path traversal in `springer-fetch`/`pdf-merge`): steps + impact.

Please do **not** file requests for DRM-circumvention help as security issues — they will be closed.

## Handling untrusted input
`springer-fetch` consumes remote HTTP responses and `pdf-merge` consumes arbitrary PDFs;
both are treated as adversarial (content-type/`%PDF` checks, encrypted/corrupt-input skips,
bounded retries, no shell execution of fetched content).
