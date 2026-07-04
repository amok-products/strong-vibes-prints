"""
============================================================
STRONG VIBES CONNECT  -  diamond boss + female socket  (two test parts)
============================================================
INTERFACE DEFINITION + parametric builders + a printable bench-test pair.

The holder (strong_vibes_holder.py) ends its camera boss in a flat-faced,
anti-rotation DIAMOND (rhombus). The outer `BAND_DEPTH` of that diamond is a
CONSTANT cross-section "band"; behind it the boss flares onto the body. A 1/4"-20
thread runs down the boss axis. A "Strong Vibes Connect" mates that boss:

    * a matching rhombus POCKET keys the parts (no rotation, single orientation),
    * the male's flare SHOULDER seats flat on the socket face (axial stop),
    * a 1/4"-20 SCREW through the socket threads >= EFF_THREAD into the boss and
      clamps the joint -> rigid + keyed.

TWO SEPARATE PARTS (print both, assemble with one 1/4"-20 x >=10 mm screw):
    strong_vibes_socket()  -> FEMALE: keyed diamond pocket (2 mm) over a PLATE_T
                              (3 mm) solid clamp the screw grabs on -> 5 mm total,
                              plus a screw clearance bore.
    strong_vibes_boss()    -> MALE  : a test stand-in for the holder boss: the
                              diamond (band + flare) on a base, with a modelled
                              1/4"-20 internal thread, EFF_THREAD (>=7 mm) deep.

OTHER AGENTS can also just import the primitives:
    vibes_pocket_cutter()  -> negative to subtract into your own material
    vibes_diamond(grow)    -> the raw rhombus profile
    MATE                   -> dict of every interface number to assert against

ORIENTATION CONTRACT (each part built in its own frame):
    SOCKET: mating face = plane Z=0; diamond plugs in along -Z (band fills
            Z in [0,-BAND_DEPTH]); screw axis = Z; LONG axis +Y, SHORT axis +X.
    BOSS  : base on the bed at Z=0, diamond face up at the top; thread down the Z
            axis from the face. (Flip 180 deg about X to seat it in the socket.)

The diamond is keyed (long != short) so it seats in ONE orientation (mod 180 deg).
============================================================
"""
from math import sin, pi, radians, sqrt
from build123d import *
from bd_warehouse.thread import IsoThread

try:
    from ocp_vscode import show
except Exception:
    show = None


# Version of the MATING STANDARD itself. Bump (MAJOR) whenever DIA_A / DIA_B /
# BAND_DEPTH or the thread spec change -- every part inherits this, so a change
# here is a repo-wide interface event (see AGENTS.md).
STANDARD_VERSION = "1.0.0"

# ============================================================
#  MALE INTERFACE  (what we mate to)  -  current holder values
# ============================================================
# holder: boss_d=16, boss_diamond=0.8, quilt_n=16, quilt_dz=15, r_out_t=26.176
DIA_A      = 11.322   # LONG  half-diagonal of the diamond  [mm]   (full 22.64)
DIA_B      = 7.759    # SHORT half-diagonal of the diamond  [mm]   (full 15.52)
BAND_DEPTH = 2.0      # constant-section depth of the band the socket grips [mm]

# ---- thread + plate spec ----
PLATE_T      = 3.0    # FEMALE solid clamp BELOW the pocket the camera screw grabs on
                      # (total female plate = BAND_DEPTH + PLATE_T) [mm]
EFF_THREAD   = 7.0    # MIN effective 1/4"-20 thread depth in the male boss [mm]
THREAD_MAJOR = 6.35   # 1/4"-20 major diameter [mm]
THREAD_PITCH = 1.27   # 1/4"-20 pitch [mm]
BOLT_CLEAR   = 7.0    # screw shank clearance hole in the female [mm]

# ---- thread ENTRY / lead-in (so a steel 1/4-20 actually STARTS and THREADS in a print) ----
LEAD_IN_D     = 9.0   # countersink mouth dia at the face -> the screw drops in + self-centres [mm]
LEAD_IN_DEPTH = 1.0   # countersink (funnel) depth [mm]
THREAD_CLEAR  = 0.6   # diametral clearance on the MODELLED internal thread so a steel 1/4-20
                      # threads into the FDM print (0 = nominal/tight, usually too tight) [mm]
SELFTAP_D     = 5.3   # plain hole the steel screw SELF-TAPS into when USE_THREAD=False [mm]

# ---- fit (TPU / FDM) ----
CLEAR      = 0.20     # added to each rhombus half-diagonal: 0.12 tight grip .. 0.35 loose
MOUTH_LEAD = 0.8      # funnel chamfer at the socket mouth so the diamond self-finds [mm]

