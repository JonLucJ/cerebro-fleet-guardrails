# cerebro-fleet-guardrails

Operational artifacts for the cerebro-* local model fleet (NVIDIA DGX Spark / GB10).

## Principle
**A guardrail must block only the genuinely-prohibited act and never impede legitimate
ability, functionality, or progress.** The DRM guardrail here refuses *circumventing*
copy protection (decrypting/stripping DRM, screenshot/OCR reconstruction, adb extraction,
fabricating "breaker" tools). It must NOT refuse lawful adjacent work: downloading content
the user is entitled to, merging/archiving PDFs, or general coding.

## modelfiles/
Ollama `SYSTEM`-layer guardrail baked into the trained models. Deploy with:
```bash
ollama create cerebro-coder  -f modelfiles/cerebro-coder.Modelfile    # FROM <name>:latest
ollama create cerebro-master -f modelfiles/cerebro-master.Modelfile
```
Note: `FROM cerebro-<role>:latest` (by name) — NOT the blob path, which is root-owned.
The SYSTEM clause overrides inherited system; weights/template/params are inherited.
Why SYSTEM-layer: LoRA on a 7B would not instill the refusal (1/10 adversarial even at
43 boundary samples; model fabricated tools to comply). SYSTEM guardrail = 10/10 refuse,
0 circumvention code. Real enforcement also lives in the tools (no decrypt binary exists).

## bin/
Lawful ebook acquisition toolchain (deployed to ~/local/bin):
- `springer-fetch <DOI>` — downloads only ENTITLED, DRM-free SpringerLink chapter PDFs
  via the live Firefox session; reports gated chapters, never reconstructs them.
- `pdf-merge <dir|files> -o OUT` — natural-sort merge + per-part bookmarks → /media/cerebro/30TB/library.
Runtime venv: ~/local/venvs/pdftools (pypdf + httpx).
