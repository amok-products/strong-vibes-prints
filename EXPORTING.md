# Exporting parts

Every part is a parametric build123d script. There are exactly **two ways to run
one**, selected by the `SV_EXPORT` environment variable — no file editing:

| Workflow | Command | What it does |
|----------|---------|--------------|
| **Preview** (default) | `python parts/<part>/<file>.py` | Builds the solid, prints validity + interface dims, shows it live in the OCP CAD Viewer. **Writes no files.** |
| **Export** | `SV_EXPORT=1 python parts/<part>/<file>.py` | Same build, and also writes `.step` + `.stl` (holder: best-effort `.3mf` too) into the gitignored **`build/`** dir. |

`SV_EXPORT` is read once at startup: unset (or anything other than `1`) means
preview-only. This is why importing a part module — or running it in CI — never
opens a viewer and never writes files.

First set up the environment once (see
[Build from source](README.md#build-from-source)):

```bash
python3.13 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .                     # wires up the shared `strongvibes` package
```

## Preview (no files)

```bash
python parts/holder/strong_vibes_holder.py     # snap-fit device holder (MALE boss)
python parts/connect/connect_test.py           # socket_180 + socket_30 + test boss
```

Each run prints the part's volume, `is_valid`, and the locked interface dims
(`DIA_A` / `DIA_B` / `BAND_DEPTH`) so you can confirm the build before exporting.
With the **OCP CAD Viewer** VS Code extension running (port 3939) the model
appears live; without a viewer the run still completes — it just skips the
preview.

## Export to `build/`

```bash
SV_EXPORT=1 python parts/holder/strong_vibes_holder.py
SV_EXPORT=1 python parts/connect/connect_test.py
```

Files land in the repo-root **`build/`** working dir (via
`strongvibes.build_path()`), which is gitignored — export freely, nothing is
committed by accident:

- `build/strong_vibes_holder.step` / `.stl`
- `build/strong_vibes_socket_180.step` / `.stl`
- `build/strong_vibes_socket_30.step` / `.stl`
- `build/strong_vibes_boss.step` / `.stl`

Slice the `.stl` in **Bambu Studio** / **PrusaSlicer**, or open the `.step` to
re-orient or tweak first.

> **3MF note:** for threaded parts the `.3mf` write is best-effort — `lib3mf`'s
> strict manifold check can reject the helical thread mesh even when the solid is
> valid. This is expected; use the `.stl` or `.step` (slicers re-mesh fine).

## Bless a release (maintainers)

Ready-to-print files users download without building live in
`parts/<part>/release/`, **named with the part's `__version__`** (read it at the
top of the script). To cut a release:

1. Export to `build/` with `SV_EXPORT=1` and confirm the printed `is_valid` is
   `True` and the interface dims are unchanged.
2. Copy the validated `.step` + `.stl` into the part's `release/` folder, renamed
   with the version — e.g. for holder `__version__ = "2.0.0"`:

   ```bash
   cp build/strong_vibes_holder.step parts/holder/release/strong_vibes_holder-2.0.0.step
   cp build/strong_vibes_holder.stl  parts/holder/release/strong_vibes_holder-2.0.0.stl
   ```

`build/` is never committed; `parts/**/release/` is (the `.gitignore` ignores
`*.stl` / `*.step` globally **except** under `release/`). See
[`AGENTS.md`](AGENTS.md) for the full versioning + release conventions.
