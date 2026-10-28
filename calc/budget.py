"""Every derived figure the concept quotes, except the shadows (shadow.py). Run: python3 budget.py"""
import math, cmath
from materials import C0, EPS0, loss_db_per_m, wavelength, speed

def loss_es(er, sigma, f):
    """dB/m in a material given as real permittivity and conductivity."""
    return 8.686 * abs((2 * math.pi * f / C0 * cmath.sqrt(er - 1j * sigma / (2 * math.pi * f * EPS0))).imag)

F24, F55 = 2.44e9, 5.5e9

print('== loss in the wall (ITU-R P.2040-3)')
for m in ('brick', 'plasterboard', 'concrete'):
    print(f'  {m:12s}', '  '.join(f'{f/1e9:.2f} GHz {loss_db_per_m(m, f):5.1f} dB/m' for f in (1e9, F24, F55, 6.5e9, 8e9)))
for t in (0.15, 0.45, 0.60):
    print(f'  brick {t*100:.0f} cm, once through: {loss_db_per_m("brick", F24)*t:.1f} dB (2.44) / {loss_db_per_m("brick", F55)*t:.1f} dB (5.5); there and back {2*loss_db_per_m("brick", F24)*t:.1f} dB')
print(f'  plasterboard 2 x 12.5 mm, once through: {loss_db_per_m("plasterboard", F24)*0.025:.2f} dB at 2.44 GHz, {loss_db_per_m("plasterboard", F55)*0.025:.2f} dB at 5.5 GHz')
print('  solid ceramic brick measured dry and damp, 1-6 GHz (PMC13165532), at 2.44 GHz:')
for name, er, sg in (('dry', 3.06, 0.014), ('3 % moisture', 3.6, 0.070), ('9 % moisture', 6.1, 0.166)):
    print(f'    {name:13s} er {er}, sigma {sg} S/m: {loss_es(er, sg, F24):5.1f} dB/m; 29 cm {loss_es(er, sg, F24)*0.29:4.1f} dB, 60 cm {loss_es(er, sg, F24)*0.6:4.1f} dB once through')
print(f'  concrete 10 cm at 60 GHz, there and back: {loss_db_per_m("concrete", 60e9)*0.2:.0f} dB')
print(f'  plasterboard 12.5 mm at 60 GHz, there and back: {loss_db_per_m("plasterboard", 60e9)*0.025:.1f} dB')
for f in (F24, F55):
    print(f'  water at {f/1e9:.2f} GHz: {loss_db_per_m("water", f)/100:.1f} dB/cm')

print('== wavelengths (lambda/2 is the resolution ceiling)')
for f in (F24, F55):
    print(f'  {f/1e9:.2f} GHz: air {C0/f*100:.1f} cm, brick {wavelength("brick", f)*100:.1f} cm (lambda/2 {wavelength("brick", f)*50:.1f} cm)')

print('== range resolution from bandwidth: c/B one way (transmission), c/(2B) there and back (a radar)')
for name, B in (('one 20 MHz channel', 20e6), ('one 40 MHz channel', 40e6), ('the whole 2.4 GHz band, 83.5 MHz', 83.5e6),
                ('the ESP32-C5 in the EU, 5.170-5.875 GHz with a gap', 0.705e9),
                ('EU 5.150-6.425 GHz, 1.275 GHz with gaps (a Wi-Fi 6E chip, not the C5)', 1.275e9)):
    print(f'  {name}: one way air {C0/B*100:.0f} cm, brick {speed("brick", F55)/B*100:.0f} cm; '
          f'radar air {C0/(2*B)*100:.0f} cm, brick {speed("brick", F55)/(2*B)*100:.0f} cm')
print(f'  an echo from the back of 60 cm brick returns after {1.2/speed("brick", F24)*1e9:.1f} ns')

print('== an oblique source: the shadow moves sideways (box on a table, wall at distance D)')
n = C0 / speed('brick', F24)
for D in (1.0, 2.0):
    for x in (1.0, 2.0, 3.0):
        a = math.atan2(x, D); t = math.asin(math.sin(a) / n)
        print(f'  box {D:.0f} m from the wall, point {x:.0f} m aside: {10*math.tan(t):.1f} cm per 10 cm of depth')

