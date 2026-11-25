"""NIC-Sluchalo (Netopýr): the 32 microphones' places on the back of the box.

The owner, 25 Nov 2026: the board as big as the box; 32 and done ("32 a hotovo"). Four
quadrants (the petals), 8 microphones each on its PCMD3180. An irregular scatter, as handheld
imagers have, searched for low ghosts.

The map is computed far-field (at 10 m the curvature over 16 cm is ~1 mm, negligible), in
direction cosines u, v over the camera's view, averaged over the leak band; the main lobe is an
ellipse (the box is wider than tall), the ghost the highest point outside it.

    python3 layout.py [width_cm height_cm] [seed]     -> layout_<w>x<h>.csv, layout_<w>x<h>.png
"""
import sys
import numpy as np

C = 343.0
BAND = np.arange(25000, 45001, 2000)  # the leaks, Hz
UMAX = 0.40                           # ±22° — the map's half-field, about OV5647's height
NU = 121                              # map points a side, in the search
HOLE = 0.050                          # the camera's hole, m (diameter)
GAP = 0.008                           # the least distance between two microphones, m
MARGIN = 0.004                        # from the board's edge, m


def beam(xy, nu=NU):
    """Band-averaged delay-and-sum map, far field, normalised to 0 dB at the axis."""
    u = np.linspace(-UMAX, UMAX, nu)
    acc = np.zeros((nu, nu))
    for f in BAND:
        k = 2 * np.pi * f / C
        ax = np.exp(1j * k * np.outer(u, xy[:, 0]))      # (u, m)
        ay = np.exp(1j * k * np.outer(xy[:, 1], u))      # (m, v)
        acc += np.abs(ax @ ay) ** 2                      # rows u, columns v
    acc /= acc.max()
    return u, 10 * np.log10(acc + 1e-12)


def judge(xy, nu=NU):
    """(-3 dB width across, up, in u; the highest ghost, dB)."""
    u, db = beam(xy, nu)
    c = len(u) // 2

    def half(p):
        i = c
        while i < len(p) - 1 and p[i] > -3:
            i += 1
        return u[i] - u[c]

    wx, wy = half(db[:, c]), half(db[c, :])
    U, V = np.meshgrid(u, u, indexing="ij")
    out = (U / (2 * wx)) ** 2 + (V / (2 * wy)) ** 2 > 1
    return 2 * wx, 2 * wy, db[out].max()


def ok(xy, i, w, h):
    x, y = xy[i]
    if abs(x) > w / 2 - MARGIN or abs(y) > h / 2 - MARGIN or np.hypot(x, y) < HOLE / 2 + GAP / 2:
        return False
    d = np.hypot(*(xy - xy[i]).T)
    d[i] = 1
    return d.min() >= GAP


QUAD = np.array([(1, 1), (-1, 1), (-1, -1), (1, -1)])


def start(w, h, rng):
    xy = np.zeros((N, 2))
    for i in range(N):
        sx, sy = QUAD[i // PER]
        while True:
            xy[i] = sx * rng.uniform(0, w / 2), sy * rng.uniform(0, h / 2)
            if ok(xy[: i + 1], i, w, h):
                break
    return xy


PER = 8                                                  # microphones a petal
N = 4 * PER


def cost(xy):
    return judge(xy)[2]


def search(w, h, seed=1, steps=20000):
    rng = np.random.default_rng(seed)
    xy = start(w, h, rng)
    best = cost(xy)
    for t in range(steps):
        i = rng.integers(N)
        old = xy[i].copy()
        step = 0.02 * (1 - t / steps) + 0.002
        xy[i] = old + rng.normal(0, step, 2)
        sx, sy = QUAD[i // PER]
        if np.sign(xy[i, 0]) != sx or np.sign(xy[i, 1]) != sy or not ok(xy, i, w, h):
            xy[i] = old
            continue
        c = cost(xy)
        if c <= best:
            best = c
        else:
            xy[i] = old
    return xy


def picture(xy, w, h, path):
    from PIL import Image, ImageDraw
    s = 4000                                              # px a metre
    W, H = int(w * s) + 40, int(h * s) + 60
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    cx, cy = W / 2, (H + 20) / 2
    d.rectangle((cx - w / 2 * s, cy - h / 2 * s, cx + w / 2 * s, cy + h / 2 * s), outline="gray")
    d.line((cx, cy - h / 2 * s, cx, cy + h / 2 * s), fill=(220, 220, 220))
    d.line((cx - w / 2 * s, cy, cx + w / 2 * s, cy), fill=(220, 220, 220))
    r = HOLE / 2 * s
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline="black")
    for i, (x, y) in enumerate(xy):
        px, py = cx + x * s, cy - y * s
        d.ellipse((px - 6, py - 6, px + 6, py + 6), fill="firebrick")
    d.text((10, 8), f"{w*100:.0f} x {h*100:.0f} cm: 32 microphones, four quadrants = four petals",
           fill="black")
    im.save(path)


if __name__ == "__main__":
    w = float(sys.argv[1]) / 100 if len(sys.argv) > 2 else 0.16
    h = float(sys.argv[2]) / 100 if len(sys.argv) > 2 else 0.10
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    xy = search(w, h, seed)
    name = f"layout_{w*100:.0f}x{h*100:.0f}"
    with open(name + ".csv", "w") as f:
        f.write("mic,petal,x_mm,y_mm\n")
        for i, (x, y) in enumerate(xy):
            f.write(f"{i+1},{i//PER+1},{x*1000:.1f},{y*1000:.1f}\n")
    picture(xy, w, h, name + ".png")
    d = np.hypot(*(xy[:, None] - xy[None]).transpose(2, 0, 1))
    d[d == 0] = 1
    wx, wy, g = judge(xy, 201)
    print(f"32: spot at 10 m {wx*1000:.0f} x {wy*1000:.0f} cm, ghost {g:.1f} dB")
    print(f"nearest two: {d.min()*1000:.1f} mm")
