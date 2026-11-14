"""The principle without a shared clock: every receiver on its own crystal. Level 4.

What a receiver gives without a common clock: for every frame the channel it measured, whose phase
is worthless — each chip's oscillator runs at its own frequency, so the phase between two receivers
is new in every frame. What is left is the amplitude, if the gain is held fixed. This script makes
the reports as such a head would: each receiver's gain a few dB off, a random phase in every frame
for every receiver, and the sender's power and the room's fading changing from frame to frame by
a few dB, the same for all receivers. Then it draws the picture from the amplitudes alone, three ways:

  levelled      each frame set against the others on the same frame (the sender falls out); each
                receiver set against its own circle over a whole turn (its gain falls out)
  focused       the same, carried back through the wall as an in-line hologram: Iskra's own wave is
                the reference, so the change in amplitude is the part of the cable's wave in step with
                it, and that part can be focused without any phase of ours
  self-scaled   no levelling at all: in each receiver, the ratio of the upright frame to the level one, which
                follow each other within a millisecond at the same gain — the receiver's gain cancels

The wall, the head and the turn are picture.py's (the head of ten, the rod mid-way out).

Run: python3 nosync.py > nosync.out   (writes nosync.png)
"""
import math
import numpy as np
from scipy.ndimage import gaussian_filter
import picture as p

def reports(fields, kind='mid', seed=5):
    cx, cy, phi = p.poses(kind, 1)
    px, py, S, M = p.measure(fields, cx, cy, phi, uncalibrated=True)
    rng = np.random.default_rng(seed); n, m = S.shape
    for V in (S, M):                                   # no shared clock: a new phase in every frame, every receiver
        V *= np.exp(1j * rng.uniform(0, 2 * np.pi, (n, m)))
        V *= 10 ** (rng.normal(0, 2, (n, 1)) / 20)     # the sender and the room, the same for all on a frame
    return phi, np.abs(S), np.abs(M)                   # only the amplitudes are kept

def placed(phi, kind='mid'):
    c, s = np.cos(phi)[:, None], np.sin(phi)[:, None]
    q = p.AXIS[kind]; lx, ly = q * math.cos(p.ROD_AT), q * math.sin(p.ROD_AT)
    hx, hy = p.HEAD_XY[:, 0] - lx, p.HEAD_XY[:, 1] - ly
    return c * hx - s * hy, s * hx + c * hy, phi[:, None] + p.HEAD_PSI

def levelled(fields, depth=None):
    phi, A, B = reports(fields)
    px, py, psi = placed(phi)
    S, M = p.level(psi, A.astype(complex), B.astype(complex), phase=False)
    a, b, c, seen = p.fit(px, py, psi, S, M, phase=False)
    if depth:
        a, b, c = p.focus(a, b, c, seen, depth)
    img = p.darker(a, b, c); img[~seen] = np.nan
    return img

def self_scaled(fields):
    """log(|S| / |M|) in each receiver, against what a bare wall would give (|cot psi|), weighted
    where both senders reach the patch; the common factor of the two senders taken out by the median."""
    phi, A, B = reports(fields)
    px, py, psi = placed(phi)
    w = np.sin(2 * psi) ** 2
    with np.errstate(divide='ignore', invalid='ignore'):
        q = np.log(A / B) - np.log(np.abs(np.cos(psi) / np.sin(psi)))
    q = np.where(w > 0.1, q, 0.0)
    q -= np.median(q[w > 0.5])
    i = np.rint((py + p.HALF) / p.PX).astype(int); j = np.rint((px + p.HALF) / p.PX).astype(int)
    ok = (i >= 0) & (i < p.NG) & (j >= 0) & (j < p.NG) & (w > 0.1); idx = (i * p.NG + j)[ok]
    g = lambda v: gaussian_filter(np.bincount(idx, v[ok], p.NG * p.NG).reshape(p.NG, p.NG), 2.0)
    W = g(w); img = -8.686 * np.abs(g(w * q) / (W + 1e-9))   # a dip in either sender shows dark
    img[W < 0.05 * W.max()] = np.nan
    return img

if __name__ == '__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    g = p.grain()
    deep = ('one cable, 10 cm deep', [dict(line=[(0.04, -0.4), (0.04, 0.4)], a=p.CABLE, d=0.10)])
    scenes = list(p.SCENES[:5]) + [deep, p.SCENES[5]]
    ways = [('levelled', lambda f, d: levelled(f)), ('focused', lambda f, d: levelled(f, d)), ('self-scaled', lambda f, d: self_scaled(f))]
    print('no shared clock: amplitudes only; gains 3 dB off, a random phase every frame for every receiver,')
    print('the sender and the room changing 2 dB from frame to frame; the head of ten turned once about the rod mid-way out')
    print('how far the object stands out / the spread of the rest, dB')
    print(f'  {"":38s}' + ''.join(f'{w:>16s}' for w, _ in ways))
    fig, axs = plt.subplots(len(scenes), 4, figsize=(6.4, 1.6 * len(scenes)), dpi=60)
    ext = [-p.HALF * 100, p.HALF * 100] * 2
    for r, (name, objs) in enumerate(scenes):
        fields = tuple(p.seen_by_a_patch(f * g) for f in p.tensor(objs))
        a, b, c = p.tensor(objs)
        axs[r, 0].imshow(p.darker(a[::2, ::2], b[::2, ::2], c[::2, ::2]), cmap='gray', vmin=-8, vmax=2, origin='lower', extent=ext)
        axs[r, 0].set_ylabel(name, fontsize=5)
        d = objs[0]['d'] if objs else 0.03
        line = f'  {name:38s}'
        for k, (word, fn) in enumerate(ways):
            img = fn(fields, d)
            lo, hi = (-8, 2) if word != 'self-scaled' else (-4, 0)
            axs[r, k + 1].imshow(img, cmap='gray', vmin=lo, vmax=hi, origin='lower', extent=ext)
            axs[r, k + 1].set_facecolor('#c8d4e8')
            if r == 0:
                axs[r, k + 1].set_title(word, fontsize=6)
            o, s = p.stands_out(img, objs)
            line += f'{o:+8.1f} /{s:4.1f}  '
        print(line)
    for ax in axs.flat:
        ax.set_xticks([]); ax.set_yticks([])
    axs[0, 0].set_title('in the wall', fontsize=6)
    fig.tight_layout(pad=0.3); fig.savefig('nosync.png')
