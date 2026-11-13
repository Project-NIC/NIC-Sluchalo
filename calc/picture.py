"""The picture: what the head would draw of a wall, for each way of moving it.

A model, not a wall. A plane wave crosses a slab of brick; every object in it is a straight
cylinder whose field is the exact 2D series (as shadow.py; here also a metal core inside an air
conduit), laid along its line, the objects' fields simply added. The wall's own grain is a
made-up pattern of the size joints.out gives for dry mortar. Each of the eleven receivers takes
the field's component along its patch, averaged over the patch; every frame has its own unknown
phase, every receiver a small leftover error of gain and phase, and noise. Not in the model: the
wall's surface and the head's ground plane (head.py), the room, the wall's change of
polarization, other channels, 5 GHz.

The head is turned about its centre, about a rod a third of the way out, about a rod on the rim,
or slid. The picture is fitted pixel by pixel as a 2 x 2 field tensor and shows its darker
direction, in dB.

Needs numpy, scipy, matplotlib. Run: python3 picture.py > picture.out   (writes picture_*.png)
"""
import math
import numpy as np
from scipy.special import jv, jvp, yv, yvp, hankel2, h2vp
from scipy.ndimage import gaussian_filter, uniform_filter, map_coordinates
from materials import k as wavenumber

F = 2.437e9
K = complex(wavenumber('brick', F)); K_AIR = complex(wavenumber('air', F))
PATCH, PITCH = 0.029, 0.045                       # as in array.py
R9 = PITCH / (2 * math.sin(math.pi / 9))          # the ring's radius
RIM = 0.0835                                      # half the head (budget.py: 167 mm across)
TH = 2 * np.pi * np.arange(9) / 9
HEAD_XY = np.vstack([np.c_[R9 * np.cos(TH), R9 * np.sin(TH)], [[0, 0], [0, 0]]])   # nine + Předseda
HEAD_PSI = np.r_[TH, 0, np.pi / 2]                # each patch's direction: radial; the pair crossed
ROD_AT = math.radians(10)                         # the rod sits 10 deg off a patch's axis
FINE, HALF = 0.002, 0.2                           # the wall's grid, m
GX = np.arange(-HALF, HALF + 1e-9, FINE); X, Y = np.meshgrid(GX, GX)
PX = 0.005; PG = np.arange(-HALF, HALF + 1e-9, PX); NG = len(PG)   # the picture's grid

# ---------------------------------------------------------------- the wall

def coef(n, k, a, pol, k1=None, a0=None):
    x = k * a; J, Jp, H, Hp = jv(n, x), jvp(n, x), hankel2(n, x), h2vp(n, x)
    if k1 is None:                                # metal
        return -J / H if pol == 'TM' else -Jp / Hp
    y = k1 * a; Z, Zp = jv(n, y), jvp(n, y)
    if a0:                                        # a metal core of radius a0 on the axis
        y0 = k1 * a0
        g = jv(n, y0) / yv(n, y0) if pol == 'TM' else jvp(n, y0) / yvp(n, y0)
        Z, Zp = Z - g * yv(n, y), Zp - g * yvp(n, y)
    if pol == 'TM':
        return (k1 * Zp * J - k * Jp * Z) / (k * Z * Hp - k1 * Zp * H)
    return (k * Zp * J - k1 * Jp * Z) / (k1 * Z * Hp - k * Zp * H)

def profile(d, u, pol, a, k1=None, a0=None, k=K):
    """The field d behind a cylinder, across it, over the field with no cylinder."""
    def tot(x):
        rho = np.hypot(x, u); phi = np.arctan2(u, x); t = np.exp(-1j * k * x) * np.ones_like(u, dtype=complex)
        for n in range(-int(abs(k) * a) - 20, int(abs(k) * a) + 21):
            t += (1j) ** (-n) * coef(n, k, a, pol, k1, a0) * hankel2(n, k * rho) * np.exp(1j * n * phi)
        return t
    if pol == 'TM':
        return tot(d) / np.exp(-1j * k * d)
    h = 2e-4
    return (tot(d + h) - tot(d - h)) / (2 * h) / (-1j * k * np.exp(-1j * k * d))

