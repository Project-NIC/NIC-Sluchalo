# NIC-Sluchalo (Netopýr), the 3.3 V branch's surges (24 Nov 2026): is one C_P (47 uF Al polymer, 40 mohm, + 1 uF)
# before the four LDOs enough when the camera shares the branch? The camera's current is still open
# (UM3354), so it is swept. U23's own answer read from TPS63020 SLVS916I fig. 21 (a 1 A step, 0.5 -> 1.5 A,
# VIN 2.4 V): the output moves ~50-60 mV (50 mV/div), settled within the 2 ms/div trace's resolution.
import math
C_U23 = 2*22e-6*0.6          # U23's 2 x 22 uF ceramics, ~60 % left at 3.3 V (DC bias, guessed)
C_P   = 47e-6 + 1e-6         # one C_P
ESR   = 0.040
FIG21 = 0.060                # V per A, from the figure
T_LOOP = 20e-6               # time until U23's loop answers (a 2.4 MHz converter, assumed)
PSRR_LDO = 10**(-75/20)      # TPS7A20 at 20 mA, 10-100 kHz (SBVS338H)
def lc(f, L=33e-6, R=0.82, C=48e-6, esr=ESR):
    w = 2*math.pi*f; zc = complex(esr, -1/(w*C)); return abs(zc/(zc + complex(R, w*L)))
print("camera step | U23 (fig. 21) | caps alone for 20 us: one C_P at the branch / two | at a petal's 1.8 V (LDO + LC at 10 kHz)")
for dI in (0.1, 0.2, 0.3, 0.5):
    v_fig = dI*FIG21
    v1 = dI*ESR/2 + dI*T_LOOP/(C_U23 + 2*C_P)      # U23's C_P and the branch's C_P in parallel
    v2 = dI*ESR/3 + dI*T_LOOP/(C_U23 + 3*C_P)
    print(f"{dI*1e3:4.0f} mA | {v_fig*1e3:5.1f} mV | {v1*1e3:5.1f} / {v2*1e3:5.1f} mV | "
          f"{max(v_fig,v1)*PSRR_LDO*lc(10e3)*1e6:.2f} uV")
# a ripple in the band: the camera's line rate (IMX335-class, ~2000 lines at 30 fps = ~60 kHz)
f = 60e3; w = 2*math.pi*f
z = abs(1/(1/complex(ESR, -1/(w*47e-6)) + 1/complex(0.002, -1/(w*(C_U23 + 1e-6)))))
for dI in (0.01, 0.05):
    v = dI*z
    print(f"line-rate ripple {dI*1e3:.0f} mA at 60 kHz: {v*1e3:.2f} mV on 3.3 V -> "
          f"{v*PSRR_LDO*lc(f)*1e9:.2f} nV at the petal")
