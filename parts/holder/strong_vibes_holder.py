"""
============================================================
Strong Vibes snap-fit holder v2  -  build123d version
z = 0 at bottom of holder, device top edge at z = H
Print: Bambu TPU for AMS (68D) or PLA Tough
Requires:  pip install build123d bd_warehouse
Run:       python3 strong_vibes_holder.py
Exports:   .step  .stl  .3mf
============================================================
"""

from math import sin, cos, pi, radians, sqrt, hypot
from build123d import *
from bd_warehouse.thread import IsoThread
from ocp_vscode import show
from strongvibes import DIA_A, DIA_B, BAND_DEPTH, build_path   # the LOCKED mating standard (single source of truth)

__version__ = "2.0.0"     # bump per AGENTS.md on any geometry change
VARIANT = "strong_vibes_holder"     # the male Strong Vibes Connect device holder

# ---------- Device (measured) ----------
d_top   = 48.8    # diameter at top edge (device top) [mm]
d_bot   = 46.5    # diameter at the taper junction / original bottom [mm]
d_end   = 46    # diameter at the new extended bottom end [mm]
dev_len = 70      # length of the original piece, kept exactly as-is [mm]
ext_len = 10      # added tapered extension at the bottom [mm]
H       = dev_len + ext_len   # total holder length [mm]

# ---------- Holder ----------
wall      = 3     # wall thickness [mm]
lip_w     = 3     # lip overhang inward over the top edge [mm]
lip_h     = 3     # lip height above the top edge [mm]
squeeze   = -1    # inner diameter reduction at mid-height (grip) [mm]
waist     = 1.5   # outer diameter reduction at mid-height (visual) [mm]
opening_w = 35    # snap opening width at the inner surface [mm]
flare     = 4     # lead-in flare per side at the outer surface [mm]
ring_h    = 5     # solid closed ring at the bottom (no opening below this) [mm]
round_up  = 45     # opening bottom-corner blend height [mm]
round_out = 17    # opening bottom-corner blend width  [mm]  (asymmetric corner)
opening_round = 0  # roundness on the long side edges of the cutout [mm]
opening_steps = 60 # loft sections for the rounded bottom corner (higher = smoother)

# ---------- thumb grip wings beside the opening (top) ----------
GRIP       = True   # add the two thumb tabs at the top of the opening
wing_from_top = 0   # grip top edge, measured down from the very top [mm]
wing_len   = 15     # how far down from the top the grip extends [mm]
wing_out   = 6     # how far it sticks out, along the flare angle [mm]
wing_thick = 3    # tab thickness [mm]
wing_inset = 12      # overlap into the wall for a clean fuse [mm]
wing_round = 1    # edge rounding on the tab [mm]

# ---------- Edge rounding ----------
r_lip    = 1      # lip top edges
r_base   = 2      # bottom rim, outside
r_basein = 1      # bottom rim, inside
r_fillet = 1    # lip / inner-wall junction

# ---------- Contact bumps ----------
bump_r       = 0
bump_angles  = [60, 120, 180, 240, 300]   # 0 deg = middle of opening
bump_heights = [15, 60]

# ---------- 1/4"-20 camera thread boss (anti-rotation diamond head) ----------
use_thread   = True   # False = plain 5.8 mm hole, self-tap a steel bolt
thread_depth = 8
THREAD_CLEAR = 0.6    # diametral clearance on the modelled 1/4-20 thread for FDM: 0 = nominal/tight
                      # (cracks the print), raise to loosen. Matches strong_vibes_connect THREAD_CLEAR.
boss_d       = 16     # reference size used only to window the boss/wall fillet-edge search [mm]
boss_aspect  = 1.5    # taller BOSS via the FLARE only: axial/Z stretch of the structural buttress
                      # BEHIND the diamond. 1.0 = round flare; >1 = taller. The mating diamond stays
                      # the Strong Vibes Connect STANDARD (DIA_A/DIA_B), so the connection NEVER changes.