def nearest(line, gx, gy):
    """Distance to a polyline and its direction there."""
    best = np.full(gx.shape, np.inf); ex = np.zeros(gx.shape); ey = np.zeros(gx.shape)
    for p0, p1 in zip(line[:-1], line[1:]):
        v = np.subtract(p1, p0); L = np.hypot(*v); e = v / L
        t = ((gx - p0[0]) * e[0] + (gy - p0[1]) * e[1]).clip(0, L)
        dist = np.hypot(gx - p0[0] - t * e[0], gy - p0[1] - t * e[1]); m = dist < best
        best[m] = dist[m]; ex[m] = e[0]; ey[m] = e[1]
    return best, ex, ey

def tensor(objs):
    """The field at the wall's near face as a tensor: xx, yy, xy (sender's direction -> field's)."""
    a = np.ones(X.shape, complex); b = a.copy(); c = np.zeros(X.shape, complex)
    uu = np.linspace(0, 0.6, 601)
    for o in objs:
        arg = (o['d'], uu, o['a'], o.get('k1'), o.get('a0'))
        par = profile(arg[0], arg[1], 'TM', *arg[2:]) - 1; perp = profile(arg[0], arg[1], 'TE', *arg[2:]) - 1
        dist, ex, ey = nearest(o['line'], X, Y)
        p = np.interp(dist, uu, par.real) + 1j * np.interp(dist, uu, par.imag)
        q = np.interp(dist, uu, perp.real) + 1j * np.interp(dist, uu, perp.imag)
        a += p * ex * ex + q * ey * ey; b += p * ey * ey + q * ex * ex; c += (p - q) * ex * ey
    return a, b, c

def grain(strength=1.0, seed=1):
    """The wall's own pattern: bed joints every 75 mm and a smooth mottle; about 3 dB peak to peak."""
    rng = np.random.default_rng(seed)
    def mottle():
        f = gaussian_filter(rng.standard_normal(X.shape), 0.015 / FINE); return f / f.std()
    joint = np.exp(-0.5 * (((Y + 0.03) % 0.075 - 0.0375) / 0.006) ** 2)
    return 10 ** (strength * (0.5 * mottle() - 1.5 * joint) / 20) * np.exp(1j * strength * (0.08 * mottle() + 0.15 * joint))

def seen_by_a_patch(f):
    n = round(PATCH / FINE)
    return uniform_filter(f.real, n) + 1j * uniform_filter(f.imag, n)

# ---------------------------------------------------------------- the head

def poses(kind, turns=3):
    """Head centre and angle for every pose; the rod, where there is one, stands at the origin."""
    if kind == 'slide':
        x = np.tile(np.linspace(-0.12, 0.12, 481), turns); return x, 0 * x, 0 * x
    p = {'centre': 0.0, 'third': R9 / 2, 'rim': RIM}[kind]
    phi = np.radians(np.arange(0, 360 * turns, 0.5))
    lx, ly = p * math.cos(ROD_AT), p * math.sin(ROD_AT)
    return -(np.cos(phi) * lx - np.sin(phi) * ly), -(np.sin(phi) * lx + np.cos(phi) * ly), phi

def measure(fields, cx, cy, phi, noise=0.015, seed=2):
    """What the eleven report for Serp's frame and for Molot's, pose by pose."""
    rng = np.random.default_rng(seed); n = len(phi)
    c, s = np.cos(phi)[:, None], np.sin(phi)[:, None]
    px = cx[:, None] + c * HEAD_XY[:, 0] - s * HEAD_XY[:, 1]
    py = cy[:, None] + s * HEAD_XY[:, 0] + c * HEAD_XY[:, 1]
    psi = phi[:, None] + HEAD_PSI
    rc = [(py + HALF) / FINE, (px + HALF) / FINE]
    a, b, x = [map_coordinates(f.real, rc, order=1, mode='nearest') + 1j * map_coordinates(f.imag, rc, order=1, mode='nearest')
               for f in fields]
    S = np.cos(psi) * a + np.sin(psi) * x; M = np.cos(psi) * x + np.sin(psi) * b
    left = 10 ** (rng.normal(0, 0.2, 11) / 20) * np.exp(1j * np.radians(rng.normal(0, 3, 11)))   # after Samokritika
    out = []
    for V in (S, M):
        V = V * left * np.exp(1j * rng.uniform(0, 2 * np.pi, (n, 1)))                          # each frame's phase
        out.append(V + noise * (rng.standard_normal(V.shape) + 1j * rng.standard_normal(V.shape)) / math.sqrt(2))
    return px, py, out[0], out[1]

