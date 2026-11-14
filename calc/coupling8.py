"""How much one patch of the head of ten hears its neighbour: S21 between two patches, a 3D FDTD.

The concept's patch_fdtd.py (published) for two patches: the head's board (FR4 1.28 mm between
the patch and its ground), the patch 30 x 37 mm fed 7 mm in (patch8.out), 15 mm of air, then
lime-cement plaster 30 mm thick (er 5.24, sigma 0.093) — or no wall, the head lifted, as when
the chips calibrate one another. Port 1 is driven through 50 ohm, port 2 is loaded with 50 ohm;
S21 = 2 V2 / (50 I1).

Two cases, both simplified to a square grid:
  'ring'  — two neighbours of the ring, side by side, 53.2 mm apart centre to centre. In the head
            they are also turned 45 deg to each other, which couples less; so this is the worse case.
  'mid'   — a ring patch and Předseda (a 30 mm square), in line along the ring patch's resonant
            length, 69.5 mm centre to centre.

Run: python3 coupling8.py <ring | mid> <wall | nowall>      (minutes to an hour or two a case)
"""
import sys
import numpy as np
from ring8 import RING_R, N_RING, PATCH_L, PATCH_W, MID

C0 = 299792458.0; EPS0 = 8.854187817e-12; MU0 = 4e-7 * np.pi
DX = DY = 1e-3; H = 1.28e-3; DZ = H / 4
DT = 0.99 / (C0 * np.sqrt(1 / DX**2 + 1 / DY**2 + 1 / DZ**2))
ER_SUB, TAN_SUB, F0 = 4.4, 0.02, 2.44e9
NSP, INSET, R0 = 12, 7, 50.0
GAP, WALL = 0.015, (5.24, 0.093)

