"""A carbon-loaded foam with aluminium foil behind it: how much of a wave from the front comes back,
and how much from behind gets through. Level 4. A plane wave at normal incidence on a lossy slab on
a perfect conductor (a transmission line ended in a short). The foam is taken as a permittivity
eps' with a loss tangent — assumed, not a product's figures: carbon foams differ widely, and the
good ones are graded. The foil: household aluminium, 10-20 um, against a skin depth of 1.7 um at
2.4 GHz.

Run: python3 absorber.py > absorber.out
"""
import cmath, math
C0, Z0 = 299792458.0, 376.73

def reflection(f, d, er, tand):
    e = er * (1 - 1j * tand)
    k = 2 * math.pi * f / C0 * cmath.sqrt(e)
    zf = Z0 / cmath.sqrt(e)
    zin = 1j * zf * cmath.tan(k * d)                 # the slab ended in the foil
    return 20 * math.log10(abs((zin - Z0) / (zin + Z0)))

if __name__ == '__main__':
    print('== from the front: what comes back off foam on foil, dB (0 dB = all of it, as off bare metal)')
    print('   foam eps\' 1.5, loss tangent as given; at 2.437 / 5.5 GHz')
    print('   thickness    ' + ''.join(f'tan d {t:<4}          ' for t in (0.3, 1.0, 3.0)))
    for d in (0.005, 0.010, 0.020, 0.030):
        row = ''.join(f'{reflection(2.437e9, d, 1.5, t):6.1f} / {reflection(5.5e9, d, 1.5, t):6.1f}     ' for t in (0.3, 1.0, 3.0))
        print(f'   {d*1000:3.0f} mm      {row}')
    best = min(((reflection(2.437e9, d / 1000, 1.5, t) + reflection(5.5e9, d / 1000, 1.5, t)) / 2, d, t)
               for d in range(5, 41) for t in (0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0))
    print(f'   the best single uniform foam up to 40 mm for both bands: {best[1]} mm, tan d {best[2]}: '
          f'{reflection(2.437e9, best[1]/1000, 1.5, best[2]):.1f} / {reflection(5.5e9, best[1]/1000, 1.5, best[2]):.1f} dB')
    for t_um in (10, 20):
        skin = 1 / math.sqrt(math.pi * 2.437e9 * 4e-7 * math.pi * 3.5e7)
        print(f'== from behind, through {t_um} um of aluminium: absorbed in the foil alone {8.686 * t_um * 1e-6 / skin:.0f} dB '
              f'(skin depth {skin*1e6:.1f} um), plus the reflection at its face; in practice the edges and seams decide')

def stack(f, n, rs, d_total, backed=True):
    """n resistive films (rs ohm per square each) spread evenly over d_total of air, foil behind or not:
    reflection from the front and, unbacked, transmission through, dB."""
    k = 2 * math.pi * f / C0
    gap = d_total / n
    y = 0j if not backed else None                     # admittance looking back, in units of 1/Z0
    if backed:
        y = -1j / math.tan(k * gap) if gap > 0 else 1e9
    else:
        y = 1 + 0j                                     # free space behind
    abcd = [[1, 0], [0, 1]]
    for i in range(n):
        y = y + Z0 / rs                                # the film, in shunt
        if i < n - 1 or not backed:
            t = math.tan(k * gap)
            y = (y + 1j * t) / (1 + 1j * y * t)        # carried forward through a gap of air
    r = (1 - y) / (1 + y)
    return 20 * math.log10(abs(r))

if __name__ == '__main__':
    lam = lambda f: C0 / f
    band = (lam(2.4e9) - lam(2.5e9)) + (lam(5.15e9) - lam(5.85e9))
    print('== the thinnest a metal-backed absorber with no magnetic material can be (Rozanov\'s bound),')
    print('   for the two bands only, 2.4-2.5 and 5.15-5.85 GHz:')
    for rdb in (-10, -20):
        print(f'   {rdb} dB over both: at least {abs(math.log(10 ** (rdb / 20))) * band / (2 * math.pi ** 2) * 1000:.1f} mm '
              f'(a bound; reaching it takes a design, and it says nothing of how)')
    print('== films stacked in front of the foil, all within 5 mm: what comes back from the front, dB at 2.437 / 5.5 GHz')
    for n, rs in ((1, 377), (5, 1000), (20, 1000), (20, 100), (20, 10)):
        print(f'   {n:2d} films of {rs:4d} ohm/sq over 5 mm: {stack(2.437e9, n, rs, 0.005):6.1f} / {stack(5.5e9, n, rs, 0.005):6.1f}')
    print('   the same 377 ohm/sq film a quarter wave in front of the foil (Salisbury): '
          f'{stack(2.437e9, 1, 377, lam(2.437e9) / 4):6.1f} dB at 2.437 GHz, {lam(2.437e9) / 4 * 1000:.0f} mm thick')
