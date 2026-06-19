# Changelog

All notable changes to this project.

## [0.2.0] — 2026-06-18
### Added
- Fleet-wide guardrail: precise-scope DRM Modelfiles for all six roles
  (master, scientist, investor, coder, analyst, creative), not just coder/master.
- `deploy.sh` — idempotent one-shot to apply every guardrail Modelfile (`FROM <name>`).
- `tests/test_pdf_merge.py` — cloud-runnable integration test (pages, bookmarks,
  corrupt-input skip, exit-code contract); wired into CI.
- `requirements.txt`, `SECURITY.md`, this changelog.
### Changed
- `pdf-merge`: encrypted/corrupt-PDF handling, atomic output write, exit codes, type hints.
- `springer-fetch`: bounded exponential backoff on transient HTTP, `--list` dry-run,
  explicit exit codes (3 = all gated, 4 = no links), `client.close()`.
- CI cloud job now installs deps, byte-compiles all scripts, `bash -n deploy.sh`, and
  runs both unit + integration tests.

## [0.1.0] — 2026-06-17
### Added
- DRM-circumvention guardrail at the Ollama `SYSTEM` layer for cerebro-coder/master
  (LoRA alone scored 1/10 adversarial; SYSTEM guardrail → robust refusal).
- Lawful ebook tools: `springer-fetch` (entitled DRM-free chapter PDFs) + `pdf-merge`.
- `tests/verify_boundary.py` (live probe) + `tests/test_judge.py` (judge unit tests).
- CI: cloud judge-logic + self-hosted Spark live probe; gating policy = hard-gate LEGIT
  + tool-layer, report circumvention (best-effort).
- README, CONTRIBUTING, MIT LICENSE, badges, usage example.
