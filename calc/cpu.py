"""Does one STM32H7A3 carry it all? Run: python3 cpu.py

The H7A3: Cortex-M7 at 280 MHz with a double-precision FPU and DSP instructions (DS13195 Rev 8).
Taken conservatively at half a multiply-accumulate a cycle.
"""
F_CPU = 280e6
CAP = 0.5 * F_CPU
loads = {
    'a Wi-Fi image with phase (50 x 50 points, 11 receivers, 64 groups of the 242 subcarriers, 20 a second)': 50 * 50 * 11 * 64 * 20,
    'Wi-Fi shadow map from amplitudes (11 receivers x 1000 packets x 16 subcarrier groups, into the map)': 11 * 1000 * 16 * 4,
    "the stroke's focusing, back-projected (100 packets/s kept, 11 receivers, 4 subcarrier groups, 50 x 50 points)": 100 * 11 * 4 * 50 * 50,
    'acoustic lock-in (8 microphones x 200 kS/s x 2)': 8 * 200e3 * 2,
    'acoustic band energies after a knock (8 microphones x 200 kS/s x 4 bands)': 8 * 200e3 * 4,
}
print(f'capacity taken as {CAP/1e6:.0f} M MAC/s')
tot = 0
for k, v in loads.items():
    tot += v
    print(f'  {k}: {v/1e6:.1f} M/s = {v/CAP*100:.0f} %')
print(f'  all at once: {tot/1e6:.1f} M/s = {tot/CAP*100:.0f} % (the PDM filtering is in the DFSDM; the display keeps its own frame in the SSD1963)')
first = tot - 50 * 50 * 11 * 64 * 20 - 100 * 11 * 4 * 50 * 50
print(f'  without the phase image and the focusing: {first/1e6:.1f} M/s = {first/CAP*100:.0f} %')
