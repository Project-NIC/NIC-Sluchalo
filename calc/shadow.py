"""How deep a shadow a cylinder in the wall casts: the exact 2D series for a plane wave on a
circular cylinder (metal or dielectric) in brick. Worst dip of |E| on a line d behind it.
'along' = E parallel to the cylinder (TM), 'across' = E perpendicular (TE). Needs numpy, scipy.
Run: python3 shadow.py
"""
import numpy as np
from scipy.special import jv, jvp, hankel2, h2vp
from materials import k as wavenumber

def coef(n, k, k1, a, pol):
    if k1 is None:  # metal
        return -jv(n, k*a) / hankel2(n, k*a) if pol == 'TM' else -jvp(n, k*a) / h2vp(n, k*a)
    J, Jp, H, Hp = jv(n, k*a), jvp(n, k*a), hankel2(n, k*a), h2vp(n, k*a)
    J1, J1p = jv(n, k1*a), jvp(n, k1*a)
    if pol == 'TM':
        return (k1*J1p*J - k*Jp*J1) / (k*J1*Hp - k1*J1p*H)
    return (k*J1p*J - k1*Jp*J1) / (k1*J1*Hp - k*J1p*H)

def field(k, k1, a, x, ys, pol):
    rho = np.hypot(x, ys); phi = np.arctan2(ys, x); N = int(abs(k)*a) + 20
    t = np.exp(-1j*k*x) * np.ones_like(ys, dtype=complex)
    for n in range(-N, N + 1):
        t += (1j)**(-n) * coef(n, k, k1, a, pol) * hankel2(n, k*rho) * np.exp(1j*n*phi)
    return t

def dip(f, a, d, pol, inside, medium='brick'):
    k = complex(wavenumber(medium, f)); k1 = None if inside is None else complex(wavenumber(inside, f))
    ys = np.linspace(-0.3, 0.3, 601)
    if pol == 'TM':
        r = field(k, k1, a, d, ys, pol) / np.exp(-1j*k*d)
    else:
        h = 2e-4
        r = ((field(k, k1, a, d+h, ys, pol) - field(k, k1, a, d-h, ys, pol)) / (2*h)) / (-1j*k*np.exp(-1j*k*d))
    return 20*np.log10(np.abs(r)).min()

CASES = [('a cable, metal, diameter 5 mm', 0.0025, None), ('a conductor, metal, diameter 10 mm', 0.005, None),
         ('a conduit 25 mm, air inside', 0.0125, 'air'), ('a conduit 32 mm, air inside', 0.016, 'air'),
         ('a pipe 32 mm, metal', 0.016, None)]
DEPTHS = (0.02, 0.05, 0.10, 0.20, 0.30)

if __name__ == '__main__':
    for f in (2.44e9, 5.5e9):
        print(f'== {f/1e9:.2f} GHz in brick; distance behind the object: ' + ', '.join(f'{d*100:.0f} cm' for d in DEPTHS))
        for name, a, inside in CASES:
            for pol, word in (('TM', 'along'), ('TE', 'across')):
                print(f'  {name:36s} {word:6s} ' + '  '.join(f'{dip(f, a, d, pol, inside):+6.1f}' for d in DEPTHS))
    f = 2.44e9
    print(f'== {f/1e9:.2f} GHz in air (a drywall cavity); distance behind the object: ' + ', '.join(f'{d*100:.0f} cm' for d in DEPTHS))
    for name, a, inside in (CASES[0], CASES[1], CASES[4]):
        for pol, word in (('TM', 'along'), ('TE', 'across')):
            print(f'  {name:36s} {word:6s} ' + '  '.join(f'{dip(f, a, d, pol, inside, medium="air"):+6.1f}' for d in DEPTHS))
    print('  (an empty plastic conduit in air has almost nothing to show; only its cable)')
