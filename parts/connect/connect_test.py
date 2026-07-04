"""
============================================================
STRONG VIBES CONNECT  -  bench-test parts
============================================================
Printable test pieces for the Strong Vibes Connect interface (defined in the `strongvibes`
package). Print them and check the fit before committing a stand/holder design:

    strong_vibes_socket_180  -> FEMALE, keyed: accepts the boss in ONE orientation (mod 180 deg).
    strong_vibes_socket_30   -> FEMALE, star : accepts the boss every 30 deg (stepwise mounting).
    strong_vibes_boss        -> MALE  : the diamond boss with a 1/4"-20 internal thread + lead-in.

The boss plugs into either socket; a 1/4"-20 screw clamps the joint. The diamond
dimensions come straight from the locked standard (strongvibes.DIA_A / DIA_B / BAND_DEPTH),
so these test parts mate with every real part in the repo.

Run:     python parts/connect/connect_test.py                 (live preview; writes nothing)
Export:  SV_EXPORT=1 python parts/connect/connect_test.py     (.step / .stl -> build/)
============================================================
"""
import os
from build123d import *
from strongvibes import (strong_vibes_socket_180, strong_vibes_socket_30, strong_vibes_boss,
                 DIA_A, DIA_B, BAND_DEPTH, PLATE_T, EFF_THREAD, STANDARD_VERSION,
                 build_path)

try:
    from ocp_vscode import show
except Exception:
    show = None

__version__ = "1.0.0"      # bump per AGENTS.md on any geometry change
VARIANT = "connect_test"   # the Strong Vibes Connect bench-test trio

EXPORT = os.environ.get("SV_EXPORT", "0") == "1"   # preview-only by default; SV_EXPORT=1 also writes files


# ============================================================
#  BUILD
# ============================================================
socket_180 = strong_vibes_socket_180()
socket_30 = strong_vibes_socket_30()
boss, _face_z = strong_vibes_boss()

socket_180.color = Color(0, 0, 0)          # female parts render black
socket_30.color = Color(0, 0, 0)


# ============================================================
#  REPORT
# ============================================================
print(f"STRONG VIBES CONNECT  (standard v{STANDARD_VERSION})  "
      f"DIA_A={DIA_A:.3f}  DIA_B={DIA_B:.3f}  BAND_DEPTH={BAND_DEPTH:.1f} mm")
for name, p in (("strong_vibes_socket_180", socket_180), ("strong_vibes_socket_30", socket_30), ("strong_vibes_boss", boss)):
    b = p.bounding_box()
    print(f"  {name:11s} valid={p.is_valid}  vol={p.volume/1000:.2f}cm3  "
          f"bbox {b.size.X:.1f}x{b.size.Y:.1f}x{b.size.Z:.1f}mm")
print(f"  assemble with one 1/4\"-20 x >= {PLATE_T + EFF_THREAD:.0f} mm screw")


if __name__ == "__main__":
    if show is not None:
        try:
            show(socket_180, Pos(40, 0, 0) * socket_30, Pos(80, 0, 0) * boss,
                 names=["strong_vibes_socket_180", "strong_vibes_socket_30", "strong_vibes_boss"])
        except Exception as e:
            print(f"  (viewer not available: {e})")
    if not EXPORT:
        print("Preview only (set SV_EXPORT=1 to write .step / .stl into build/)")
    else:
        for part, name in ((socket_180, "strong_vibes_socket_180"), (socket_30, "strong_vibes_socket_30"),
                           (boss, "strong_vibes_boss")):
            export_step(part, build_path(f"{name}.step"))
            export_stl(part, build_path(f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
            print(f"Exported to build/: {name}  (.step  .stl)")
