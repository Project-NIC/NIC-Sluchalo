"""Wall materials and constants: the one home of every material figure in NIC-Sluchalo.

ITU-R P.2040-3 (08/2023), Table 3: real permittivity eps' = a*f^b, conductivity sigma = c*f^d,
f in GHz. Water: Debye model at 20 degC (eps_s 80.1, eps_inf 5.6, tau 9.36 ps).
"""
import math, cmath

C0 = 299792458.0
EPS0 = 8.854187817e-12
MU0 = 4e-7 * math.pi
ETA0 = 376.730313

ITU = {  # name: (a, b, c, d, valid GHz)
    'brick': (3.91, 0.0, 0.0238, 0.16, (1, 10)),
    'plasterboard': (2.73, 0.0, 0.0085, 0.9395, (1, 100)),
    'concrete': (5.24, 0.0, 0.0462, 0.7822, (1, 100)),
}

def eps_sigma(m, f_ghz):
    a, b, c, d, _ = ITU[m]
    return a * f_ghz ** b, c * f_ghz ** d

def eps_complex(m, f_hz):
    if m == 'air':
        return 1.0 + 0j
    if m == 'water':
        w = 2 * math.pi * f_hz
        return 5.6 + (80.1 - 5.6) / (1 + 1j * w * 9.36e-12)
    er, s = eps_sigma(m, f_hz / 1e9)
    return er - 1j * s / (2 * math.pi * f_hz * EPS0)

def k(m, f_hz):
    """Complex wavenumber, time convention e^{+jwt} (Im < 0 means loss)."""
    return 2 * math.pi * f_hz / C0 * cmath.sqrt(eps_complex(m, f_hz))

def loss_db_per_m(m, f_hz):
    return 8.686 * abs(k(m, f_hz).imag)

def speed(m, f_hz):
    """Phase velocity in m/s."""
    return 2 * math.pi * f_hz / k(m, f_hz).real

def wavelength(m, f_hz):
    return speed(m, f_hz) / f_hz
