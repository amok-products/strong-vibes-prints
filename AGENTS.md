# AGENTS.md — Strong Vibes Prints

Operating manual for AI coding agents (and humans) working in this repo. Read this
before editing any part. It defines the **locked mating interface**, the
**variant vs. version** model, and the **versioning + commit conventions** every
change must follow. Keep edits parametric, keep the interface locked, and bump the
version in the same commit as the geometry change.

---

## 1. Project map

The repo is a family of parametric [build123d](https://build123d.readthedocs.io) CAD
parts that all share **one mating interface** — the **Strong Vibes Connect** (a keyed
diamond boss + female socket clamped by a 1/4"-20 screw). The interface is defined
**once** in the `strongvibes` package and imported by every part, so the connection can never
drift. Each part is a single `.py` script that builds a solid, prints validity, and
exports `.step` / `.stl` / `.3mf`.

```
strongvibes/                 # SHARED STANDARD — the single source of truth
  strong_vibes_connect.py    #   STANDARD_VERSION + DIA_A/DIA_B/BAND_DEPTH + thread spec + builders
  __init__.py                #   re-exports the standard; provides build_path()
parts/<part>/                # one folder per part
  <file>.py                  #   the part script (carries __version__ + VARIANT)
  images/                    #   rendered previews (refreshed on each version bump)
  release/                   #   COMMITTED blessed exports, named with the version
docs/                        # GitHub Pages landing page + the .glb models it loads
build/                       # gitignored working dir — exports land here while iterating
pyproject.toml               # packaging: name = "strongvibes", packages = ["strongvibes"]
CHANGELOG.md                 # top-level, newest first
```

Current parts: `parts/holder/strong_vibes_holder.py` (male device holder) and
`parts/connect/connect_test.py` (the bench-test socket/boss set).

**Setup (do this once):**

```bash
pip install -e .          # makes `strongvibes` importable everywhere
```

After this, any part can `from strongvibes import DIA_A, DIA_B, BAND_DEPTH, build_path`
regardless of where it lives. Build artifacts go to the gitignored repo-root
`build/` dir via `strongvibes.build_path(name)`.

---

## 2. The locked interface rule (MOST IMPORTANT)

The **Strong Vibes Connect diamond is the single source of truth**, defined only in
`strongvibes/strong_vibes_connect.py`:

```python
STANDARD_VERSION = "1.0.0"   # version of the MATING STANDARD itself
DIA_A      = 11.322   # LONG  half-diagonal of the diamond [mm]
DIA_B      = 7.759    # SHORT half-diagonal of the diamond [mm]
BAND_DEPTH = 2.0      # constant-section depth of the band the socket grips [mm]
# + the 1/4"-20 thread spec: THREAD_MAJOR=6.35, THREAD_PITCH=1.27, EFF_THREAD=7.0, ...
```

These values are the published **Strong Vibes Connect** standard (see the umbrella
`connect/strong-vibes-connect.md`). They are **frozen**: do not change them in a part.

**Rules for every part:**

- Parts **MUST** import `DIA_A`, `DIA_B`, `BAND_DEPTH` (and the cutters/builders such
  as `vibes_pocket_cutter`, `vibes_diamond`) **from `strongvibes`**. See `strong_vibes_holder.py`
  (`from strongvibes import DIA_A, DIA_B, BAND_DEPTH, build_path`).
- Parts **MUST NOT** define local parameters that change the mating format. Do not
  recompute or hardcode the diamond half-diagonals, the band depth, or the thread
  spec inside a part.
- When reviewing or editing a part, **verify no knob alters the diamond**. A knob is
  allowed only if it changes geometry *behind* or *around* the mating band, never the
  band itself.

**Allowed knob example** — holder `boss_aspect` (in `strong_vibes_holder.py`): it stretches only
the axial/Z height of the structural flare *buttress behind* the diamond. The mating
band stays `DIA_A`/`DIA_B`/`BAND_DEPTH`, so the connection never changes. Contrast: a
knob that scaled `dia_a`/`dia_b` or `BAND_DEPTH` would break the standard and is
forbidden in a part.

**Editing the standard itself is a repo-wide MAJOR event.** If you change `DIA_A`,
`DIA_B`, `BAND_DEPTH`, or the thread spec in `strongvibes/strong_vibes_connect.py`:

1. Bump `STANDARD_VERSION` (MAJOR).
2. Understand that **every part inherits the change** — it cascades. Re-verify and
   re-release **all** parts (each gets a MAJOR `__version__` bump; see §4).
3. Note it prominently in `CHANGELOG.md`, and update the published
   `connect/strong-vibes-connect.md` standard in the umbrella repo.

---

## 3. Variants vs. versions

Both live side by side; do not conflate them.

- **Variant** = a *meaningfully different design* = **its own file**, identified by the
  `VARIANT` constant near the top of the file (a string id like `"strong_vibes_holder"`).
  Example: two different holder designs would live in two files (e.g. `strong_vibes_holder.py` and `strong_vibes_holder_xl.py`), each its own variant. Creating a genuinely
  new design means a new file with a new `VARIANT`, not a version bump on an old one.
- **Version** = an *iteration of one variant* = the `__version__` semver in that file
  (e.g. `strong_vibes_holder.py` carries `__version__ = "2.0.0"`).

```python
__version__ = "2.0.0"     # iteration of THIS variant (semver)
VARIANT     = "strong_vibes_holder" # the design identity (its own file)
```

---

## 4. Semantic versioning rules (a part's `__version__`)

For the `__version__` string `X.Y.Z` in a part file:

- **PATCH (x.y.Z)** — a tweak that does **not** change fit or interface: a fillet, a
  comment, a small non-mating dimension, a print-quality fix.
- **MINOR (x.Y.z)** — **new parameters/features** that keep the mating interface
  unchanged. The part still mates exactly as before.
- **MAJOR (X.y.z)** — changes the part's own **mating-relevant geometry**, or the part
  **stops being interchangeable** with its prior release.

Changing the **shared standard** (`strongvibes/strong_vibes_connect.py`) is a **MAJOR for
`STANDARD_VERSION`** and **cascades to a MAJOR bump on every part** (§2).

---

## 5. Commit conventions

- **Subject** — Conventional-style, scoped by `VARIANT`, with the new version:
  ```
  strong_vibes_holder: taller flare buttress (v2.1.0)
  ```
- **Bump `__version__` in the SAME commit** as the geometry change. Never let code and
  version drift apart across commits.
- **On a version bump, in the same commit:**
  1. Regenerate the part's exports into `build/` (run the script with `EXPORT = True`).
  2. Copy the blessed files into `parts/<part>/release/`, **named with the version**,
     e.g. `strong_vibes_holder-2.1.0.stl`, `strong_vibes_holder-2.1.0.step`. `release/` **is committed**.
  3. Refresh the part's `images/` previews.
  4. Update the top-level `CHANGELOG.md` (**newest first**).
- **Tag releases:** `strong_vibes_holder-v2.1.0` (`<VARIANT>-v<version>`).
- **Never commit `build/`** — it is the gitignored working dir. Note the root
  `.gitignore` also ignores `*.step`, `*.stl`, `*.3mf` globally; the committed
  `release/` artifacts are version-named copies you add deliberately. `release/` IS
  committed.
- **Sign off every commit** with the DCO: `git commit -s` (adds a
  `Signed-off-by:` trailer). Use your real name and a reachable email.
- **Do NOT add AI co-author trailers** (e.g. a `Co-authored-by:` line crediting an
  AI). Mentioning AI vendors, tools, or their APIs in docs/code is fine — the rule
  is only about commit authorship.
- **Work on a feature branch → open a PR** against `main`; a maintainer merges.

---

## 6. Build & verify checklist (before committing a geometry change)

1. **Run the part:** `python parts/<part>/<file>.py` (or run headless with the
   `show()` call stripped/guarded).
2. **Confirm validity:** the printed `is_valid` is `True`.
3. **Confirm solid count:** it is a **single solid** — unless it is *intentionally*
   not (the part script may already drop stray fragments and report it).
4. **Confirm the interface is unchanged:** print `DIA_A`, `DIA_B`, `BAND_DEPTH` and
   verify they still equal the standard. Parts already echo this, e.g. `strong_vibes_holder.py`
   prints `DIA_A=... DIA_B=... BAND_DEPTH=...` and labels them the locked STANDARD.
5. **Export** only after the above pass (exports land in `build/`).

---

## 7. How an AI should approach a change request

1. **Identify the variant file** — `parts/<part>/<file>.py`; confirm its `VARIANT`.
   A genuinely new design = a new file (new variant), not a bump.
2. **Make the parametric edit** — change a parameter/feature; do not hardcode geometry.
3. **Keep the interface locked** — confirm no edited knob touches the diamond
   (`DIA_A`/`DIA_B`/`BAND_DEPTH`/thread). Still imports the standard from `strongvibes`.
4. **Rebuild & verify validity** — run the script; confirm `is_valid` and the
   intended solid count; confirm the interface dims are unchanged (§6).
5. **Bump `__version__`** — PATCH / MINOR / MAJOR per §4.
6. **Regenerate release + images** — copy version-named exports into
   `parts/<part>/release/`; refresh `images/`.
7. **Commit** — scoped, versioned subject (§5), bump in the same commit, `git commit -s`.
8. **Update `CHANGELOG.md`** — newest first.

---

*Reminder: the diamond is sacred. If a change would alter how parts mate, it is either
a forbidden edit to a part, or a deliberate MAJOR bump of `STANDARD_VERSION` that
cascades to every part. Never silently change the fit.*
