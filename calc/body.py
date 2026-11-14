"""The head of ten as decided on 13 Nov 2026: what it draws, weighs and sheds, and how many frames
a turn needs. Level 4; the layout is layout.py's. The concept's budget.py did the same for the head
of eleven on foam and stays as the record of 28 Oct; the sheet figures below are the ones it
cites, with its sources.

Run: python3 body.py > body.out
"""
import math
from materials import wavelength
from layout import N_RING, HEAD_R, from_rod

N_RX = N_RING + 2                                         # the ring and Předseda's two
F24 = 2.437e9

print('== power: what the head draws (3.3 V rail unless said)')
loads = [  # name, mA, source
    (f'{N_RX} ESP32-C5 receiving, 2.4 GHz HE20, 87 mA each with the CPU idle (datasheet v1.5, Table 5-7); 100 mA taken for the CSI work', N_RX * 100, 'sheet + assumed'),
    ('STM32H7A3 at 280 MHz, all peripherals on, with the LDO (DS13195, Table 35)', 132.5, 'sheet'),
    ('the 48 MHz oscillator and the fan-out buffer', 30, 'assumed'),
    ('Datel: eight PDM microphones, about 1 mA each', 8, 'assumed'),
    ('Razvedčik: a magnetic angle sensor', 10, 'assumed, a part not chosen'),
    ('Iljič: its amplifier', 3, 'assumed'),
]
tot = sum(ma for _, ma, _ in loads)
for name, ma, src in loads:
    print(f'  {name}: {ma:.0f} mA [{src}]')
disp_w = 1.5
w = tot / 1000 * 3.3 + disp_w
print(f'  Pravda, the 5" display with its backlight: {disp_w} W [assumed, open]')
print(f'  all at once: {tot:.0f} mA at 3.3 V = {tot/1000*3.3:.1f} W, with the display {w:.1f} W')
for name, wh in (('two 18650 cells in parallel, about 6 Ah at 3.6 V', 21.6),):
    print(f'  Pajok, {name}: {wh} Wh -> about {wh*0.85/w:.1f} h at 85 % conversion')
ant = N_RX * 100 + 30 + 8
print(f'  the supply to Front: {ant/1000:.2f} A, {(ant+320)/1000:.2f} A while a C5 sends (Samokritika)')

print('== Kolchoz: weight and warmth (rough)')
a_head = math.pi * HEAD_R ** 2
front = a_head * 0.003 * 2700                             # Front: an aluminium disc, 3 mm at least (the owner: threads)
board = a_head * 0.0016 * 1850                            # Tyl: FR4
cells, display = 2 * 0.047, 0.100                         # an 18650 about 47 g; the display assumed
felt_all = a_head * 0.005 * 300                           # hard pressed felt about 0.3 g/cm3 (assumed), 5 mm
felt_rim = math.pi * 2 * HEAD_R * 0.015 * 0.005 * 300     # a band 15 mm wide round the rim
print(f'  the head {2*HEAD_R*1000:.0f} mm across: Front, 3 mm of aluminium, {front*1000:.0f} g; Tyl {board*1000:.0f} g; two cells {cells*1000:.0f} g; '
      f'the display {display*1000:.0f} g: {(front+board+cells+display)*1000:.0f} g before the modules, the antennas and the housing')
print(f'  felt 5 mm on the whole wall side {felt_all*1000:.0f} g, or on a 15 mm band round the rim {felt_rim*1000:.0f} g')
area_out = 2 * a_head + math.pi * 2 * HEAD_R * 0.04       # off the wall now: both faces and a 40 mm rim
h_air = 10.0                                              # W/m2K, still air and radiation together (assumed)
print(f'  {w:.1f} W out through both faces and the rim ({area_out*1e4:.0f} cm2) at about {h_air:.0f} W/m2K: '
      f'about {w/(area_out*h_air):.0f} K over the room outside, more inside; no fan')

print('== frames: how many a turn needs')
lam = wavelength('brick', F24); r_out = from_rod()[-1]
for t_turn in (2, 4, 8):
    v = 2 * math.pi * r_out / t_turn
    need = v / (lam / 8)
    print(f'  a turn in {t_turn} s: the outermost antenna, {r_out*1000:.0f} mm from the rod, moves {v*100:.0f} cm/s; '
          f'a frame every {lam/8*1000:.0f} mm (lambda/8 in brick) needs {need:.0f} a second from each of the two senders of Iskra')

print(f'== {N_RX} receivers into one processor (CSI as int8 I/Q + 50 B of header)')
for sc, bw in ((64, '20 MHz'), (242 + 53, 'HE20 + LLTF')):
    rep = sc * 2 + 50
    for pps in (100, 1000):
        print(f'  {bw}, {pps} frames/s: {rep*pps*8/1e6:.1f} Mbit/s a receiver, {N_RX*rep*pps/1e6:.2f} MB/s for {N_RX}')

print('== Kuranty: what the clock lines must keep')
# a branch of the star from the buffer at the centre: to a ring chip about the ring's radius, to Předseda's a few mm
er_eff = 3.3                                              # a trace on layer 4 over layer 3, FR4 (as budget.py's star)
ps_mm = math.sqrt(er_eff) / 299792458.0 * 1e-3 * 1e12
from layout import RING_R
ring_mm, mid_mm = RING_R * 1000, 15.0
deg = lambda ps: ps * 1e-12 * F24 * 360                   # the PLL carries a reference delay up to the carrier
print(f'  a branch {ring_mm:.0f} mm to a ring chip: {ring_mm*ps_mm:.0f} ps; {mid_mm:.0f} mm to Předseda\'s: {mid_mm*ps_mm:.0f} ps; '
      f'unmatched, the difference is {deg((ring_mm-mid_mm)*ps_mm):.0f} deg at the carrier - fixed, so levelled out with the rest')
for tc in (50e-6, 200e-6):                                # how the delay of FR4 trace moves with temperature (assumed range)
    print(f'  if the delay moves {tc*1e6:.0f} ppm/K: a {ring_mm:.0f} mm branch drifts {deg(ring_mm*ps_mm*tc)*1000:.0f} mdeg/K, '
          f'the unmatched difference {deg((ring_mm-mid_mm)*ps_mm*tc)*1000:.0f} mdeg/K')
print(f'  a tick of the 48 MHz clock is {1e9/48e6:.1f} ns: the sync edge need only arrive within it, a metre of trace is {1000*ps_mm/1000:.1f} ns')
# the 51st harmonic of the 48 MHz clock: a trapezoid, 3.3 V, half duty, rise time tr (the buffer's is not yet known)
T, n = 1 / 48e6, 51
for tr in (0.5e-9, 1e-9, 2e-9):
    x = n * math.pi * tr / T
    v = 3.3 * 2 / (n * math.pi) * abs(math.sin(x) / x)
    print(f'  the {n}st harmonic, {n*48} MHz, edges of {tr*1e9:.1f} ns: {v*1000:.1f} mV, {10*math.log10(v**2/2/50*1000):.0f} dBm into 50 ohm on the line itself')
for ch, fc in ((1, 2412), (6, 2437), (11, 2462)):
    lo, hi = fc - 9.6, fc + 9.6                           # an HE20 frame's occupied band
    inside = [k * 48 for k in range(48, 54) if lo <= k * 48 <= hi]
    print(f'  channel {ch}, {lo:.1f}-{hi:.1f} MHz: harmonics of 48 MHz inside: {inside or "none"}')
