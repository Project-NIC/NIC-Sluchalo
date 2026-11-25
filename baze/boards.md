# The boards weighed (for the Báze)

*23 Nov 2026. Material for the parts (level 5), not its decision.* The owner: a maker's finished
board, the best ratio of what it does to what it costs, every option gone through. Prices found
today, one piece, without VAT unless said, from different shops and dates; **the processors'
speeds from memory**, rough.

## What the board must do

- **Take 32 channels** of TDM (eight PCMD3140, two to a line, or four PCMD3180): 32 × 16 bit ×
  96 kHz, on two to four lines.
- **Compute the map** — [`calc/compute.py`](calc/compute.py): the FFTs ~0.15 GFLOP/s always;
  a coarse map (32 × 24 points, 5 bins, 10 frames/s) **~0.5 GFLOP/s**; the same cleaned by
  CLEAN-SC at 2 frames/s ~0.9; a fine map (64 × 48, 20 bins, 10 frames/s) ~5; the fine one
  cleaned at 5 frames/s **~28 GFLOP/s**. A processor sustains perhaps a third of its peak.
- **Save the picture, nothing more:** no raw recording on the tool (the owner, 23 Nov 2026: "na
  kartu se nenahrává … max komprimovaný obraz") — a compressed image, as a photograph.
- **Be held in the hand on a battery:** a camera, a display, a few watts at most.

## The candidates

| board | processor (peak, from memory) | in the box | 32 channels in | price found |
|---|---|---|---|---|
| **STM32N6570-DK** | M55 800 MHz Helium, ~3 GFLOP/s; **NPU** | 5" touch, 5 Mpx camera | SAI2 block B + SPI5 (UM3300, below); four lines possible | ~198 € (Farnell DE) |
| STM32H747I-DISCO | M7 480 MHz, ~1 | 4" touch; camera apart | SAI1 the codec's; others unchecked | ~200 S$ (RS) |
| STM32H7S78-DK | M7 600 MHz, ~1.2 | 5" touch; camera connector, camera? | unchecked | £77 (RS) – 149 € (TME) |
| Renesas EK-RA8D1 | M85 480 MHz Helium, ~2 | 4.5" touch, 3 Mpx camera | unchecked | £248 (Farnell UK) |
| NXP MIMXRT1170-EVKB | M7 1 GHz + M4, ~2 | camera; display apart | SAI1 on the header (Zephyr's pin map) | ~185 € (DigiKey IE) |
| Espressif ESP32-P4-Function-EV-Board | 2 × RISC-V 400 MHz, ~1.6 | 7" touch, 2 Mpx camera | I2S with TDM — unchecked | ~55 $ at launch (2024) |
| Alif AK-E7-AIML | 2 × M55 (400 + 160 MHz), **2 NPUs** | 4.3" display, camera | unchecked | not found |
| STM32MP135F-DK (Linux) | A7 1 GHz, ~2–4 | 4.3" touch, 2 Mpx camera | unchecked | £107 (RS) – £138 |
| STM32MP257F-DK (Linux) | 2 × A35 1.5 GHz, ~12; **NPU** | display and camera apart | unchecked | ~140 S$ + extras |
| Raspberry Pi 5 8 GB (Linux) | 4 × A76 2.4 GHz, ~150 | Touch Display 2 5" ~40 $, Camera Module 3 ~32–44 $ apart | I2S on the header, TDM unchecked; else a bridge by USB | ~130 $ (Oct 2026) |
| BeagleY-AI (Linux) | 4 × A53 + C7x DSPs, ~4 TOPS | — | McASP (TDM) — on the header? unchecked | £58 (RS) – 136 $ |
| Orange Pi 5 / RK3588S (Linux) | 4 × A76 + 4 × A55; 6 TOPS NPU | — | unchecked | 60 $ (2022) – 181 $ now |
| Jetson Orin Nano (Linux) | a GPU, far beyond the need | — | — | ~250 $; 7–25 W — out for a battery |

Sources: [N6570-DK](https://www.st.com/en/evaluation-tools/stm32n6570-dk.html),
[Farnell](https://de.farnell.com/en-DE/stmicroelectronics/stm32n6570-dk/arm-development-kit/dp/4587312);
[H747I-DISCO](https://www.st.com/en/evaluation-tools/stm32h747i-disco.html);
[H7S78-DK](https://www.st.com/en/evaluation-tools/stm32h7s78-dk.html),
[RS](https://uk.rs-online.com/web/p/microcontroller-development-tools/0276880);
[EK-RA8D1](https://www.renesas.com/en/design-resources/boards-kits/ek-ra8d1),
[Farnell](https://uk.farnell.com/renesas/rtk7eka8d1s01001be/evaluation-kit-32bit-arm-cortex/dp/4294100);
[RT1170-EVKB](https://www.nxp.com/part/MIMXRT1170-EVKB),
[DigiKey](https://www.digikey.ie/en/products/detail/nxp-usa-inc/MIMXRT1170-EVKB/19528850),
[Zephyr](https://docs.zephyrproject.org/latest/boards/nxp/mimxrt1170_evk/doc/index.html);
[ESP32-P4-Function-EV-Board](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4-function-ev-board/user_guide.html),
[CNX](https://www.cnx-software.com/2024/08/07/esp32-p4-function-ev-board-development-board-launched-for-55-with-7-inch-display-and-camera-module/);
[Alif AK-E7-AIML](https://alifsemi.com/support/kits/ensemble-e7appkit/);
[MP135F-DK](https://www.st.com/en/evaluation-tools/stm32mp135f-dk.html);
[MP257F-DK](https://www.st.com/en/evaluation-tools/stm32mp257f-dk.html);
[Pi prices](https://www.tomshardware.com/raspberry-pi/component-shortages-drive-raspberry-pi-prices-up-by-up-to-23-percent-escalating-lpddr4-lpddr5-costs-trigger-the-third-price-hike-of-the-year);
[BeagleY-AI](https://beagleboard.org/beagley-ai);
[Orange Pi 5](https://www.cnx-software.com/2022/11/11/orange-pi-5-most-affordable-rockchip-rk3588s-sbc/).

## What falls out

- **The Jetson:** watts. **The Orange Pi and the BeagleY-AI:** strong, but no display or camera in
  the box, their audio pins unchecked, ecosystems less sure.
- **The H747, H7S78, RT1170, RA8D1:** each does the coarse map, none has an NPU, none is cheaper
  than the N6570-DK for what is in the box (the H7S78 is, but it is a slower M7 and its camera is
  not certain).
- **The MP135F-DK:** everything in the box, Linux, but one A7 — no better at the map than the N6.
- **The MP257F-DK:** Linux and an NPU, but the display and camera bought apart bring it over the
  N6570-DK, and its two A35 do not reach the fine cleaned map either.
- **The Alif kit:** two NPUs, but no price found and a smaller maker.

## What stays

1. **The STM32N6570-DK alone** (~198 €): an STM32 as the owner knows it; display and camera in
   the box; the 32 channels in by SAI2 block B and SPI5 (UM3300, below); the coarse map live, cleaned at a
   few frames a second; the NPU for a network that takes out the ghosts later; ~1–2 W. At the
   bench only, during the development, the raw stream goes live to a PC by USB, where the fine
   cleaned map (Acoular) is made — nothing kept on the tool, and no second board.
2. **The Raspberry Pi 5 with a bridge** (~130 + 40 + 35 $ and an STM32 board passing the 32
   channels by USB): the fine cleaned map live in Acoular as it is; but two boards, two programs,
   5–7 W, a Linux boot.
3. **The ESP32-P4 board** (~55 $ at launch): the cheapest whole kit, a 7" display; as fast as an
   H7, no NPU; its TDM to be checked.

**The lead: 1, the N6570-DK.** Its risk is supply: the NUCLEO-N6 shows lead times of a year and
more at DigiKey; the DK was in stock at Farnell (more incoming) on 23 Nov 2026.

## Still to check before buying

- UM3300: SAI2's clock on STMod+ — or the SPI way settled (the converters' bit clock, the SPI
  slave's limit).
- The N6's sustained speed on the map: a Helium benchmark (CMSIS-DSP's complex dot product).

## Sixteen microphones into one SPI — 23 Nov 2026

From TI's PCMD3180 sheet (SBASA14A, rev. Jan 2026):

- **One line, sixteen channels, fits exactly:** 16 slots × 16 bit = 256 BCLK a frame; at 96 kHz
  that is **24.576 MHz, the highest BCLK the sheet lists** (Table 6-6, ratio 256 at 96 kHz), and
  the BCLK period's minimum is 40 ns (§5, timing; 24.576 MHz is 40.7 ns). No headroom: the
  slots must be 16 bit, and 96 kHz is the ceiling.
- **Several converters share one line:** each is given its slots (up to 64 configurable), leaves
  the others in Hi-Z, a bus-holder keeps the line between them; four I2C addresses by pins and an
  I2C broadcast to start them together (§6.3, "Multiple PCMD3180 devices"). Two PCMD3180, or four
  PCMD3140 (the same family, to be read in its own sheet), on each line.
- **All 32 must be sampled together**, so **one converter is the clock's master** for both lines:
  fed by one oscillator on its MCLK input (up to 36.864 MHz, §5), it drives BCLK and FSYNC to every
  other converter and to both SPIs. The others take BCLK and FSYNC and set themselves (§6.3.2).
- **The N6 receives, as an SPI slave, by DMA:** SCK = BCLK, the data on an SPI's MOSI, or on its
  MISO with the pins swapped (IOSWP). Which SPIs and pins: *UM3300 read* below — SPI2 is out. The
  frame must start at a slot's first bit: the NSS of both SPIs is pulled low once, at a frame's
  start, by a flip-flop and a gate on the microphones' board that wait for FSYNC (TX_OFFSET set so
  the data's first bit follows it, §6.3.1); after that the stream runs continuously, and an
  alignment check in the firmware resets it if a bit is ever lost.
- **The microphones' board then carries everything:** the converters, the oscillator, the
  flip-flop; to the N6 only power, I2C, BCLK, FSYNC-gated NSS and two data lines.
- **Checked 23 Nov 2026:**
  - **The N6's SPI as a target receiver: up to 100 MHz** (DS14791 Rev 2, Table 99); NSS setup
    4 ns, data setup 4.5 ns. 24.576 MHz is a quarter of it. (Its SAI as a target receiver: 50 MHz.)
  - **IOSWP exists on the N6's SPI** (`SPI_CFG2_IOSWP`, bit 15, in ST's CMSIS header
    `stm32n657xx.h`): an SPI can take its data on MISO.
  - **The microphones:** Knowles SPH0641LU4H-1, 10 Hz – 80 kHz, its ultrasonic mode clocked at
    3.072–4.8 MHz (the response measured at 3.072 MHz) — third-party copies of its Rev A/B sheet;
    the current one to be fetched. **The converter gives exactly 3.072 MHz** (PDMCLK_DIV = 0,
    §6.3.5), and 96 kHz out: the band to ~0.45 × 96 ≈ 43 kHz. How quiet the 25–45 kHz band is at
    that clock, the trial measures.
  - **PCMD3140 has one fixed I2C address** (1001110, or 1001100 for broadcast; SBASA64A §7.5.1.1,
    Table 7-43) and no SPI control: eight of them cannot be told apart on one bus without an I2C
    mux. **PCMD3180 has four addresses by pins and SPI control:** so **four PCMD3180**, each
    serving two of the eight groups of four — the eight groups' layout kept, the PDM lines a few
    centimetres.
  - **UM3300:** read — below.
- **A gift for the calibration:** each channel has its own gain (0.1 dB) and phase (163 ns)
  correction in the converter (§1).

## One core or two, one board or two — 23 Nov 2026

The owner: a dual core — one for the picture, one for the computing — or two processors joined?

- **The N6 is already split, in hardware** (DS14791 Rev 2, features): the picture's work is not
  the core's — the camera through the **ISP**, the map laid over it by the **Neo-Chrom GPU** and
  **DMA2D**, the display by its controller, the saved picture by the **hardware JPEG codec**; the
  32 channels come in by **DMA**. The **M55 at 800 MHz with Helium** is left for the arithmetic,
  and the **Neural-ART NPU (1 GHz, 600 GOPS)** stands beside it for a network. A second core would
  be given little to do.
- **The arithmetic made to fit one core** (`calc/compute.py`): not the fine map everywhere
  (~5 GFLOP/s, ~28 cleaned), but the **whole field coarse at 10 frames/s and a fine patch round the
  loudest spot, cleaned, at 5 frames/s: ~0.9 GFLOP/s** — the sharpness where the leak is, the
  overview elsewhere.
- **The dual-core chips gain nothing here:** the H747 (M7 + M4), the RT1170 (M7 + M4) give the
  second core to the picture, which the N6 does in hardware, and their main core is slower than
  the M55 with Helium.
- **Two boards joined, if ever wanted:** the beamforming needs every microphone's spectrum in one
  place, but only in the band's bins — after the FFT, 32 channels × 20 bins × 94 frames/s × 8 B
  ≈ 0.5 MB/s. So two N6 could each take one line (16 microphones), compute its FFTs, swap the
  band's bins over an SPI, and each compute half the map. Easy to add later; not needed for the
  map above, and it doubles the price.
- **So: one N6570-DK.** If its core proves too slow on the trial's benchmark, the map is made
  coarser or the NPU takes the cleaning, before a second board.

## SAI and SPI are separate — how many lines the N6 could take (23 Nov 2026)

- **Separate blocks** (DS14791 Rev 2, features): **6 SPI** (four of them I2S-capable) and **2 SAI**
  — all can run at once. The chip could take four lines and more; the limit is the board's pins.
- **On the N6570-DK's connectors:** first read from Zephyr's map alone; superseded by *UM3300
  read* below.
- **The NUCLEO-N657X0-Q** brings out nearly every pin on its headers — four lines certain — but
  has no display or camera, and showed lead times of a year and more.

## UM3300 read — the lines on the N6570-DK's connectors (23 Nov 2026)

UM3300 (given by the owner) with ST's pin data:

- **A0–A5 are wired twice** (§7.17, Fig. 11): each to an ADC pin in the 1.8 V domain *through an
  amplifier*, and to a 3.3 V digital pin directly — A0 PD7, A1 PC10, A2 PE12, A3 PD11, A4 PC12
  (pin table, "A0D"…"A4D"). The ADC sides (PA5, PA9, PA10, PA12, PF3, PB10) cannot carry a
  24 MHz clock. **So SPI2 is out:** its SCK reaches the connectors only on those ADC pins.
  (Corrected here; written as usable above until today.)
- **STMod+ (CN4, Table 13):** SPI5 (shared with the Arduino pins), I2C1, and GPIO pins: 11 PC11,
  12 PB3, 17 **PD13 (SAI2_SCK_A)**, 18 PF1, 19 **PB8 (SAI2_FS_B)**, 20 PG9; pin 4 is SPI5_SCK or,
  with SB10/12/14/17 on (UART2 to STMod+), PG14.
- **SAI2's block A cannot be used:** its FS (PG13) is the display's LCD_DE, its SD (PF5) the
  Ethernet's clock. **Block B can:** SCK PE12 on A2, FS PB8 on STMod+ 19 (or PE13 on D6), SD PE7
  on D8.
- **D13 (PE15, SPI5_SCK) carries the green LED LD6** (Table of LEDs) — SPI5's clock taken on D4
  (PH5) instead.

**The lines that are there, all at 3.3 V, no solder bridge:**

| line | clock | data | frame |
|---|---|---|---|
| SAI2 block B | PE12 (A2) | PE7 (D8) | FS PB8 (STMod+ 19) — the SAI aligns itself |
| SPI5 | PH5 (D4) | PG2 (D11, MOSI) | NSS PA3 (D10) |
| SPI3 | PC10 (A1) | PC11 (STMod+ 11, MISO, IOSWP) | NSS PD7 (A0) |
| SPI6 (a fourth) | PC12 (A4) | PG14 (STMod+ 4, SB10/12/14/17 on) | no NSS pin free (PB15, PF4, PA15, PA0 taken or not out) |

- **96 kHz, two lines: SAI2 block B + SPI5** — no change to the board.
- **192 kHz, four lines: + SPI3 + SPI6.** SPI6 has no NSS, so its word boundary is found in the
  firmware (the samples' sign bits run together at a fixed place) and the stream shifted — cheap
  on the M55, to be tried. Three lines without it would carry 24 microphones at 192 kHz.
- **The rest on the same pins:** I2C1 to the converters on D14/D15 (PC1/PH9); BCLK from the
  master converter wired to every clock pin above.

## How the microphones' board is joined (23 Nov 2026)

UM3300, Fig. 1, 2 and 5: **the display is on the DK's top side; the Arduino connectors (CN7, CN8,
CN11, CN12, female) and the camera's connector (CN14, a 22-pin ZIF for the MB1854 module's flex)
are on its bottom side; STMod+ (CN4) is on the top.**

- **So the microphones' board is an Arduino shield on the DK's back**, facing the scene while the
  display faces the user — the tool's shape given by the kit. The board may be larger than the
  Arduino footprint (the honeycomb); the headers only hold it.
- **The camera through the middle:** the MB1854 camera module sits in the honeycomb's central
  hole, its flex to CN14 beside it on the same side.
- **At 96 kHz everything is on the Arduino pins** — SAI2 block B: SCK A2, SD D8, **FS D6** (PE13,
  instead of STMod+ 19); SPI5: SCK D4, data D11, NSS D10; I2C1 to the converters D14/D15; 5 V and
  GND from the power header. A plain shield, nothing else.
- **At 192 kHz two data lines come from STMod+ on the top side** (SPI3's PC11 on pin 11, SPI6's
  PG14 on pin 4 with its solder bridges set): a short cable round the DK's edge, each data wire
  beside a ground; their clocks (A1, A4) and SPI3's NSS (A0) stay on the shield.
- **On the shield:** BCLK from the master converter through a clock buffer, one output and one
  series resistor per clock pin (each converter, A2, D4, and A1, A4 at 192 kHz); the converters'
  own 3.3 V from a quiet regulator on the 5 V, not the DK's 3V3 — the microphones are the noise
  floor. A0–A5 also feed the DK's ADC amplifiers (§7.17): a load on those lines, small, to be
  measured.

## The microphones, and the board that carries them (23 Nov 2026)

**The microphones — the candidates found:**

| part | PDM, ultrasonic | SNR, sensitivity | price, stock found today |
|---|---|---|---|
| **Knowles (now Syntiant) SPH0641LU4H-1** | to 80 kHz; ultrasonic mode at 3.072–4.8 MHz | 64.3 dB; −26 dBFS ±1 dB | DigiKey EU ~2.75 € each, ~1.72 € at 100; 8 000–18 000 in stock; LCSC out of stock |
| TDK ICS-41352 | to 85 kHz in its ultrasonic mode | "high"; −26 dB ±1 dB | one shop marks it **obsolete**, others list stale prices — not to be built on |
| Infineon IM67D128B | no ultrasonic figure found (only its sibling IM68D128B shows a curve) | 67 dB(A) | 27 weeks' lead at one shop |

- **The lead: SPH0641LU4H-1** — in stock, its ultrasonic mode on the converter's 3.072 MHz, the
  sensitivity matched to ±1 dB between pieces (the rest the converter's per-channel gain and phase
  take up). 32 pieces ~60–90 €. Its current datasheet to be fetched (only Rev A/B copies read).
- Sources: [DigiKey SPH0641LU4H-1](https://www.digikey.ie/en/products/detail/syntiant/SPH0641LU4H-1/5332438),
  [LCSC](https://fat.lcsc.com/product-detail/MEMS-Microphones_Knowles-sph0641lu4h-1_C2879853.html),
  [TDK ICS-41352](https://invensense.tdk.com/?p=7432),
  [DigiKey ICS-41352](https://www.digikey.at/en/products/detail/tdk-invensense/ICS-41352/8544632),
  [Infineon IM67D128B](https://www.infineon.com/assets/row/public/documents/24/49/infineon-im67d128b-datasheet-en.pdf).

**A board for the PCMD3180 — none to buy:** TI makes no evaluation board for it (only the
four-channel PCMD3140EVM-PDK, ~300 $ at one shop, one microphone on it). So **the shield is ours
and it is the only board of ours**: 32 microphones, four PCMD3180, the clock buffer, the quiet
regulator, the Arduino headers. No processor, no BGA (WQFN-24 and the microphones' LGA), four
layers; made and assembled by the board house, the parts it lacks (both are out at LCSC) bought
by its global sourcing or sent to it from DigiKey.

**The front of the shield is the "plate full of holes":** a bottom-port microphone sits on the
board's back (towards the DK), its sound coming through a hole drilled through the board — the
face towards the scene is flat, the holes in the honeycomb, the camera in the middle. **The hole
is a short tube and rings** (`calc/port.py`, a quarter-wave estimate): through 1.6 mm its first
resonance is ~45–47 kHz — in the band; through **0.8 mm ~78–85 kHz**, 0.6 mm ~95–106 kHz. So the
shield is **0.8 mm thick** (four layers at 0.8 mm are a standard build), the hole ~0.7 mm; the
microphone's own port and its maker's note on the hole to be read before the layout.

## The converter's "22 kHz filter" (23 Nov 2026)

The owner asked whether the PCMD's 22 kHz filter can be switched off. **It is the decimation
filter, and it cannot be switched off — but it is not fixed at 22 kHz: its edge moves with the
output rate** (22 kHz is where it sits at 48 kHz). From the sheet (SBASA14A §6.3.6.7, Tables
6-24…6-40), flat within ±0.05 dB up to:

| output rate | linear phase (default) | low latency (DECI_FILT = 01) |
|---|---|---|
| 96 kHz | 0.454 fs = 43.6 kHz | 0.466 fs = 44.7 kHz |
| 192 kHz | **0.3 fs = 57.6 kHz** | **0.463 fs = 88.9 kHz** |
| 384 kHz | 0.212 fs = 81 kHz | (ultra-low latency 0.1 fs) |

- **The low-latency filter is the one for us:** its phase is not linear, but it is the same on
  every channel, so it cancels in the cross-spectra the map is made of. At 192 kHz it keeps the
  band flat to ~89 kHz, where the linear one stops at ~58. (Written "to ~86 kHz" before, from a
  rule of thumb; now from the sheet — `calc/compute.py`.)
- **What can be switched off:** the high-pass filter (HPF_SEL, §6.3.6.4) and the biquads
  (§6.3.6.5) are programmable; the microphones' own upper limit (~80 kHz) stays.

## 192 kHz, four lines — the owner's choice (23 Nov 2026)

"Tak jedeme na 192 kHz se čtyřma linkama." What follows from it, gathered from the sections above:

- **One converter, one line:** each PCMD3180 sends its eight channels alone — 8 slots × 16 bit =
  128 BCLK a frame, **24.576 MHz at 192 kHz** (Table 6-6, ratio 128); no slots shared, no Hi-Z
  hand-over between devices. One converter is the clock's master for all four.
- **In each converter:** PDMCLK 3.072 MHz (the microphones' ultrasonic mode), output 192 kHz,
  **the low-latency decimation filter** (DECI_FILT = 01, flat to ~89 kHz), HPF and biquads as the
  map needs.
- **The four lines on the N6570-DK** (*UM3300 read*): SAI2 block B (A2, D8, FS on D6); SPI5 (D4,
  D11, NSS D10); SPI3 (A1, data PC11 on STMod+ 11, NSS A0); SPI6 (A4, data PG14 on STMod+ 4 with
  SB10/12/14/17 on and SB11/13/15/18 off, no NSS — aligned in the firmware). The two STMod+ wires
  run round the DK's edge.
- **The band ~25–80 kHz**, split in the map into a low part (to ~45 kHz, reach) and a high part
  (sharper, metres only — `calc/air.py`).
- **The arithmetic** (`calc/compute.py`, now at 192 kHz): the FFTs double to ~0.31 GFLOP/s; the
  coarse field with the fine cleaned patch **~1.05 GFLOP/s** — on the N6's M55, to be benchmarked.
  The stream into memory 12.3 MB/s by DMA.
- **The holes must ring above the band:** at 0.8 mm the hole rings at ~78–85 kHz — now inside it;
  **the shield 0.6 mm** (~95–106 kHz, `calc/port.py`) — whether the board house makes four layers
  at 0.6 mm, to be asked; else the holes shaped (wider, or the board thinned under them).

## Another board, fed straight from a cell? (23 Nov 2026)

The owner: rather than 5 V made only to be turned down again — is there another board? Found
today (nothing checked beyond the pages named):

| board | processor | from a cell | display, camera | price found | to check |
|---|---|---|---|---|---|
| **OpenMV N6** | STM32N6 | **3.7 V Li-Pol connector, 500 mA charger on board**, falls back to the cell when USB drops | camera yes; no display (one to add) | 108 $ (Kickstarter) – 180 $ | which pins give four serial lines (only I2S2 on P0 seen) |
| **Seeed AI Assistant** (made with ST, a hand-held platform) | STM32N657 | a lithium battery port in one listing, not in the wiki seen | **4" 480 × 480 touch**, global-shutter camera, mic, codec, Wi-Fi | A$375 (AU, out of stock) | the battery port; free SAI/SPI lines |
| Ohm Lab Neuro N6 | STM32N6 | 3.7 V Li-Pol and a 500 mA charger | camera and TFT modules | crowdfunding, a prototype in March 2026 | whether it ships |
| M5Stack Tab5 | ESP32-P4 (no NPU, slower) | **a 2S NP-F550 pack in the kit**, the power made on board | 5" 720p touch, 2 Mpx camera | £63–86 with the pack | three I2S: 24 channels at 192 kHz, 32 only at 96 kHz |

Sources: [OpenMV N6](https://openmv.io/products/openmv-n6),
[OpenMV N6 docs](https://docs.openmv.io/openmvcam/quickref/openmv-n6.html),
[review](https://derekmolloy.ie/the-openmv-n6-a-micropython-camera-with-a-real-npu/);
[Seeed AI Assistant wiki](https://wiki.seeedstudio.com/ai_assistant_getting_started/),
[Pakronics](https://www.pakronics.com.au/products/ai-assistant-stm32n6-ai-development-kit-with-global-shutter-camera-ss114993645),
[ST case study](https://st.com/content/st_com/en/st-edge-ai-suite/case-studies/handheld-development-platform-for-real-time-vision-motion-and-voice-at-the-edge.html);
[Ohm Lab Neuro N6](https://www.cnx-software.com/2026/03/23/ohm-lab-neuro-n6-modular-stm32n6-ai-vision-devkit-support-rolling-shutter-global-shutter-or-thermal-camera/);
[M5Stack Tab5](https://docs.m5stack.com/en/core/Tab5),
[CNX](https://www.cnx-software.com/2025/05/09/m5stack-tab5-tablet-esp32-p4-iot-development-kit-5-inch-touchscreen-display-and-front-facing-camera/),
[RobotShop](https://eu.robotshop.com/products/m5stack-tab5-iot-development-kit-esp32-p4-w-np-f550-battery).

- **The closest to the owner's wish: the Seeed AI Assistant** — the same N6, already a hand-held
  with its display and camera; whether it takes a cell and gives four lines decides it.
- **OpenMV N6** takes a Li-Pol for certain, but wants a display and has few pins.
- **Tab5** has the whole power solved, but is a weaker chip and takes 32 microphones only at 96 kHz.
- **Without a display or camera in the set** (the owner, 23 Nov 2026) — looked at again:
  - **OpenMV N6** ([docs](https://docs.openmv.io/dev/openmvcam/quickref/openmv-n6.html)): runs
    from a Li-Pol straight — RAW 3.6–5 V, the board's own power controller picks USB, VIN or the
    cell and charges it (500 mA); its camera is on board. **But only two serial lines reach its
    header:** SPI2/I2S2 on P0–P3, and SPI4 on P15–P18 only after moving a 0 Ω resistor from the
    gigabit Ethernet PHY. So **32 microphones at 96 kHz, or 16 at 192 kHz** — and no pins left for
    a display (it would take an SPI), unless the picture goes out by its Wi-Fi.
  - **No STM32N6 core board** (WeAct and the like) found; ST's NUCLEO-N657X0-Q brings out every
    pin but is fed 5 V like the DK (to be confirmed in UM3417) and was on a year's lead time.
  - So the choice is between **the DK with 192 kHz on four lines, fed 5 V** (two cells into VIN
    once its regulator is known, or one cell with a boost), and **the OpenMV N6 on one cell,
    at 96 kHz** (band to ~45 kHz) with the picture shown elsewhere.
  - **UM3417 read (the NUCLEO-N657X0-Q, given by the owner):** the same power tree as the DK
    (Fig. 9 against UM3300 Fig. 7) — **no 3.3 V input**; three 5 V sources (§7.4.1, Table 6):
    ST-LINK's USB-C, USB-C (5V_UCPD, up to 1.5 A), and **VIN 7–12 V through an LDO whose current
    falls with the voltage: 800 mA at 7 V, 450 mA from 7 to 9 V, 250 mA from 9 to 12 V.** The DK's
    VIN is "up to 0.8 A … depending on VIN source voltage" (UM3300 §7.4.4) — the same kind, most
    likely. **So two cells on VIN (6.0–8.4 V) are out:** below 7 V for the last of their charge, and
    ~450 mA in the middle, while the DK with its camera draws more than 550 mA. The DK is fed 5 V
    at USB-C (up to 3 A), from one cell and a boost or two and a buck — there is no way round it
    with ST's boards.
  - **The DK's VIN regulator is a 1117** (the owner, off the schematic, 23 Nov 2026) — a plain
    linear regulator. UM3417's limits are its heat budget, ~1.6–1.8 W (`calc/power.py`). Two cells
    at ~0.6 A: **2.0 W at 8.4 V** (full — over the budget), 1.4 W at 7.4 V, and 22–40 % of the
    battery burnt; near empty its dropout (~1 V and more, the 1117 family) pulls the 5 V down.
    Confirmed: not this way.

## One cell straight on the DK's 5 V net? — from the schematic (23 Nov 2026)

The owner sent the MB1939 schematic's power parts (screenshots). Behind the 5 V net:

| part | job | input range |
|---|---|---|
| U21 LD1117S50TR | VIN → 5V_VIN | (VIN only; not in this path) |
| U1, U22 ST1S31PUR | 3 A bucks: VDD3V3, VDD1V8 | **2.8–5.5 V** (abs. max 7 V; ST) |
| U5 LD39020ADTPU33R | 200 mA LDO → VDDIO 3.3 V | **1.5–5.5 V**, dropout ~200 mV (ST) |
| U43 LD39020ADTPU18R | → VDDA1V8_AON | **1.5–5.5 V** |
| U45 LD56100DPU18R | 1 A LDO → VDDA1V8 | **1.8–5.5 V**, dropout ~120 mV (ST) |
| TPS62088YFP | buck, the core (FB 160 k) | 2.4–5.5 V (TI; from memory, to be confirmed) |

- **So every regulator on the 5 V net runs from 2.8 V up** — one Li-Pol cell (3.0–4.2 V) put on
  that net, not on USB or VIN, feeds them all. The 1.8 V and 0.8 V rails stay regulated to the
  cell's end; the 3.3 V rails (ST1S31, LD39020) hold 3.3 V down to a cell of ~3.4–3.5 V and then
  follow it a little below — and the N6's VDD runs 1.71–3.6 V (DS14791), so it does not care. No
  boost, no 5 V made at all.
- **What still has to be read in the schematic — what else hangs on the 5 V net:** the display
  board MB1860 (its white-LED backlight driver: does it start from 3 V?), the USB-A host port's
  VBUS (it would carry the cell's voltage — unused, harmless), the Arduino +5V pin (our shield:
  its supply then from the DK's 3V3 through the chokes, no LDO of its own), the camera (VDD_CAM is
  3.3 V, UM3300 Table 19), and anything with an undervoltage lock-out above 3 V.
- **Where the cell goes in:** on JP2's common pin (the 5 V net after the source selector), the
  jumper removed — so no USB or VIN path feeds back into the cell; the charger is a separate 1S
  module with load sharing, the cell protected at ~3.0 V.
- **The display, read (MB1860 schematic, rev. B-01, given by the owner):** its backlight is
  driven by **TPS61042DRB** (U102, a boost LED driver) from **BL_5V** (CN1 pin 45, through a
  600 Ω ferrite); the STLD40D beside it is the unfitted backup. The TPS61042 runs from **1.8–6 V**
  (TI; from memory, to be confirmed) — so it lights from one cell too. The panel's logic is on
  **3V3** (CN1 pin 50). **The last open item on the 5 V net is closed for the display;** left: the
  USB-A port's VBUS (unused) and our shield's +5V (moved to the 3V3), and JP2's exact pin for the
  cell, from the MB1939 schematic.
- **The N6 comes only in BGA** (DS14791 Rev 2): VFBGA142 8 × 8 mm at 0.5 mm, VFBGA169 6 × 6 at
  0.4, VFBGA178 12 × 12 at 0.8, VFBGA198 10 × 10 at 0.65, VFBGA223 10 × 10 at 0.5, VFBGA264
  14 × 14 at 0.8; and it has **no internal flash** — its BootROM loads the firmware from an
  external one. A board of our own would carry the BGA, the external flash and the rails
  (0.8 V core, 1.8 V analog, 3.3 V I/O) at the least. The board's choice is waiting for the owner
  (23 Nov 2026: "zatím počkej").
- **A tiny N6 module, everything on its edges?** (the owner, 23 Nov 2026: a camera connector, a
  display connector, the rest to pins). Searched twice: **no STM32N6 system-on-module or core
  board found** — only ST's DK and Nucleo, and the boards above (OpenMV N6, Neuro N6 in Feather
  size with a cell charger and camera/display modules, still a crowdfunded prototype in March
  2026). The chip came out in 2025, is BGA only, needs external flash and three rails — makers
  have built dev kits and cameras, not modules, so far. To be looked for again later; the Neuro
  N6's state (shipping or not) first.

## Is the N6 enough for all of it? (23 Nov 2026)

The owner: two pictures laid over each other and the rest — what is the chip's power?
DS14791 Rev 2 and `calc/compute.py`:

- **The core:** Cortex-M55 at 800 MHz, 3360 CoreMark, 1280 DMIPS, Helium, single- and
  half-precision FPU. Its floating-point peak (Arm's per-cycle rates, from memory): scalar FP32
  ~1.6 GFLOP/s, **Helium FP32 ~3.2**, Helium FP16 ~6.4.
- **The NPU:** Neural-ART, 1 GHz, **600 GOPS** int8, 288 MAC/cycle.
- **The pictures cost the core nothing:** the camera through the ISP (three pipes, crop, downsize,
  YUV); **the display controller (LTDC) blends two layers on the fly** (§3.28: "Composition:
  2 layers", blend, layer 1 may be YUV420) — the camera on one, the map with its transparency on
  the other; DMA2D and the Neo-Chrom GPU scale and colour the map; JPEG saves the picture.
- **The map** (192 kHz, coarse field 10 frames/s + fine cleaned patch 5 frames/s): ~1.05 GFLOP/s
  — a third of Helium's FP32 peak. A hand-made loop reaches perhaps a third to a half of peak, so
  in FP32 **the core is near full**; in FP16 about half. **Room to spare:** the patch at fewer
  frames or bins; FP16 where the precision allows (the map needs ~30 dB, FP16 carries ~66); and
  **the NPU**, idle so far: the beamformer is a matrix times a vector (the steering vectors times
  each snapshot's spectra) — a dense layer to the NPU, the squaring and averaging left to the core.
- **To be measured** on the bench: CMSIS-DSP's complex dot product on the M55 at 800 MHz; then
  the split between the core and the NPU decided.

## Ohm Lab Neuro N6 — read (23 Nov 2026, the owner's link)

[CNX Software, 23 Mar 2026](https://www.cnx-software.com/2026/03/23/ohm-lab-neuro-n6-modular-stm32n6-ai-vision-devkit-support-rolling-shutter-global-shutter-or-thermal-camera/),
[Kickstarter](https://www.kickstarter.com/projects/ohmlab-ltd/neuro-n6), [GitHub](https://github.com/ohmlab-ltd):

- **STM32N6** (M55 800 MHz, NPU 600 GOPS), **64 MB PSRAM, 32 MB flash**, a microphone, an IMU and a
  magnetometer, USB-C; **Feather size, 53 × 23 × 9 mm, 6.7 g**.
- **Power: 5 V at USB-C, or a 3.7 V Li-Pol on a 2-pin connector with a 500 mA charger** — the cell
  straight on, as the owner wants.
- **Everything else on two high-density connectors underneath (40 and 30 pins):** SDMMC, **LTDC
  (RGB565) for a display, MIPI CSI-2 for a camera up to 5 Mpx, SAI**, I2C, SPI, UART, SWD, 3V3,
  1V8, VIN; Feather's 16 + 12 pins on the sides. Add-ons: cameras (OV5640, a global-shutter one,
  a FLIR thermal), **Vision TFT (800 × 480 touch, OV5640, ToF, speaker)**, Ethernet, Wi-Fi.
- **Price:** the board 73 $, with the OV5640 99 $, the full bundle 399 $ (Kickstarter);
  **deliveries planned from November 2026.**
- **The owner's dream board, nearly:** small, a cell, camera and display on connectors, the rest to
  pins. **What decides it for us:** how many serial lines (SAI blocks, SPIs with SCK, data and NSS)
  its two connectors carry — two give 32 microphones at 96 kHz, four give 192 kHz. Its pin table
  is not public in what could be read here (GitHub refuses this container); Ohm Lab's documents
  or the board itself.

## Three from AliExpress (the owner, 23 Nov 2026)

- **Alientek (正点原子) CNN647B — an STM32N647 core board.** What the owner wished for: the chip
  (STM32N647X0H3Q — the N657 without its cryptography), **32 MB NOR flash (Octo-SPI), 32 MB
  HyperRAM, 2 GB SD NAND, 2 Kb EEPROM**, an **RGB LCD FPC connector on the board**, USB-C,
  SWD and UART pads, reset and user buttons; the rest on board-to-board connectors underneath, to
  Alientek's DNN647 base board (which carries the MIPI camera connector, a 6–15 V DC input and
  the usual dev-board crowd) — "can be used with the base plate, or alone". ~57–64 € (the
  owner's link). Sources: the owner's screenshot,
  [Alientek wiki](https://wiki.alientek.com/docs/Boards/STM32/DNN647/start-guide/stm32n647-board-introduction),
  [downloads](https://www.openedv.com/docs/boards/stm32/zdyz_stm32N647.html) (schematics on a
  Baidu disk, not reachable here). **Wanted:** the underside connectors' pin table — are the MIPI
  CSI lanes, SAI2 and three SPIs there — and how the core board is fed (5 V only, or 3.3 V too).
- **CamThink NeoEyes NE301** (~200 €): a finished STM32N6 camera in a case, batteries inside;
  a product, not a board to build on.
- **MicroPhase A7-Lite, Xilinx Artix-7 FPGA** (~106 €): the FPGA way, not needed while the N6
  takes four lines.
- **Alientek without registering (23 Nov 2026):** the wiki (wiki.alientek.com, DNN647) is open
  but gives no pin tables — its examples name the projects (`Projects/45_Recorder` …) and the
  core board's parts (NOR flash MX25UM25645G or two BY25FQ128EL, per the external loaders), not
  the connector; the schematics and the software package sit only on a Baidu disk; Alientek's
  GitHub (openedv) shows no N647 code. Left: the AliExpress listing's own pictures, or the
  seller asked for the core board's schematic PDF.

## Alientek CNN647B — its schematic read (23 Nov 2026, given by the owner)

Alientek's ATK-CNN647B V1.0 schematic. **45 × 32 mm.**

**Power — one cell will do** (Power.SchDoc): everything is made from **VCC_5V** (J5 pins 1–3):
U1 XC6206P182 → VDDA_1V8_AON, U2 XC6206P332 → VDD_3V3_VDD, **U3 TMI3113 buck → VDDSMPS_1V8**
(the N6's own SMPS makes the core), U5 RT9013-18 → VDD_1V8, U4 RT9013-33 → VDD_3V3. Their inputs:
TMI3113 **2.7–5.5 V** (TOLL's sheet; OVP 6.1 V), RT9013 and XC6206 from ~2 V (from memory). So **a
Li-Pol cell (3.0–4.2 V) on VCC_5V runs the board**: 1.8 V and the core regulated to the end, 3.3 V
following the cell below ~3.5 V — the N6's VDD runs 1.71–3.6 V. No boost, no 5 V anywhere.

**Two 80-pin board-to-board connectors underneath, J5 and J6** (Pinout.SchDoc): VCC_5V, VDD_1V8,
VDD_3V3, VREFP, VBAT, NRST, PWR_ON, both USB, **MIPI CSI-2 (D0, D1, clock pairs on J6)**, the LTDC
(also on the board's own RGB LCD FPC) and ~100 GPIOs. Cross-checked against ST's pin data:

- **Both SAIs are free** (no codec on the core board) — **four lines on SAI alone, each SAI
  aligning its own frames: no SPI, no flip-flop, no firmware alignment:**

| line | data | clock, frame |
|---|---|---|
| SAI2 block B | PE7 (J6) — or PE11, PF11 | SCK_B PE12 (J5), FS_B PB8 (J5) |
| SAI2 block A | PF5 (J6) | synchronous to block B (inside the SAI) |
| SAI1 block A | PB7 (J5) — or PB2 | SCK_A PC2 (J5) or PB6, FS_A PB0 (J5) |
| SAI1 block B | PE3 (J5) — or PA3 | synchronous to block A |

  (SAI2_FS_A is PG13 = LTDC_DE, so block A runs synchronous; all clocks from the one BCLK/FSYNC.)
- **I2C to the converters:** I2C2 on PD4/PD14 (J5, so labelled), leaving PE13/PE14 (I2C4) free.
- **The camera:** its CSI pairs on J6 — routed on our board to a camera FPC in the honeycomb's
  middle (100 Ω differential, short).
- **The display:** on the core board's own RGB LCD connector.

**So the tool becomes:** the CNN647B plugged onto **our board** — the microphones, the four
converters, the camera's connector, the cell and its charger, the two mating connectors.
**Open:** the mating connector's part (Alientek's base board DNN647 has it; 80 pins, fine pitch);
the 3.3 V LDO dropouts against the cell, read in their sheets; SAI target at 24.576 MHz (DS: 50 MHz).
- **The mating connector — not found (23 Nov 2026):** the CNN647B schematic names J5 and J6 only as
  80-pin parts, numbered round the body (pin 1 facing 80: two rows of 40 counted one after the
  other); the wiki, the download page and a search in English and Chinese give no part. Ways left:
  the seller asked ("mating connector part number for J5/J6 on the CNN647B"), the DNN647 base
  board's schematic, or the board in hand — the marking on the connector, its pitch, row spacing
  and stacking height measured.

## The display (23 Nov 2026, the owner: "vybrat display")

The core board's own RGB LCD connector (its J4, 40 pins, Alientek's ATK-MDxxxxR modules) feeds the
display **VCC_5V — on our build the cell's 3.0–4.2 V** — and nothing found says whether
Alientek's modules (4.3" 480 × 272 / 800 × 480, 7" 800 × 480 / 1024 × 600) light their backlight
from that: no module sheet open, the wiki silent. Two ways:

- **A — an Alientek module on the core board's connector:** nothing to route, Alientek's examples
  drive it as they are. Needs: the module's supply range (its listing or the module in hand).
- **B — the display on our board, driven from J6:** J6 carries the LTDC's R2–R7, G2–G7, B2–B7
  (18-bit), its clock and DE (PG13) — not HSYNC/VSYNC, so **a panel run in DE mode**. A plain
  40-pin RGB panel (4.3" or 5", 800 × 480, IPS) brings its LED string's anode and cathode out, and
  **our board drives it — a TPS61042 as ST's MB1860 does, running from 1.8–6 V, so straight from
  the cell**; the touch controller on I2C2. More routing on our board (one 0.5 mm FPC, ~24 lines),
  but any panel, a backlight that works from the cell for certain, and the brightness ours to set.
- **The size:** 4.3–5", 800 × 480 — a hand-held's, and what the map needs; daylight readability
  (an IPS with a bright backlight) matters more than pixels.
- **The owner's choice: the display stays on the core board** (23 Nov 2026 — keep the fast signals
  off our board). The core board's **J4 is Alientek's 40-pin, 0.5 mm FPC** (Devices.SchDoc):
  1 RESET, 2 TP_PEN (PB3), 3 TP_SCL (PD14), 4 TP_MISO (PD8), 5 TP_SDA (PD4), 6 TP_CS (PD10), 7 BL
  (PA3, TIM16_CH1 — the backlight's PWM), 8 DE, 9 VSYNC, 10 HSYNC, 11 CLK, 12/21/30 GND, 13–20
  B7–B0, 22–29 G7–G0, 31–38 R7–R0 (**full 24-bit**), 39–40 VCC (= VCC_5V). **Its pinout is
  Alientek's own, not the common 40-pin panel's** (which has the LED string on pins 1–2): what fits
  is **Alientek's RGB LCD modules, ATK-MDxxxxR** — 4.3" 800 × 480 (ATK-MD0430R-800480) the size
  for us. To ask the seller: **does the module's backlight run from a 3.0–4.2 V VCC?**
- **The camera with as little fast routing as possible:** its 22-pin FPC connector put **right
  beside J6** on our board — the CSI pairs a few millimetres on the board, the flex cable carrying
  them to the camera in the honeycomb's middle. A USB camera instead would need the core board's
  USB host and **5 V on VBUS** (the core board ties VBUS to VCC_5V — the cell), so a boost for it
  alone; MIPI is the simpler.
- **A candidate, the owner's link (23 Nov 2026):** RONBO Electronics **MRG7115** — 7" IPS
  **1024 × 600**, EK79001 driver, **FT5446** capacitive touch (5 points, I2C), 24-bit RGB,
  "apply to Alientek STM32 board directly" (the same 40-pin), **350 cd/m²**, board
  164.9 × 100 mm, −20…70 °C, **"operating voltage 5.0 V"**
  ([made-in-china](https://m.made-in-china.com/product/7-0-Inch-IPS-1024X600-Alientek-Stm32-Capacitive-Touch-LCD-Display-with-RGB-Driver-Board-927964215.html)).
  RONBO seems to be the maker of these modules and offers custom ones. **To ask them:** the
  backlight driver's part and the lowest VCC it lights at (3.0–4.2 V wanted), or a version for a
  1S cell; and the same in 4.3" or 5" 800 × 480. **To weigh:** 7" is ~20 cm across the board —
  the honeycomb's size, so it fits the face; its backlight is the largest draw (~1 W and more at
  350 cd/m², against ~0.3–0.5 W for a 4.3"); 350 cd/m² reads in a hall, not in sunlight;
  1024 × 600 × 2 B = 1.2 MB a frame, in the HyperRAM.
- **A display on 3.3 V? (the owner, 23 Nov 2026):** none found for Alientek's connector. The
  modules that fit it — Alientek's own, RONBO's MRG7115 (7"), **MRG4311 (4.3" 800 × 480, its
  manual on [LCDWiki](https://www.lcdwiki.com/res/MRG4311/4.3inch_RGB_Display_User_Manual_EN.pdf):
  "P2 interface compatible with atomic RGB interface")** — all take **5 V in and make their 3.3 V
  on the module** (an LDO, "the power circuit converts the input 5 V to 3.3 V"), the backlight fed
  from the 5 V; the MRG4311 draws 50 mA with the backlight off, 165 mA at full (~0.8 W). From a cell
  (3.0–4.2 V): the module's LDO passes the cell less its dropout to the panel's logic (fine down to
  a cell of ~3.3–3.4 V); **the backlight depends on its driver, which no page names.** **The cheap
  way to know: one module on a bench supply, swept 4.2 → 3.0 V** — or the driver's part asked of
  RONBO. Failing that, way B above (the panel on our board, our own backlight driver from the cell).
- **Displays with their own controller (RA8875, SSD1963 — EastRising's ER-TFTM070-5 and -4V3,
  set to 3.3 V by a jumper; brought by the owner, 23 Nov 2026) are left:** they take the picture
  over SPI or an 8080 bus into their own memory, so the N6's display controller and its two-layer
  blending (the camera and the map) go unused and every frame is pushed by the core — at
  800 × 480 × 2 B, ~1.6 frames/s over a 10 MHz SPI; and ~0.5 A at 3.3 V would overload the core
  board's 3.3 V regulator (RT9013, 500 mA). The point that stands: **a panel's logic runs on 3.3 V
  and its LED string needs a boost — whose input may well be the cell**; so the RGB module's own
  backlight driver is the one thing to learn (the bench test above).
- **BuyDisplay ER-TFTM070-4V3** (the owner's link, 23 Nov 2026): 7" 800 × 480, **SSD1963**, 8080
  bus 8/16/18/24-bit, **3.3 V typical, up to 480 mA**, **200 cd/m²**, ~35 $
  ([BuyDisplay](https://www.buydisplay.com/7-tft-screen-touch-lcd-display-module-w-ssd1963-controller-board-mcu)).
  Against the RGB module on the core board's connector: **its 3.3 V would need a supply of its
  own** (0.48 A is the core board's whole 3.3 V regulator; from the cell a buck-boost, as 4.2 V is
  above 3.3 V and 3.0 V below), **a 16-bit 8080 bus through our board** (FMC: ~20 lines, which
  collide with the SAI and I2C pins chosen), the N6's display controller and its two-layer blend
  left idle, and a dimmer panel. **Not taken**; the RGB module stays, its backlight to be tested.
- **Two bare 7" panels (the owner's sheets, 23 Nov 2026):**

| | Newhaven NHD-7.0-800480EF-ATXL-T | Winstar WF70B2SIAGDNGA# |
|---|---|---|
| panel | 800 × 480, 24-bit RGB, no touch | 800 × 480, 24-bit RGB, PCAP (ILI2130, I2C) |
| logic | **VDD 3.0–3.3–3.6 V, 60–85–120 mA** | **VCC 3.0–3.3–3.6 V, 76–114 mA**; touch VDDT 3.0–3.6 V |
| backlight | **its LED string on pins 1–2: 15–17 V, 45–60–75 mA** (~1 W) | its LED string on pins 1–2 (figures not in this sheet) |
| luminance | 170–220 cd/m² | — |
| connector | 40-pin 0.5 mm FFC (Molex 54104-4031) | 40-pin |

  **Their pinout is the common one, not Alientek's** (LED−, LED+, GND, VDD, R0–R7, G0–G7, B0–B7,
  GND, CLK, DISP/R-L, HSYNC, VSYNC, DE …), so neither plugs into the core board's J4 as it is.
- **What the panels show: way C — a small adapter of our own between J4 and a bare panel.**
  J4 gives the 24-bit RGB, the syncs, DE, the touch lines, BL (PWM) and VCC (the cell). The adapter
  passes the RGB lines straight across (two 40-pin 0.5 mm FPC connectors, a few centimetres, no
  fast lines on our main board) and adds **an LDO 3.3 V from VCC for the panel's logic** (~0.1 A;
  3.0 V is the panel's floor, so a low-dropout part keeps it to a cell of ~3.15 V) and **a boost
  LED driver from VCC for the string** (16 V, 60 mA — the TPS61042 class, from 1.8 V up), dimmed
  by BL. That is what Alientek's modules are — with the backlight working from the cell for
  certain. Kept as the answer if the bought module fails the bench test.
