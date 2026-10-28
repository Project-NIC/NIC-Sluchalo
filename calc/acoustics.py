"""Ultrasound in solid brick: wavelengths, impedances, reflections, echo times. Run: python3 acoustics.py

Sources (in ../concept.md): brick Vp 1430-3100 m/s (fired clay studies, dry); masonry panel 1584 m/s
with joints; mortar Vp 1939-2649 m/s at 1514-1840 kg/m3; solid brick CP 4.5 kg for 290x140x65 mm;
copper 8960 kg/m3, 4660 m/s; air 1.2 kg/m3, 343 m/s. Poisson's ratio of brick not found:
0.15-0.25 assumed, Vs = Vp*sqrt((1-2v)/(2(1-v))); Rayleigh speed taken as 0.92 Vs. Rods: steel
E 200 GPa, 7850 kg/m3; aluminium 69 GPa, 2700 kg/m3 (handbook values).
"""
import math

RHO_BRICK = 4.5 / (0.290 * 0.140 * 0.065)
VP_BRICK = (1430, 3100)
VP_MORTAR, RHO_MORTAR = (1939, 2649), (1514, 1840)
RHO_CU, VP_CU = 8960, 4660
RHO_AIR, V_AIR = 1.2, 343

def vs(vp, nu):
    return vp * math.sqrt((1 - 2 * nu) / (2 * (1 - nu)))

print(f'== solid brick: density {RHO_BRICK:.0f} kg/m3')
for nu in (0.15, 0.25):
    print(f'  Poisson {nu}: Vs/Vp = {vs(1, nu):.2f}')
print('== wavelengths in brick (cm)')
for f in (25e3, 45e3, 100e3):
    p = [v / f * 100 for v in VP_BRICK]
    s = [vs(VP_BRICK[0], 0.25) / f * 100, vs(VP_BRICK[1], 0.15) / f * 100]
    print(f'  {f/1e3:.0f} kHz: P {p[0]:.1f}-{p[1]:.1f}, S {s[0]:.1f}-{s[1]:.1f}')
Zb = [RHO_BRICK * v for v in VP_BRICK]
Zm = [RHO_MORTAR[0] * VP_MORTAR[0], RHO_MORTAR[1] * VP_MORTAR[1]]
Za, Zc = RHO_AIR * V_AIR, RHO_CU * VP_CU
print(f'== acoustic impedance (MRayl): brick {Zb[0]/1e6:.1f}-{Zb[1]/1e6:.1f}, mortar {Zm[0]/1e6:.1f}-{Zm[1]/1e6:.1f}, '
      f'copper {Zc/1e6:.0f}, air {Za:.0f} Rayl; brick/air = {Zb[0]/Za:,.0f}-{Zb[1]/Za:,.0f} times')
def R(z1, z2): return (z2 - z1) / (z2 + z1)
print('== reflection at normal incidence (amplitude)')
print(f'  brick -> air: {R(Zb[0], Za):+.3f}  (all of it, phase inverted)')
worst = max(abs(R(a, b)) for a in Zb for b in Zm)
print(f'  brick -> mortar: up to {worst:.2f} in magnitude over both ranges (a joint is a weak mirror)')
print(f'  brick -> copper: {R(Zb[1], Zc):+.2f} to {R(Zb[0], Zc):+.2f} (same phase)')
print('== echo time, there and back (us)')
for d in (0.015, 0.03, 0.05):
    t = [2 * d / vs(v, nu) * 1e6 for v, nu in ((VP_BRICK[1], 0.15), (VP_BRICK[0], 0.25))]
    print(f'  {d*100:.1f} cm by shear wave: {t[0]:.0f}-{t[1]:.0f}')
for f in (45e3, 100e3):
    print(f'  a pulse of 1-2 cycles at {f/1e3:.0f} kHz lasts {1/f*1e6:.0f}-{2/f*1e6:.0f} us')

print('== surface (Rayleigh) waves, which a microphone above the wall hears')
for f in (25e3, 40e3, 45e3):
    lo, hi = 0.92 * vs(VP_BRICK[0], 0.25), 0.92 * vs(VP_BRICK[1], 0.15)
    print(f'  {f/1e3:.0f} kHz: speed {lo:.0f}-{hi:.0f} m/s, wavelength {lo/f*100:.1f}-{hi/f*100:.1f} cm (they reach about one wavelength deep)')
