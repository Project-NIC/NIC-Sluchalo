"""NIC-Sluchalo (Netopýr): the sound hole through the board in front of a bottom-port microphone.

The hole is a short tube, open to the air at one end, closed by the microphone's small front
volume at the other: its first resonance near a quarter wavelength over its length with the end
correction. Rough (a quarter-wave tube, not the full Helmholtz model with the microphone's own
cavity); it says only which board thickness keeps the resonance above the band.
"""
C = 343.0


def quarter_wave(board_mm, hole_mm):
    r = hole_mm / 2 / 1000
    l_eff = board_mm / 1000 + 0.6 * r          # flanged open end
    return C / (4 * l_eff)


if __name__ == "__main__":
    print("board mm  hole mm  first resonance kHz")
    for t in (1.6, 1.0, 0.8, 0.6):
        for d in (0.7, 1.0):
            print(f"  {t:4.1f}     {d:3.1f}       {quarter_wave(t, d)/1000:5.0f}")