def angle_from_sensor(phi):
    return phi + math.radians(0.5) * np.sin(phi + 1.0)       # a magnetic sensor's leftover non-linearity

def angle_from_radio(S, M):
    """Serp and Molot are linear, the nine patches radial: the ring's pattern turns with the head."""
    e = np.exp(-1j * TH); z = (S[:, :9] @ e) * np.conj(S[:, :9] @ e.conj()) - (M[:, :9] @ e) * np.conj(M[:, :9] @ e.conj())
    two = np.unwrap(np.angle(z)); return 0.5 * (two - two[0])

# ---------------------------------------------------------------- the picture

def fit(px, py, psi, S, M, phase=False, serp_only=False, blur=2.0):
    """Pixel by pixel the tensor (a, b, c) that explains the reports; None where the head never was."""
    cs, sn = np.cos(psi), np.sin(psi)
    if phase:
        s = S / ((S * cs).sum(1) / (cs ** 2).sum(1))[:, None]; m = M / ((M * sn).sum(1) / (sn ** 2).sum(1))[:, None]
    else:
        s = np.abs(S) * np.sign(cs) / ((np.abs(S) * np.abs(cs)).sum(1) / (cs ** 2).sum(1))[:, None]
        m = np.abs(M) * np.sign(sn) / ((np.abs(M) * np.abs(sn)).sum(1) / (sn ** 2).sum(1))[:, None]
    i = np.rint((py + HALF) / PX).astype(int); j = np.rint((px + HALF) / PX).astype(int)
    ok = (i >= 0) & (i < NG) & (j >= 0) & (j < NG); idx = (i * NG + j)[ok]
    def acc(v):
        v = np.broadcast_to(v, ok.shape)[ok]
        g = lambda w: gaussian_filter(np.bincount(idx, w, NG * NG).reshape(NG, NG), blur)
        return g(v.real) + 1j * g(v.imag) if np.iscomplexobj(v) else g(v)
    w2 = 0.0 if serp_only else 1.0
    Naa, Nbb, Nac, Nbc = acc(cs ** 2), acc(w2 * sn ** 2), acc(cs * sn), acc(w2 * cs * sn)
    Ncc = acc(sn ** 2 + w2 * cs ** 2); W = acc(np.ones_like(cs))
    ra, rb, rc = acc(cs * s), acc(w2 * sn * m), acc(sn * s + w2 * cs * m)
    eps = 0.03 * W + 1e-9
    N = np.zeros((NG, NG, 3, 3)); N[..., 0, 0] = Naa + eps; N[..., 1, 1] = Nbb + eps; N[..., 2, 2] = Ncc + eps
    N[..., 0, 2] = N[..., 2, 0] = Nac; N[..., 1, 2] = N[..., 2, 1] = Nbc
    r = np.stack([ra + eps, rb + eps, rc], -1)
    x = np.linalg.solve(N.astype(complex), r[..., None])[..., 0]
    return x[..., 0], x[..., 1], x[..., 2], W > 0.03 * W.max()

def darker(a, b, c):
    mean, rad = (a + b) / 2, np.sqrt(((a - b) / 2) ** 2 + c ** 2)
    return 20 * np.log10(np.minimum(np.abs(mean + rad), np.abs(mean - rad)) + 1e-6)

