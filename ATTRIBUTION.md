# Attribution

The parametric parts in this repository (the build123d source and the models it
generates) are licensed **CC-BY-4.0** — see [`LICENSE`](LICENSE). This file credits
the third-party works this repo builds on; each keeps its **own** license.

## The CAD builds on

| Work | License | Used for |
|---|---|---|
| [build123d](https://github.com/gumyr/build123d) | Apache-2.0 | the Python CAD framework the parts are written in |
| [OCP](https://github.com/CadQuery/OCP) (`cadquery-ocp` bindings) | Apache-2.0 | the Python bindings to the geometry kernel |
| [OpenCASCADE (OCCT)](https://dev.opencascade.org/), bundled by `cadquery-ocp` | LGPL-2.1 + OCCT exception | the geometry kernel behind build123d |
| [bd_warehouse](https://github.com/gumyr/bd_warehouse) | Apache-2.0 | thread modelling (the 1/4"-20 helical thread) |
| [OCP CAD Viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) (`ocp_vscode`, `ocp-tessellate`) | Apache-2.0 | the live VS Code 3D preview |

The complete, pinned Python dependency set is in
[`requirements.txt`](requirements.txt); each package retains its own upstream
license.

## The landing page uses

| Work | License | Used for |
|---|---|---|
| [`<model-viewer>`](https://github.com/google/model-viewer) by Google | Apache-2.0 | the interactive 3D part previews in `docs/` (loaded from Google's CDN) |
| [Inter](https://github.com/rsms/inter) & [JetBrains Mono](https://github.com/JetBrains/JetBrainsMono) fonts | SIL OFL-1.1 | the landing-page typography (loaded from Google Fonts) |

## Standard

The **Strong Vibes Connect** dimensions (`DIA_A`, `DIA_B`, `BAND_DEPTH`, thread
spec) in `strongvibes/strong_vibes_connect.py` are the source of truth for the
[Strong Vibes Connect standard](https://github.com/amok-products/strong-vibes/blob/main/connect/strong-vibes-connect.md)
published in the umbrella repo.

If you believe an attribution is missing or incorrect, please open an issue.
