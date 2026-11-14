"""The head as decided on 13 Nov 2026: eight radial patches in a ring around Předseda, each patch at
its full width. The one home of the head's layout figures; picture.py takes them from here.

The ring's radius is the smallest that leaves the neighbours' inner corners as far apart as they
were in the ring of nine (array.py). Run: python3 ring8.py > ring8.out
"""
import math

N_RING = 8
PATCH_L, PATCH_W = 0.030, 0.037        # along the radius (the resonant length), across it
MID = 0.030                            # Předseda's square patch
CORNER_GAP = 0.0075                    # between neighbours' inner corners, as in the ring of nine
RIM_MARGIN = 0.0014                    # board beyond the outer corners, as in the ring of nine
ROD_AT = math.radians(10)              # the rod stands 10 deg off a patch's axis

def corner_gap(r):
    a = 2 * math.pi / N_RING; x, y = r - PATCH_L / 2, PATCH_W / 2
    return math.hypot(x - (x * math.cos(a) + y * math.sin(a)), y - (x * math.sin(a) - y * math.cos(a)))

lo, hi = 0.05, 0.12
for _ in range(60):
    mid = (lo + hi) / 2; lo, hi = (mid, hi) if corner_gap(mid) < CORNER_GAP else (lo, mid)
RING_R = math.ceil(hi * 2000) / 2000   # up to the next half millimetre
HEAD_R = math.hypot(RING_R + PATCH_L / 2, PATCH_W / 2) + RIM_MARGIN
ROD_R = RING_R / 2                     # the rod: midway between Předseda's edge and the ring's inner edge

def from_rod():
    return sorted(math.hypot(RING_R * math.cos(2 * math.pi * k / N_RING) - ROD_R * math.cos(ROD_AT),
                             RING_R * math.sin(2 * math.pi * k / N_RING) - ROD_R * math.sin(ROD_AT)) for k in range(N_RING))

if __name__ == '__main__':
    pitch = 2 * RING_R * math.sin(math.pi / N_RING)
    print(f'eight patches {PATCH_L*1000:.0f} x {PATCH_W*1000:.0f} mm, radial, around a middle patch {MID*1000:.0f} mm square')
    print(f'  ring radius {RING_R*1000:.1f} mm; neighbours {pitch*1000:.1f} mm centre to centre (half a wavelength at 2.44 GHz is 61 mm)')
    print(f'  between neighbours: {(pitch - PATCH_W)*1000:.1f} mm at their centres, {corner_gap(RING_R)*1000:.1f} mm at their inner corners')
    print(f'  between the middle patch and the ring: {(RING_R - PATCH_L/2 - MID/2)*1000:.1f} mm, all the way round')
    print(f'  the head {2*HEAD_R*1000:.0f} mm across')
    d = from_rod()
    print(f'  the rod {ROD_R*1000:.1f} mm from the centre: the eight at ' + ', '.join(f'{v*1000:.0f}' for v in d) + f' mm from it, Předseda at {ROD_R*1000:.0f}')
    print(f'  one turn covers a disc {2*(d[-1] + PATCH_L/2)*1000:.0f} mm across, blind within {max(0, d[0] - PATCH_L/2)*1000:.0f} mm of the rod')
