"""Iljič's amplifier: how much gain, and how fast an op-amp. Level 5.

The plate's coupling to the live core comes from hum.py (published, level 4): the charge on the plate
per volt on the core, for walls from bone dry to damp. The first stage is a charge amplifier: its
output is the charge over its feedback capacitor, so its "gain" is set by that capacitor, not by the
op-amp; what the op-amp's bandwidth must carry is the noise gain, 1 + C_in / C_f. The second stage
brings the signal up for the processor's ADC. Assumed, not from a sheet: the plate, its trace and the
op-amp's input together 20 pF; C_f 10 pF; the tracer's 10 V on its cable; the ADC 16 bits over 3.3 V.

Run: python3 iljic_amp.py > iljic_amp.out
"""
import math
from hum import plate_charge, DEPTHS

C_IN, C_F = 20e-12, 10e-12
ADC_FS, ADC_BITS = 3.3, 16
LSB = ADC_FS / 2 ** ADC_BITS
cases = [('50 Hz mains, 230 V', 50, 230), ('a tracer, 10 V at 33 kHz', 33e3, 10), ('a tracer, 10 V at 125 kHz', 125e3, 10)]
walls = [('bone dry', 1e-9), ('ordinary', 1e-5), ('damp', 1e-3)]
print(f'the charge amplifier: C_f {C_F*1e12:.0f} pF, the input {C_IN*1e12:.0f} pF; the ADC\'s step {LSB*1e6:.0f} uV')
print('== the charge amplifier\'s output, peak, cable 3 cm deep')
lo, hi = 1e9, 0
for name, f, volts in cases:
    row = []
    for wname, sg in walls:
        v = abs(plate_charge(f, 0.03, sg)) * volts / C_F
        lo, hi = min(lo, v), max(hi, v)
        row.append(f'{wname} {v*1000:9.3f} mV')
    print(f'  {name:28s} ' + '  '.join(row))
print(f'  from {lo*1e6:.1f} uV to {hi*1000:.0f} mV: a range of {20*math.log10(hi/lo):.0f} dB — so the gain is switched, not fixed')
noise_gain = 1 + C_IN / C_F
print('== what the op-amp must carry (gain-bandwidth product)')
for gbw in (1e6, 10e6, 50e6):
    print(f'  GBW {gbw/1e6:4.0f} MHz: the charge amplifier, noise gain {noise_gain:.0f}, holds to {gbw/noise_gain/1e6:5.2f} MHz; '
          f'a second stage of gain 10 to {gbw/10/1e3:6.0f} kHz, of gain 100 to {gbw/100/1e3:5.0f} kHz')
print('== the gain the weakest case wants before the ADC')
weak = lo
for g in (1, 10, 100):
    print(f'  second stage x{g:<3d}: {weak*g*1e6:9.1f} uV peak = {weak*g/LSB:7.2f} ADC steps; a narrow filter in software '
          f'over 0.1 s at 125 kHz gains about {10*math.log10(125e3*0.1/2):.0f} dB more')

# ---- the gain set so that each case fills about 80 % of the ADC (added 14 Nov 2026)
FS = 1.8                                   # the ADC's reference, if the analog supply runs at 1.8 V (the owner's
                                           # recollection; the H7A3 takes a reference from 1.62 V up — to confirm)
C_FS = (100e-12, 10e-12, 1e-12)            # the charge amplifier's feedback, switched: x0.1, x1, x10 against 10 pF
STAGE2 = (1, 10)                           # the second stage: passed by, or x10
PGA = (1, 2, 4, 8, 16)                     # the processor's own op-amp as a programmable gain (to confirm)
print(f'== the gain set for about 80 % of an ADC of {FS} V full scale ({0.8*FS*1000:.0f} mV peak)')
for name, f, volts in cases:
    for wname, sg in walls:
        q = abs(plate_charge(f, 0.03, sg)) * volts
        best = None
        for cf in C_FS:
            for s2 in STAGE2:
                for g in PGA:
                    v = q / cf * s2 * g
                    if v <= 0.8 * FS and (best is None or v > best[0]):
                        best = (v, cf, s2, g)
        v, cf, s2, g = best
        print(f'  {name:28s} {wname:9s} C_f {cf*1e12:5.0f} pF, x{s2:<2d}, PGA x{g:<2d}: {v*1000:6.0f} mV = {v/FS*100:3.0f} % of the ADC')
