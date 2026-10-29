# Repository instructions

## Commit messages

- Do not add AI attribution to commits. No `Generated with Codebuff` line, no
  `Co-Authored-By` trailer, and no mention of the assistant or tooling in the
  subject or body.
- End the commit message at its own last line of real content. A subject plus a
  short body explaining why the change was made is enough.
- Keep the existing style: a plain declarative subject line, then a body only
  when the reasoning is not obvious from the subject.

## Project notes

- `index.html` is the whole site: markup, styles and scripts in one file, with
  photos in `images/`.
- Deploying needs `python3 scripts/build_site.py` first (requires Pillow). It
  writes the `build/` bundle (WebP re-encodes, Workers entry point, Sites
  manifest). `build/` is generated and ignored by Git.
- Keep the originals in `images/` at full quality; only the build step
  re-encodes them.