boss_fillet  = 10      # blend radius where the boss meets the wall (smooth all around)
boss_len     = 7      # protrusion beyond outer wall
thread_from_top = 30  # camera-thread centre, measured down from the top [mm]
boss_flare   = 7      # how much the boss widens past the diamond onto the body (no neck) [mm]
boss_face_round = 0.6 # tiny lead-in round on the flat-face diamond rim [mm]

# ---------- outer-surface diamond quilt (recessed pyramids) ----------
QUILT        = True   # texture toggle (set False for faster previews of other edits)
quilt_n      = 16     # diamonds around the full circle -> cell width (smaller = bigger)
quilt_dz     = 15     # axial diagonal of each diamond [mm] (larger = taller/elongated)
quilt_z0, quilt_z1 = 10, 62   # axial band covered [mm]
quilt_depth  = 1.3    # how far the centre (5th point) is pulled inward [mm]
quilt_ridge  = 0.9    # cell fill: 1.0 = sharp shared edges, <1 = thin flat ridges
quilt_over   = 0.5    # tool overshoot past the surface for a clean cut [mm]
quilt_open_skip = 46  # skip +/- deg around the snap opening (0 deg)
quilt_boss_skip = 34  # skip +/- deg around the camera boss (180 deg)

# ---------- workflow ----------
EXPORT = True        # False = preview only (fast iteration); True = also write files


# ---------- derived ----------
def base_dia(z):
    # original taper above the junction (kept exactly as before), plus a steeper
    # taper on the added bottom section, narrowing down to d_end.
    if z >= ext_len:
        return d_bot + (d_top - d_bot) * (z - ext_len) / dev_len
    return d_end + (d_bot - d_end) * z / ext_len

def pinch(z):
    # squeeze/waist grip sinusoid, anchored to the original device region only
    return sin(pi * (z - ext_len) / dev_len) if z >= ext_len else 0.0

def r_in(z):
    return base_dia(z) / 2 - (squeeze / 2) * pinch(z)

def r_out(z):
    return base_dia(z) / 2 + wall - (waist / 2) * pinch(z)

thread_z = H - thread_from_top      # camera-thread centre height [mm]
r_out_t = r_out(thread_z)           # outer radius at the boss
N = 64
inner_pts = [(r_in(H * i / N), H * i / N) for i in range(N + 1)]
outer_pts = [(r_out(H * (N - i) / N), H * (N - i) / N) for i in range(N + 1)]

# ---------- diamond boss cross-section = the LOCKED Strong Vibes Connect standard ----------
# The mating rhombus is NOT computed here -- it is IMPORTED from strong_vibes_connect.py
# (DIA_A, DIA_B, BAND_DEPTH), the single source of truth. So no holder parameter can ever
# change the connection: the boss always plugs into any standard socket. The pair
# (dia_a, dia_b), the face plane at tip_x, and BAND_DEPTH are the whole spec the female
# socket needs: it is just diamond_face(clear) cut BAND_DEPTH deep. (boss_aspect stretches
# only the structural flare BEHIND this band -- see below -- never the band itself.)
dia_a, dia_b = DIA_A, DIA_B                       # axial (Z) / tangential (Y) half-diagonals [mm]  -- STANDARD
dia_r = DIA_A * DIA_B / sqrt(DIA_A ** 2 + DIA_B ** 2)   # rhombus inscribed circle = boss core radius [mm]

def diamond_face(grow=0.0):
    """Boss rhombus as a sketch in a plane's local XY (local x = tangential / part Y,
    local y = axial / part Z). `grow` enlarges every half-diagonal -- pass a small
    positive value as the clearance when reusing this to cut the equal female part."""
    return Polygon((dia_b + grow, 0), (0, dia_a + grow),
                   (-dia_b - grow, 0), (0, -dia_a - grow), align=None)

