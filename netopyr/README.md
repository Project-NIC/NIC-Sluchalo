# Netopýr — the acoustic camera's head (and Datel, its knock)

*25 Nov 2026 (the owner: "postav tu strukturu, báze a netopýr").*
Netopýr sees sound: gas leaks hissing, a machine's bearings, partial discharges. **Datel** is its
tap mode — the knock heard and the hollows behind a surface seen. The head plugs into the Báze
(`../baze/`).

| file | what |
|---|---|
| `schematic.md` | the head: the propeller of microphones, four PCMD3180, the STM32H723, the PSSI out; Datel's knock |
| `purpose.md`, `WHY.md` | level 1, the purpose, and the log of why |
| `calc/` | `acam.py`, `air.py`, `leak.py`, `layout.py`, `propeller.py` (+ `propeller_14.csv`), `compute.py`, `membrane.py`, `port.py` |
| `netopyr.jpg`, `datel.jpg` | the pictures |

## Decided (25 Nov 2026, the owner)

- **The propeller, Ø 14 cm:** 8 spiral arms, 16 places an arm (128), **32 microphones fitted**
  (SPH0641LU4H-1), a converter for each two arms; 64 possible on the same board. At 10 m,
  25–45 kHz: spot ~88 cm, ghost −12.9 dB.
- **The head:** four PCMD3180 (192 kHz) → the STM32H723VGT6's four SAI blocks → **raw on 8 PSSI
  lines** to the Báze; the commands on a UART; the clock from the Báze into OSC_IN, BCLK from MCO1,
  FSYNC from a timer reset by the PPS. The whole band, 0–96 kHz (~85 usable).
- Two heads = 64 on the same Báze (H1 + H2).

## Open

- The head's PCB (the places from `propeller_14.csv`), its LCSC parts; the bench check of FSYNC
  against BCLK; the coupon (one petal) first.
