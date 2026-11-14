"""The face of the head of ten with the bought antennas: where everything sits on Front. Level 4.

The antenna is the Ezurio dual-band FlexPIFA (datasheet: 38.5 x 12.7 x 2.5 mm), made to sit over
metal; the maker asks 5 mm free of raised metal beside its long sides. The ring: eight, each turned
radially. Předseda: two, at right angles, as a pinwheel round the middle, so that the middle stays
free for Datel's rod. The rod the head turns on stands in the quadrant the pinwheel leaves free.
Datel's eight microphones sit by the ring, each in the gap between two of its antennas.
The one home of the face's layout; the figures are printed and drawn.

Run: python3 layout.py > layout.out   (writes layout.png)
"""
import math

L, W = 0.0385, 0.0127          # the antenna, along and across
GAP = 0.005                    # between antennas' sides, and round the holes (the maker's 5 mm)
HOLE_DATEL, HOLE_ROD, HOLE_MIC = 0.003, 0.004, 0.0015   # radii of the holes
N = 8
MARGIN = 0.005                 # face beyond the ring's outer ends

def rect(cx, cy, ang, l=L, w=W):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + c * dx - s * dy, cy + s * dx + c * dy) for dx, dy in ((-l/2, -w/2), (l/2, -w/2), (l/2, w/2), (-l/2, w/2))]

