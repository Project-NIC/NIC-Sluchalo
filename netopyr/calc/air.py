"""NIC-Sluchalo (Netopýr): how much the air takes from a leak's sound, by frequency (ISO 9613-1).

alpha in dB/m at a temperature, relative humidity and pressure; then what a path costs.
"""
import math


def alpha(f, t_c=20.0, rh=50.0, p_kpa=101.325):
    T, T0, T01 = t_c + 273.15, 293.15, 273.16
    pr = p_kpa / 101.325
    psat = 10 ** (-6.8346 * (T01 / T) ** 1.261 + 4.6151)
    h = rh * psat / pr
    fro = pr * (24 + 4.04e4 * h * (0.02 + h) / (0.391 + h))
    frn = pr * (T / T0) ** -0.5 * (9 + 280 * h * math.exp(-4.170 * ((T / T0) ** (-1 / 3) - 1)))
    return 8.686 * f * f * (1.84e-11 / pr * (T / T0) ** 0.5 + (T / T0) ** -2.5 * (
        0.01275 * math.exp(-2239.1 / T) / (fro + f * f / fro)
        + 0.1068 * math.exp(-3352.0 / T) / (frn + f * f / frn)))


if __name__ == "__main__":
    print("f kHz   dB/m (20 C, 50 %)   (10 C, 30 %)   lost over 3 m / 10 m (20 C, 50 %)")
    for f in (20e3, 40e3, 60e3, 80e3, 100e3):
        a, b = alpha(f), alpha(f, 10, 30)
        print(f"{f/1000:5.0f}   {a:8.2f}            {b:8.2f}        {3*a:5.1f} / {10*a:5.1f} dB")
