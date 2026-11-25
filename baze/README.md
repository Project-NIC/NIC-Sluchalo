# The Báze — the main board every tool plugs into

*Built 25 Nov 2026 (the owner: "postav tu strukturu, báze a netopýr").* The common part of
NIC-Sluchalo's tools: the board with the N6, the power, the display, the camera, the card, the
communication module, the buttons — and the ports the heads plug into. A tool = the Báze + its
head behind its front mask.

| file | what |
|---|---|
| `schematic.md` | the netlist by chapters: power, camera, **the heads' ports**, lights, card and module, the J5/J6 table |
| `kuranty.md` | every clock: the 24.576 MHz, the PPS, each head's BCLK and FSYNC |
| `konstrukce/valenki.md` | what touches the surface; the box and the masks to come |
| `boards.md` | the processor boards weighed (23 Nov 2026) |
| `calc/` | `power.py`, `supply.py`, `surge.py`, `sodium.py` |
| `baze.jpg` | its picture |

## Decided (25 Nov 2026, the owner)

- **The CNN647B (STM32N647)**, one cell (sodium 1S, the pack not chosen), BQ25628, the two
  TPS63020; the display in the core board's J4 (≤ 7", backlight on our U30); the camera on CSI-2
  (J7, 15-pin); the card on SDMMC1; **the communication module (ESP32-S31-WROOM-1, ESP32-MINI-1
  the fallback) on SPI2**.
- **Two head ports H1, H2** — each 8 lines of the N6's one PSSI (H1 the low byte, H2 the high),
  24.576 MHz; a UART each for the commands and a new firmware; NRST; the clock and the PPS; a
  2 × 15 connector, the power together, a ground beside every signal. 100 kΩ pull-downs on the 16
  data lines. No ESD on these inside connectors.
- **The Báze's own sensors:** the SHT45 (air temperature and humidity, I2C1) and **a red-dot laser
  rangefinder module** in the chassis — the **Benewake TF40** (UART7, its supply switched).
- **Eight inductive buttons** (▲▼◄► OK, ESC, MENU, the trigger; two LDC2114 on I2C2 **(m)**) and **a power
  button**: a magnet over a DRV5032 Hall switch on the charger's QON.
- **The thermal camera: InfiRay Tiny1-C**, 256 × 192, above the propeller behind a germanium window, on the
  N6's second USB (OTG2) as a host, its supply switched.
- **The IMU: ST LSM6DSV16X (m)** on SPI5, its two interrupts on PB2/PE3 — alive in the N6's Stop.
- **The power under the N6's hand:** U23's EN, a load switch for each head and for the rangefinder;
  sleep = Stop, self-off in steps, off = the BQ25628's ship mode. Q1 I2C port; the scene's PWM on
  PF1. The N6's four SAIs free.
- **The communication module on SPI2 and USART2** (its UART0: the loader and the console).
- **One audio microphone on the Báze** — the IM69D130 on ADF1 (CCK0 PE2, SDI0 PB0).
- **One clock, 24.576 MHz, and a PPS** for everything, **made by the N6** (I2S3's MCK on PC7 from an audio
  PLL, independent of the core and of the PSSI; the PPS counted from it) — no crystal of our own;
  the SAIs free (`kuranty.md`).

## Open

- RM0486: the PSSI's DMA byte exchange; I2S3's MCK out with its data pins unassigned;
  the kernel PLL for 24.576 MHz.
- The protocol: the start-up talk ("who are you", the head's calibration and serial from its
  flash), the frame's 128 byte-places, the commands — a protocol of our own.
- The mating connector of J5/J6; the box; the display module; LCSC numbers.
