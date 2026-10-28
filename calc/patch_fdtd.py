"""How much a wall pulls the 2.44 GHz patch off tune: a small 3D FDTD.

The patch of budget.py (29 x 37 mm on FR4 1.6 mm, er 4.4, tan d 0.02) over a full ground plane,
fed by a probe 8 mm in from one radiating edge; a homogeneous wall slab 30 mm thick in front of it
at a gap g. A Gaussian pulse 1.5-3.5 GHz is driven through the probe; the resonance is the peak
of the probe voltage's spectrum after the pulse. Absorbing sponge on all open sides. Needs numpy.

Run: python3 patch_fdtd.py <gap mm | none> <wall er> <wall sigma S/m> [patch width mm, default 37]
The ring of nine (array.py) needs the patch narrowed to 29 x 29 mm; the width is the fourth argument.

The match: python3 patch_fdtd.py s11 <gap mm | none> <wall er> <wall sigma> <width mm> <length mm>
<feed inset mm> [<cover er> <cover sigma>] [nowall] [sub=<mm>]. The probe is a current source; the
input impedance is the probe's voltage over that current, S11 against 50 ohm; the gap filled with
the cover (a solid spacer on the patch) if one is given, the wall left out with 'nowall', and the
substrate made thinner with sub= (four cells across it, whatever its thickness) — a 4-layer board
with the patch on layer 1 and its ground on layer 3 has about 1.3 mm.
"""
import sys
import numpy as np

C0 = 299792458.0; EPS0 = 8.854187817e-12; MU0 = 4e-7 * np.pi
DX = DY = 1e-3; DZ = 0.4e-3
DT = 0.99 / (C0 * np.sqrt(1 / DX**2 + 1 / DY**2 + 1 / DZ**2))
L, W, H = 0.029, 0.037, 1.6e-3
ER_SUB, TAN_SUB, F0 = 4.4, 0.02, 2.44e9
NSP = 12                                   # sponge cells

