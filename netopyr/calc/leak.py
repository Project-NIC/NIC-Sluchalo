"""NIC-Sluchalo (Netopýr): how small a leak the camera hears, against the ear (24 Nov 2026). A rough model.

The source: air (or another gas) through a round hole from a pressure p (bar gauge), choked above
~0.9 bar: mass flow m = 0.0404 A p0 / sqrt(T) (air, SI), jet ~400 m/s, jet power 1/2 m U^2;
the sound ETA of it (1e-4 here; jets 1e-4..1e-3 — the largest unknown), its spectrum rising as f^2
to a peak at f = 0.2 U / d and falling as 1/f^2 above (a common rough shape). Spread in a half space
(the leak on a pipe or wall). The air's loss from air.py (ISO 9613-1, 20 degC, 50 %).
The camera: 32 SPH0641, each ~94 - 64.3 = ~30 dB SPL of its own noise over ~20 kHz (its audio-band
SNR, assumed flat into 25-45 kHz — ultrasonic mode to be checked in the sheet), the array's 15 dB
on uncorrelated noise, and the map averaged 0.1 s over the 20 kHz band: 5 log10(B T) more.
The ear: 2-16 kHz, the threshold ~10-20 dB SPL there in a quiet room; in a hall the hall decides.
"""
import math
from air import alpha

ETA = 1e-4
def band_power(d, p_bar, f1, f2):
    a = math.pi * d * d / 4; p0 = (p_bar + 1.013) * 1e5
    m = 0.0404 * a * p0 / math.sqrt(293.0); u = 400.0
    w = ETA * 0.5 * m * u * u; fp = 0.2 * u / d
    def shape(f): return (f / fp) ** 2 if f < fp else (fp / f) ** 2
    tot = sum(shape(fp * 10 ** (k / 100)) * fp * 10 ** (k / 100) for k in range(-400, 400)) * math.log(10) / 100
    inb = sum(shape(f1 * (f2 / f1) ** (k / 200)) * f1 * (f2 / f1) ** (k / 200) for k in range(200)) * math.log(f2 / f1) / 200
    return w * inb / tot, m / 1.2 * 6e4            # W in the band; litres a minute (standard)

def spl(w, r, fmid):
    return 10 * math.log10(w / 1e-12) - 10 * math.log10(2 * math.pi * r * r) - alpha(fmid) * r

FLOOR = 94 - 64.3 - 10 * math.log10(32) - 5 * math.log10(20e3 * 0.1)
print(f"the camera's floor in 25-45 kHz: ~{FLOOR:.0f} dB SPL (quiet place; a hall's own ultrasound is usually higher)")
print("the ear's: ~10-20 dB SPL in 2-16 kHz in a quiet room; a hall's 70-90 dB drowns any hiss\n")
print(" hole, 6 bar     flow L/min | camera band 25-45 kHz at 1 / 3 / 10 m | ear band 2-16 kHz at 1 m")
for d in (0.05e-3, 0.1e-3, 0.2e-3, 0.5e-3, 1e-3):
    wb, q = band_power(d, 6, 25e3, 45e3); we, _ = band_power(d, 6, 2e3, 16e3)
    c = [spl(wb, r, 35e3) for r in (1, 3, 10)]; e = spl(we, 1, 8e3)
    print(f" {d*1e3:4.2f} mm   {q:9.2f}      | " + " / ".join(f"{v:5.0f}" for v in c) + f" dB      | {e:5.0f} dB")
