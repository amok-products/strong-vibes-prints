# Contributing to Strong Vibes Prints

Thanks for your interest! This repo holds parametric [build123d](https://build123d.readthedocs.io)
CAD parts that all share the **Strong Vibes Connect** mating interface. It's part
of the [Strong Vibes](https://github.com/amok-products/strong-vibes) open builder
program.

Before editing a part, read [`AGENTS.md`](AGENTS.md) — it is the operating manual
for this repo (the locked interface rule, variant-vs-version model, and the
versioning + commit conventions every change must follow).

## Where does my change go?

| Change | Repository |
|---|---|
| A printable part / CAD source (`parts/`, `strongvibes/`) | **here** (`amok-products/strong-vibes-prints`) |
| The **Strong Vibes Connect** dimensions/standard | starts **here** in `strong_vibes_connect.py`, then the [umbrella](https://github.com/amok-products/strong-vibes) `connect/` doc follows |
| Protocol spec, builder kit, community docs | [umbrella](https://github.com/amok-products/strong-vibes) |

## Ground rules

- Be respectful — see [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
- **The mating diamond is frozen.** `DIA_A`, `DIA_B`, `BAND_DEPTH` and the thread
  spec in `strongvibes/strong_vibes_connect.py` are the published Strong Vibes
  Connect standard. Do not change them in a part — that breaks compatibility with
  every other part (see `AGENTS.md` §2). A deliberate standard change is a
  repo-wide MAJOR event.
- Keep edits **parametric** — change a parameter, never hardcode mating geometry.
- **Rebuild and verify** before committing: the part must report `is_valid`, the
  intended solid count, and the unchanged interface dims (`AGENTS.md` §6).
- These are printed physical parts. Use body-safe materials and test fit at the
  bench before relying on a mount.

## Developer Certificate of Origin (DCO)

This project uses the **DCO** instead of a CLA. By contributing, you certify the
[Developer Certificate of Origin 1.1](https://developercertificate.org/). Sign
off every commit:

```bash
git commit -s -m "your message"
```

which adds a `Signed-off-by: Your Name <you@example.com>` trailer. Use your real
name and a reachable email.

> Note: do **not** add AI co-author trailers to commits (e.g. a `Co-authored-by:`
> line crediting an AI). Mentioning AI vendors, tools, or their APIs in docs and
> code is fine — the rule is only about commit authorship.

## Branch & PR flow

Work on a feature branch → open a PR against `main` → a maintainer merges. Bump the
part's `__version__` and update `CHANGELOG.md` in the same commit as a geometry
change (`AGENTS.md` §4–5).

## Branding & trademark constraint

The CAD is CC-BY-4.0, but the **names are trademarks** (see [`TRADEMARK.md`](TRADEMARK.md)).
Contributions must not introduce uses of the "Strong Vibes" or "Europe Magic
Wand®" names that conflict with that policy (e.g. implying a fork is the official
project, or marking "Strong Vibes" as a registered trademark). Factual
compatibility statements are fine.
