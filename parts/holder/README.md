# Holder (`strong_vibes_holder.py`)

The snap-fit device holder — the **MALE** side of the Strong Vibes Connect. The device clips into the holder, and the holder carries a keyed diamond boss that plugs into any Strong Vibes Connect socket, clamped by a 1/4"-20 screw.

> Spin it in 3D in the [interactive viewer](https://amok-products.github.io/strong-vibes-prints/).

## Role

**MALE** — diamond boss (`DIA_A` / `DIA_B` / `BAND_DEPTH`, imported from `strongvibes`) with a 1/4"-20 internal thread down the boss axis. The mating diamond is the locked standard and is never recomputed here.

## Key parameters

| Param | Default | What it does |
|-------|---------|--------------|
| `boss_aspect` | `1.5` | Taller buttress via the flare only (axial Z stretch behind the diamond). The mating diamond stays the standard. |
| `boss_flare` | `7` | How far the boss widens past the diamond onto the body. |
| `boss_fillet` | `10` | Blend radius where the boss meets the wall. |
| `THREAD_CLEAR` | `0.6` | Diametral clearance on the modelled 1/4-20 thread for FDM (raise to loosen). |
| `use_thread` | `True` | Model the helical thread (`False` = plain 5.8 mm self-tap hole). |
| `QUILT` | `True` | Recessed diamond-quilt texture on the outer surface. |

For **Europe Magic Wand®** models. Tested in Bambu Lab **TPU for AMS (68D)** or **PLA Tough** — ordinary PLA will crack. For a perfect fit, add a **4 cm strip of Bambu Lab non-slip tape** to the lower back. Assemble with a **1/4"-20 × 9–10 mm** camera screw (Bambu Lab).

## Preview & export

```bash
python parts/holder/strong_vibes_holder.py     # live 3D in the OCP CAD Viewer (port 3939)
```

Set `EXPORT = True` (already the default) to also write `.step` / `.stl` / `.3mf` to the gitignored `build/` dir. The `.3mf` is best-effort and may be skipped for the threaded mesh — use the `.stl` or `.step`.
