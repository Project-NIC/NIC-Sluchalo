"""The head: nine receivers in a square or a ring. Run: python3 array.py

Patches on FR4 1.6 mm, square for either polarization: 29 mm at 2.44 GHz (budget.py). Pitch: the
patch plus a gap of ~16 mm against coupling -> 45 mm between neighbours (a choice, to be simulated).
"""
import math
from materials import C0

PATCH, PITCH = 0.029, 0.045
F24, F55 = 2.44e9, 5.5e9
half = {f: C0 / f / 2 for f in (F24, F55)}

def report(name, pts, centre_free):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    d = [math.dist(a, b) for i, a in enumerate(pts) for b in pts[i+1:]]
    nn = sorted(d)[0]
    aperture = max(d)
    size = aperture + PATCH * 1.3
    print(f'== {name}')
    print(f'  nearest neighbours {nn*1000:.0f} mm, widest pair {aperture*1000:.0f} mm, head about {size*1000:.0f} mm across')
    for f in (F24, F55):
        print(f'  {f/1e9:.2f} GHz: half a wavelength {half[f]*1000:.0f} mm -> direction finding '
              f'{"unambiguous" if nn <= half[f] else "ambiguous"}; resolution about {math.degrees(C0/f/aperture):.0f} deg')
    print(f'  free middle for the ultrasound tips and the optical sensors: {centre_free}')

square = [(i * PITCH, j * PITCH) for i in (-1, 0, 1) for j in (-1, 0, 1)]
report('3 x 3 square', square, 'none; the tips go into the corners between patches')

R8 = PITCH / (2 * math.sin(math.pi / 8))
ring8 = [(R8 * math.cos(2 * math.pi * k / 8), R8 * math.sin(2 * math.pi * k / 8)) for k in range(8)] + [(0, 0)]
report(f'a ring of 8 around a ninth, radius {R8*1000:.0f} mm', ring8,
       f'an annulus {(R8 - PATCH*0.5 - PATCH*0.5)*1000:.0f} mm wide between the middle patch and the ring')

R9 = PITCH / (2 * math.sin(math.pi / 9))
ring9 = [(R9 * math.cos(2 * math.pi * k / 9), R9 * math.sin(2 * math.pi * k / 9)) for k in range(9)]
report(f'a ring of 9, radius {R9*1000:.0f} mm', ring9, f'a disc {(2*R9 - PATCH)*1000:.0f} mm across')

print('== polarization: how far is a cable at any angle from the nearest element\'s field direction')
def worst(dirs):
    dirs = [d % 180 for d in dirs]
    w = 0
    for c in range(0, 180):
        w = max(w, min(min(abs(c - d), 180 - abs(c - d)) for d in dirs))
    return w
schemes = {
    '3 x 3 square, all one way': [0] * 9,
    '3 x 3 square, checkerboard 0/90': [0, 90] * 4 + [0],
    'ring of 8 + 1, ring patches radial': [45 * k for k in range(8)] + [0],
    'ring of 9, all patches radial': [40 * k for k in range(9)],
}
for name, dirs in schemes.items():
    distinct = sorted(set(d % 180 for d in dirs))
    w = worst(dirs)
    print(f'  {name}: {len(distinct)} directions, worst {w} deg off -> the field along the cable at least {math.cos(math.radians(w))**2*100:.0f} % of the best case')

print('== the ring of 9 for calibration: the distances between its antennas, and what a millimetre costs')
R9 = PITCH / (2 * math.sin(math.pi / 9))
print('  from the middle to every antenna: ' + f'{R9*1000:.1f} mm; between ring antennas: '
      + ', '.join(f'{2*R9*math.sin(k*math.pi/9)*1000:.1f}' for k in range(1, 5)) + ' mm (each class alike by symmetry)')
for f in (F24, F55):
    print(f'  1 mm of path at {f/1e9:.2f} GHz: {360/(C0/f)/1000:.1f} deg of phase; 0.1 mm (a board\'s placement): {36/(C0/f)/1000:.2f} deg')