def run(gap, er_w, sg_w, t_end=16e-9, W=W, cover=None, inset=8, length=L, wall=True, series=False):
    nx = ny = 90
    nsub = int(round(H / DZ))              # 4 cells of substrate
    ngap = 0 if gap is None else int(round(gap / DZ))
    nwall = 0 if gap is None else int(round(0.030 / DZ))
    nz = nsub + ngap + nwall + int(round(0.008 / DZ)) + NSP
    eps = np.ones((nx, ny, nz), np.float32); sig = np.zeros((nx, ny, nz), np.float32)
    eps[:, :, :nsub] = ER_SUB
    sig[:, :, :nsub] = 2 * np.pi * F0 * EPS0 * ER_SUB * TAN_SUB
    if gap is not None and wall:
        eps[:, :, nsub + ngap:nsub + ngap + nwall] = er_w
        sig[:, :, nsub + ngap:nsub + ngap + nwall] = sg_w
    if gap is not None and cover is not None:
        eps[:, :, nsub:nsub + ngap], sig[:, :, nsub:nsub + ngap] = cover
    # sponge: graded conductivity on x, y, z-top faces, matched magnetic loss
    prof = np.zeros((nx, ny, nz), np.float32)
    g = (np.arange(NSP, 0, -1) / NSP) ** 2
    smax = 0.8 * 4 / (376.73 * NSP * DX)
    px = np.zeros(nx); px[:NSP] = g; px[-NSP:] = g[::-1]
    pz = np.zeros(nz); pz[-NSP:] = g[::-1]
    prof += smax * np.maximum(np.maximum(px[:, None, None], px[None, :, None]), pz[None, None, :])
    sig_e = sig + prof * eps
    sig_m = prof * MU0 / EPS0
    def ce(axis):
        e = eps; s = sig_e
        e = 0.5 * (e + np.roll(e, -1, axis)); s = 0.5 * (s + np.roll(s, -1, axis))
        a = s * DT / (2 * EPS0 * e)
        return ((1 - a) / (1 + a)).astype(np.float32), (DT / (EPS0 * e) / (1 + a)).astype(np.float32)
    cax, cbx = ce(0); cay, cby = ce(1); caz, cbz = ce(2)
    am = sig_m * DT / (2 * MU0)
    dh, ch = ((1 - am) / (1 + am)).astype(np.float32), ((DT / MU0) / (1 + am)).astype(np.float32)
    Ex = np.zeros((nx, ny, nz), np.float32); Ey = np.zeros_like(Ex); Ez = np.zeros_like(Ex)
    Hx = np.zeros_like(Ex); Hy = np.zeros_like(Ex); Hz = np.zeros_like(Ex)
    cx, cy = nx // 2, ny // 2
    nl = int(round(length / DX))
    pl = slice(cx - nl // 2, cx - nl // 2 + nl)                          # x: the resonant length
    pw = slice(cy - int(W / DY / 2), cy + int(W / DY / 2) + 1)
    kp = nsub                                                           # the patch's plane
    xf = cx - nl // 2 + inset                                           # the feed, inset mm in
    nsteps = int(t_end / DT)
    t0, tau = 1.0e-9, 0.25e-9
    v = np.zeros(nsteps, np.float32); cur = np.zeros(nsteps)
    for n in range(nsteps):
        Hx[:, :-1, :-1] = dh[:, :-1, :-1] * Hx[:, :-1, :-1] - ch[:, :-1, :-1] * (
            (Ez[:, 1:, :-1] - Ez[:, :-1, :-1]) / DY - (Ey[:, :-1, 1:] - Ey[:, :-1, :-1]) / DZ)
        Hy[:-1, :, :-1] = dh[:-1, :, :-1] * Hy[:-1, :, :-1] - ch[:-1, :, :-1] * (
            (Ex[:-1, :, 1:] - Ex[:-1, :, :-1]) / DZ - (Ez[1:, :, :-1] - Ez[:-1, :, :-1]) / DX)
        Hz[:-1, :-1, :] = dh[:-1, :-1, :] * Hz[:-1, :-1, :] - ch[:-1, :-1, :] * (
            (Ey[1:, :-1, :] - Ey[:-1, :-1, :]) / DX - (Ex[:-1, 1:, :] - Ex[:-1, :-1, :]) / DY)
        Ex[:-1, 1:, 1:] = cax[:-1, 1:, 1:] * Ex[:-1, 1:, 1:] + cbx[:-1, 1:, 1:] * (
            (Hz[:-1, 1:, 1:] - Hz[:-1, :-1, 1:]) / DY - (Hy[:-1, 1:, 1:] - Hy[:-1, 1:, :-1]) / DZ)
        Ey[1:, :-1, 1:] = cay[1:, :-1, 1:] * Ey[1:, :-1, 1:] + cby[1:, :-1, 1:] * (
            (Hx[1:, :-1, 1:] - Hx[1:, :-1, :-1]) / DZ - (Hz[1:, :-1, 1:] - Hz[:-1, :-1, 1:]) / DX)
        Ez[1:, 1:, :-1] = caz[1:, 1:, :-1] * Ez[1:, 1:, :-1] + cbz[1:, 1:, :-1] * (
            (Hy[1:, 1:, :-1] - Hy[:-1, 1:, :-1]) / DX - (Hx[1:, 1:, :-1] - Hx[1:, :-1, :-1]) / DY)
        t = n * DT
        cur[n] = np.exp(-((t - t0) / tau) ** 2) * np.sin(2 * np.pi * F0 * (t - t0))   # the probe's current, A
        Ez[xf, cy, :nsub] -= cbz[xf, cy, :nsub] * np.float32(cur[n]) / (DX * DY)
        Ex[:, :, 0] = 0; Ey[:, :, 0] = 0                                # the ground plane
        Ex[pl, pw, kp] = 0; Ey[pl, pw, kp] = 0                          # the patch
        v[n] = Ez[xf, cy, :nsub].sum() * DZ
    tt = np.arange(nsteps) * DT
    if series:
        return v.astype(float), cur
    late = tt > t0 + 4 * tau
    sig_t = v[late] * np.hanning(late.sum())
    nfft = 1 << 18
    sp = np.abs(np.fft.rfft(sig_t, nfft)); fr = np.fft.rfftfreq(nfft, DT)
    band = (fr > 1.5e9) & (fr < 3.5e9)
    return fr[band][np.argmax(sp[band])]

def s11(gap, er_w, sg_w, W, length, inset, cover=None, wall=True, t_end=30e-9):
    v, i = run(gap, er_w, sg_w, t_end=t_end, W=W, cover=cover, inset=inset, length=length, wall=wall, series=True)
    nfft = 1 << 18
    fr = np.fft.rfftfreq(nfft, DT); band = (fr > 2.0e9) & (fr < 3.0e9)
    Z = -np.fft.rfft(v, nfft)[band] / np.fft.rfft(i, nfft)[band]; f = fr[band]
    S = 20 * np.log10(np.abs((Z - 50) / (Z + 50)))
    k = int(np.argmin(S)); lo = hi = k
    while lo > 0 and S[lo - 1] < -10: lo -= 1
    while hi < S.size - 1 and S[hi + 1] < -10: hi += 1
    bw = f[hi] - f[lo] if S[k] < -10 else 0.0
    ch = {c: S[np.argmin(np.abs(f - c))] for c in (2.412e9, 2.442e9, 2.472e9)}
    return f[k], S[k], bw, Z[k], ch

if __name__ == '__main__':
    if sys.argv[1] == 's11':
        a = sys.argv[2:]
        gap = None if a[0] == 'none' else float(a[0]) / 1000
        er_w, sg_w, w, length, inset = float(a[1]), float(a[2]), float(a[3]) / 1000, float(a[4]) / 1000, int(a[5])
        rest = a[6:]; wall = 'nowall' not in rest; rest = [r for r in rest if r != 'nowall']
        for r in [r for r in rest if r.startswith('sub=')]:
            H = float(r[4:]) / 1000; DZ = H / 4
            DT = 0.99 / (C0 * np.sqrt(1 / DX**2 + 1 / DY**2 + 1 / DZ**2))
        rest = [r for r in rest if not r.startswith('sub=')]
        cover = (float(rest[0]), float(rest[1])) if rest else None
        f0, smin, bw, z, ch = s11(gap, er_w, sg_w, w, length, inset, cover=cover, wall=wall)
        what = (f'patch {length*1000:.0f} x {w*1000:.0f} mm, feed {inset} mm in, '
                + (f'FR4 {H*1000:.2f} mm, ' if H != 1.6e-3 else '')
                + ('no wall' if gap is None or not wall else f'wall er {er_w}, sigma {sg_w}') +
                (f', gap {gap*1000:.0f} mm' if gap is not None else '') +
                (f' filled with er {cover[0]}' if cover else ''))
        print(f'{what}: best match {f0/1e9:.3f} GHz, S11 {smin:.1f} dB, Z {z.real:.0f}{z.imag:+.0f}j ohm, '
              f'-10 dB band {bw/1e6:.0f} MHz; at 2412/2442/2472 MHz ' + ' / '.join(f'{x:.1f}' for x in ch.values()) + ' dB', flush=True)
        sys.exit()
    gap = None if sys.argv[1] == 'none' else float(sys.argv[1]) / 1000
    er_w, sg_w = float(sys.argv[2]), float(sys.argv[3])
    w = float(sys.argv[4]) / 1000 if len(sys.argv) > 4 else W
    f = run(gap, er_w, sg_w, W=w)
    label = 'no wall' if gap is None else f'wall er {er_w}, sigma {sg_w} S/m, gap {gap*1000:.0f} mm'
    label = f'patch {L*1000:.0f} x {w*1000:.0f} mm, {label}'
    print(f'{label}: resonance {f/1e9:.3f} GHz', flush=True)