print(f'  sound straight through the air: 343 m/s - slower than any of them, so the ring can tell it apart by its arrival')
T = [4 * z * Za / (z + Za) ** 2 for z in Zb]
print(f'== brick -> air, energy across the boundary: {10*math.log10(T[1]):.1f} to {10*math.log10(T[0]):.1f} dB')
print('== a half-wave rod on a 40 kHz exciter (bar speed sqrt(E/rho))')
for name, E, rho in (('steel', 200e9, 7850), ('aluminium', 69e9, 2700)):
    c = math.sqrt(E / rho)
    print(f'  {name}: {c:.0f} m/s, half a wavelength at 40 kHz = {c/40e3/2*100:.1f} cm')

print('== the tap: a steel ball\'s contact time on concrete Tc = 0.0043*D, useful up to about 291/D Hz')
print('   (Sansalone & Streett; on softer plaster the contact is longer and the top frequency lower)')
for D in (0.003, 0.005, 0.009, 0.015):
    print(f'  ball {D*1000:.0f} mm: contact {0.0043*D*1e6:.0f} us, up to about {291/D/1e3:.0f} kHz')

print('== shaping the knock: the edge\'s rise time sets how high its spectrum reaches (f ~ 0.35/tr)')
print('   a buzzer disc is ~45-50 nF (PUI AB2720B / AB2726B); the edge is set by the resistor it charges through')
C = 47e-9
for R in (10, 100, 1000, 10000):
    tr = 2.2 * R * C
    print(f'  {R:>5} ohm: rise {tr*1e6:7.1f} us -> up to about {0.35/tr/1e3:7.1f} kHz')

print('== the knock\'s energy: 1/2 C V^2 per edge, lost in the resistor or the MOSFET whatever its value')
for V in (5, 15, 30):
    e = 0.5 * C * V ** 2
    print(f'  buzzer 47 nF at {V:>2} V: {e*1e6:5.1f} uJ an edge; on and off 10 times a second {2*e*10*1e3:.2f} mW, 1000 times {2*e*1000*1e3:.0f} mW')
print(f'  for comparison, a professional point-contact probe (ACS S1802, 700 pF) at 200 V: {0.5*700e-12*200**2*1e6:.0f} uJ')

print('== SNR: the microphone sets it, the chain behind it only must not spoil it')
for name, snr, sens in (('analog MEMS, SPU0410LR5H-QB', 63.0, -38.0), ('digital PDM, SPH0641LU4H-1', 64.3, None)):
    noise_spl = 94 - snr
    line = f'  {name}: SNR {snr} dB(A) -> its own noise {noise_spl:.1f} dB SPL (A-weighted, 20 kHz band)'
    if sens is not None:
        v = 10 ** (sens / 20) * 20e-6 * 10 ** (noise_spl / 20)
        line += f' = {v*1e6:.1f} uV at its output'
    print(line)
amp = 5e-9 * math.sqrt(20e3)
print(f'  an op-amp of 5 nV/sqrt(Hz) over 20 kHz adds {amp*1e6:.2f} uV - far under the microphone')
for bits in (12, 16):
    print(f'  an ideal {bits}-bit ADC: {6.02*bits+1.76:.0f} dB (the real ENOB is lower; from the datasheet)')
print('  what a coherent measurement adds, the same for analog and digital:')
for bw in (1000, 100):
    print(f'    a {bw} Hz band around the tone instead of 20 kHz: +{10*math.log10(20e3/bw):.0f} dB')
for n in (10, 100):
    print(f'    {n} knocks averaged in step: +{10*math.log10(n):.0f} dB')

print("== what the microphone gets: the wall's surface moving radiates p = rho c v")
for x_nm in (0.1, 1.0, 10.0):
    for f in (40e3, 80e3):
        v = 2 * math.pi * f * x_nm * 1e-9
        print(f'  {x_nm:4.1f} nm at {f/1e3:.0f} kHz: {20*math.log10(412 * v / 20e-6):.0f} dB SPL')
print('  against the microphone\'s own noise of about 30 dB SPL, A-weighted in the audio band; its noise at 40-80 kHz is not published (open)')

print('== the tap against the knock, and what drives a disc')
m9 = 7850 * 4 / 3 * math.pi * 0.0045 ** 3
print(f'  a 9 mm steel ball ({m9*1000:.1f} g) at 1 m/s: {0.5*m9*1e3:.1f} mJ, against 5.3 uJ of electrical energy in a 15 V knock')
print(f'  a 47 nF disc at 40 kHz: {1/(2*math.pi*40e3*47e-9):.0f} ohm - more than an on-chip op-amp of a few mA can drive')

