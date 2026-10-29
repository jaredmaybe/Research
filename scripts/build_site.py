#!/usr/bin/env python3
"""Build the deployable copy of the page into build/.

Sites accepts at most 10 MiB of assets per deployment, and the original
photos weigh ~15 MB together. This copies index.html and images/ into
build/public, re-encoding the photos to WebP at a 1600px long edge.
The originals in images/ are never modified, so local previews keep
using the full-quality files.

Usage: python3 scripts/build_site.py
"""

import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
PUBLIC = BUILD / "public"
MAX_EDGE = 1600
QUALITY = 82
PHOTO_SUFFIXES = {".png", ".jpg", ".jpeg"}

WORKER = """export default {
  async fetch(request, env) {
    return env.ASSETS.fetch(request);
  },
};
"""


def main() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    (PUBLIC / "images").mkdir(parents=True)

    html = (ROOT / "index.html").read_text(encoding="utf-8")

    for source in sorted((ROOT / "images").iterdir()):
        target = PUBLIC / "images" / source.name
        # cat.png is 6 KB and already the right size.
        if source.suffix.lower() in PHOTO_SUFFIXES and source.name != "cat.png":
            with Image.open(source) as image:
                image = image.convert("RGB")
                image.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
                target = target.with_suffix(".webp")
                image.save(target, "WEBP", quality=QUALITY, method=6)
            html = html.replace(f"images/{source.name}", f"images/{target.name}")
        else:
            shutil.copy2(source, target)

    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    (BUILD / "worker.js").write_text(WORKER, encoding="utf-8")
    (BUILD / "manifest.json").write_text(
        json.dumps(
            {
                "entrypoint": "worker.js",
                "compatibilityDate": "2026-10-29",
                "modules": [
                    {"name": "worker.js", "type": "esm", "path": "./worker.js"}
                ],
                "assetsDirectory": "./public",
                "spa": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    total = sum(f.stat().st_size for f in PUBLIC.rglob("*") if f.is_file())
    print(f"assets: {total / 1024 / 1024:.2f} MiB in {PUBLIC}")
    for path in sorted(PUBLIC.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(PUBLIC)}  {path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
