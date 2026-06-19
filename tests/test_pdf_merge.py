#!/usr/bin/env python3
"""Integration test for bin/pdf-merge — runs anywhere with pypdf, NO models.

Builds synthetic PDFs, runs the real CLI, and asserts: correct page count,
one bookmark per part at the right page, a corrupt input is skipped (not fatal),
and the exit code contract holds.
"""
import os, subprocess, sys, tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "bin" / "pdf-merge"


def make_pdf(path: Path, pages: int):
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(width=200, height=200)
    with open(path, "wb") as f:
        w.write(f)


def run(args):
    return subprocess.run([sys.executable, str(TOOL), *args],
                          capture_output=True, text=True)


def outline_targets(reader):
    out = []
    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                out.append((it.title, reader.get_destination_page_number(it) + 1))
    walk(reader.outline)
    return out


def main():
    fails = 0
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        make_pdf(d / "01_front.pdf", 2)
        make_pdf(d / "02_chapter_one.pdf", 3)
        make_pdf(d / "03_chapter_two.pdf", 1)
        (d / "04_corrupt.pdf").write_bytes(b"%PDF-1.4 not really a pdf")  # must be skipped
        out = d / "merged.pdf"

        r = run([str(d), "-o", str(out), "--title", "Test Book"])
        print(r.stdout.strip())
        if r.returncode != 0:
            print(f"[FAIL] exit {r.returncode} (want 0)\n{r.stderr}"); fails += 1

        reader = PdfReader(str(out))
        if len(reader.pages) != 6:
            print(f"[FAIL] pages={len(reader.pages)} (want 6)"); fails += 1
        else:
            print("[ok] page count = 6 (corrupt input skipped)")

        bm = outline_targets(reader)
        want = [("front", 1), ("chapter one", 3), ("chapter two", 6)]
        if bm != want:
            print(f"[FAIL] bookmarks {bm} (want {want})"); fails += 1
        else:
            print(f"[ok] bookmarks = {bm}")

        # exit-code contract: no usable input → 2
        empty = d / "empty"; empty.mkdir()
        r2 = run([str(empty), "-o", str(d / "x.pdf")])
        if r2.returncode != 2:
            print(f"[FAIL] empty-dir exit {r2.returncode} (want 2)"); fails += 1
        else:
            print("[ok] empty input → exit 2")

    print(f"\n{'PASS' if fails == 0 else 'FAIL'}: {fails} failing case(s)")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