print('== a sound pipe from the wall to a microphone behind the antenna board')
c_air, nu, gamma, Pr = 343.0, 1.5e-5, 1.4, 0.71
for d in (0.001, 0.002, 0.003):
    print(f'  {d*1000:.0f} mm across: one plane wave only up to {1.841*c_air/(math.pi*d)/1e3:.0f} kHz')
for a in (0.0005, 0.001):
    for f in (40e3, 80e3):
        w = 2 * math.pi * f
        alpha = math.sqrt(w * nu / 2) * (1 + (gamma - 1) / math.sqrt(Pr)) / (a * c_air)   # Np/m, wide-tube limit
        print(f'  {a*2000:.0f} mm across at {f/1e3:.0f} kHz: the walls cost {alpha*8.686/100:.2f} dB a centimetre')
for L in (0.005, 0.010, 0.0166):
    res = [c_air * (2 * k + 1) / (4 * L) / 1e3 for k in range(6)]
    print(f'  {L*1000:.0f} mm long, closed at the microphone: resonances at ' + ', '.join(f'{r:.0f}' for r in res if r < 120) + ' kHz')

print("== Datel in the head: the tip through the middle patch, the microphones around it")
for name, E, rho in (('POM (acetal)', 3.0e9, 1410), ('PEEK', 3.6e9, 1300), ('aluminium', 69e9, 2700)):
    c = math.sqrt(E / rho)
    print(f'  a rod of {name}: {c:.0f} m/s, half a wavelength at 40 kHz {c/2/40e3*100:.1f} cm')
r_in, r_out = 0.015 + 0.003, 0.0658 - 0.015 - 0.003      # beyond the middle patch, short of the ring's patches
print(f'  the free annulus for microphones: {r_in*1000:.0f}-{r_out*1000:.0f} mm from the middle')
for r in (0.025, 0.035, 0.045):
    print(f'  a microphone {r*1000:.0f} mm from the tip: the wall\'s surface wave after {r/1830*1e6:.0f}-{r/760*1e6:.0f} us, '
          f'the sound through the air after {r/343*1e6:.0f} us')

print("== Datel's rod: what holds it on the wall (the rod 28 mm: 15 mm of foam with its sheet, 1.6 mm of board, 11 mm to the disc)")
E_POM, L_ROD = 3.0e9, 0.0276
for d in (0.001, 0.002):
    I = math.pi * d ** 4 / 64
    print(f'  a POM rod {d*1000:.0f} mm thick buckles at {math.pi**2*E_POM*I/(2*L_ROD)**2:.1f} N '
          f'(glued at one end, free at the other) to {math.pi**2*E_POM*I/L_ROD**2:.1f} N (both ends held)')
D_br = 100e9 * 0.2e-3 ** 3 / (12 * (1 - 0.3 ** 2))         # a 27 mm buzzer: brass 0.2 mm, the ceramic left out
k_disc = 16 * math.pi * D_br / 0.0135 ** 2                  # a clamped plate pushed at its centre
print(f'  the buzzer disc at its centre, clamped at its rim: at least {k_disc/1000:.0f} N/mm (its ceramic stiffens it further)')
for dx in (0.05, 0.15):
    print(f'    the foam giving {dx:.2f} mm more under the hand: {k_disc*dx/1000:.0f} N more on the rod')
k_foam, m_disc = 500.0, 0.002                               # assumed: a soft foam ring, the disc with its rod
print(f'  the disc on a soft foam ring of {k_foam/1000:.1f} N/mm (assumed), pressed 2 mm: {k_foam*0.002:.1f} N on the rod, '
      f'{k_foam*0.00015:.2f} N more for 0.15 mm of the foam')
print(f'    the disc ({m_disc*1000:.0f} g with its rod) bounces on the foam at {math.sqrt(k_foam/m_disc)/(2*math.pi):.0f} Hz; '
      'above that the knock pushes against the disc\'s own mass, as an inertial exciter does')
print(f'  the rod itself, {L_ROD*1000:.0f} mm of POM ({math.sqrt(E_POM/1410):.0f} m/s), rings along its length at '
      + ', '.join(f'{k*math.sqrt(E_POM/1410)/(2*L_ROD)/1e3:.0f}' for k in (1, 2, 3)) + ' kHz - the same every knock')
