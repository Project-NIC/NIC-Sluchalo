"""Can the joints' pattern be divided out? The real wall of wall_fdtd.py, scanned along a line.

Bed joints are horizontal lines across the whole wall. A vertical cable crosses them: in the
tool's map the bed joints are the same in every row, so each row divided by its own median loses
them, and what is left across the cable is the head joints (a horizontal section, joints every
300 mm in a 14 cm stretcher course, every 150 mm in a 29 cm header course). A horizontal cable
lies along them: in a vertical scan its dip sits among the bed joints' pattern, and only the
pattern's regularity separates them — the scan folded over one course (75 mm) and the median
taken as the pattern. Here: the scan alone, divided by the folded pattern, and divided by the
true bare wall (the best any reference could do); regular joints and joints 7-13 mm thick.
2.4 GHz, three channels' power summed, the field along the cable. Needs numpy (wall_fdtd.py).

Run: python3 joints.py <config>   one configuration, saved to joints_<config>.npz
     python3 joints.py grooves <config>   the same grooves empty, to tell the cable from its groove
     python3 joints.py report     the table, from the saved runs
A fourth way: the pattern aligned on each joint — the scan cut into pieces around the joints'
centres, their median put back at every joint — for joints that are not evenly spaced; the
centres are taken as known (in a wall they would be found from the scan itself, open).
"""
import sys
import numpy as np
import wall_fdtd as wf

FREQS = (2.412e9, 2.442e9, 2.472e9)
GROOVE = (0.04, 0.03)
CONFIGS = {   # name: (section, wall, mortar, joints)
    'v140_wet': ('vertical', 0.14, 'mortar_wet', 'regular'),
    'v140_wet_irr': ('vertical', 0.14, 'mortar_wet', 'irregular'),
    'v140_hi': ('vertical', 0.14, 'mortar_hi', 'regular'),
    'v290_wet': ('vertical', 0.29, 'mortar_wet', 'regular'),
    'v290_wet_irr': ('vertical', 0.29, 'mortar_wet', 'irregular'),
    'v290_hi': ('vertical', 0.29, 'mortar_hi', 'regular'),
    'h140_wet': ('horizontal', 0.14, 'mortar_wet', 'regular'),
    'h290_wet': ('horizontal', 0.29, 'mortar_wet', 'regular'),
}

def courses(section, wall_t, kind, seed=7):
    """(start, end of brick, end of joint) along the scan line, filling the periodic section."""
    if section == 'vertical':
        brick, n = 65, 8                                # 65 mm bricks, 75 mm courses
    else:
        brick, n = (290, 2) if wall_t < 0.2 else (140, 4)   # stretchers, or headers
    joints = np.full(n, 10)
    if kind == 'irregular':
        rng = np.random.default_rng(seed)
        joints = rng.integers(7, 14, n)
        while joints.sum() > 10 * n:                    # keep the section's length
            i = rng.integers(n); joints[i] -= joints[i] > 7
        while joints.sum() < 10 * n:
            i = rng.integers(n); joints[i] += joints[i] < 13
    out, y = [], 0
    for j in joints:
        out.append((y / 1000, (y + brick) / 1000, (y + brick + j) / 1000)); y += brick + j
    return out

def section(f, wall_t, mortar, crs, collar, cable_y):
    er, sg, pec, irx, isrc, _ = wf.build(f, wall_t, None, groove=GROOVE if cable_y is not None else None,
                                         cable=cable_y is not None, ylab=0.3 if cable_y is None else cable_y)
    nx, ny = er.shape
    x = (np.arange(nx) - wf.NPML) * wf.DX; y = np.arange(ny) * wf.DX
    X, Y = np.meshgrid(x, y, indexing='ij')
    xb0 = wf.GAP_SRC + wf.PLASTER_T; xb1 = xb0 + wall_t
    inbrick = (X >= xb0) & (X < xb1)
    mask = np.zeros_like(inbrick)
    for k, (a, b, c) in enumerate(crs):
        mask |= (Y >= b) & (Y < c)
        if collar and k % 2 == 0:                       # a collar joint in every other course
            mask |= (Y >= a) & (Y < b) & (np.abs(X - (xb0 + xb1) / 2) < 0.005)
    mask &= inbrick
    if cable_y is not None:                             # the groove was cut after the wall was laid
        mask &= ~((np.abs(Y - cable_y) < GROOVE[0] / 2) & (X >= xb1 - GROOVE[1]))
    er[mask], sg[mask] = wf.materials(f)[mortar]
    return er, sg, pec, irx, isrc

