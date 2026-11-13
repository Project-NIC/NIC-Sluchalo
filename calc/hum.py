"""Iljič: what a plate and a coil on the head pick up from a cable in the wall, from 50 Hz to 1 MHz.

Rough, to the order of magnitude and for the trends. The plate lies in the head's ground plane,
GAP of air from the wall; the cable is a sheathed three-core at depth h in a wall that both
stores charge and conducts (eps - j sigma/omega), with its own earth a way behind its face.
Inside the sheath the live core lifts the sheath's surface towards a third of its voltage,
through the cores' insulation; the wall loads that; and the sheath's field crosses the wall and
the gap to the plate (the layered solution for a line source, solved per wavenumber). The coil sees the go-and-return
pair as a two-wire line. Assumed, not from a sheet: the cable's sizes, PVC's permittivity, the
wall's conductivity (swept over four decades), the distance to the wall's own earth.

Run: python3 hum.py > hum.out
"""
import math
import numpy as np
from materials import EPS0, MU0

GAP = 0.016                       # foam and sheet between the wall and the head's face
PLATE_W, PLATE_L = 0.02, 0.02     # the plate
R_BUNDLE, R_SHEATH, EPS_INS = 0.003, 0.0045, 4.0     # a 3 x 1.5 cable: its cores' circle, its sheath; PVC
EPS_WALL, EARTH = 4.0, 0.30       # the wall's permittivity; how far behind the face its own earth lies, m
PAIR = 0.0035                     # live to neutral, centre to centre
COIL_TURNS, COIL_AREA = 200, 1e-4
WALLS = (('bone dry', 1e-9), ('dry', 1e-7), ('ordinary', 1e-5), ('damp', 1e-3))    # S/m, assumed
FREQS = (50, 1e4, 33e3, 1e5, 125e3, 1e6)
DEPTHS = (0.01, 0.03, 0.05, 0.10)

def layers(k, h, e1):
    """Line source of 1 C/m at depth h in the wall; air gap and the head's plane in front, the wall's
    earth EARTH behind. Returns the potential at the source's own depth and the charge density on the
    head's plane, both per k."""
    s = 1 / (2 * e1 * k); eh, eT, eg = np.exp(-k * h), np.exp(-k * EARTH), np.exp(-2 * k * GAP)
    M = np.zeros((len(k), 3, 3), complex); r = np.zeros((len(k), 3), complex)      # unknowns A, C, B e^{kg}/2
    M[:, 0, 0] = eT; M[:, 0, 1] = 1; r[:, 0] = -s * np.exp(-k * (EARTH - h))        # zero at the wall's earth
    M[:, 1, 0] = 1; M[:, 1, 1] = eT; M[:, 1, 2] = -(1 - eg); r[:, 1] = -s * eh      # potential continuous at the face
    M[:, 2, 0] = e1; M[:, 2, 1] = -e1 * eT; M[:, 2, 2] = EPS0 * (1 + eg); r[:, 2] = e1 * s * eh   # and the flux
    A, C, B = np.linalg.solve(M, r[..., None])[..., 0].T
    return s + A * eh + C * np.exp(-k * (EARTH - h)), 2 * EPS0 * k * B * np.exp(-k * GAP)

def plate_charge(f, h, sigma, x0=0.0):
    """Charge on the plate per volt on the live core, C/V, complex; x0 = the plate's offset from the cable."""
    e1 = EPS0 * EPS_WALL - 1j * sigma / (2 * math.pi * f)
    c_src = 2 * math.pi * EPS0 * EPS_INS / math.log(R_SHEATH / R_BUNDLE)          # cores to the sheath's surface, F/m
    k = np.geomspace(1e-2, 50 / R_SHEATH, 20000)
    at_sheath, dens = layers(k, h, e1)
    P = np.trapezoid(at_sheath * np.cos(k * R_SHEATH), k) / math.pi                # volts on the sheath per C/m
    lam = c_src * (1 / 3) / (1 + c_src * P)                                        # a third of the voltage behind c_src
    strip = (np.sin(k * (x0 + PLATE_W / 2)) - np.sin(k * (x0 - PLATE_W / 2))) / k  # integral of cos(kx) over the plate
    return lam * PLATE_L * np.trapezoid(dens * strip, k) / math.pi

def coil_volts(f, h, amps, x0=0.0):
    """Volts on the coil, its axis along the wall and across the cable, from a go-and-return pair."""
    r2 = (h + GAP) ** 2 + x0 ** 2
    b = MU0 * amps * PAIR / (2 * math.pi * r2) * abs((h + GAP) ** 2 - x0 ** 2) / r2
    return 2 * math.pi * f * COIL_TURNS * COIL_AREA * b

def width(fn):
    """Full width at half height of a profile across the cable, m."""
    x = np.linspace(0, 0.5, 51); v = np.array([abs(fn(xi)) for xi in x])
    return 2 * x[np.argmax(v < v[0] / 2)]

if __name__ == '__main__':
    print(f'the plate {PLATE_W*1000:.0f} x {PLATE_L*1000:.0f} mm, {GAP*1000:.0f} mm from the wall; the wall eps {EPS_WALL}')
    print('\n== the wall stops being a conductor above (sigma / 2 pi eps):')
    for name, s in WALLS:
        print(f'  {name:9s} {s:.0e} S/m: {s/(2*math.pi*EPS0*EPS_WALL):12.0f} Hz')
    print('\n== the plate: coupling to the live core, fF; and the current at 230 V (50 Hz) or 10 V (a tracer), pA')
    for name, s in WALLS:
        print(f'  -- {name} wall; depth: ' + ', '.join(f'{d*100:.0f} cm' for d in DEPTHS))
        for f in FREQS:
            volts = 230 if f == 50 else 10
            row = [abs(plate_charge(f, d, s)) for d in DEPTHS]
            print(f'  {f:9.0f} Hz  ' + '  '.join(f'{c*1e15:7.2f} fF {2*math.pi*f*volts*c*1e12:9.0f} pA' for c in row))
    print('\n== the plate: how wide the cable looks (full width at half height), cm')
    for name, sg, f in (('bone dry', 1e-9, 50), ('ordinary', 1e-5, 50), ('ordinary', 1e-5, 125e3), ('damp', 1e-3, 1e6)):
        print(f'  {name:9s} {f:8.0f} Hz  ' + '  '.join(f'{d*100:.0f} cm deep: {width(lambda x: plate_charge(f, d, sg, x))*100:.0f}' for d in DEPTHS))
    print(f'\n== the coil, {COIL_TURNS} turns of {COIL_AREA*1e4:.0f} cm2: microvolts; depth: ' + ', '.join(f'{d*100:.0f} cm' for d in DEPTHS))
    for f, amps, word in ((50, 1.0, '1 A of load'), (50, 10.0, '10 A of load'), (33e3, 0.01, '10 mA of a tracer'),
                          (125e3, 0.01, '10 mA of a tracer'), (1e6, 0.01, '10 mA of a tracer')):
        print(f'  {f:9.0f} Hz, {word:18s} ' + '  '.join(f'{coil_volts(f, d, amps)*1e6:10.2f}' for d in DEPTHS))
    amb = 0.1e-6
    print(f'  for scale: a room\'s own 50 Hz field of {amb*1e6:.1f} uT gives {2*math.pi*50*COIL_TURNS*COIL_AREA*amb*1e6:.2f} uV')
    print('  how wide the cable looks to the coil, cm: ' + '  '.join(f'{d*100:.0f} cm deep: {width(lambda x: coil_volts(50, d, 1.0, x))*100:.0f}' for d in DEPTHS))