def focus(a, b, c, seen, d):
    """Carry the fitted field back through d of wall to where the object lies (needs the phase)."""
    P = 160; kr = K.real; f = 2 * np.pi * np.fft.fftfreq(P, PX); kz2 = kr ** 2 - f[None, :] ** 2 - f[:, None] ** 2
    back = np.where(kz2 > 0, np.exp(1j * (np.sqrt(np.abs(kz2)) - kr) * d), 0)
    soft = gaussian_filter(seen.astype(float), 2)
    def one(v, rest):
        z = np.zeros((P, P), complex); z[:NG, :NG] = (v - rest) * soft
        return np.fft.ifft2(np.fft.fft2(z) * back)[:NG, :NG] + rest
    return one(a, 1), one(b, 1), one(c, 0)

def draw(fields, kind, turns=3, phase=False, serp_only=False, radio=False, depth=None, noise=0.015):
    cx, cy, phi = poses(kind, turns)
    px, py, S, M = measure(fields, cx, cy, phi, noise / math.sqrt(1))
    est = phi if kind == 'slide' else angle_from_radio(S, M) if radio else angle_from_sensor(phi)
    err = math.degrees(np.sqrt(np.mean((est - phi) ** 2)))
    c, s = np.cos(est)[:, None], np.sin(est)[:, None]                    # where the head believes it is
    if kind != 'slide':
        p = {'centre': 0.0, 'third': R9 / 2, 'rim': RIM}[kind]; lx, ly = p * math.cos(ROD_AT), p * math.sin(ROD_AT)
        hx, hy = HEAD_XY[:, 0] - lx, HEAD_XY[:, 1] - ly
        px, py = c * hx - s * hy, s * hx + c * hy
    a, b, x, seen = fit(px, py, est[:, None] + HEAD_PSI, S, M, phase, serp_only)
    if depth:
        a, b, x = focus(a, b, x, seen, depth)
    img = darker(a, b, x); img[~seen] = np.nan
    return img, err

# ---------------------------------------------------------------- the walls

CABLE, PIPE = 0.0025, 0.011
SCENES = [
    ('one cable, upright, 3 cm deep', [dict(line=[(0.04, -0.4), (0.04, 0.4)], a=CABLE, d=0.03)]),
    ('a 60 mm conduit with a cable in it', [dict(line=[(0.03, -0.4), (0.03, 0.4)], a=0.03, k1=K_AIR, a0=0.004, d=0.05)]),
    ('two cables 4 cm apart', [dict(line=[(0.02, -0.4), (0.02, 0.4)], a=CABLE, d=0.03),
                               dict(line=[(0.06, -0.4), (0.06, 0.4)], a=CABLE, d=0.03)]),
    ('a cable that turns', [dict(line=[(-0.04, -0.4), (-0.04, 0.03), (0.4, 0.03)], a=CABLE, d=0.03)]),
    ('a 22 mm metal pipe, level', [dict(line=[(-0.4, -0.04), (0.4, -0.04)], a=PIPE, d=0.04)]),
    ('nothing: the wall alone', []),
]
MOVES = [('centre', 'turned about its centre'), ('third', 'about a rod a third out'),
         ('rim', 'about a rod on the rim'), ('slide', 'slid 24 cm')]

def stands_out(img, objs):
    """dB by which the object's pixels are darker than the rest, and the rest's own spread."""
    gx, gy = np.meshgrid(PG, PG); on = np.zeros(img.shape, bool)
    for o in objs:
        on |= nearest(o['line'], gx, gy)[0] < 0.008
    seen = ~np.isnan(img)
    if not (on & seen).any():
        return float('nan'), float('nan')
    rest = img[seen & ~on]
    return np.median(img[seen & on]) - np.median(rest), np.percentile(rest, 95) - np.percentile(rest, 5)