# ---- workflow ----
USE_THREAD    = True  # model the 1/4"-20 IsoThread (False = plain hole, fast preview)
FEMALE_THREAD = True  # thread the FEMALE bore too (1/4-20) so the camera screw threads in and STAYS
                      # CAPTIVE; False = plain BOLT_CLEAR clearance bore (screw passes straight through)
EXPORT     = True    # False = preview only; True = also write .step / .stl / .3mf

# one-stop interface summary another agent can read/assert against
MATE = {
    "shape": "rhombus (diamond) prism band",
    "half_long_DIA_A_mm": DIA_A, "half_short_DIA_B_mm": DIA_B,
    "full_long_mm": 2 * DIA_A, "full_short_mm": 2 * DIA_B,
    "band_depth_mm": BAND_DEPTH, "screw_axis": "Z",
    "thread": "1/4-20 screw (major 6.35, pitch 1.27); boss has a countersink lead-in + "
              "internal thread loosened +THREAD_CLEAR for FDM (or a self-tap hole if USE_THREAD=False). "
              "FEMALE_THREAD also taps the socket clamp so the screw stays captive (else BOLT_CLEAR bore)",
    "min_effective_thread_mm": EFF_THREAD, "clamp_thickness_mm": PLATE_T,
    "total_female_plate_mm": BAND_DEPTH + PLATE_T,
    "keyed": "long != short -> single orientation (mod 180 deg)",
    "seat": "male flare shoulder seats on socket face at Z=0",
}


def vibes_dims(boss_d=16.0, boss_diamond=0.8, quilt_n=16, quilt_dz=15.0,
               r_out_t=26.176):
    """Recompute (DIA_A, DIA_B) from holder parameters if they change.
    r_out_t = holder OUTER radius at the boss height (r_out(thread_z))."""
    q_aspect = quilt_dz / (r_out_t * radians(360 / quilt_n))
    dia_r = (boss_d / 2) * boss_diamond
    dia_a = dia_r * sqrt(q_aspect ** 2 + 1)
    return dia_a, dia_a / q_aspect


def vibes_diamond(grow=0.0, half_long=DIA_A, half_short=DIA_B):
    """The mating rhombus as a 2D face in the XY plane: SHORT axis on X, LONG on
    Y. `grow` enlarges every half-diagonal (CLEAR for a socket; 0 for the nominal
    male). Matches the holder's diamond_face() convention exactly."""
    return Polygon((half_short + grow, 0), (0, half_long + grow),
                   (-half_short - grow, 0), (0, -half_long - grow), align=None)


# ============================================================
#  FEMALE  -  pocket cutter (subtract into your own material)
# ============================================================
def vibes_pocket_cutter(clear=CLEAR, lead_in=MOUTH_LEAD, depth=BAND_DEPTH,
                        thru_screw=True):
    """Tool volume to SUBTRACT so a holder diamond plugs in. Mating face = Z=0,
    pocket opens toward +Z, floor at Z=-depth, funnel mouth, breaks the surface
    (+0.6) for a clean cut. thru_screw -> also a BOLT_CLEAR bore down the axis."""
    cut = extrude(Plane.XY * vibes_diamond(grow=clear), amount=-depth)         # straight pocket
    cut += loft([Plane((0, 0, 0.6)) * vibes_diamond(grow=clear + lead_in),     # funnel mouth
                 Plane((0, 0, -lead_in)) * vibes_diamond(grow=clear)], ruled=True)
    if thru_screw:
        cut += Pos(0, 0, 0.6) * Cylinder(BOLT_CLEAR / 2, depth + 60,
                                         align=(Align.CENTER, Align.CENTER, Align.MAX))
    return cut


def vibes_pocket_cutter_star(clear=CLEAR, lead_in=MOUTH_LEAD, depth=BAND_DEPTH,
                             step_deg=30, thru_screw=True):
    """STAR pocket cutter: the diamond pocket UNIONED at every `step_deg` around the
    screw axis, so the holder boss plugs in at any step_deg rotation -> STEPWISE
    mounting (rotate the device in step_deg increments). The rhombus is symmetric mod
    180 deg, so the lobes repeat every 180; step_deg=30 -> a 12-point star (mount every
    30 deg). step_deg=180 -> a single diamond == vibes_pocket_cutter (keyed, one way)."""
    one = vibes_pocket_cutter(clear=clear, lead_in=lead_in, depth=depth, thru_screw=False)
    cut = one
    a = step_deg
    while a < 180:                                 # rhombus repeats every 180 deg
        cut += Rot(0, 0, a) * one
        a += step_deg
    if thru_screw:
        cut += Pos(0, 0, 0.6) * Cylinder(BOLT_CLEAR / 2, depth + 60,
                                         align=(Align.CENTER, Align.CENTER, Align.MAX))
    return cut