print('== the receivers\' polarization against the cable: how deep a -5 dB shadow (field along the cable) still shows')
print('   the sender in two turns, linear at 0 and 90 deg (Fonar\'s crossed antennas); the cable at any angle;')
print('   the deepest dip among receivers that are not cross-polarized to the sender, the worst cable angle')
import cmath
keep = 10 ** (-5 / 20)                           # the along-cable field behind the cable
def recv_power(E, kind, chi=0.0):
    if kind == 'cp':
        return abs((E[0] - 1j * E[1]) / math.sqrt(2)) ** 2
    return abs(E[0] * math.cos(chi) + E[1] * math.sin(chi)) ** 2
def behind(E, a):                                 # shadow the component along a cable at angle a
    u = (math.cos(a), math.sin(a)); along = E[0] * u[0] + E[1] * u[1]
    return (E[0] - (1 - keep) * along * u[0], E[1] - (1 - keep) * along * u[1])
configs = {
    'ring of 9, radial linear patches': [('lin', math.radians(40 * k)) for k in range(9)],
    'all one way, linear': [('lin', 0.0)] * 9,
    'alternately across, linear (0 / 90)': [('lin', math.radians(90 * (k % 2))) for k in range(9)],
    'all circular': [('cp', 0.0)] * 9,
}
for name, rx in configs.items():
    worst, at = -1e9, 0
    for a_deg in range(0, 91):
        a = math.radians(a_deg); best = 0.0
        for psi in (0.0, math.pi / 2):
            E0 = (math.cos(psi), math.sin(psi)); E1 = behind(E0, a)
            for kind, chi in rx:
                p0 = recv_power(E0, kind, chi)
                if p0 < 0.25 * (0.5 if kind == 'cp' else 1.0):
                    continue                      # cross-polarized to the sender: no use
                best = min(best, 10 * math.log10(recv_power(E1, kind, chi) / p0))
        if best > worst:
            worst, at = best, a_deg
    print(f'  {name:38s}: worst {worst:+.1f} dB (a cable at {at} deg)')

print('== how many around one middle: n radial patches on a ring, the middle a crossed pair (two C5s)')
print('   neighbours 45 mm apart (the gap against coupling); a 30 mm patch; the shadow metric as above')
for n in (6, 7, 8, 9):
    R = PITCH / (2 * math.sin(math.pi / n))
    rx = [('lin', math.radians(360 / n * k)) for k in range(n)]
    dirs = sorted({round(math.degrees(chi) % 180, 1) for _, chi in rx})
    worst = -1e9
    for a_deg in range(0, 91):
        a = math.radians(a_deg); best = 0.0
        for psi in (0.0, math.pi / 2):
            E0 = (math.cos(psi), math.sin(psi)); E1 = behind(E0, a)
            for kind, chi in rx:
                p0 = recv_power(E0, kind, chi)
                if p0 >= 0.25:
                    best = min(best, 10 * math.log10(recv_power(E1, kind, chi) / p0))
        worst = max(worst, best)
    free = R - 0.015 - 0.015                         # from the middle patch's edge to a ring patch's inner edge
    print(f'  {n} around: radius {R*1000:.1f} mm ({"= the neighbours\' distance, all triangles equal" if abs(R-PITCH) < 1e-4 else "neighbours " + format(PITCH*1000, ".0f") + " mm"}), '
          f'{len(dirs)} field directions, worst shadow {worst:+.1f} dB; gap middle-to-ring {free*1000:.0f} mm; '
          f'head ~{(2*R + 0.030*1.3)*1000:.0f} mm; {n + 2} C5s')

print('== the ring of nine as built: patches 30 mm long (radial, set by the match) and 29 mm wide')
L_RAD, W_TAN = 0.030, 0.029
th = math.radians(40)
def inner_corner(t, side):
    r = R9 - L_RAD / 2
    return (r * math.cos(t) - side * W_TAN / 2 * math.sin(t), r * math.sin(t) + side * W_TAN / 2 * math.cos(t))
print(f'  between neighbours: {(PITCH - W_TAN)*1000:.0f} mm at their centres, '
      f'{math.dist(inner_corner(0, +1), inner_corner(th, -1))*1000:.1f} mm at their inner corners')