def layout(case):
    """Two patches as (x0, length, y0, width) in cells, and the grid's size."""
    m = NSP + 14
    if case == 'ring':
        pitch = int(round(2 * RING_R * np.sin(np.pi / N_RING) / DY))
        nl, nw = int(round(PATCH_L / DX)), int(round(PATCH_W / DY))
        nx, ny = 2 * m + nl, 2 * m + nw + pitch
        return nx, ny, [(m, nl, m, nw), (m, nl, m + pitch, nw)]
    nl, nw, nm = int(round(PATCH_L / DX)), int(round(PATCH_W / DY)), int(round(MID / DX))
    pitch = int(round(RING_R / DX))
    nx, ny = 2 * m + nl // 2 + pitch + nm // 2, 2 * m + nw
    yc = ny // 2
    return nx, ny, [(m, nl, yc - nw // 2, nw), (m + nl // 2 + pitch - nm // 2, nm, yc - nm // 2, nm)]

def run(case, wall, t_end=30e-9):
    nx, ny, P = layout(case)
    nsub, ngap, nwall = 4, int(round(GAP / DZ)), int(round(0.030 / DZ))
    nz = nsub + ngap + (nwall if wall else 0) + int(round(0.008 / DZ)) + NSP
    eps = np.ones((nx, ny, nz), np.float32); sig = np.zeros((nx, ny, nz), np.float32)
    eps[:, :, :nsub] = ER_SUB; sig[:, :, :nsub] = 2 * np.pi * F0 * EPS0 * ER_SUB * TAN_SUB
    if wall:
        eps[:, :, nsub + ngap:nsub + ngap + nwall], sig[:, :, nsub + ngap:nsub + ngap + nwall] = WALL
    feeds = [(x0 + INSET, y0 + w // 2) for x0, l, y0, w in P]
    for k, (xf, yf) in enumerate(feeds):                 # 50 ohm across each probe, spread over its cells
        sig[xf, yf, :nsub] += (nsub * DZ) / (R0 * DX * DY)
    g = (np.arange(NSP, 0, -1) / NSP) ** 2; smax = 0.8 * 4 / (376.73 * NSP * DX)
    px = np.zeros(nx); px[:NSP] = g; px[-NSP:] = g[::-1]
    py = np.zeros(ny); py[:NSP] = g; py[-NSP:] = g[::-1]
    pz = np.zeros(nz); pz[-NSP:] = g[::-1]
    prof = (smax * np.maximum(np.maximum(px[:, None, None], py[None, :, None]), pz[None, None, :])).astype(np.float32)
    sig_e = sig + prof * eps; sig_m = prof * MU0 / EPS0
    def ce(axis):
        e = 0.5 * (eps + np.roll(eps, -1, axis)); s = 0.5 * (sig_e + np.roll(sig_e, -1, axis))
        if axis == 2:                                    # the probes' resistors sit on Ez exactly
            e, s = eps, sig_e
        a = s * DT / (2 * EPS0 * e)
        return ((1 - a) / (1 + a)).astype(np.float32), (DT / (EPS0 * e) / (1 + a)).astype(np.float32)
    cax, cbx = ce(0); cay, cby = ce(1); caz, cbz = ce(2)
    am = sig_m * DT / (2 * MU0)
    dh, ch = ((1 - am) / (1 + am)).astype(np.float32), ((DT / MU0) / (1 + am)).astype(np.float32)
    Ex = np.zeros((nx, ny, nz), np.float32); Ey, Ez, Hx, Hy, Hz = (np.zeros_like(Ex) for _ in range(5))
    nsteps = int(t_end / DT); t0, tau = 1.0e-9, 0.25e-9
    v2 = np.zeros(nsteps); cur = np.zeros(nsteps)
    (x1, y1), (x2, y2) = feeds
    for n in range(nsteps):
        Hx[:, :-1, :-1] = dh[:, :-1, :-1] * Hx[:, :-1, :-1] - ch[:, :-1, :-1] * ((Ez[:, 1:, :-1] - Ez[:, :-1, :-1]) / DY - (Ey[:, :-1, 1:] - Ey[:, :-1, :-1]) / DZ)
        Hy[:-1, :, :-1] = dh[:-1, :, :-1] * Hy[:-1, :, :-1] - ch[:-1, :, :-1] * ((Ex[:-1, :, 1:] - Ex[:-1, :, :-1]) / DZ - (Ez[1:, :, :-1] - Ez[:-1, :, :-1]) / DX)
        Hz[:-1, :-1, :] = dh[:-1, :-1, :] * Hz[:-1, :-1, :] - ch[:-1, :-1, :] * ((Ey[1:, :-1, :] - Ey[:-1, :-1, :]) / DX - (Ex[:-1, 1:, :] - Ex[:-1, :-1, :]) / DY)
        Ex[:-1, 1:, 1:] = cax[:-1, 1:, 1:] * Ex[:-1, 1:, 1:] + cbx[:-1, 1:, 1:] * ((Hz[:-1, 1:, 1:] - Hz[:-1, :-1, 1:]) / DY - (Hy[:-1, 1:, 1:] - Hy[:-1, 1:, :-1]) / DZ)
        Ey[1:, :-1, 1:] = cay[1:, :-1, 1:] * Ey[1:, :-1, 1:] + cby[1:, :-1, 1:] * ((Hx[1:, :-1, 1:] - Hx[1:, :-1, :-1]) / DZ - (Hz[1:, :-1, 1:] - Hz[:-1, :-1, 1:]) / DX)
        Ez[1:, 1:, :-1] = caz[1:, 1:, :-1] * Ez[1:, 1:, :-1] + cbz[1:, 1:, :-1] * ((Hy[1:, 1:, :-1] - Hy[:-1, 1:, :-1]) / DX - (Hx[1:, 1:, :-1] - Hx[1:, :-1, :-1]) / DY)
        t = n * DT
        cur[n] = np.exp(-((t - t0) / tau) ** 2) * np.sin(2 * np.pi * F0 * (t - t0))
        Ez[x1, y1, :nsub] -= cbz[x1, y1, :nsub] * np.float32(cur[n]) / (DX * DY)
        Ex[:, :, 0] = 0; Ey[:, :, 0] = 0
        for x0, l, y0, w in P:
            Ex[x0:x0 + l, y0:y0 + w, nsub] = 0; Ey[x0:x0 + l, y0:y0 + w, nsub] = 0
        v2[n] = Ez[x2, y2, :nsub].sum() * DZ
    nfft = 1 << 18
    fr = np.fft.rfftfreq(nfft, DT); band = (fr > 2.3e9) & (fr < 2.6e9)
    S21 = 20 * np.log10(np.abs(2 * np.fft.rfft(v2, nfft)[band] / (R0 * np.fft.rfft(cur, nfft)[band])) + 1e-30)
    f = fr[band]
    ch3 = ' / '.join(f'{S21[np.argmin(np.abs(f - c))]:.1f}' for c in (2.412e9, 2.442e9, 2.472e9))
    return f'{case}, {"wall" if wall else "no wall, the head lifted"}: S21 at 2412/2442/2472 MHz {ch3} dB; the most in 2.3-2.6 GHz {S21.max():.1f} dB at {f[np.argmax(S21)]/1e9:.3f} GHz'

if __name__ == '__main__':
    print(run(sys.argv[1], sys.argv[2] == 'wall'), flush=True)
