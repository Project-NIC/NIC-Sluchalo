"""Does one STM32H7A3 carry the head of ten? The arithmetic as picture.py does it. Level 4; the
concept's cpu.py counted a slid head of eleven and stays as its record.

The H7A3 taken, as there, at half a multiply-accumulate a cycle of its 280 MHz (DS13195 Rev 8).
Counted in real multiply-accumulates; a complex one is four.

Run: python3 cpu8.py > cpu8.out
"""
import math
from layout import N_RING, from_rod, PATCH_L

CAP = 0.5 * 280e6
N_RX = N_RING + 2
PX = 0.005                                        # the picture's pixel, as picture.py
R_PIC = from_rod()[-1] + PATCH_L / 2
PIX = math.pi * R_PIC ** 2 / PX ** 2              # pixels in the disc one turn covers
T_TURN, FPS = 4.0, 100                            # a turn of four seconds; frames a second from each sender
GROUPS = 16                                       # subcarriers taken in 16 groups, each its own picture, then combined
FRAMES = 2 * FPS * T_TURN                         # the upright's and the level's

per_report = 2 * 4 + 6 * 2                        # weights cos/sin, the report into its pixel's six sums (complex)
stream = N_RX * 2 * FPS * GROUPS * per_report     # every second, while turning
level = 40 * FRAMES * N_RX * GROUPS * 4 * 4       # picture.py's levelling: 40 rounds, four complex products a report
blur = 9 * 2 * 21 * PIX * GROUPS                  # nine sums blurred, separable, 21 taps each way
solve = PIX * GROUPS * 3 ** 3 * 4                 # a 3 x 3 complex solve a pixel
fft = 3 * 2 * 5 * 160 * 160 * math.log2(160 * 160) / 2 * GROUPS / GROUPS   # focusing: three fields, there and back, once
end = level + blur + solve + fft

print(f'the head of {N_RX}; a turn of {T_TURN:.0f} s at {FPS} frames a second from each sender; {GROUPS} groups of subcarriers;')
print(f'the picture a disc {2*R_PIC*100:.0f} cm across in {PX*1000:.0f} mm pixels, {PIX:.0f} of them; capacity {CAP/1e6:.0f} M MAC/s')
print(f'  while turning, every report into the picture: {stream/1e6:.2f} M/s = {stream/CAP*100:.1f} %')
print(f'  at the end of the turn, once:')
for name, v in (('levelling the receivers (40 rounds)', level), ('blurring the sums', blur),
                ('the 3 x 3 solve in every pixel', solve), ('carrying it back through the wall (FFT)', fft)):
    print(f'    {name}: {v/1e6:.1f} M = {v/CAP*1000:.0f} ms')
print(f'    together: {end/1e6:.0f} M = {end/CAP:.2f} s after the turn')
datel = 8 * 200e3 * 2 + 8 * 200e3 * 4
print(f'  Datel while the head stands (lock-in and band energies, as cpu.py): {datel/1e6:.1f} M/s = {datel/CAP*100:.0f} %')

held = FRAMES * N_RX * GROUPS * 8                 # the reduced reports, complex single precision, kept for the levelling
raw = FRAMES * N_RX * ((242 + 53) * 2 + 50)       # what the receivers measured, int8, for Kádrovák
sums = 9 * PIX * GROUPS * 8
print(f'  memory: the reduced reports of one turn {held/1e6:.2f} MB, the pixel sums {sums/1e6:.2f} MB, against about 1.4 MB of RAM;')
print(f'          the raw reports of one turn {raw/1e6:.1f} MB go straight on to Kádrovák, not into RAM')
