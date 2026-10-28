"""The head against the wall: does its ground plate change the cable's dip? 2D, beside wall_fdtd.py.

The antenna board faces the wall: the wall, a spacer g thick (air, or rubber), the patches,
1.6 mm of FR4, the ground plane — a plate as wide as the head, 167 mm. In 2D the patches cannot be
drawn (they resonate along the cable, out of the section), so the board is its FR4 and ground,
and what a patch would see is taken as the field along the cable in the patch plane, averaged
over a patch's 29 mm. The dip: the groove with the cable against the same groove empty, the head
in the same place; beside it the same without any head, 2 mm in front of the wall. A 14 cm wall,
mortar er 5, gypsum plaster, the cable mid-brick; 2.442 GHz. The rubber is taken as unfilled
silicone, er 3.0, tan d about 0.005 (assumed; carbon-black rubber is far lossier); the foam as
closed-cell car foam, er 1.2, tan d 0.001 (assumed — it is mostly air). Needs numpy.

Run: python3 head.py <config>   one configuration, saved to head_<config>.npz
     python3 head.py report     the table, from the saved runs
     python3 head.py depth <config>, then depthreport: the cable 20, 30, 40 mm from the wall's face
     (grooves 10, 30, 50 mm deep), the head over it — the plate makes a standing wave in the wall,
     so how much a cable shows depends on where it lies in that wave.
     python3 head.py cdepth <config> [plaster], then cdepthreport: the same, the complex field kept —
     the amplitude and the change in amplitude and phase together, as the receivers measure them.
"""
import sys
import numpy as np
import wall_fdtd as wf

wf.GAP_RX = 0.060                      # room in front of the wall for the head
F = 2.442e9
HEAD, PATCH, FR4 = 0.167, 0.029, 0.0016
RUBBER = (3.0, 2 * np.pi * F * wf.EPS0 * 3.0 * 0.005)
FOAM = (1.2, 2 * np.pi * F * wf.EPS0 * 1.2 * 0.001)   # closed-cell PE or EPDM foam, mostly air (assumed)
YC = 0.3375                            # the cable, mid-brick
OFFSETS = (0.0, 0.066)                 # the head's centre from the cable: over it, and the cable under a ring patch
CONFIGS = {'none': None, 'air5': ('air', 0.005), 'rubber5': ('rubber', 0.005),
           'rubber10': ('rubber', 0.010), 'rubber20': ('rubber', 0.020),
           'foam10': ('foam', 0.010), 'foam15': ('foam', 0.015), 'foam20': ('foam', 0.020), 'foam25': ('foam', 0.025), 'foam30': ('foam', 0.030),
           'air15': ('air', 0.015), 'air20': ('air', 0.020), 'air25': ('air', 0.025),
           'foam20pe': ('foam', 0.020, ('PE', 0.001, 2.3, 0.0003)), 'foam20pc': ('foam', 0.020, ('PC', 0.001, 2.9, 0.01))}
# the last two: a hard sheet 1 mm on the foam's face, against the wall, within the 20 mm
# (polyethylene er 2.3, polycarbonate er 2.9, handbook values)

def label(spacer):
    if spacer is None:
        return 'no head, 2 mm in front of the wall'
    return f'head, {spacer[0]} {spacer[1]*1000:.0f} mm' + (f' + {spacer[2][0]} {spacer[2][1]*1000:.0f} mm' if len(spacer) > 2 else '')

def model(cable, spacer, offset, gd=0.03):
    er, sg, pec, irx, isrc, _ = wf.build(F, 0.14, 'mortar_hi', groove=(0.04, gd), cable=cable, ylab=YC)
    if spacer is None:
        return er, sg, pec, irx, isrc
    ny = er.shape[1]
    i_n = int(round((wf.GAP_SRC + 2 * wf.PLASTER_T + 0.14) / wf.DX)) + wf.NPML - 2
    while er[i_n, 0] != 1.0:                            # the first cell of air in front of the plaster
        i_n += 1
    mat, g = spacer[:2]
    G = int(round(g / wf.DX))                           # whole cells: the spacer, 2 of FR4, 2 of copper
    j = np.abs(np.arange(ny) * wf.DX - (YC + offset)) < HEAD / 2
    if mat in ('rubber', 'foam'):
        er[i_n:i_n + G, j], sg[i_n:i_n + G, j] = RUBBER if mat == 'rubber' else FOAM
    if len(spacer) > 2:                                 # the hard sheet, on the wall's side
        _, t, e, tand = spacer[2]
        T = int(round(t / wf.DX))
        er[i_n:i_n + T, j], sg[i_n:i_n + T, j] = e, 2 * np.pi * F * wf.EPS0 * e * tand
    er[i_n + G:i_n + G + 2, j], sg[i_n + G:i_n + G + 2, j] = 4.4, 2 * np.pi * F * wf.EPS0 * 4.4 * 0.02
    pec[i_n + G + 2:i_n + G + 4, j] = True
    return er, sg, pec, i_n + G, isrc

def compute(name):
    spacer = CONFIGS[name]
    out = {}
    for off in ((0.0,) if spacer is None else OFFSETS):
        for cable in (False, True):
            er, sg, pec, irx, isrc = model(cable, spacer, off)
            out[f'{"c" if cable else "g"}{off*1000:.0f}'] = np.abs(wf.run(F, 'TM', er, sg, pec, irx, isrc)) ** 2
            print(f'{name}: offset {off*1000:.0f} mm, cable {cable} done', flush=True)
    np.savez(f'head_{name}.npz', **out)

