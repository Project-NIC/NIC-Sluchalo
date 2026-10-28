"""A real wall instead of ideal brick: 2D FDTD of a solid-brick wall in vertical section.

The wave comes from the far side (a plane wave, as from a box a metre or more away), crosses
plaster, brick with its bed joints, plaster, and the field is read in a line 2 mm in front of the
near face, where the receiver lies. The section is periodic in height (8 courses of 75 mm).
'along' = E along the cable (TMz: Ez), 'across' = E across it, in the section (TEz: Ey).
CW at one frequency at a time; the phasor is taken over the last periods. Needs numpy.

Run: python3 wall_fdtd.py            (the table)
     python3 wall_fdtd.py <mm> <mortar> <brick> [plaster]   (one wall; e.g. 290 mortar_wet brick)
     python3 wall_fdtd.py validate   (against shadow.py: a cable in homogeneous brick)
"""
import sys
import numpy as np
from materials import C0, EPS0, MU0, eps_sigma, ITU

DX = 1e-3                      # 1 mm cells
DT = 0.99 * DX / (C0 * np.sqrt(2))
NPML = 40
W = 0.600                      # height of the periodic section: 8 courses of 65 + 10 mm
COURSE, BRICK_H = 0.075, 0.065
PLASTER_T = 0.015
GAP_SRC, GAP_RX = 0.060, 0.030
RX_OFF = 0.002                 # the receiving line 2 mm in front of the near plaster
PLASTER = 'plaster'            # the plaster on both faces and in the groove; 'plaster_lc' for lime-cement

def materials(f):
    er_b, s_b = eps_sigma('brick', f / 1e9)
    return {
        'air': (1.0, 0.0),
        'brick': (er_b, s_b),
        'brick_damp': (3.6, 0.070),         # solid ceramic brick at 3 % moisture, 1-6 GHz (PMC13165532)
        'mortar_lo': (2.5, 0.02),           # bracket: dry mortar below brick ...
        'mortar_hi': (5.0, 0.05),           # ... damp mortar above it (no single value found)
        'mortar_wet': (8.0, 0.15),          # ... and wet mortar well above it, the far end of the bracket
        'plaster': (2.5, 0.01),             # gypsum plaster blocks |er| ~2.1, plasterboard 2.73 (ITU)
        'plaster_lc': eps_sigma('concrete', f / 1e9),   # lime-cement plaster, taken as ITU concrete
    }

