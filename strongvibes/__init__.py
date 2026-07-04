"""
Strong Vibes Prints — shared library.

`strongvibes` is the single source of truth for the **Strong Vibes Connect** mating
standard. Every part imports its diamond interface from here so the connection
can never drift:

    from strongvibes import DIA_A, DIA_B, BAND_DEPTH, vibes_pocket_cutter

Install once (editable) so the parts in ../parts/ can import it from anywhere:

    pip install -e .

Build artifacts go to the gitignored repo-root build/ dir via build_path().
"""
from pathlib import Path

from .strong_vibes_connect import (
    # --- the locked mating standard ---
    DIA_A, DIA_B, BAND_DEPTH, CLEAR, MOUTH_LEAD, BOLT_CLEAR, MATE,
    STANDARD_VERSION,
    # --- thread spec ---
    THREAD_MAJOR, THREAD_PITCH, THREAD_CLEAR, EFF_THREAD, PLATE_T,
    LEAD_IN_D, LEAD_IN_DEPTH, SELFTAP_D, USE_THREAD, FEMALE_THREAD,
    # --- builders ---
    vibes_diamond, vibes_pocket_cutter, vibes_pocket_cutter_star,
    vibes_female_screw,
    strong_vibes_socket, strong_vibes_socket_180, strong_vibes_socket_30,
    strong_vibes_boss, vibes_dims,
)

__all__ = [
    "DIA_A", "DIA_B", "BAND_DEPTH", "CLEAR", "MOUTH_LEAD", "BOLT_CLEAR", "MATE",
    "STANDARD_VERSION", "THREAD_MAJOR", "THREAD_PITCH", "THREAD_CLEAR",
    "EFF_THREAD", "PLATE_T", "LEAD_IN_D", "LEAD_IN_DEPTH", "SELFTAP_D",
    "USE_THREAD", "FEMALE_THREAD", "vibes_diamond", "vibes_pocket_cutter",
    "vibes_pocket_cutter_star", "vibes_female_screw", "strong_vibes_socket",
    "strong_vibes_socket_180", "strong_vibes_socket_30", "strong_vibes_boss",
    "vibes_dims", "build_path",
]


def build_path(name):
    """Absolute path under the repo-root, gitignored ``build/`` working dir.

    Parts export here while iterating (clutter-free, never committed); copy the
    blessed files into ``parts/<part>/release/`` when cutting a version."""
    out = Path(__file__).resolve().parent.parent / "build"
    out.mkdir(exist_ok=True)
    return str(out / name)