def report():
    print('the dip a patch over the cable sees (its 29 mm averaged), the cable against the same groove empty;')
    print("and the head's own pattern across it, peak to peak (fixed to the head, calibrated out)")
    for name, spacer in CONFIGS.items():
        try:
            z = np.load(f'head_{name}.npz')
        except FileNotFoundError:
            continue
        y = np.arange(z['g0'].size) * wf.DX
        line = f'  {label(spacer):38s}'
        for off in ((0.0,) if spacer is None else OFFSETS):
            g, c = z[f'g{off*1000:.0f}'], z[f'c{off*1000:.0f}']
            p = np.abs(y - YC) < PATCH / 2
            dip = 10 * np.log10(c[p].mean() / g[p].mean())
            where = 'cable under the centre' if off == 0 else 'cable under a ring patch'
            line += f' | {where}: {dip:+.1f} dB'
            if spacer is not None and off == 0:
                h = np.abs(y - YC) < HEAD / 2 - PATCH / 2
                gdb = 10 * np.log10(g[h])
                line += f' (pattern {gdb.max() - gdb.min():.1f} dB)'
        print(line)

DEPTHS = (0.010, 0.030, 0.050)         # groove depths; the cable in the middle, 15 mm of plaster over it

DEPTHS_LC = (0.010, 0.020, 0.030)      # the typical wall here: lime-cement plaster, cables 2-3 cm deep

def depth(name, plaster='plaster'):
    wf.PLASTER = plaster
    out = {}
    for gd in (DEPTHS if plaster == 'plaster' else DEPTHS_LC):
        for cable in (False, True):
            er, sg, pec, irx, isrc = model(cable, CONFIGS[name], 0.0, gd)
            out[f'{"c" if cable else "g"}{gd*1000:.0f}'] = np.abs(wf.run(F, 'TM', er, sg, pec, irx, isrc)) ** 2
        print(f'{name}: groove {gd*1000:.0f} mm done', flush=True)
    np.savez(f'head_depth_{name}{"" if plaster == "plaster" else "_" + plaster}.npz', **out)

def cdepth(name, plaster='plaster'):
    """The same runs, the complex field kept: the receivers measure phase as well as amplitude."""
    wf.PLASTER = plaster
    out = {}
    for gd in (DEPTHS if plaster == 'plaster' else DEPTHS_LC):
        for cable in (False, True):
            er, sg, pec, irx, isrc = model(cable, CONFIGS[name], 0.0, gd)
            out[f'{"c" if cable else "g"}{gd*1000:.0f}'] = wf.run(F, 'TM', er, sg, pec, irx, isrc)
        print(f'{name}: groove {gd*1000:.0f} mm done', flush=True)
    np.savez(f'head_cdepth_{name}{"" if plaster == "plaster" else "_" + plaster}.npz', **out)

def cdepthreport():
  print('what a patch over the cable sees, the field along it summed over its 29 mm as an antenna sums it,')
  print('against the same groove empty: the amplitude alone, and the change in the complex field (amplitude')
  print('and phase together) as a share of the field, in dB - the receivers measure both')
  for plaster, depths in (('plaster', DEPTHS), ('plaster_lc', DEPTHS_LC)):
    print(f'  {"gypsum" if plaster == "plaster" else "lime-cement"} plaster:')
    for name, spacer in CONFIGS.items():
        try:
            z = np.load(f'head_cdepth_{name}{"" if plaster == "plaster" else "_" + plaster}.npz')
        except FileNotFoundError:
            continue
        y = np.arange(z['g10'].size) * wf.DX; p = np.abs(y - YC) < PATCH / 2
        line = f'  {label(spacer):38s}'
        for gd in depths:
            g, c = z[f'g{gd*1000:.0f}'][p].mean(), z[f'c{gd*1000:.0f}'][p].mean()
            line += (f' | {15 + gd*500:.0f} mm: amplitude {20*np.log10(abs(c)/abs(g)):+.1f}, '
                     f'change {20*np.log10(abs(c - g)/abs(g)):+.1f} dB ({abs(c - g)/abs(g)*100:.0f} %)')
        print(line)

def depthreport():
  print('the dip a patch over the cable sees, against the same groove empty, by the cable\'s distance from the face')
  for plaster, depths in (('plaster', DEPTHS), ('plaster_lc', DEPTHS_LC)):
    print(f'  {"gypsum" if plaster == "plaster" else "lime-cement"} plaster:')
    for name, spacer in CONFIGS.items():
        try:
            z = np.load(f'head_depth_{name}{"" if plaster == "plaster" else "_" + plaster}.npz')
        except FileNotFoundError:
            continue
        y = np.arange(z['g10'].size) * wf.DX; p = np.abs(y - YC) < PATCH / 2
        line = f'  {label(spacer):38s}'
        for gd in depths:
            g, c = z[f'g{gd*1000:.0f}'], z[f'c{gd*1000:.0f}']
            line += f' | {15 + gd*500:.0f} mm: {10*np.log10(c[p].mean()/g[p].mean()):+.1f} dB'
        print(line)

if __name__ == '__main__':
    if sys.argv[1] == 'report':
        report()
    elif sys.argv[1] == 'depthreport':
        depthreport()
    elif sys.argv[1] == 'depth':
        depth(sys.argv[2], *sys.argv[3:4])
    elif sys.argv[1] == 'cdepth':
        cdepth(sys.argv[2], *sys.argv[3:4])
    elif sys.argv[1] == 'cdepthreport':
        cdepthreport()
    else:
        compute(sys.argv[1])