def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    vx, vy = bx - ax, by - ay; t = max(0, min(1, ((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy)))
    return math.hypot(px - ax - t * vx, py - ay - t * vy)

def poly_dist(P, Q):
    """Least distance between two convex polygons that do not overlap (0 if they do)."""
    def inside(p, R):
        sgn = None
        for a, b in zip(R, R[1:] + R[:1]):
            cr = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if sgn is None: sgn = cr > 0
            elif (cr > 0) != sgn: return False
        return True
    if any(inside(p, Q) for p in P) or any(inside(q, P) for q in Q): return 0.0
    return min(min(seg_dist(p, a, b) for a, b in zip(Q, Q[1:] + Q[:1])) for p in P) if True else 0

def point_poly(p, P):
    return min(seg_dist(p, a, b) for a, b in zip(P, P[1:] + P[:1]))

def layout(R):
    ring = [rect(R * math.cos(k * 2 * math.pi / N), R * math.sin(k * 2 * math.pi / N), k * 2 * math.pi / N) for k in range(N)]
    e = HOLE_DATEL + GAP                                   # the pinwheel's arms keep clear of Datel's hole
    serp = rect(-L / 2 + e * 0.0 + (e - L) / 2 + L / 2 - e + 0.0, e + W / 2, 0.0)   # level arm, upper left
    serp = rect(e - L / 2, e + W / 2, 0.0)                  # spans x from e-L to e, y from e to e+W
    molot = rect(e + W / 2 + GAP, -(e - L / 2) - L + e + 0.0, math.pi / 2)
    molot = rect(e + GAP + W / 2, e - L / 2 - 0.0, math.pi / 2)   # upright arm, lower right: x from e+GAP to e+GAP+W
    a_rod = 2 * math.pi / N / 2 + math.radians(10)          # the rod: in the free quadrant, 10 deg off a gap's middle
    mics = [(R * math.cos((k + 0.5) * 2 * math.pi / N), R * math.sin((k + 0.5) * 2 * math.pi / N)) for k in range(N)]
    return ring, serp, molot, a_rod, mics

def check(R, r_rod):
    ring, serp, molot, a_rod, mics = layout(R)
    rod = (r_rod * math.cos(a_rod), r_rod * math.sin(a_rod))
    ants = ring + [serp, molot]
    d_ants = min(poly_dist(ants[i], ants[j]) for i in range(len(ants)) for j in range(i + 1, len(ants)))
    d_rod = min(point_poly(rod, P) for P in ants) - HOLE_ROD
    d_mic = min(point_poly(m, P) for m in mics for P in ants) - HOLE_MIC
    d_datel = min(point_poly((0, 0), P) for P in ants) - HOLE_DATEL
    d_rod_mic = min(math.hypot(rod[0] - m[0], rod[1] - m[1]) for m in mics) - HOLE_ROD - HOLE_MIC
    return min(d_ants, d_rod, d_mic, d_datel, d_rod_mic), (d_ants, d_rod, d_mic, d_datel, d_rod_mic), rod

best = None
for R_mm in range(40, 90):
    R = R_mm / 1000
    for r_mm in range(10, R_mm):
        m, parts, rod = check(R, r_mm / 1000)
        if m >= GAP - 1e-9:
            best = (R, r_mm / 1000, parts, rod); break
    if best: break
R, R_ROD, parts, ROD = best
HEAD_R = math.hypot(R + L / 2, W / 2) + MARGIN

def from_rod():
    ring, serp, molot, a_rod, mics = layout(R)
    return sorted(math.hypot(R * math.cos(k * 2 * math.pi / N) - ROD[0], R * math.sin(k * 2 * math.pi / N) - ROD[1]) for k in range(N))

if __name__ == '__main__':
    print(f'the antenna {L*1000:.1f} x {W*1000:.1f} mm; {GAP*1000:.0f} mm kept between antennas and round every hole')
    print(f'the ring: eight, radial, centres on a circle of {R*1000:.0f} mm; the head {2*HEAD_R*1000:.0f} mm across')
    names = ('between antennas', 'rod to an antenna', 'microphone to an antenna', "Datel's rod to an antenna", 'rod to a microphone')
    print('  clearances, mm: ' + ', '.join(f'{n} {v*1000:.1f}' for n, v in zip(names, parts)))
    print(f'  the rod the head turns on: {R_ROD*1000:.0f} mm from the centre, at {math.degrees(math.atan2(ROD[1], ROD[0])):.0f} deg')
    d = from_rod()
    print(f'  the ring\'s antennas from the rod: ' + ', '.join(f'{v*1000:.0f}' for v in d) + ' mm; one turn covers a disc '
          f'{2*(d[-1]+L/2)*1000:.0f} mm across')
    print(f'  Datel: the knock in the middle; its eight microphones {R*1000:.0f} mm out, between the ring\'s antennas')
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon, Circle
    ring, serp, molot, a_rod, mics = layout(R)
    fig, ax = plt.subplots(figsize=(5, 5), dpi=90)
    ax.add_patch(Circle((0, 0), HEAD_R * 1000, fc='#e8e8e8', ec='k'))
    for P, col, lab in [(p, '#4a7bd0', None) for p in ring] + [(serp, '#c0392b', 'Serp'), (molot, '#c0392b', 'Molot')]:
        ax.add_patch(Polygon([(x * 1000, y * 1000) for x, y in P], fc=col, ec='k'))
        if lab:
            cx = sum(x for x, _ in P) / 4 * 1000; cy = sum(y for _, y in P) / 4 * 1000
            ax.text(cx, cy, lab, ha='center', va='center', fontsize=7, color='w')
    ax.add_patch(Circle((0, 0), HOLE_DATEL * 1000, fc='k')); ax.text(0, -6, 'Datel (the knock)', ha='center', fontsize=6)
    ax.add_patch(Circle((ROD[0] * 1000, ROD[1] * 1000), HOLE_ROD * 1000, fc='#27ae60')); ax.text(ROD[0] * 1000, ROD[1] * 1000 + 6, 'Kuří nožka', ha='center', fontsize=6)
    for m in mics:
        ax.add_patch(Circle((m[0] * 1000, m[1] * 1000), HOLE_MIC * 1000 * 2, fc='#f39c12'))
    ax.text(mics[0][0] * 1000, mics[0][1] * 1000 + 5, "Datel's mic", ha='center', fontsize=6)
    ax.set_xlim(-HEAD_R * 1000 - 5, HEAD_R * 1000 + 5); ax.set_ylim(-HEAD_R * 1000 - 5, HEAD_R * 1000 + 5)
    ax.set_aspect('equal'); ax.set_xlabel('mm'); ax.set_title('Front, seen from the wall: Kosy (blue), Serp and Molot (red)', fontsize=8)
    fig.tight_layout(); fig.savefig('layout.png')

# the names the other scripts of level 4 take the head from (they took them from ring8.py before)
N_RING, RING_R, HEAD_R_, ROD_R = N, R, HEAD_R, R_ROD
ROD_AT = math.atan2(ROD[1], ROD[0])                     # the rod's direction, from the first ring antenna's axis
PATCH_L, PATCH_W = L, W
_ring, _serp, _molot, _a, _mics = layout(R)
MID_XY = [(sum(x for x, _ in P) / 4, sum(y for _, y in P) / 4) for P in (_serp, _molot)]   # Předseda's two antennas
MID_PSI = [0.0, math.pi / 2]