print(f'  inside the brick the ray bends to at most {math.degrees(math.asin(1/n)):.0f} deg: at most {10*math.tan(math.asin(1/n)):.1f} cm per 10 cm of depth')
for d in (0.03, 0.25):
    print(f'  an object {d*100:.0f} cm in front of the receiver: shifts up to {d*math.tan(math.asin(1/n))*100:.1f} cm between a sender straight behind and one at grazing angle')

print("== the sender's direction from the ring: time or phase?")
D = 0.130                                        # the ring's widest pair (array.py)
print(f'  across the ring a wave arrives at most {D/C0*1e9:.2f} ns apart; the C5 samples every 50 ns at 20 MHz,')
print('  stamps packets to the microsecond, and each module runs on its own crystal - times cannot give the angle')
print(f'  1 deg of carrier phase at 2.44 GHz = {1/360/F24*1e12:.2f} ps = {C0/F24/360*1000:.2f} mm of path')
snr, nsc = 1e4, 242
sp = 1 / math.sqrt(2 * snr * nsc)
print(f'  phase on one clock (the coherent build), SNR 40 dB, 242 subcarriers, one packet: {math.degrees(sp):.3f} deg,'
      f' the angle {math.degrees(sp * (C0/F24) / (2*math.pi*D)):.4f} deg - thermal noise only; multipath and calibration rule')

print("== the head's motion as an aperture (synthetic aperture, 'Doppler' sharpening)")
lam_b = wavelength('brick', F24)
for v in (0.05, 0.2, 0.5):
    print(f'  the head at {v*100:.0f} cm/s: the scattered phase turns at most {v/lam_b:.1f} times a second; at 1000 packets/s that is {1000*lam_b/v:.0f} packets a turn')
print(f'  position to within lambda/8 in brick: {lam_b/8*1000:.0f} mm; lambda/16: {lam_b/16*1000:.0f} mm (an optical mouse drifts 1-2 % of the stroke: 3-6 mm over 30 cm)')
for d in (0.03, 0.10):
    for A in (0.10, 0.20, 0.30):
        print(f'  an object {d*100:.0f} cm deep, a stroke of {A*100:.0f} cm: focus to about {4*lam_b*(d/A)**2*1000:.0f} mm in depth (4 lambda (d/A)^2, rough)')

print('== the clock star: what a millimetre of the 48 MHz trace does to the 2.44 GHz phase')
for name, ee in (('microstrip on FR4 (eps_eff ~3.3)', 3.3), ('stripline in FR4 (eps 4.4)', 4.4)):
    ps = math.sqrt(ee) / C0 * 1e-3 * 1e12                   # ps per mm
    print(f'  {name}: {ps:.1f} ps a millimetre = {ps*1e-12*F24*360:.1f} deg of the 2.44 GHz carrier (the PLL multiplies the skew\'s time, not its phase)')
R_board = 0.066
print(f'  a star to a ring of {R_board*1000:.0f} mm radius: {R_board*1000:.0f} mm a branch, {math.sqrt(3.3)/C0*R_board*1e12:.0f} ps; the buffer sits beside Datel\'s hole, so every branch is meandered to the longest')
print('  a static skew is calibrated out; what must stay equal is how it drifts - equal lengths on one layer drift alike')

print('== the antenna board: one 4-layer board, 1.6 mm (JLCPCB 7628: 0.2 mm prepreg, 1.065 mm core, 0.2 mm prepreg)')
h13 = 0.2e-3 + 0.0175e-3 + 1.065e-3                       # layer 1 to layer 3, layer 2 cleared under the patches
print(f'  the patch on layer 1 over its ground on layer 3: {h13*1000:.2f} mm of FR4 (not 1.6)')
er, h = 4.4, 0.2e-3                                        # 50 ohm microstrip on layer 4 over the ground on layer 3
A = 50 / 60 * math.sqrt((er + 1) / 2) + (er - 1) / (er + 1) * (0.23 + 0.11 / er)
print(f'  a 50 ohm trace on layer 4 over layer 3: {8 * math.exp(A) / (math.exp(2 * A) - 2) * h * 1000:.2f} mm wide (Hammerstad)')
SPC, PCB, GAP = 15.0, 1.6, 11.0                            # mm: the foam with its sheet, the antenna board, the header's height
print(f'  the electronics board {GAP:.0f} mm behind it: from there the wall is {SPC+PCB+GAP:.0f} mm away - '
      f'the optical sensors (15-35 mm) go on the antenna board\'s back instead, {SPC+PCB:.0f} mm from the wall '
      f'plus their own height; Datel\'s rod {SPC+PCB+GAP:.0f} mm long')

