"""NIC-Sluchalo (Netopýr): what the map costs to compute, roughly, so that boards can be weighed.

Counts floating-point operations (a complex multiply-add = 8). Rough: no memory traffic, no
overheads; a processor sustains perhaps a third to a half of its peak on such loops.
"""
import math

FS = 192_000         # samples a second, each microphone (the owner, 23 Nov 2026: 192 kHz, four lines)
NFFT = 1024          # FFT length -> bins ~188 Hz apart, ~188 frames a second
N = 32               # microphones


def fft_flops(n):
    return 5 * n * math.log2(n)


def need(grid, bins, fps, clean_iter=0, n=N):
    frames = FS / NFFT
    ffts = n * fft_flops(NFFT) * frames                 # every channel, all the time
    csm = 8 * n * (n + 1) / 2 * bins * frames           # the cross-spectral matrix, Hermitian
    beam = 8 * n * n * grid * bins * fps                # w^H R w at every point and bin
    clean = 8 * n * n * grid * bins * fps * clean_iter  # CLEAN-SC, each iteration ~ one more map
    return ffts, csm, beam, clean


CASES = [
    ("coarse map, 32 x 24, 5 bins, 10 fps", 32 * 24, 5, 10, 0),
    ("coarse map + CLEAN-SC 10 it., 2 fps", 32 * 24, 5, 2, 10),
    ("fine map, 64 x 48, 20 bins, 10 fps", 64 * 48, 20, 10, 0),
    ("fine map + CLEAN-SC 10 it., 5 fps", 64 * 48, 20, 5, 10),
]

# Coarse everywhere, fine only round the peak: the whole field at 32 x 24, 5 bins, and a
# 16 x 16 patch at the fine pitch, 10 bins, cleaned (3 iter.), at 5 frames/s.
ZOOM = [("coarse field", 32 * 24, 5, 10, 0), ("fine patch round the peak, cleaned", 16 * 16, 10, 5, 3)]

# The converter's decimation filter: its flat pass-band as a fraction of fs (PCMD3180 SBASA14A,
# §6.3.6.7). Linear phase: 0.454 at 96 kHz, only 0.3 at 192 kHz, 0.212 at 384 kHz. Low latency:
# 0.466 at 96 kHz, 0.463 at 192 kHz. The same filter on every channel, so its phase cancels in
# the cross-spectra: the low-latency filter is taken.
PASSBAND = {96_000: 0.466, 192_000: 0.463, 384_000: 0.212}  # 384 kHz: linear phase (low latency not listed)

BCLK_MAX = 24.576e6   # PCMD3180's highest BCLK (SBASA14A, Table 6-6; period >= 40 ns)


def lines_needed(fs, n=N, bits=16):
    """TDM lines for n channels at fs, each line at most BCLK_MAX."""
    per_line = int(BCLK_MAX // (bits * fs))
    return per_line, math.ceil(n / per_line)


if __name__ == "__main__":
    print(f"{N} microphones, {FS/1000:.0f} kHz, FFT {NFFT}")
    print("case                                   FFT   CSM   map  CLEAN  total GFLOP/s")
    for lab, g, b, f, c in CASES:
        parts = [x / 1e9 for x in need(g, b, f, c)]
        print(f"{lab:37s} " + " ".join(f"{x:5.2f}" for x in parts) + f"  {sum(parts):6.2f}")
    raw = N * 2 * FS / 1e6
    print(f"\nthe raw stream, 16 bit: {raw:.1f} MB/s (to a PC at the bench only; never kept)")
    tot = sum(sum(need(g, b, f, c)[1:]) for _, g, b, f, c in ZOOM) + need(1, 1, 1)[0]
    print(f"\ncoarse field at 10 fps + fine cleaned patch round the peak at 5 fps: {tot/1e9:.2f} GFLOP/s")
    print("\nthe bus: 16-bit slots, BCLK at most 24.576 MHz")
    for fs in (96_000, 192_000, 384_000):
        per, k = lines_needed(fs)
        print(f"  {fs/1000:3.0f} kHz (flat to ~{PASSBAND[fs]*fs/1000:3.0f} kHz): {per:2d} channels a line, {k} lines for {N}")

    print("\nfront-end processors sending only spectra (complex 16+16 bit), FFT 1024")
    for fs, bins_lab, bins in ((96_000, "20 bins", 20), (96_000, "25-45 kHz all", None),
                               (192_000, "20 bins", 20), (192_000, "25-80 kHz all", None)):
        df = fs / NFFT
        nb = bins if bins else int(((45e3 if fs == 96_000 else 80e3) - 25e3) / df)
        mbs = N * nb * 4 * (fs / NFFT) / 1e6
        raw = N * 2 * fs / 1e6
        print(f"  {fs/1000:3.0f} kHz, {bins_lab:14s} ({nb:3d} bins): {mbs:5.2f} MB/s for {N}, raw {raw:5.1f} MB/s")

    # --- What the N6 has, against it (DS14791 Rev 2 for the clock, the NPU and the blocks; the
    # M55's per-cycle rates from Arm's design, a 64-bit "dual-beat" Helium — from memory) ------
    F = 800e6
    peaks = {"scalar FPU, FP32 (1 FMA/cycle)": 2 * F, "Helium FP32 (2 FMA/cycle)": 4 * F,
             "Helium FP16 (4 FMA/cycle)": 8 * F}
    need = sum(sum(need(g, b, f, c)[1:]) for _, g, b, f, c in ZOOM) + need(1, 1, 1)[0]
    print(f"\nthe N6's M55 at 800 MHz against the map's {need/1e9:.2f} GFLOP/s:")
    for k, v in peaks.items():
        print(f"  {k:32s} peak {v/1e9:4.1f} GFLOP/s -> {need/v*100:4.0f} % of peak, ~{need/(v/3)*100:4.0f} % at a third of it")
    print("  NPU 600 GOPS (int8) idle; camera (ISP), overlay (LTDC 2 layers, DMA2D, GPU), JPEG — hardware")