def build(f, wall_t, mortar, brick='brick', groove=None, cable=False, conduit=0.0, ylab=0.30,
          homogeneous=False):
    """Return eps_r, sigma, pec on the Ez grid, and the x index of the receiving line."""
    m = materials(f)
    nx_body = int(round((GAP_SRC + 2 * PLASTER_T + wall_t + GAP_RX) / DX))
    nx = nx_body + 2 * NPML
    ny = int(round(W / DX))
    x = (np.arange(nx) - NPML) * DX            # 0 at the inner edge of the left PML
    y = np.arange(ny) * DX
    X, Y = np.meshgrid(x, y, indexing='ij')
    er = np.ones((nx, ny)); sg = np.zeros((nx, ny)); pec = np.zeros((nx, ny), bool)
    x0 = GAP_SRC                                # far face of the far plaster
    xb0, xb1 = x0 + PLASTER_T, x0 + PLASTER_T + wall_t
    xn = xb1 + PLASTER_T                        # near face
    def put(mask, name):
        er[mask], sg[mask] = m[name]
    if homogeneous:
        put(np.ones_like(er, bool), brick)
    else:
        put((X >= x0) & (X < xb0), PLASTER)
        put((X >= xb0) & (X < xb1), brick)
        put((X >= xb1) & (X < xn), PLASTER)
        if mortar:
            bed = ((Y % COURSE) >= BRICK_H) & (X >= xb0) & (X < xb1)
            put(bed, mortar)
            if wall_t > 0.2:                    # a 290 wall: a collar joint in every other course
                course = (Y // COURSE).astype(int)
                mid = (xb0 + xb1) / 2
                collar = (course % 2 == 0) & (np.abs(X - mid) < 0.005) & (X >= xb0) & (X < xb1)
                put(collar, mortar)
    if groove:                                  # (width, depth into the brick), filled with plaster
        gw, gd = groove
        put((np.abs(Y - ylab) < gw / 2) & (X >= xb1 - gd) & (X < xb1), PLASTER)
    xc = xb1 - (groove[1] / 2 if groove else 0.05)
    if conduit:
        put((X - xc) ** 2 + (Y - ylab) ** 2 < conduit ** 2, 'air')
    if cable:
        pec |= (X - xc) ** 2 + (Y - ylab) ** 2 < 0.0025 ** 2
    irx = int(round((xn + RX_OFF) / DX)) + NPML
    if homogeneous:                             # validation: read 5 cm behind the cable
        irx = int(round((xc + 0.05) / DX)) + NPML
    return er, sg, pec, irx, int(round((GAP_SRC / 2) / DX)) + NPML, xc

def pml_profile(nx, er_bg):
    smax = 4 * np.log(1e6) / (2 * 376.73 * NPML * DX) * np.sqrt(er_bg)
    s = np.zeros(nx)
    d = np.arange(NPML, 0, -1) / NPML
    s[:NPML] = smax * d ** 3
    s[-NPML:] = smax * d[::-1] ** 3
    return s

def coeffs(er, sg, extra):
    e = er * EPS0; a = (sg + extra) * DT / (2 * e)
    return (1 - a) / (1 + a), (DT / e) / (1 + a)

def run(f, pol, er, sg, pec, irx, isrc, er_bg=1.0, periods=6):
    nx, ny = er.shape
    sx = pml_profile(nx, er_bg)                       # electric PML conductivity on integer x
    sxh = pml_profile(nx + 1, er_bg)[1:nx]            # on half x (nx-1 points)
    sxm, sxhm = sx * MU0 / (EPS0 * er_bg), sxh * MU0 / (EPS0 * er_bg)
    w = 2 * np.pi * f
    T = 1 / f
    nsteps_ramp = int(3 * T / DT)
    transit = (nx * DX) * np.sqrt(er.max()) / C0
    nsteps = int((4 * transit + 8 * T) / DT)
    ndft = int(periods * T / DT)
    acc = np.zeros(ny, complex)
    if pol == 'TM':
        Ezx = np.zeros((nx, ny)); Ezy = np.zeros((nx, ny))
        Hx = np.zeros((nx, ny)); Hy = np.zeros((nx - 1, ny))
        cax, cbx = coeffs(er, sg, sx[:, None])
        cay, cby = coeffs(er, sg, 0.0)
        ah = sxhm[:, None] * DT / (2 * MU0)
        dhy, chy = (1 - ah) / (1 + ah), (DT / MU0) / (1 + ah)
        for n in range(nsteps):
            Ez = Ezx + Ezy
            Hx -= DT / MU0 * (np.roll(Ez, -1, axis=1) - Ez) / DX
            Hy = dhy * Hy + chy * (Ez[1:] - Ez[:-1]) / DX
            Ezx[1:-1] = cax[1:-1] * Ezx[1:-1] + cbx[1:-1] * (Hy[1:] - Hy[:-1]) / DX
            Ezy = cay * Ezy - cby * (Hx - np.roll(Hx, 1, axis=1)) / DX
            t = n * DT
            ramp = min(1.0, n / nsteps_ramp)
            Ezx[isrc] += 0.5 * ramp * np.sin(w * t) * cbx[isrc] / DX
            Ezx[pec] = 0; Ezy[pec] = 0
            if n >= nsteps - ndft:
                acc += (Ezx[irx] + Ezy[irx]) * np.exp(-1j * w * t)
    else:
        # TEz: Ey on integer x (half y), Ex on half x (integer y), Hz on half x (half y)
        Ey = np.zeros((nx, ny)); Ex = np.zeros((nx - 1, ny))
        Hzx = np.zeros((nx - 1, ny)); Hzy = np.zeros((nx - 1, ny))
        erh = 0.5 * (er[1:] + er[:-1]); sgh = 0.5 * (sg[1:] + sg[:-1])
        pech = pec[1:] | pec[:-1]
        cay, cby = coeffs(er, sg, sx[:, None])
        cax, cbx = coeffs(erh, sgh, 0.0)
        ah = sxhm[:, None] * DT / (2 * MU0)
        dhz, chz = (1 - ah) / (1 + ah), (DT / MU0) / (1 + ah)
        for n in range(nsteps):
            Hzx = dhz * Hzx - chz * (Ey[1:] - Ey[:-1]) / DX
            Hzy = Hzy + DT / MU0 * (np.roll(Ex, -1, axis=1) - Ex) / DX
            Hz = Hzx + Hzy
            Ex = cax * Ex + cbx * (Hz - np.roll(Hz, 1, axis=1)) / DX
            Ey[1:-1] = cay[1:-1] * Ey[1:-1] - cby[1:-1] * (Hz[1:] - Hz[:-1]) / DX
            t = n * DT
            ramp = min(1.0, n / nsteps_ramp)
            Ey[isrc] += 0.5 * ramp * np.sin(w * t) * cby[isrc] / DX
            Ey[pec] = 0; Ex[pech] = 0
            if n >= nsteps - ndft:
                acc += Ey[irx] * np.exp(-1j * w * t)
    return acc

def db(a):
    return 20 * np.log10(np.abs(a))

def validate():
    from shadow import dip
    for f in (2.44e9,):
        er, sg, pec, irx, isrc, xc = build(f, 0.15, None, homogeneous=True, cable=True)
        er0, sg0, pec0, *_ = build(f, 0.15, None, homogeneous=True, cable=False)
        for pol in ('TM', 'TE'):
            r = run(f, pol, er, sg, pec, irx, isrc, er_bg=er[0, 0]) / run(f, pol, er0, sg0, pec0, irx, isrc, er_bg=er0[0, 0])
            print(f'{f/1e9:.2f} GHz {pol}: FDTD worst dip 5 cm behind {db(r).min():+.1f} dB; '
                  f'series {dip(f, 0.0025, 0.05, pol, None):+.1f} dB')

CASES = [  # name, groove (w, d), cable, conduit radius
    ('the groove, empty', (0.04, 0.03), False, 0.0),
    ('the groove with a cable', (0.04, 0.03), True, 0.0),
    ('the groove with a 25 mm conduit and a cable', (0.045, 0.04), True, 0.0125),
]

def table(wall_t, mortar, brick='brick'):
    ylab = 0.30 + 0.0375                       # the object level with the middle of a brick
    for f in (2.44e9, 5.5e9):
        for pol in ('TM', 'TE'):
            er, sg, pec, irx, isrc, _ = build(f, wall_t, None, brick=brick, ylab=ylab)
            base = run(f, pol, er, sg, pec, irx, isrc)          # no joints, no groove
            er, sg, pec, irx, isrc, _ = build(f, wall_t, mortar, brick=brick, ylab=ylab)
            wall = run(f, pol, er, sg, pec, irx, isrc)          # the joints alone
            clutter = db(wall / base)
            line = f'  {f/1e9:.2f} GHz {"along " if pol == "TM" else "across"}: joints {clutter.max()-clutter.min():4.1f} dB p-p'
            iy = int(round(ylab / DX))
            for name, g, cab, cond in CASES:
                er, sg, pec, irx, isrc, _ = build(f, wall_t, mortar, brick=brick, groove=g, cable=cab,
                                                  conduit=cond, ylab=ylab)
                r = db(run(f, pol, er, sg, pec, irx, isrc) / wall)
                win = slice(iy - 40, iy + 41)
                line += f' | {name}: {r[win].min():+5.1f} / {r[win].max():+5.1f} dB'
            print(line, flush=True)

def table_avg(wall_t, mortar, pol, freqs, brick='brick', gd=0.03):
    """The same wall, the power averaged over several channels: does frequency diversity wash out
    the joints' interference while the cable's shadow, which is broadband, stays?"""
    ylab = 0.30 + 0.0375
    iy = int(round(ylab / DX)); win = slice(iy - 40, iy + 41)
    P = {k: 0 for k in ('base', 'wall', 'cable', 'groove')}
    for f in freqs:
        runs = {'base': build(f, wall_t, None, brick=brick, ylab=ylab),
                'wall': build(f, wall_t, mortar, brick=brick, ylab=ylab),
                'groove': build(f, wall_t, mortar, brick=brick, groove=(0.04, gd), ylab=ylab),
                'cable': build(f, wall_t, mortar, brick=brick, groove=(0.04, gd), cable=True, ylab=ylab)}
        for k, (er, sg, pec, irx, isrc, _) in runs.items():
            P[k] = P[k] + np.abs(run(f, pol, er, sg, pec, irx, isrc)) ** 2
    clutter = 10 * np.log10(P['wall'] / P['base'])
    g = 10 * np.log10(P['groove'] / P['wall']); c = 10 * np.log10(P['cable'] / P['wall'])
    c2 = 10 * np.log10(P['cable'] / P['groove'])
    print(f'  {len(freqs)} channels {freqs[0]/1e9:.2f}-{freqs[-1]/1e9:.2f} GHz, {"along " if pol == "TM" else "across"}: '
          f'joints {clutter.max()-clutter.min():4.1f} dB p-p | the empty groove {g[win].min():+5.1f} dB | '
          f'the cable in it {c[win].min():+5.1f} dB, against the empty groove {c2[win].min():+5.1f} dB', flush=True)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'validate':
        validate()
    elif len(sys.argv) in (6, 7, 8) and sys.argv[1] == 'avg':   # avg <mm> <mortar> <TM|TE> <band 24|55> [plaster] [groove depth mm]
        wall_t, mortar, pol, band = int(sys.argv[2]) / 1000, sys.argv[3], sys.argv[4], sys.argv[5]
        if len(sys.argv) >= 7:
            PLASTER = sys.argv[6]
        gd = int(sys.argv[7]) / 1000 if len(sys.argv) == 8 else 0.03
        freqs = [2.412e9, 2.442e9, 2.472e9] if band == '24' else [5.18e9, 5.32e9, 5.5e9, 5.66e9, 5.82e9]
        print(f'== brick {wall_t*1000:.0f} mm, {mortar}, {PLASTER}, groove {gd*1000:.0f} mm deep (the cable '
              f'{(PLASTER_T + gd/2)*1000:.0f} mm from the face), averaged over channels', flush=True)
        table_avg(wall_t, mortar, pol, freqs, gd=gd)
    elif len(sys.argv) in (4, 5):               # one wall: thickness in mm, mortar, brick [, plaster]
        wall_t, mortar, brick = int(sys.argv[1]) / 1000, sys.argv[2], sys.argv[3]
        if len(sys.argv) == 5:
            PLASTER = sys.argv[4]
        print(f'== {brick} {wall_t*1000:.0f} mm, 15 mm {PLASTER} each side, {mortar}', flush=True)
        table(wall_t, mortar, brick)
    else:
        for wall_t in (0.14, 0.29):
            for mortar in ('mortar_lo', 'mortar_hi'):
                print(f'== brick {wall_t*1000:.0f} mm, 15 mm plaster each side, {mortar}', flush=True)
                table(wall_t, mortar)
