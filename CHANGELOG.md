# Changelog

All notable changes to Strong Vibes Prints are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com); newest first. Individual
parts also carry their own `__version__` (see [`AGENTS.md`](AGENTS.md)).

## [Unreleased]

Tooling & packaging only — **no geometry changes**, so no part `__version__`
bumps and the exported models are identical to 1.0.0.

- **Headless-safe parts.** `strong_vibes_holder.py` now guards its `ocp_vscode`
  import (`try/except`) and runs its preview + export under
  `if __name__ == "__main__"`, matching `connect_test.py`. Running a part with no
  OCP CAD Viewer no longer errors, and merely importing a part module opens no
  viewer and writes no files.
- **`SV_EXPORT` export toggle.** Exporting no longer means hand-editing an
  `EXPORT` constant: a plain run previews only, and
  `SV_EXPORT=1 python parts/<part>/<file>.py` also writes `.step` / `.stl` into
  the gitignored `build/`. New [`EXPORTING.md`](EXPORTING.md) documents both
  workflows; linked from the README.
- **First blessed release files.** `parts/holder/release/` and
  `parts/connect/release/` now hold the version-named `.stl` + `.step` the
  landing page's "STL / STEP files" links serve — `strong_vibes_holder-2.0.0`,
  and `strong_vibes_socket_180` / `strong_vibes_socket_30` / `strong_vibes_boss`
  at `1.0.0`.

## [1.0.0] — 2026-07-04

Initial public release as part of the [Strong Vibes](https://github.com/amok-products/strong-vibes)
open builder program.

- **Strong Vibes Connect** mating standard (`STANDARD_VERSION = 1.0.0`) — keyed
  diamond boss + socket clamped by a 1/4"-20 screw, defined once in the
  `strongvibes` package and imported by every part.
- **Holder** (`strong_vibes_holder.py`) — snap-fit device holder, MALE diamond boss.
- **Connect** bench-test set (`connect_test.py`) — `strong_vibes_socket_180`,
  `strong_vibes_socket_30`, and a male test boss for validating the interface.
- Interactive 3D landing page (GitHub Pages).
