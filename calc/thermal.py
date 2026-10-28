"""Does a loaded cable show through the plaster? Run: python3 thermal.py (needs scipy)

A 2D section through a solid-brick wall 29 cm thick, a cable in a groove under the plaster. The
cable's I^2 R heat leaves through both faces into still room air. Taken as: brick and plaster one
homogeneous material, k 0.8 W/m K, density 1705 kg/m^3 (acoustics.py), specific heat 840 J/kg K;
the faces' combined convection and radiation h = 1/0.13 W/m^2 K (ISO 6946's inside surface
resistance, heat flowing horizontally). Copper at its IEC 60228 resistance, 12 % up for a conductor
at about 50 C. Gives the surface rise over the cable, its width, how soon it comes, and how
finely an 80 x 62 sensor finds the band's middle (pixels 1 cm on the wall, 150 mK noise a frame).
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as sla

K, RHO, CP = 0.8, 1705.0, 840.0
H = 1 / 0.13
WALL, WIDTH = 0.29, 0.60
R20 = {1.5: 12.1e-3, 2.5: 7.41e-3, 4.0: 4.61e-3}           # ohm/m, IEC 60228 class 1
HOT = 1.12

def heat(mm2, amps, loaded):
    return loaded * amps**2 * R20[mm2] * HOT                # W per metre of cable

def system(dx):
    nx, ny = int(round(WIDTH / dx)), int(round(WALL / dx))
    n = nx * ny
    idx = lambda i, j: i * ny + j
    rows, cols, vals = [], [], []
    diag = np.zeros(n)
    g = K                                                   # conductance between cells, per metre of cable
    for i in range(nx):
        for j in range(ny):
            p = idx(i, j)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                a, b = i + di, j + dj
                if 0 <= a < nx and 0 <= b < ny:
                    rows.append(p); cols.append(idx(a, b)); vals.append(-g); diag[p] += g
            if j == 0 or j == ny - 1:                       # a face: half a cell of brick, then the air film
                diag[p] += 1 / (dx / (2 * K * dx) + 1 / (H * dx))
    A = sp.csr_matrix((vals + list(diag), (rows + list(range(n)), cols + list(range(n)))), shape=(n, n))
    return A, nx, ny

def steady(depth, dx=1e-3):
    A, nx, ny = system(dx)
    q = np.zeros(nx * ny); q[(nx // 2) * ny + int(depth / dx)] = 1.0   # 1 W/m
    T = sla.spsolve(A.tocsc(), q).reshape(nx, ny)
    face = T[:, 0]
    half = face > face.max() / 2
    return face.max(), half.sum() * dx, face

def centre_error(face, watts, dx=1e-3, pix=0.010, noise=0.15, trials=2000, seed=1):
    """RMS error of a Gaussian fit to the band, the cable anywhere within a pixel."""
    from scipy.optimize import curve_fit
    rng = np.random.default_rng(seed)
    x = (np.arange(face.size) - face.size // 2) * dx
    g = lambda u, a, c, w, b: a * np.exp(-((u - c) / w) ** 2 / 2) + b
    npx = int(0.30 / pix)                                   # 30 cm of wall across the band
    err = []
    for _ in range(trials):
        shift = rng.uniform(-pix / 2, pix / 2)
        edges = (np.arange(npx + 1) - npx / 2) * pix
        mid = (edges[:-1] + edges[1:]) / 2
        seen = np.array([watts * face[(x + shift >= lo) & (x + shift < hi)].mean() for lo, hi in zip(edges[:-1], edges[1:])])
        seen += rng.normal(0, noise, npx)
        p, _ = curve_fit(g, mid, seen, p0=(seen.max(), mid[np.argmax(seen)], 0.05, 0))
        err.append(p[1] - shift)
    return np.sqrt(np.mean(np.square(err)))

def rise_time(depth, dx=2e-3, dt=60.0, hours=48):
    A, nx, ny = system(dx)
    C = RHO * CP * dx * dx
    M = (sp.identity(nx * ny) * (C / dt) + A).tocsc()
    lu = sla.splu(M)
    q = np.zeros(nx * ny); q[(nx // 2) * ny + int(depth / dx)] = 1.0
    T = np.zeros(nx * ny); over = []
    for _ in range(int(hours * 3600 / dt)):
        T = lu.solve(C / dt * T + q)
        over.append(T.reshape(nx, ny)[nx // 2, 0])
    over = np.array(over); end = over[-1]
    t = lambda frac: (np.argmax(over >= frac * end) + 1) * dt / 3600
    return t(0.5), t(0.9), end

if __name__ == '__main__':
    cables = [('CYKY 3 x 1.5, one phase', 1.5, 10, 2), ('CYKY 3 x 1.5, one phase', 1.5, 16, 2),
              ('CYKY 3 x 2.5, one phase', 2.5, 16, 2), ('CYKY 5 x 4, three phases', 4.0, 25, 3)]
    print('heat in the cable:')
    for name, mm2, amps, loaded in cables:
        print(f'  {name} at {amps} A: {heat(mm2, amps, loaded):.1f} W/m')
    print('the plaster over the cable, steady state, per W/m of heat:')
    per, faces = {}, {}
    for d in (0.015, 0.025, 0.035):
        dT, w, faces[d] = steady(d)
        per[d] = dT
        print(f'  cable {d*1000:.0f} mm under the surface: +{dT:.2f} K, {w*1000:.0f} mm wide at half height')
    print('so, cable 25 mm deep:')
    for name, mm2, amps, loaded in cables:
        print(f'  {name} at {amps} A: +{per[0.025] * heat(mm2, amps, loaded):.1f} K')
    print('the band\'s middle found by an 80 x 62 sensor at 1 m (1 cm a pixel, 150 mK a frame), cable 25 mm deep:')
    for name, mm2, amps, loaded in cables[:2]:
        e = centre_error(faces[0.025], heat(mm2, amps, loaded))
        print(f'  {name} at {amps} A, one frame: {e*1000:.1f} mm RMS')
    t50, t90, end = rise_time(0.025)
    print(f'how soon (25 mm deep, from cold, 2 mm grid): half of it after {t50:.1f} h, 90 % after {t90:.1f} h')