# ============================================================
#  FEMALE  -  captive screw thread (subtract the cutter, fuse the thread)
# ============================================================
def vibes_female_screw(total_t, use_thread=USE_THREAD):
    """Captive 1/4"-20 screw feature for a female socket, in the socket frame (mating
    face Z=0, body in Z<0, BOTTOM face at Z=-total_t). The camera screw enters from the
    BOTTOM and threads in so it STAYS captive. Returns (cutter, thread):
        cutter -- SUBTRACT: the axial screw hole + a countersink lead-in funnel at the
                  BOTTOM face so the screw self-centres entering from below.
        thread -- FUSE (or None): the 1/4-20 internal thread filling the clamp below the
                  pocket (loosened +THREAD_CLEAR for FDM). use_thread=False -> thread=None
                  and the hole is a plain SELFTAP_D bore the steel screw self-taps into.
    The thread sits in the clamp (Z in [-total_t, -BAND_DEPTH]); a thin clamp -> short
    engagement, so the clamp (PLATE_T) is what sets how many turns the screw grabs."""
    C = Align.CENTER
    z_bot = -total_t
    hole_d = (THREAD_MAJOR + THREAD_CLEAR - 0.35) if use_thread else SELFTAP_D
    cutter = Pos(0, 0, 0.6) * Cylinder(hole_d / 2, total_t + 60.6, align=(C, C, Align.MAX))
    cutter += Pos(0, 0, z_bot) * Cone(LEAD_IN_D / 2, hole_d / 2, LEAD_IN_DEPTH,
                                      align=(C, C, Align.MIN))     # funnel: wide at the bottom face
    thread = None
    if use_thread:
        L = (total_t - BAND_DEPTH) - LEAD_IN_DEPTH - 0.4          # fill the clamp, clear of funnel + floor
        if L > 0:
            th = IsoThread(major_diameter=THREAD_MAJOR + THREAD_CLEAR, pitch=THREAD_PITCH,
                           length=L, external=False, end_finishes=("square", "fade"))
            thread = th.located(Pos(0, 0, z_bot + LEAD_IN_DEPTH + 0.2))
    return cutter, thread


# ============================================================
#  FEMALE  -  ready socket plate (PART 1)
# ============================================================
def strong_vibes_socket(clamp_t=PLATE_T, wall_pad=6.0, threaded=FEMALE_THREAD,
                        step_deg=180):
    """FEMALE part: the keyed diamond pocket (BAND_DEPTH deep) sits OVER a solid
    clamp `clamp_t` thick that the camera screw grabs on -> total plate =
    BAND_DEPTH + clamp_t. Mating face on Z=0, body in Z<0; the screw enters from
    the back (bottom). threaded=True -> the bore is a captive 1/4-20 thread in the
    clamp so the screw STAYS in place; threaded=False -> a plain BOLT_CLEAR bore.
    step_deg=180 -> single keyed diamond (one orientation); step_deg=30 -> a STAR
    pocket that accepts the boss every 30 deg (stepwise rotational mounting)."""
    total_t = BAND_DEPTH + clamp_t                              # pocket + solid clamp
    reach_x = DIA_A if step_deg < 180 else DIA_B                # star sweeps DIA_A in every dir
    w = 2 * (reach_x + CLEAR + wall_pad)
    h = 2 * (DIA_A + CLEAR + wall_pad)
    plate = Pos(0, 0, -total_t / 2) * Box(w, h, total_t)        # face on Z=0
    sock = plate - vibes_pocket_cutter_star(step_deg=step_deg, thru_screw=not threaded)
    thread = None
    if threaded:                                                # captive screw thread in the clamp
        cutter, thread = vibes_female_screw(total_t)
        sock -= cutter
    try:                                                        # ease the outer edges (before the thread)
        sock = sock.fillet(1.2, sock.edges().filter_by(Axis.Z))
    except Exception:
        pass
    if thread is not None:
        sock = sock.fuse(thread)
    return sock


def strong_vibes_socket_180(**kw):
    """Keyed socket: accepts the boss in ONE orientation (mod 180 deg). The default."""
    return strong_vibes_socket(step_deg=180, **kw)


def strong_vibes_socket_30(**kw):
    """STAR socket: accepts the boss every 30 deg for stepwise rotational mounting."""
    return strong_vibes_socket(step_deg=30, **kw)


