"""The head of ten against the wall: how closely must Valenki keep the gap? Level 4.

head.py's 2D model (the concept's, published) with the new head put in: the ground plane 176 mm
wide, the patch 37 mm, air in the gap (no foam), the gap in steps of one millimetre about 15 mm.
A degree of tilt moves a ring patch about 1.2 mm nearer or farther (ring8.py: 69.5 mm out), so
these steps stand for tilt as well. Gypsum plaster, the worst case of head_cdepth.out; the cable
in grooves 10, 30 and 50 mm deep. The complex field kept, as the receivers measure it.

Run: python3 head8.py <gap mm>   (writes head8_<gap>.npz here)
     python3 head8.py channel <1 | 6 | 11>   (the cable at seven depths, one channel)
     python3 head8.py disc <1 | 6 | 11>, then discreport > head8_disc.out   (the bought antennas on the disc)
     python3 head8.py report > head8.out
"""
import sys, math
import numpy as np
import head as hd
from ring8 import HEAD_R, PATCH_W, RING_R

hd.HEAD, hd.PATCH = 2 * HEAD_R, PATCH_W
GAPS = (13, 14, 15, 16, 17)

def run(g):
    cfg = ('air', g / 1000)
    out = {}
    for gd in hd.DEPTHS:
        for cable in (False, True):
            er, sg, pec, irx, isrc = hd.model(cable, cfg, 0.0, gd)
            out[f'{"c" if cable else "g"}{gd*1000:.0f}'] = hd.wf.run(hd.F, 'TM', er, sg, pec, irx, isrc)
        print(f'gap {g} mm: groove {gd*1000:.0f} mm done', flush=True)
    np.savez(f'head8_{g}.npz', **out)

def patch_sum(f):
    y = np.arange(len(f)) * hd.wf.DX
    return f[np.abs(y - hd.YC) < hd.PATCH / 2].sum()

def report():
    print(f'the head of ten: the plate {hd.HEAD*1000:.0f} mm, the patch {hd.PATCH*1000:.0f} mm, air in the gap, gypsum plaster;')
    print('what the patch over the cable sees against the same groove empty: amplitude, and the change in the complex field')
    print(f'(a degree of tilt moves a ring patch {RING_R*math.tan(math.radians(1))*1000:.1f} mm)')
    for g in GAPS:
        try:
            d = np.load(f'head8_{g}.npz')
        except FileNotFoundError:
            continue
        row = []
        for gd in hd.DEPTHS:
            c, e = patch_sum(d[f'c{gd*1000:.0f}']), patch_sum(d[f'g{gd*1000:.0f}'])
            row.append(f'cable {15+gd*500:.0f} mm deep: amplitude {20*np.log10(abs(c)/abs(e)):+.1f}, change {abs(c-e)/abs(e)*100:3.0f} %')
        print(f'  gap {g} mm | ' + ' | '.join(row))


# ---- the three channels: does what one misses show on another? (added 14 Nov 2026)
CHANNELS = {1: 2.412e9, 6: 2.437e9, 11: 2.462e9, 36: 5.18e9, 165: 5.825e9}
GROOVES = (0.010, 0.016, 0.023, 0.030, 0.036, 0.043, 0.050)     # the cable 20 to 40 mm from the face

def run_channel(ch, g=15):
    hd.F = CHANNELS[ch]
    cfg = ('air', g / 1000); out = {}
    for gd in GROOVES:
        for cable in (False, True):
            er, sg, pec, irx, isrc = hd.model(cable, cfg, 0.0, gd)
            out[f'{"c" if cable else "g"}{gd*1000:.0f}'] = hd.wf.run(hd.F, 'TM', er, sg, pec, irx, isrc)
    np.savez(f'head8_ch{ch}.npz', **out)

def report_channels():
    print('\n== the three channels, gap 15 mm, gypsum plaster: what the patch over the cable sees against the same groove empty')
    print('   amplitude in dB, and in brackets the change in amplitude and phase together')
    res = {}
    for ch in CHANNELS:
        try:
            d = np.load(f'head8_ch{ch}.npz')
        except FileNotFoundError:
            return
        for gd in GROOVES:
            c, e = patch_sum(d[f'c{gd*1000:.0f}']), patch_sum(d[f'g{gd*1000:.0f}'])
            res[ch, gd] = (20 * np.log10(abs(c) / abs(e)), abs(c - e) / abs(e) * 100)
    print('  cable deep  ' + ''.join(f'| channel {ch:2d}          ' for ch in CHANNELS) + '| the three: amplitude')
    for gd in GROOVES:
        a = [res[ch, gd][0] for ch in CHANNELS]
        row = ''.join(f'| {res[ch, gd][0]:+5.1f} dB ({res[ch, gd][1]:3.0f} %)   ' for ch in CHANNELS)
        print(f'  {15+gd*500:4.0f} mm    {row}| best {min(a):+5.1f}, mean {np.mean(a):+5.1f} dB')

