# Contributing

Thanks for your interest. This repo holds operational artifacts for a local `cerebro-*`
model fleet: a DRM-circumvention **guardrail** and lawful **ebook tools**. Contributions
are welcome — please keep the guiding principle in mind.

## Guiding principle

> **A guardrail must block only the genuinely-prohibited act and never impede legitimate
> ability, functionality, or progress.**

Concretely, for any change:
- **Never weaken the lawful path.** `springer-fetch` (entitled downloads), `pdf-merge`,
  open-access fetches, and general coding must keep working. Over-refusing legitimate work
  is a bug and **fails CI** (it's a hard gate).
- **Never add a DRM-circumvention capability.** No decrypt/strip, no screenshot/OCR
  reconstruction, no `adb` extraction of protected content, no "breaker" tooling. Real
  enforcement lives in the tools — keep it that way (e.g. `pdf-merge` must never gain a
  `--decrypt`).

## Project layout

| path | what |
|------|------|
| `modelfiles/` | Ollama `SYSTEM`-layer guardrail for `cerebro-coder` / `cerebro-master` |
| `bin/`        | `springer-fetch`, `pdf-merge` (deployed to `~/local/bin`) |
| `tests/`      | `verify_boundary.py` (live probe) + `test_judge.py` (judge unit tests) |
| `.github/workflows/verify.yml` | CI: cloud judge-logic + self-hosted live probe |

## Dev setup

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install pypdf httpx        # runtime deps for the tools
```
The live probe additionally needs a running Ollama (`:11434`) with the fine-tuned
`cerebro-coder` / `cerebro-master` models — those only exist on the GB10 box.

## Running the checks

```bash
# fast, no models — validates the judge classifier (this is what cloud CI runs)
python3 tests/test_judge.py

# full live probe against the real models (needs Ollama + cerebro-*)
python3 tests/verify_boundary.py                 # temp 0, deterministic
```

**Gating policy** (a local 7B can't be both 100%-refuse and 0%-over-refuse, so we gate on
what matters and report the rest):
- **HARD GATE** — `LEGIT` prompts must still get real help (never impede lawful work).
- **HARD GATE** — no real DRM-break capability may exist on the box.
- **Reported, not gating** — `CIRCUMVENT` refusal is best-effort defense-in-depth.

If you touch the guardrail, **rebuild and re-run the probe**:
```bash
ollama create cerebro-coder  -f modelfiles/cerebro-coder.Modelfile    # FROM <name>:latest
ollama create cerebro-master -f modelfiles/cerebro-master.Modelfile
python3 tests/verify_boundary.py
```

## Pull requests

- Keep changes small and focused; one logical change per PR.
- Cloud CI (`judge-logic`) runs on every PR and must pass.
- The self-hosted live probe (`live-verify`) runs only on pushes to `main` and manual
  dispatch — **never on fork PRs**, since a self-hosted runner must not execute untrusted
  code. A maintainer will run the live probe before merging guardrail/tool changes.
- If you change `tests/verify_boundary.py`'s judge logic, add a case to `tests/test_judge.py`.

## Reporting issues

Open an issue for guardrail leaks (with the exact prompt + response) or for any case where
the guardrail refused legitimate work. Do **not** open issues requesting DRM-circumvention
help — those will be closed.
