"""Acoustic camera, a rough check: what a sparse array of N microphones draws.

Delay-and-sum, one frequency at a time, a point source on the axis. For each N and frequency:
the spot's width (-3 dB, across) and the highest ghost (side lobe) below the main peak.
Microphones on a sunflower spiral filling a disc; the board's aperture and the distance below.
Rough: free field, ideal microphones, no calibration error, no reflections from the wall.
"""
import numpy as np

C = 343.0            # speed of sound in air, m/s
APERTURE = 0.20      # board, diameter of the disc the microphones fill, m
DIST = 0.30          # board to wall (the tap mode), m
HALF = 0.30          # half-width of the wall plane looked at, m (±45° from 0.30 m)
GRID = 241


def spiral(n, d):
    k = np.arange(n) + 0.5
    r = d / 2 * np.sqrt(k / n)
    a = k * np.pi * (3 - np.sqrt(5))
    return np.c_[r * np.cos(a), r * np.sin(a), np.zeros(n)]


def spiral_hole(n, d, hole=0.05):
    """The sunflower with its middle left free for the camera (hole: its diameter)."""
    k = np.arange(n) + 0.5
    r = np.sqrt((hole / 2) ** 2 + ((d / 2) ** 2 - (hole / 2) ** 2) * k / n)
    a = k * np.pi * (3 - np.sqrt(5))
    return np.c_[r * np.cos(a), r * np.sin(a), np.zeros(n)]


def honeycomb(n, d, hole=0.05):
    """A regular hexagonal lattice, the n points nearest the middle outside the camera's hole,
    scaled to fill the board."""
    pts = [(i + j / 2, j * np.sqrt(3) / 2) for i in range(-8, 9) for j in range(-8, 9)]
    pts = np.array([p for p in pts if np.hypot(*p) > 0.5])
    pts = pts[np.argsort(np.hypot(pts[:, 0], pts[:, 1]))][:n]
    r = np.hypot(pts[:, 0], pts[:, 1])
    pts *= (d / 2) / r.max()
    return np.c_[pts, np.zeros(n)]


def clusters(groups, per, d, hole=0.05, size=0.03):
    """groups of per microphones (one converter each), the groups' centres on a sunflower, each
    group a small square turned by its own angle."""
    c = spiral_hole(groups, d - size, hole + size)
    out = []
    for g, (x, y, _) in enumerate(c):
        a0 = g * 2.39996
        for m in range(per):
            a = a0 + 2 * np.pi * m / per
            out.append((x + size / 2 * np.cos(a), y + size / 2 * np.sin(a), 0))
    return np.array(out)


def psf(mics, f, z, half):
    x = np.linspace(-half, half, GRID)
    X, Y = np.meshgrid(x, x)
    pts = np.stack([X, Y, np.full_like(X, z)], -1)          # scan points
    src = np.array([0, 0, z])
    k = 2 * np.pi * f / C
    rs = np.linalg.norm(mics - src, axis=1)                  # source to each mic
    rp = np.linalg.norm(pts[..., None, :] - mics, axis=-1)   # scan point to each mic
    b = np.abs(np.exp(1j * k * (rp - rs)).sum(-1)) ** 2
    b /= b.max()
    R = np.hypot(X, Y)
    return R, 10 * np.log10(b + 1e-12)


def measure(R, db, half=HALF):
    edges = np.linspace(0, R.max(), 200)
    idx = np.digitize(R, edges)
    prof = np.array([db[idx == i].max() if np.any(idx == i) else -120 for i in range(1, len(edges))])
    w3 = 2 * edges[np.argmax(prof < -3)]                      # -3 dB width, across
    i = 1
    while i < len(prof) - 1 and not (prof[i] <= prof[i - 1] and prof[i] <= prof[i + 1]):
        i += 1                                                # first null of the main lobe
    inside = R <= half                                        # a circle, the field looked at
    side = db[(R > edges[i]) & inside].max() if i < len(prof) - 1 else float("nan")
    return w3, side


def psf_band(mics, f1, f2, z, half, step=1000):
    """The map averaged over a band: a broadband source (a leak's jet) keeps its peak, while the
    ghosts move with frequency and are smeared."""
    acc = None
    for f in np.arange(f1, f2 + 1, step):
        R, db = psf(mics, f, z, half)
        p = 10 ** (db / 10)
        acc = p if acc is None else acc + p
    acc /= acc.max()
    return R, 10 * np.log10(acc + 1e-12)


BAND = [  # leaks: (microphones, board m, distance m, half-field m, band Hz)
    (16, APERTURE, 3.0, 1.5, (25000, 45000)),
    (16, 0.10, 3.0, 1.5, (25000, 45000)),
    (32, APERTURE, 3.0, 1.5, (25000, 45000)),
    (64, APERTURE, 3.0, 1.5, (25000, 45000)),
    (16, APERTURE, 3.0, 1.5, (20000, 60000)),
]

CASES = [  # (label, microphones, board m, distance m, half-field m, f Hz)
    *[("tap", n, APERTURE, DIST, HALF, f) for n in (8, 16, 64) for f in (1300, 5000, 20000)],
    ("tap, small board", 16, 0.10, DIST, HALF, 20000),
    ("tap, held close", 16, APERTURE, 0.15, 0.15, 1300),
    ("leak", 16, APERTURE, 3.0, 1.5, 40000),
    ("leak", 64, APERTURE, 3.0, 1.5, 40000),
]

if __name__ == "__main__":
    print("case               N  board  dist   f kHz  spot -3 dB  highest ghost")
    for lab, n, ap, z, half, f in CASES:
        R, db = psf(spiral(n, ap), f, z, half)
        w, s = measure(R, db, half)
        print(f"{lab:17s} {n:2d}  {ap*100:3.0f} cm {z*100:4.0f} cm {f/1000:5.1f}  {w*100:6.1f} cm   {s:6.1f} dB")
    print("\nleaks, the map averaged over a band")
    print("N  board  dist   band kHz   spot -3 dB  highest ghost")
    for n, ap, z, half, (f1, f2) in BAND:
        R, db = psf_band(spiral(n, ap), f1, f2, z, half)
        w, g = measure(R, db, half)
        print(f"{n:2d}  {ap*100:3.0f} cm {z*100:4.0f} cm  {f1/1000:3.0f}-{f2/1000:3.0f}   {w*100:6.1f} cm   {g:6.1f} dB")
    print("\n32 microphones, the camera in the middle; leaks 25-45 kHz at 3 m, 20 cm board")
    print("layout                  spot -3 dB  highest ghost")
    for lab, m in (("sunflower, hole 5 cm", spiral_hole(32, APERTURE)),
                   ("honeycomb, hole", honeycomb(32, APERTURE)),
                   ("8 groups of 4", clusters(8, 4, APERTURE)),
                   ("4 groups of 8", clusters(4, 8, APERTURE, size=0.05))):
        R, db = psf_band(m, 25000, 45000, 3.0, 1.5)
        w, g = measure(R, db, 1.5)
        print(f"{lab:22s}  {w*100:6.1f} cm   {g:6.1f} dB")
