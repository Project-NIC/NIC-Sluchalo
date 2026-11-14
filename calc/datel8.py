"""Datel on the head of ten: the knock's rod through Předseda's middle, the microphones in the
annulus between Předseda and the ring, the head 15 mm of air off the wall (no foam, no pipes
through it). Does the wall's answer still come before the sound through the air? Level 4.

A leaky surface wave radiates into the air at the angle asin(c_air / v_R); a microphone at height
h above the wall, d from the knock along it, hears it after (d - h tan a) / v_R + h / (c_air cos a)
(the ray leaves the wall short of the microphone). The sound straight from the rod's tip comes
after sqrt(d^2 + h^2) / c_air. Speeds as acoustics.py (brick Vp 1430-3100 m/s, Poisson 0.15-0.25,
v_R = 0.92 Vs).

Run: python3 datel8.py > datel8.out
"""
import math, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):     # acoustics.py prints its own tables on import
    from acoustics import vs, VP_BRICK, V_AIR
import layout

GAP = 0.015                                       # the head's face from the wall
BOARD = 0.0016
R_MIC = layout.R                                  # the microphones by the ring, between its antennas (layout.py)
print(f'the microphones {R_MIC*1000:.0f} mm from the knock (layout.py)')
speeds = sorted(0.92 * vs(vp, nu) for vp in VP_BRICK for nu in (0.15, 0.25))
v_slow, v_fast = speeds[0], speeds[-1]
print(f'surface waves in brick {v_slow:.0f}-{v_fast:.0f} m/s; air {V_AIR} m/s')
for h, word in ((GAP, 'a microphone at the wall side of Front, 15 mm off'), (GAP + BOARD, 'on Front\'s back, through a hole, 16.6 mm off')):
    print(f'== {word}')
    for d in (0.040, 0.050, R_MIC):
        air = math.hypot(d, h) / V_AIR
        row = []
        for v in (v_slow, v_fast):
            a = math.asin(V_AIR / v)
            t = (d - h * math.tan(a)) / v + h / (V_AIR * math.cos(a))
            row.append((t, air - t))
        print(f'  {d*1000:.0f} mm from the knock: the wall\'s answer after {row[0][0]*1e6:.0f}-{row[1][0]*1e6:.0f} us, '
              f'the air\'s after {air*1e6:.0f} us: {row[0][1]*1e6:.0f}-{row[1][1]*1e6:.0f} us between them')