# Diamond head solids, built in algebra mode here (outside the builder, like the
# opening tool) and added to the part below. A plane whose local x = part Y and
# local y = part Z, placed along the boss axis (part X); the face is at tip_x.
tip_x = -(r_out_t + boss_len)                        # flat screw face / diamond face plane [mm]
def _boss_plane(x):
    return Plane(origin=(x, 0, thread_z), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
# Band + flare are sampled as fixed-vertex superellipse rings so the diamond->round
# morph has MATCHED point counts at every section. A direct 4-edge-diamond -> circle
# loft warps 4 big "sail" faces that pinch a triangular notch where two sails meet at
# each sharp corner (the artifacts at the top/bottom of the head). Re-sampling every
# section as the same _NS-gon and relaxing the corner exponent 1 (diamond) -> 2
# (circle) removes the pinch and gives a smooth organic shoulder onto the body.
# _NS divisible by 4 lands a vertex on each diamond corner, so the band stays exact.
_NS = 72
def _ring(A, B, n):                              # superellipse |x/A|^n + |y/B|^n = 1
    pts = []
    for _i in range(_NS):
        _t = 2 * pi * _i / _NS
        _c, _s = cos(_t), sin(_t)
        _r = 1.0 / ((abs(_c) / A) ** n + (abs(_s) / B) ** n) ** (1.0 / n)
        pts.append((_r * _c, _r * _s))
    return Polygon(*pts, align=None)

# The band is the exact 4-point diamond (clean 4-edge face -> takes the lead-in
# fillet); the flare's first ring _ring(dia_b, dia_a, 1) is the same outline sampled
# as an _NS-gon, so the two fuse cleanly. The female socket reuses diamond_face(clear).
diamond_band = extrude(_boss_plane(tip_x) * diamond_face(), amount=BAND_DEPTH)  # standard pure-diamond band

_flare_Rh = dia_r + boss_flare                                  # flare base half-WIDTH (Y) at the body
_flare_Rv = _flare_Rh * boss_aspect                             # flare base half-HEIGHT (Z): >1 = taller buttress
_flare_embed = r_out_t - sqrt(max(r_out_t ** 2 - _flare_Rh ** 2, 0.0)) + 0.5  # width sets the radial reach
_Mf, _x0, _x1 = 12, tip_x + BAND_DEPTH, -r_out_t + _flare_embed
_fsec = []
for _j in range(_Mf + 1):
    _ss = _j / _Mf                                              # 0 at the band, 1 at the body
    _A = (1 - _ss) * dia_b + _ss * _flare_Rh                    # width:  diamond -> round
    _B = (1 - _ss) * dia_a + _ss * _flare_Rv                    # height: diamond -> (taller) ellipse
    _fsec.append(_boss_plane(_x0 + (_x1 - _x0) * _ss) * _ring(_A, _B, 1 + _ss))  # corner 1 -> 2
diamond_flare = loft(_fsec)                                     # smooth diamond -> body shoulder

# ---------- inner-bore solid (used to clip the boss and the grip wings) ----------
# A solid of revolution filling the inside (incl. the lip overhang). Subtracting
# it keeps the bore clear, so the boss/wings can penetrate deeply for a clean,
# wall-thickness-independent fuse without ever protruding on the inside diameter.
with BuildPart() as _bore:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline((0, 0), (r_in(0), 0))
            Spline(*inner_pts)
            Polyline(inner_pts[-1], (d_top / 2 - lip_w, H),
                     (d_top / 2 - lip_w, H + lip_h), (0, H + lip_h), (0, 0))
        make_face()
    revolve(axis=Axis.Z)
bore = _bore.part

# ---------- snap-opening cut tool (built in algebra mode, subtracted below) ----------
# Lead-in flare + asymmetric rounded bottom corners: a closed ring stays below
# z = ring_h, and the two bottom corners are blended with an elliptical sweep
# (round_up mm tall x round_out mm wide) instead of being sharp. Built by lofting
# (ruled) the flared cross-section through widths that grow from
# (opening_w - 2*round_out) at the ring up to opening_w over round_up mm.
_x_f = r_in(H / 2) - 1
_x_o = r_out(H) + boss_len + 10

def _open_section(z, w):                    # flared slot cross-section at height z
    hw = w / 2
    return Plane.XY.offset(z) * Polygon(
        (-1, -hw), (_x_f, -hw), (_x_o, -hw - flare), (_x_o, hw + flare),
        (_x_f, hw), (-1, hw), align=None)

_osec, _M = [], opening_steps
for _k in range(_M + 1):                    # elliptical corner over the bottom round_up mm
    _z = ring_h + round_up * _k / _M
    _fr = (_z - (ring_h + round_up)) / round_up
    _osec.append(_open_section(_z, opening_w - 2 * round_out * (1 - sqrt(max(0.0, 1 - _fr * _fr)))))
_osec.append(_open_section(H + lip_h + 2, opening_w))   # straight up past the lip
opening_tool = loft(_osec, ruled=True)

with BuildPart() as holder:

    # ----- revolved body: inner pinch, lip, outer waist -----
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Spline(*inner_pts)                                  # inner wall, up
            Polyline(
                inner_pts[-1],
                (d_top / 2 - lip_w, H),                         # lip underside
                (d_top / 2 - lip_w, H + lip_h),                 # lip inner top
                (d_top / 2 + wall,  H + lip_h),                 # lip outer top
                outer_pts[0],                                   # lip outer face
            )
            Spline(*outer_pts)                                  # outer wall, down
            Line(outer_pts[-1], inner_pts[0])                   # bottom rim
        make_face()
    revolve(axis=Axis.Z)

    # ----- fillets on the revolved body (full circles = clean) -----
    circles = holder.edges().filter_by(GeomType.CIRCLE)
    fillet(circles.group_by(Axis.Z)[-1], r_lip)                 # lip top edges

    bottom = (holder.edges().filter_by(GeomType.CIRCLE)
              .group_by(Axis.Z)[0].sort_by(SortBy.RADIUS))
    fillet(bottom[0], r_basein)                                 # foot, inside
    fillet(bottom[-1], r_base)                                  # foot, outside

    lip_junction = [e for e in holder.edges().filter_by(GeomType.CIRCLE)
                    if abs(e.arc_center.Z - H) < 1e-6]
    fillet(lip_junction, r_fillet)                              # lip / inner wall

    # ----- diamond thread boss (at 180 deg, opposite the opening) -----
    # A round core cylinder, fillet-welded into the curved wall so the wall
    # transition stays smooth ALL the way around, then capped by a diamond head
    # (below) for anti-rotation. The core penetrates to the bore, so the weld is
    # clean regardless of wall thickness; the diamond is added outboard of it.
    tip_x = -(r_out_t + boss_len)                            # flat screw face (= diamond face)
    boss_base_x = -(r_in(thread_z) - 5)                      # deep base, inside the bore
    with Locations(Pos(boss_base_x, 0, thread_z) * Rot(0, -90, 0)):
        # radius kept 1 mm INSIDE the diamond's inscribed circle (= dia_r): a core
        # exactly on it sits tangent to the 4 diamond faces and splinters the face
        # rim, which then refuses the lead-in fillet. The flare hides the core anyway.
        Cylinder(radius=dia_r - 1, height=boss_base_x - tip_x,
                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    add(bore, mode=Mode.SUBTRACT)                            # keep the bore clear

    # Smooth fillet weld around the boss/outer-wall junction curve. The boss
    # penetrates to the bore (above), so this works regardless of wall thickness;
    # a very thin wall that can't take boss_fillet falls back to a smaller radius.
    boss_junction = [e for e in holder.edges()
                     if -(r_out_t + 1) < e.center().X < -(r_out_t - 4)
                     and e.length > 3 and abs(e.center().Z - thread_z) < boss_d]
    for _r in (boss_fillet, boss_fillet * 0.6, boss_fillet * 0.3, 1.0, 0.5):
        if _r <= 0:
            continue
        try:
            fillet(boss_junction, _r)
            if _r < boss_fillet:
                print(f"  (boss_fillet reduced to {_r:.1f} mm — wall too thin for {boss_fillet})")
            break
        except Exception:
            continue

    # NOTE: the diamond head (band + flare) and the screw hole are fused/cut AFTER
    # the builder closes (see below). The diamond->round flare loft mis-fuses
    # through the builder and collapses the whole part, exactly like the thread.

    # ----- snap opening (tool built above in algebra mode) -----
    add(opening_tool, mode=Mode.SUBTRACT)
    # Soften the long side edges of the cutout (inner + outer, both sides).
    # Skipped for opening_round <= 0; a tall bottom-corner blend (large round_up)
    # makes these edges too curved for OCCT to fillet, so we fail gracefully.
    if opening_round > 0:
        _op_edges = [e for e in holder.edges() if e.center().X > 6 and e.length > 30]
        try:
            fillet(_op_edges, opening_round)
        except Exception:
            print(f"  (opening edges won't take a {opening_round} mm fillet at "
                  f"round_up={round_up}; reduce round_up or opening_round)")

    # ----- contact bumps -----
    # Embed each bump slightly INTO the wall (and grow its radius to match) so it
    # fuses cleanly. A sphere centered exactly on the curved inner wall fuses
    # tangentially and leaves an invalid (non-manifold) solid; the protrusion into
    # the cavity stays bump_r (= 1 mm).
    bump_embed = 0.4
    for a in bump_angles:
        for z in bump_heights:
            with Locations(Rot(0, 0, a) * Pos(r_in(z) + bump_embed, 0, z)):
                Sphere(bump_r + bump_embed)

part = holder.part

# ----- diamond head, fused OUTSIDE the builder (the builder mis-fuses the
# diamond->round flare loft and collapses the part, like the thread below).
# Order matters: fuse the diamond first, THEN drill the screw hole, so the solid
# band can't plug the outer 2 mm of the bore. -----
part = part.fuse(diamond_band, diamond_flare)
# The flare base sinks into the wall and (with a big boss_flare) can reach past the
# inner wall; re-clip with the bore so it is trimmed flush and never protrudes inside.
# With a thin wall at the boss, the bore cut can SHEAR the flare's inboard tip into a
# free fragment floating in the cavity (OCCT splits the result -> a multi-solid). That
# fragment IS the unwanted inside protrusion, so keep only the main body solid.
part = part - bore
_solids = part.solids()
if len(_solids) > 1:
    part = max(_solids, key=lambda s: s.volume)
    print(f"  (bore re-clip dropped {len(_solids) - 1} inside fragment(s) — flare poked past the wall)")

# tiny lead-in round on the flat-face diamond rim (eases the socket start; crash-proof)
if boss_face_round > 0:
    _rim = (part.edges().filter_by(GeomType.LINE)
            .filter_by(lambda e: abs(e.center().X - tip_x) < 1e-3))
    try:
        part = part.fillet(boss_face_round, _rim)
    except Exception:
        print(f"  (diamond face lead-in {boss_face_round} mm skipped)")

# ----- 1/4"-20 camera thread: clearance / tap-drill hole through the diamond face -----
# Drill a touch under the 6.35 major dia so the internal thread bites into solid
# material (an exact-major hole leaves coincident faces -> invalid solid).
hole_d = (6.35 + THREAD_CLEAR - 0.35) if use_thread else 5.8   # 1/4-20: FDM clearance vs steel self-tap
part = part - (Pos(tip_x + thread_depth / 2 - 0.01, 0, thread_z) * Rot(0, 90, 0)
               * Cylinder(radius=hole_d / 2, height=thread_depth + 0.02))

# Fuse the camera thread here, OUTSIDE the builder, so it doesn't collapse the
# part (the builder mis-fuses this multi-solid IsoThread). See note above.
if use_thread:
    thread = IsoThread(major_diameter=6.35 + THREAD_CLEAR, pitch=1.27, length=thread_depth,
                       external=False, end_finishes=("square", "square"))
    part = part.fuse(thread.located(Pos(tip_x, 0, thread_z) * Rot(0, 90, 0)))

# ----- thumb grip wings on each side of the opening (for easy removal) -----
# Two tabs at the top edge of the opening, protruding outward along the flare
# angle and tapering downward; press them to spread the slit so the lip releases
# and the holder glides off. Built in algebra mode and fused.
if GRIP:
    # (reuses the shared `bore` solid built near the top) each wing is clipped
    # against it so the grip can never protrude on the inside diameter.
    def _wing(s):
        L = hypot(_x_o - _x_f, flare)
        ux, uy = (_x_o - _x_f) / L, s * flare / L      # outward flare direction (xy)
        ye = opening_w / 2
        wing_top_z = H + lip_h - wing_from_top         # top edge of the grip
        xe = sqrt(max(r_out(wing_top_z) ** 2 - ye ** 2, 1.0))   # opening edge on the surface
        pl = Plane(origin=(xe, s * ye, wing_top_z - wing_len),
                   x_dir=(ux, uy, 0), z_dir=(uy, -ux, 0))
        # profile (upside-down): the protruding ledge is at the BOTTOM so the
        # thumb presses down on it; it tapers up the curved (spline) long edge.
        with BuildSketch(pl) as sk:
            with BuildLine():
                Polyline((-wing_inset, wing_len), (-wing_inset, 0), (wing_out, 0))
                Spline((wing_out, 0), (-wing_inset, wing_len), tangents=[(0, 1), (-1, 0)])
            make_face()
        tab = extrude(sk.sketch, amount=wing_thick / 2, both=True)
        tab = tab.fillet(wing_round, tab.edges())
        return tab.cut(bore)                           # never enter the bore
    part = part.fuse(_wing(1), _wing(-1))

# ----- elongated-diamond quilt on the outer surface -----
# Tessellate the wall into diamonds, each a shallow 4-sided pyramid whose centre
# (the 5th point) is pulled inward -> a quilted 3D pattern. Rows are offset by half
# a cell so diamonds meet edge-to-edge; all pockets are removed in ONE cut.
# Diamonds over the snap opening / boss are skipped (no wall there).
if QUILT:
    Dth = 360 / quilt_n                                  # angular diagonal per cell

    def _pocket(R):
        wc = R * radians(Dth / 2) * quilt_ridge          # half circumferential diagonal
        hz = (quilt_dz / 2) * quilt_ridge                # half axial diagonal
        face = Pos(0, 0, quilt_over) * Polygon((-wc, 0), (0, hz), (wc, 0), (0, -hz),
                                               align=None)
        return loft([face, Vertex(0, 0, -quilt_depth)])  # diamond -> recessed apex

    pockets = []
    row, zc = 0, quilt_z0
    while zc <= quilt_z1:
        R = r_out(zc)
        pk = _pocket(R)
        ang_off = Dth / 2 if row % 2 else 0              # interleave -> edge-to-edge tiling
        th = ang_off
        while th < 360 + ang_off:
            t = th % 360
            near_open = min(t, 360 - t) < quilt_open_skip
            near_boss = abs(t - 180) < quilt_boss_skip
            if not (near_open or near_boss):
                c, s = cos(radians(t)), sin(radians(t))
                pl = Plane(origin=(R * c, R * s, zc), x_dir=(-s, c, 0), z_dir=(c, s, 0))
                pockets.append(pl * pk)
            th += Dth
        row += 1
        zc = quilt_z0 + row * (quilt_dz / 2)            # half-diagonal row spacing

    if pockets:
        part = part.cut(*pockets)

print(f"Volume: {part.volume / 1000:.1f} cm^3   valid: {part.is_valid}")
print(f"boss diamond = Strong Vibes Connect STANDARD (locked): DIA_A={dia_a:.3f}  DIA_B={dia_b:.3f}  "
      f"BAND_DEPTH={BAND_DEPTH:.1f} mm   (boss_aspect={boss_aspect} stretches the flare buttress only)")

show(part, names=["strong_vibes_holder"])         # live preview in OCP CAD Viewer

if not EXPORT:
    print("Preview only (set EXPORT = True to write .step / .stl / .3mf)")
else:
    export_step(part, build_path(f"{VARIANT}.step"))
    export_stl(part, build_path(f"{VARIANT}.stl"), tolerance=0.05, angular_tolerance=0.3)
    exported = [".step", ".stl"]

    # 3mf is best-effort: lib3mf's strict manifold check rejects the helical thread
    # mesh even when the solid is valid. STL/STEP slice fine (Bambu re-meshes).
    try:
        m = Mesher()
        m.add_shape(part, linear_deflection=0.05, angular_deflection=0.5)
        m.write(build_path(f"{VARIANT}_b123d.3mf"))
        exported.append(".3mf")
    except RuntimeError as e:
        print(f"Skipped .3mf ({e}); use the .stl/.step for slicing.")

    print(f"Exported to build/: {VARIANT}  ({'  '.join(exported)})")