print('== power: what the head draws (3.3 V rail unless said)')
loads = [  # name, mA, source
    ('eleven ESP32-C5 receiving, 2.4 GHz HE20, 87 mA each with the CPU idle (datasheet v1.5, Table 5-7); 100 mA taken for the CSI work', 11 * 100, 'sheet + assumed'),
    ('STM32H7A3 at 280 MHz, all peripherals on: 63.5 mA with its SMPS, 132.5 mA with the LDO (DS13195, Table 35); the LDO taken', 132.5, 'sheet'),
    ('two PAA5100JE optical-flow sensors, 6 mA each (Pimoroni)', 12, 'sheet'),
    ('the 48 MHz oscillator and the fan-out buffer', 30, 'assumed'),
    ('eight PDM microphones, about 1 mA each', 8, 'assumed'),
]
tot = sum(ma for _, ma, _ in loads)
for name, ma, src in loads:
    print(f'  {name}: {ma:.0f} mA [{src}]')
disp_w = 1.5
print(f'  the 5" display with its backlight: {disp_w} W [assumed, open]')
w = tot / 1000 * 3.3 + disp_w
print(f'  all at once: {tot:.0f} mA at 3.3 V = {tot/1000*3.3:.1f} W, with the display {w:.1f} W; a calibration burst adds one C5 sending, 245-320 mA')
for name, wh in (('two 18650 cells in parallel, about 6 Ah at 3.6 V', 21.6), ('one 18650 cell, about 3 Ah at 3.6 V', 10.8)):
    print(f'  {name}: {wh} Wh -> about {wh*0.85/w:.1f} h at 85 % conversion')
ant = 11 * 100 + 30 + 8                                    # the antenna board: the C5s, the clock, the microphones
rest = tot - ant + disp_w / 3.3 * 1000
print(f'  two converters to 3.3 V: the antenna board {ant/1000:.2f} A ({(ant+320)/1000:.2f} A while a C5 sends), '
      f'the electronics board with the display {rest/1000:.2f} A - each under the 2 A of a TPS63021 from 2.5 V up')
print(f'  from the cells at their end, 3.0 V: {w/0.85/3.0:.1f} A, {w/0.85/3.0/2:.1f} A a cell')

print('== the body: weight and warmth (rough)')
D_HEAD = 0.167
a_head = math.pi * D_HEAD ** 2 / 4
rubber = a_head * 0.010 * 1150                            # unfilled silicone 1.1-1.2 g/cm3
foam = a_head * 0.015 * 45                                # closed-cell PE foam 30-60 kg/m3, 15 mm
board = a_head * 0.0016 * 1850                            # FR4
cells, display = 2 * 0.047, 0.100                         # an 18650 about 47 g; the display module assumed
sheet = a_head * 0.001 * 950                              # a 1 mm polyethylene sheet on the foam's face
print(f'  the spacer {D_HEAD*1000:.0f} mm across: rubber 10 mm would be {rubber*1000:.0f} g; '
      f'closed-cell foam 15 mm {foam*1000:.0f} g with a 1 mm PE sheet on its face {sheet*1000:.0f} g')
print(f'  two boards {2*board*1000:.0f} g; two cells {cells*1000:.0f} g; the display {display*1000:.0f} g (assumed): '
      f'{(foam+sheet+2*board+cells+display)*1000:.0f} g before the housing')