if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    ext = [-HALF * 100, HALF * 100] * 2
    def show(ax, img, title=None):
        ax.imshow(img, cmap='gray', vmin=-8, vmax=2, origin='lower', extent=ext); ax.set_xticks([]); ax.set_yticks([])
        ax.set_facecolor('#c8d4e8')
        if title: ax.set_title(title, fontsize=7)

    print(f'the model: brick, {F/1e9:.3f} GHz, wavelength in it {2*math.pi/K.real*1000:.0f} mm; ring radius {R9*1000:.1f} mm')
    for kind, word in MOVES[:3]:
        p = {'centre': 0.0, 'third': R9 / 2, 'rim': RIM}[kind]
        d = np.sort(np.hypot(HEAD_XY[:9, 0] - p * math.cos(ROD_AT), HEAD_XY[:9, 1] - p * math.sin(ROD_AT))) * 1000
        print(f'  {word:26s} the nine at ' + ', '.join(f'{v:.0f}' for v in d) + f' mm from the axis; Předseda at {p*1000:.0f}')

    g = grain(); walls = {}
    for name, objs in SCENES:
        a, b, c = tensor(objs); walls[name] = (a, b, c, tuple(seen_by_a_patch(f * g) for f in (a, b, c)))

    # figure 1: every wall, every way of moving; amplitude only, both senders, angle from a sensor, three turns
    fig, axs = plt.subplots(len(SCENES), 5, figsize=(8, 9.6), dpi=80)
    print('\n== amplitude only, Serp and Molot, three turns: how far the object stands out / the spread of the rest, dB')
    print(f'  {"":36s}' + ''.join(f'{w:>28s}' for _, w in MOVES))
    for r, (name, objs) in enumerate(SCENES):
        a, b, c, seen = walls[name]
        show(axs[r, 0], darker(a[::2, ::2], b[::2, ::2], c[::2, ::2]), 'in the wall (no grain)' if r == 0 else None)
        axs[r, 0].set_ylabel(name, fontsize=6); line = f'  {name:36s}'
        for q, (kind, word) in enumerate(MOVES):
            img, _ = draw(seen, kind); show(axs[r, q + 1], img, word if r == 0 else None)
            o, s = stands_out(img, objs); line += f'{o:+14.1f} /{s:5.1f}      '
        print(line)
    fig.tight_layout(pad=0.3); fig.savefig('picture_moves.png'); plt.close(fig)

    # the angle from the radio alone
    print('\n== the angle from the radio alone (Serp and Molot on the nine radial patches), rms error, degrees')
    for name, objs in SCENES:
        line = f'  {name:36s}'
        for kind, word in MOVES[:3]:
            line += f'{draw(walls[name][3], kind, radio=True)[1]:10.2f}'
        print(line)

    # figure 2: what each thing adds, on the cable that turns, the rod a third out and on the rim
    name = 'a cable that turns'; objs = SCENES[3][1]; seen = walls[name][3]
    deep = [dict(line=[(0.04, -0.4), (0.04, 0.4)], a=CABLE, d=0.10)]
    seen_deep = tuple(seen_by_a_patch(f * g) for f in tensor(deep))
    wet = tuple(seen_by_a_patch(f * grain(3.0)) for f in walls[name][:3])
    cases = [('Serp alone', seen, objs, dict(serp_only=True)),
             ('Serp and Molot', seen, objs, dict()),
             ('one turn', seen, objs, dict(turns=1)),
             ('angle from the radio', seen, objs, dict(radio=True)),
             ('with phase, focused 3 cm', seen, objs, dict(phase=True, depth=0.03)),
             ('cable 10 cm deep, amplitude', seen_deep, deep, dict()),
             ('the same, focused 10 cm', seen_deep, deep, dict(phase=True, depth=0.10)),
             ('grain three times stronger', wet, objs, dict()),
             ('the same, focused 3 cm', wet, objs, dict(phase=True, depth=0.03)),
             ('noise ten times higher', seen, objs, dict(noise=0.15))]
    fig, axs = plt.subplots(2, len(cases), figsize=(1.6 * len(cases), 3.6), dpi=80)
    print('\n== what each thing adds: stands out / spread, dB; and the angle\'s rms error, degrees')
    for r, kind in enumerate(('third', 'rim')):
        for q, (word, fields, ob, kw) in enumerate(cases):
            img, err = draw(fields, kind, **kw); show(axs[r, q], img, word if r == 0 else None)
            o, s = stands_out(img, ob); print(f'  {dict(MOVES)[kind]:26s} {word:30s} {o:+6.1f} /{s:5.1f}   angle {err:5.2f}')
        axs[r, 0].set_ylabel(dict(MOVES)[kind], fontsize=6)
    fig.tight_layout(pad=0.3); fig.savefig('picture_adds.png'); plt.close(fig)
