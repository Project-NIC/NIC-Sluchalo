"""Samokritika: what the head can learn about its own receivers by sending between them.

When chip j sends and chip i listens, the report is  Y[i,j] = r[i] * H[i,j] * t[j]  — the listener's
own response r, the path between the two patches H, the sender's own response t. The picture
needs the r's against one another.

1. Nothing but "the path is the same both ways" (H[i,j] = H[j,i]) does not give them. For any
   numbers a[i], the set  r[i]*a[i],  t[i]*a[i],  H[i,j]/(a[i]*a[j])  explains the same reports.
   Sending both ways fixes only t[i]/r[i].
2. The ring's symmetry does: a path depends only on how many places apart the two patches are
   (four classes, for nine in the ring and for eight), and with H the same both ways the freedom
   left is one common factor — and, for a ring of an even number, one sign: every second receiver
   may be turned by half a turn against the others without the reports changing. That sign is
   settled by knowing roughly the phase of the path between neighbours, from the layout.
   Then the error is whatever breaks the symmetry. This script measures that: it makes the reports
   with paths that depart from their class by a given fraction, solves for r, t and the four
   classes, and compares r with the truth (the sign taken as known).

Předseda: among nine its square patch fits no symmetry of the ring. Among eight it does — four
patches face its sides and four its corners, so its paths are two unknown numbers, not nine; that
is reasoned, not run here.

Needs numpy. Run: python3 samokritika.py > samokritika.out
"""
import numpy as np

import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8          # the ring: eight as decided; 9 for the earlier head
CLASS = np.array([[min(abs(i - j), N - abs(i - j)) for j in range(N)] for i in range(N)])   # 0 on the diagonal
OFF = CLASS > 0

def reports(rng, asym, noise):
    r = 10 ** (rng.normal(0, 1, N) / 20) * np.exp(1j * rng.uniform(0, 2 * np.pi, N))
    t = 10 ** (rng.normal(0, 1, N) / 20) * np.exp(1j * rng.uniform(0, 2 * np.pi, N))
    h = np.array([0, 1.0, 0.35, 0.2, 0.15]) * np.exp(1j * rng.uniform(0, 2 * np.pi, 5))      # nearer couples more
    e = rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N)); e = (e + e.T) / 2     # the same both ways
    H = h[CLASS] * (1 + asym * e)
    Y = r[:, None] * H * t[None, :]
    Y = Y + noise * np.abs(Y[OFF]).mean() * (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2)
    return r, Y * OFF

def solve(Y, rng, tries=6):
    """Least squares for r, t and the four class paths, each in turn; the best of a few starts."""
    best = None
    for _ in range(tries):
        r = np.exp(1j * rng.uniform(0, 2 * np.pi, N)); t = np.exp(1j * rng.uniform(0, 2 * np.pi, N)); h = np.ones(5, complex)
        for _ in range(300):
            G = h[CLASS] * OFF
            r = (Y * np.conj(G * t[None, :])).sum(1) / (np.abs(G * t[None, :]) ** 2).sum(1)
            t = (Y * np.conj(G * r[:, None])).sum(0) / (np.abs(G * r[:, None]) ** 2).sum(0)
            P = r[:, None] * t[None, :]
            for d in range(1, 5):
                m = CLASS == d; h[d] = (Y[m] * np.conj(P[m])).sum() / (np.abs(P[m]) ** 2).sum()
        res = np.abs(Y - r[:, None] * h[CLASS] * OFF * t[None, :]).sum()
        if best is None or res < best[0]:
            best = (res, r.copy())
    return best[1]

def error(r, est):
    out = []
    for flip in ((1, -1) if N % 2 == 0 else (1,)):                   # the sign an even ring leaves open
        e = est * np.where(np.arange(N) % 2, flip, 1)
        c = (e * np.conj(r)).sum() / (np.abs(r) ** 2).sum()          # the common factor nothing can fix
        q = e / (c * r)
        out.append((np.degrees(np.sqrt(np.mean(np.angle(q) ** 2))), np.sqrt(np.mean((20 * np.log10(np.abs(q))) ** 2))))
    return min(out)

if __name__ == '__main__':
    rng = np.random.default_rng(3)
    print(f'the ring of {N}, each chip sending in turn; noise 1 % of a report')
    print('how far the paths depart from the ring\'s symmetry -> the receivers\' error after Samokritika')
    for asym in (0.0, 0.01, 0.03, 0.10, 0.30):
        res = np.array([error(r, solve(Y, rng)) for r, Y in (reports(rng, asym, 0.01) for _ in range(40))])
        print(f'  {asym*100:5.0f} %   phase {np.median(res[:, 0]):5.1f} deg   gain {np.median(res[:, 1]):5.2f} dB')