if __name__ == '__main__' and sys.argv[1] == 'channel':
    run_channel(int(sys.argv[2]))
if __name__ == '__main__' and sys.argv[1] not in ('channel', 'disc', 'discreport'):
    report() if sys.argv[1] == 'report' else run(int(sys.argv[1]))
if __name__ == '__main__' and sys.argv[1] == 'report':
    report_channels()

# ---- the head as laid out for the bought antennas (added 14 Nov 2026): Front an aluminium disc
# with 2 mm of plastic on its face and the antennas on the plastic; what an antenna sees is taken
# as the field along the cable in its plane, summed over its 38.5 mm. The three channels, the cable
# at five depths, gypsum plaster.
DISC_GROOVES = (0.010, 0.020, 0.030, 0.040, 0.050)        # the cable 20 to 40 mm from the face

def model_disc(cable, g, gd):
    er, sg, pec, irx, isrc = hd.model(cable, None, 0.0, gd)
    ny = er.shape[1]
    i_n = int(round((hd.wf.GAP_SRC + 2 * hd.wf.PLASTER_T + 0.14) / hd.wf.DX)) + hd.wf.NPML - 2
    while er[i_n, 0] != 1.0:
        i_n += 1
    G = int(round(g / hd.wf.DX))
    j = np.abs(np.arange(ny) * hd.wf.DX - hd.YC) < 0.177 / 2
    er[i_n + G:i_n + G + 2, j], sg[i_n + G:i_n + G + 2, j] = 2.9, 2 * np.pi * hd.F * hd.wf.EPS0 * 2.9 * 0.01   # polycarbonate
    pec[i_n + G + 2:i_n + G + 5, j] = True                                                                       # 3 mm of aluminium
    return er, sg, pec, i_n + G, isrc

def run_disc(ch, g=15):
    hd.F = CHANNELS[ch]; out = {}
    for gd in DISC_GROOVES:
        for cable in (False, True):
            er, sg, pec, irx, isrc = model_disc(cable, g / 1000, gd)
            out[f'{"c" if cable else "g"}{gd*1000:.0f}'] = hd.wf.run(hd.F, 'TM', er, sg, pec, irx, isrc)
    np.savez(f'head8_disc_ch{ch}.npz', **out)

def report_disc(chs=(1, 6, 11)):
    hd.PATCH = 0.0385
    print('== the head with the bought antennas: an aluminium disc 177 mm across, 2 mm of plastic, the antenna')
    print('   on it 15 mm from the wall; gypsum plaster; the antenna over the cable sees, against the groove empty:')
    print('   amplitude in dB, and in brackets the change in amplitude and phase together')
    res = {}
    for ch in chs:
        d = np.load(f'head8_disc_ch{ch}.npz')
        for gd in DISC_GROOVES:
            c, e = patch_sum(d[f'c{gd*1000:.0f}']), patch_sum(d[f'g{gd*1000:.0f}'])
            res[ch, gd] = (20 * np.log10(abs(c) / abs(e)), abs(c - e) / abs(e) * 100)
    print('  cable deep  ' + ''.join(f'| channel {ch:3d}         ' for ch in chs) + '| together: amplitude')
    for gd in DISC_GROOVES:
        a = [res[ch, gd][0] for ch in chs]
        row = ''.join(f'| {res[ch, gd][0]:+5.1f} dB ({res[ch, gd][1]:3.0f} %)   ' for ch in chs)
        print(f'  {15+gd*500:4.0f} mm    {row}| best {min(a):+5.1f}, mean {np.mean(a):+5.1f} dB')

if __name__ == '__main__' and sys.argv[1] == 'disc':
    run_disc(int(sys.argv[2]))
if __name__ == '__main__' and sys.argv[1] == 'discreport':
    report_disc(tuple(int(c) for c in sys.argv[2:]) or (1, 6, 11))