def grooves(name):
    sec, wall_t, mortar, kind = CONFIGS[name]
    crs = courses(sec, wall_t, kind); collar = sec == 'vertical' and wall_t > 0.2
    k = 4 if sec == 'vertical' else 0
    pos = {'mid': (crs[k][0] + crs[k][1]) / 2, 'joint': (crs[k][1] + crs[k][2]) / 2}
    P = {key: 0 for key in pos}
    for f in FREQS:
        for key in P:
            er, sg, pec, irx, isrc = section(f, wall_t, mortar, crs, collar, pos[key])
            pec[:] = False                              # the groove without its cable
            P[key] = P[key] + np.abs(wf.run(f, 'TM', er, sg, pec, irx, isrc)) ** 2
        print(f'{name} grooves: {f/1e9:.3f} GHz done', flush=True)
    np.savez(f'joints_{name}_grooves.npz', **P)

def aligned(S, crs, dx):
    """The pattern rebuilt from the median of the scan around each joint's centre."""
    n = S.size; c = np.array([int(round((b + e) / 2 / dx)) for _, b, e in crs])
    half = int(round(min(np.diff(np.r_[c, c[0] + n])) / 2))
    seg = np.median(np.stack([np.roll(S, -ci + half)[:2 * half] for ci in c]), axis=0)
    T = np.empty(n); idx = np.arange(n)
    for ci in c:                                        # each sample from its nearest joint
        d = (idx - ci + n // 2) % n - n // 2
        m = np.abs(d) < half
        T[idx[m]] = seg[d[m] + half]
    return T

def compute(name):
    sec, wall_t, mortar, kind = CONFIGS[name]
    crs = courses(sec, wall_t, kind)
    collar = sec == 'vertical' and wall_t > 0.2
    k = 4 if sec == 'vertical' else 0                   # the course the cable lies in
    pos = {'mid': (crs[k][0] + crs[k][1]) / 2, 'joint': (crs[k][1] + crs[k][2]) / 2}
    P = {key: 0 for key in ('wall', 'mid', 'joint')}
    for f in FREQS:
        for key in P:
            cy = None if key == 'wall' else pos[key]
            er, sg, pec, irx, isrc = section(f, wall_t, mortar, crs, collar, cy)
            P[key] = P[key] + np.abs(wf.run(f, 'TM', er, sg, pec, irx, isrc)) ** 2
        print(f'{name}: {f/1e9:.3f} GHz done', flush=True)
    period = (crs[-1][2]) / len(crs)
    np.savez(f'joints_{name}.npz', period=period, y_mid=pos['mid'], y_joint=pos['joint'], **P)

def metrics(q, y, yc, W):
    d = np.abs(y - yc); d = np.minimum(d, W - d)
    win, out = d < 0.04, d > 0.08
    qdb = 10 * np.log10(q / np.median(q[out]))
    dip, low, pp = qdb[win].min(), qdb[out].min(), qdb[out].max() - qdb[out].min()
    return dip, pp, low - dip

def fold(S, period, dx):
    n = int(round(S.size * dx / period)); step = S.size // n
    return np.median(np.stack([np.roll(S, -i * step) for i in range(n)]), axis=0)

def report():
    print('dip: the cable, dB under the median away from it; pattern: peak to peak away from it;')
    print('margin: how much deeper the dip is than the deepest dip of the pattern (> 0: it stands out)')
    for name, (sec, wall_t, mortar, kind) in CONFIGS.items():
        try:
            z = np.load(f'joints_{name}.npz')
        except FileNotFoundError:
            continue
        W = z['wall'].size * wf.DX; y = np.arange(z['wall'].size) * wf.DX
        what = f'{sec} section ({"a horizontal" if sec == "vertical" else "a vertical"} cable), {wall_t*100:.0f} cm, {mortar}, {kind} joints'
        print(f'== {what}')
        crs = courses(sec, wall_t, kind)
        try:
            gz = np.load(f'joints_{name}_grooves.npz')
        except FileNotFoundError:
            gz = None
        for at in ('mid', 'joint'):
            S = z[at]; yc = float(z['y_' + at])
            line = f'  cable {"mid-brick" if at == "mid" else "at a joint"}:'
            ways = [('the scan alone', S), ('divided by the folded pattern', S / fold(S, float(z['period']), wf.DX)),
                    ('by the pattern aligned on each joint', S / aligned(S, crs, wf.DX)),
                    ('divided by the true bare wall', S / z['wall'])]
            if gz is not None:
                ways.append(('against the same groove empty', S / gz[at]))
            for label, q in ways:
                dip, pp, mg = metrics(q, y, yc, W)
                line += f' | {label}: dip {dip:+.1f}, pattern {pp:.1f}, margin {mg:+.1f} dB'
            print(line)

if __name__ == '__main__':
    if sys.argv[1] == 'report':
        report()
    elif sys.argv[1] == 'grooves':
        grooves(sys.argv[2])
    else:
        compute(sys.argv[1])