for F_hand in (10, 20):
    p_kpa = F_hand / a_head / 1000
    print(f'  {F_hand} N of the hand over the whole face: {p_kpa:.2f} kPa, against 35-65 kPa that squeezes '
          f'30 kg/m3 PE foam by a quarter: under {p_kpa/35*25:.1f} % of its thickness, {p_kpa/35*0.25*15:.2f} mm of 15, if linear')
area_out = a_head + math.pi * D_HEAD * 0.04               # the back and a 40 mm rim; the front is the rubber on the wall
h_air = 10.0                                              # W/m2K, still air and radiation together (assumed)
print(f'  {w:.1f} W out through the back and the rim ({area_out*1e4:.0f} cm2) at about {h_air:.0f} W/m2K: '
      f'about {w/(area_out*h_air):.0f} K over the room outside, more inside; no fan')

print('== locating the box by angle alone')
for D in (1, 2, 5):
    print(f'  {D} m: 1 cm sideways = {math.degrees(0.01/D):.2f} deg; a 1.3 deg error = {math.tan(math.radians(1.3))*D*100:.1f} cm')
print(f'  a 20 cm array at 5.5 GHz separates two sources {math.degrees(C0/F55/0.20):.0f} deg apart')

print('== eleven receivers into one processor (CSI as int8 I/Q + 50 B of header)')
for sc, bw in ((64, 20), (128, 40), (242 + 53, 'HE20 + LLTF')):
    rep = sc * 2 + 50
    for pps in (100, 1000):
        print(f'  {bw}{" MHz" if isinstance(bw, int) else ""}, {pps} packets/s: {rep*pps*8/1e6:.1f} Mbit/s a receiver, {11*rep*pps/1e6:.2f} MB/s for eleven')

print('== a reduced report: 16 groups of subcarriers, 2 B each, 20 B of header')
print(f'  1000 packets/s: {(16*2+20)*1000*8/1e3:.0f} kbit/s a receiver')

print('== the link: is the receiver short of signal? (2.44 GHz, 20 MHz)')
EIRP, G_PATCH, NF = 20.0, 3.0, 6.0      # dBm: the EU limit (ETSI EN 300 328); dBi and dB: assumed
noise = -174 + 10 * math.log10(20e6) + NF
print(f'  sender {EIRP:.0f} dBm EIRP, patch {G_PATCH:.0f} dBi (assumed), noise {noise:.0f} dBm in 20 MHz (NF {NF:.0f} dB assumed)')
for d, wall, t in ((3, 'brick', 0.29), (3, 'brick', 0.60), (10, 'brick', 0.60), (3, 'damp', 0.60)):
    fspl = 20 * math.log10(4 * math.pi * d / (C0 / F24))
    wl = (loss_db_per_m('brick', F24) if wall == 'brick' else loss_es(3.6, 0.070, F24)) * t
    rx = EIRP - fspl - wl + G_PATCH
    print(f'  {d:2d} m of air, {wall} {t*100:.0f} cm ({wl:.0f} dB): {rx:.0f} dBm, SNR {rx-noise:.0f} dB on every subcarrier')
print('  so thermal noise is not the limit; the int8 CSI and the gain\'s stability are (open)')

print('== a patch on FR4 (er 4.4, 1.6 mm), transmission-line model')
er, h = 4.4, 1.6e-3
for f in (F24, F55):
    W = C0 / (2 * f) * math.sqrt(2 / (er + 1))
    ee = (er + 1) / 2 + (er - 1) / 2 * (1 + 12 * h / W) ** -0.5
    dL = 0.412 * h * (ee + 0.3) * (W / h + 0.264) / ((ee - 0.258) * (W / h + 0.8))
    print(f'  {f/1e9:.2f} GHz: {(C0/(2*f*math.sqrt(ee))-2*dL)*1e3:.0f} x {W*1e3:.0f} mm (half a wavelength in air {C0/f/2*1e3:.0f} mm)')

print('== a PZT disc in its first radial mode, f = Np/D, Np 2000-2230 Hz*m')
for Dm in (0.020, 0.040, 0.050):
    print(f'  {Dm*1000:.0f} mm: {2000/Dm/1e3:.0f}-{2230/Dm/1e3:.0f} kHz')