# ============================================================
#  MALE  -  test boss with a real 1/4"-20 thread (PART 2)
# ============================================================
def strong_vibes_boss(base_d=30.0, base_t=6.0, flare_h=4.0, use_thread=USE_THREAD):
    """MALE part: a bench stand-in for the holder boss. A round base carries the
    diamond (flare + BAND_DEPTH band). A countersink LEAD-IN funnel at the face
    lets the screw self-centre; below it a 1/4"-20 internal thread (loosened
    +THREAD_CLEAR for FDM) runs EFF_THREAD deep -- or set use_thread=False for a
    plain SELF-TAP hole. Built base-down, face up (print-ready). Seats into
    strong_vibes_socket() flipped 180 deg about X."""
    face_z = base_t + flare_h + BAND_DEPTH
    flare_base_r = DIA_A + 3.0

    boss = Cylinder(base_d / 2, base_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
    boss += loft([Plane((0, 0, base_t)) * Circle(flare_base_r),               # flare onto base
                  Plane((0, 0, base_t + flare_h)) * vibes_diamond()], ruled=True)
    boss += extrude(Plane((0, 0, base_t + flare_h)) * vibes_diamond(),        # constant band
                    amount=BAND_DEPTH)
    # hole down the axis, through the part (prints cleanly, screw can exit). For a
    # modelled thread, size it just under the (loosened) major so the thread bites;
    # for self-tap, an undersized bore the steel screw cuts its own thread into.
    hole_d = (THREAD_MAJOR + THREAD_CLEAR - 0.35) if use_thread else SELFTAP_D
    boss -= Pos(0, 0, face_z + 0.01) * Cylinder(
        hole_d / 2, face_z + 0.02, align=(Align.CENTER, Align.CENTER, Align.MAX))
    # countersink LEAD-IN funnel at the mouth: the screw drops in and self-centres
    boss -= Pos(0, 0, face_z) * Cone(
        hole_d / 2, LEAD_IN_D / 2, LEAD_IN_DEPTH,
        align=(Align.CENTER, Align.CENTER, Align.MAX))
    if use_thread:                                # 1/4-20 loosened for FDM, started below the funnel
        th = IsoThread(major_diameter=THREAD_MAJOR + THREAD_CLEAR, pitch=THREAD_PITCH,
                       length=EFF_THREAD, external=False, end_finishes=("fade", "square"))
        thread_top = face_z - LEAD_IN_DEPTH - 0.2
        boss = boss.fuse(th.located(Pos(0, 0, thread_top - EFF_THREAD)))
    boss.label = "test_boss"
    return boss, face_z


# ============================================================
#  DEMO / PREVIEW / EXPORT  (runs only when executed directly, so importing
#  this module is cheap -- other parts use the builders/constants above)
# ============================================================
if __name__ == "__main__":
    socket = strong_vibes_socket()
    boss, _face_z = strong_vibes_boss()
    socket.color = Color(0, 0, 0)               # render the FEMALE part black in the viewer

    print("STRONG VIBES CONNECT — interface:", MATE)
    sb = socket.bounding_box()
    print(f"socket(female) valid={socket.is_valid}  vol={socket.volume/1000:.2f}cm3  "
          f"clamp={PLATE_T}mm total={BAND_DEPTH+PLATE_T:.0f}mm  "
          f"bbox {sb.size.X:.1f}x{sb.size.Y:.1f}x{sb.size.Z:.1f}mm")
    bb = boss.bounding_box()
    print(f"boss(male)     valid={boss.is_valid}  vol={boss.volume/1000:.2f}cm3  "
          f"thread={EFF_THREAD}mm  bbox {bb.size.X:.1f}x{bb.size.Y:.1f}x{bb.size.Z:.1f}mm")

    # fit check: the pocket must fully accept the nominal diamond band
    _band = extrude(Plane.XY * vibes_diamond(), amount=-BAND_DEPTH)
    _spill = (_band - vibes_pocket_cutter()).volume
    print(f"fit: band outside pocket = {_spill:.4f} mm^3 (0 -> accepts) | "
          f"clearance {CLEAR:.2f}mm/half-diag | screw 1/4-20 x >= {PLATE_T+EFF_THREAD:.0f}mm")

    if show is not None:
        try:
            show(socket, Pos(45, 0, 0) * boss,
                 names=["socket_female", "test_boss_male"])
        except Exception as e:
            print(f"(viewer off: {e})")

    if not EXPORT:
        print("Preview only (set EXPORT = True to write .step / .stl / .3mf)")
    else:
        for part, name in ((socket, "strong_vibes_socket"), (boss, "strong_vibes_boss")):
            export_step(part, f"{name}.step")
            export_stl(part, f"{name}.stl", tolerance=0.05, angular_tolerance=0.3)
            done = [".step", ".stl"]
            try:                                       # 3mf best-effort (thread mesh can be rejected)
                m = Mesher()
                m.add_shape(part, linear_deflection=0.05, angular_deflection=0.5)
                m.write(f"{name}_b123d.3mf")
                done.append(".3mf")
            except RuntimeError as e:
                print(f"  {name}: skipped .3mf ({e})")
            print(f"Exported {name}:", "  ".join(done))
