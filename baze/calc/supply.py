"""NIC-Sluchalo (Netopýr): does the microphones' supply need a low-noise LDO?

The microphone (SPH0641LU4H-1 Rev B, ultrasonic mode): PSRR 55 dBV/FS (200 mVpp at 1 kHz),
i.e. 1 Vrms on VDD shows at -55 dBFS; its own noise floor is the sensitivity (-26 dBFS at 94 dB SPL)
less its SNR (64.3 dB). An LDO's output noise, in Vrms over the band, against that floor.
PSRR is given at 1 kHz only; in the 25-80 kHz band it is likely worse — a margin is taken.
"""
import math

PSRR_DBVFS = 55.0
FLOOR = -26.0 - 64.3          # dBFS, the microphone's own noise
MARGIN_HF = 20.0              # assumed loss of PSRR at ultrasound, dB


def at_output(noise_vrms):
    return 20 * math.log10(noise_vrms) - PSRR_DBVFS + MARGIN_HF


if __name__ == "__main__":
    print(f"microphone's own noise floor: {FLOOR:.1f} dBFS")
    for lab, v in (("TPS7A20, 7 uVrms", 7e-6), ("a plain LDO, ~100 uVrms", 100e-6),
                   ("a noisy one, ~1 mVrms", 1e-3), ("DK's 5 V switching ripple passed, ~10 mVrms", 10e-3)):
        o = at_output(v)
        print(f"  {lab:44s} -> {o:6.1f} dBFS, {FLOOR - o:5.1f} dB under the floor")


# --- The filter in front of each petal: an RC, or a choke's LC? ---------
def rc(f, R, C):
    return -10 * math.log10(1 + (2 * math.pi * f * R * C) ** 2)


def lc(f, L, C, Rs):
    """A series L (with its resistance Rs) into a shunt C: the second-order low-pass."""
    w = 2 * math.pi * f
    zl = complex(Rs, w * L)
    zc = 1 / complex(0, w * C)
    return 20 * math.log10(abs(zc / (zl + zc)))


if __name__ == "__main__":
    L, CL, RL = 2.2e-6, 20e-6, 0.1        # SWPA252012S2R2MT (C23894), the π's 2 x 10 uF, DCR + ESR
    R, CR = 4.7, 22e-6                     # 4.7 ohm, 22 uF: ~25 mA a petal drops ~0.12 V
    f0 = 1 / (2 * math.pi * math.sqrt(L * CL))
    print(f"\nthe choke's LC resonates at {f0/1e3:.0f} kHz (Q ~ {math.sqrt(L/CL)/RL:.1f}); the RC's corner at {1/(2*math.pi*R*CR)/1e3:.1f} kHz")
    print("  f kHz    LC dB    RC dB")
    for f in (1e3, 10e3, 25e3, 35e3, 45e3, 80e3, 1e6):
        print(f"  {f/1e3:6.0f}  {lc(f, L, CL, RL):6.1f}   {rc(f, R, CR):6.1f}")

    print("\nsmaller or larger LC, against the RC")
    cases = [("1 uH + 1 uF", 1e-6, 1e-6, 0.1), ("2.2 uH + 20 uF", 2.2e-6, 20e-6, 0.1),
             ("10 uH + 47 uF", 10e-6, 47e-6, 0.3), ("22 uH + 47 uF", 22e-6, 47e-6, 0.5)]
    print("  case                         f0 kHz   peak dB   25 kHz   45 kHz   80 kHz")
    for lab, L_, C_, R_ in cases:
        f0_ = 1 / (2 * math.pi * math.sqrt(L_ * C_))
        print(f"  {lab:28s} {f0_/1e3:6.1f}   {lc(f0_, L_, C_, R_):6.1f}   "
              + "   ".join(f"{lc(f, L_, C_, R_):6.1f}" for f in (25e3, 45e3, 80e3)))
    print(f"  {'RC 4.7 ohm + 22 uF':28s}    —        —     "
          + "   ".join(f"{rc(f, R, CR):6.1f}" for f in (25e3, 45e3, 80e3)))

    print("\nthe owner's larger chokes (23 Nov 2026), with 47 uF; DCR as a chip choke of that value has")
    for lab, L_, R_ in (("33 uH, DCR ~2 ohm", 33e-6, 2.0), ("56 uH, DCR ~3.5 ohm", 56e-6, 3.5)):
        f0_ = 1 / (2 * math.pi * math.sqrt(L_ * 47e-6))
        print(f"  {lab:22s} f0 {f0_/1e3:4.1f} kHz, peak {lc(f0_, L_, 47e-6, R_):4.1f} dB; "
              + ", ".join(f"{f/1e3:.0f} kHz {lc(f, L_, 47e-6, R_):6.1f} dB" for f in (25e3, 45e3, 80e3))
              + f"; drop at 25 mA {0.025*R_*1000:.0f} mV")

    print("\nunder 1 ohm (the owner: they can be had), with 47 uF")
    for lab, L_, R_ in (("33 uH, 0.5 ohm", 33e-6, 0.5), ("33 uH, 0.9 ohm", 33e-6, 0.9), ("56 uH, 0.8 ohm", 56e-6, 0.8)):
        f0_ = 1 / (2 * math.pi * math.sqrt(L_ * 47e-6))
        print(f"  {lab:16s} f0 {f0_/1e3:4.1f} kHz, peak {lc(f0_, L_, 47e-6, R_):5.1f} dB; "
              + ", ".join(f"{f/1e3:.0f} kHz {lc(f, L_, 47e-6, R_):6.1f} dB" for f in (25e3, 45e3, 80e3))
              + f"; drop at 25 mA {0.025*R_*1000:.0f} mV")

    # --- An LDO, the LC, or both? (the owner, 23 Nov 2026) ---------------------------------
    # TPS7A20 PSRR (SBVS338H, electrical characteristics, VIN = VOUT + 1 V): light load 75 dB at
    # 10 kHz and 100 kHz, 45 dB at 1 MHz; at 300 mA 75 / 60 / 40 dB. Taken at our ~110 mA as the
    # worse row, read between: ~70 dB at 25 kHz, ~65 at 45, ~60 at 80, ~40 at 1 MHz.
    ldo = {25e3: 70, 45e3: 65, 80e3: 60, 1e6: 40}
    L_, C_, R_ = 33e-6, 47e-6, 0.82          # SWPA3015S330MT (C68342), 47 uF
    print("\nhow much of the source's ripple is taken out, dB")
    print("  f kHz   LC alone   LDO alone   LDO + LC")
    for f in (25e3, 45e3, 80e3, 1e6):
        a = -lc(f, L_, C_, R_)
        print(f"  {f/1e3:5.0f}    {a:5.0f}      {ldo[f]:5.0f}       {a + ldo[f]:5.0f}")
    pd = (5.0 - 3.3) * 0.110
    print(f"  the LDO from the DK's 5 V at ~110 mA: {pd:.2f} W, SOT-23 187 C/W -> +{pd*187:.0f} C")
