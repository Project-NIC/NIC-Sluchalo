"""NIC-Sluchalo (Netopýr): what a cover over the sound holes takes from the ultrasound — rough.

A non-porous film, by the mass law at normal incidence (unclamped, so the best case: a film
clamped over a sub-millimetre hole is stiffer and loses more):  TL = 10 log10(1 + (w m / 2 rho c)^2).
A porous mesh, as a pure acoustic resistance R in series:      IL = 20 log10(1 + R / (2 rho c)).
"""
import math

RHO, C = 1.2, 343.0
Z2 = 2 * RHO * C


def film(f, thick_um, density=1390.0):          # PET by default
    m = density * thick_um * 1e-6
    return 10 * math.log10(1 + (2 * math.pi * f * m / Z2) ** 2)


def mesh(R):
    return 20 * math.log10(1 + R / Z2)


if __name__ == "__main__":
    fs = (25e3, 45e3, 80e3)
    print("film (PET)      " + "  ".join(f"{f/1e3:4.0f} kHz" for f in fs))
    for t in (2, 5, 10, 25):
        print(f"  {t:3d} um       " + "  ".join(f"{film(f, t):6.1f} dB" for f in fs))
    print("mesh, resistance  loss (all frequencies, ideal)")
    for R in (20, 75, 260):
        print(f"  {R:4d} rayl       {mesh(R):4.1f} dB")
