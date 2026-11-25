# Netopýr — the acoustic camera's head, as a netlist

*Built 25 Nov 2026 (the owner: "postav tu strukturu, báze a netopýr"). Datel — the knock — is this tool's tap mode, its
chapter at the end.* The head plugs into the Báze's port H1 or H2 (`../baze/schematic.md`, *The
heads' ports*); its clocks in `../baze/kuranty.md`. Datasheets named where used.

## The head — STM32H723, the raw data out on the PSSI (25 Nov 2026)

The owner, 25 Nov 2026: **all four converters through the H723, one path for every channel**;
the 32 channels raw, the whole band, out on 8 lines of the Báze's PSSI; the commands on a UART;
the head on the Báze's clock and PPS; the converters' BCLK and FSYNC made on the head. One board
for H1 and H2 alike. **STM32H723VGT6, LQFP-100** (the owner: leads, not balls — they take a bent
board and a fall), Cortex-M7, 1 MB flash, 564 kB RAM; pins from ST's open pin data
(`mcu/STM32H723VGTx.xml`), timing from DS13313 Rev 5.

| ref | part | job |
|---|---|---|
| U10 | **STM32H723VGT6**, LQFP-100 | four SAI lines in, the PSSI out, the UART, the converters' setup |
| U11 | **LMK1C1104 (m)**, 1:4 | the incoming CLOCK → OSC_IN (PH0) and PDCK (PA6), a test point |
| U12 | **LMK1C1108PWR**, 1:8 | BCLK from MCO1 → U1–U4, SAI1_SCK_A (PE5), SAI4_SCK_A (PD13), a test point |
| U13 | **LMK1C1108PWR**, 1:8 | FSYNC from TIM2_CH1 → U1–U4, SAI1_FS_A (PE4), SAI4_FS_A (PD12), a test point |
| J1 | 2 × 15, 1.27 mm, shrouded, keyed | the Báze's head connector, pin for pin (`../baze/schematic.md`) |
| J2 | Tag-Connect TC2030 pads | SWD: PA13 (72), PA14 (76), NRST (14), PB3 (89) SWO |

**The microphones on the propeller** (`calc/propeller_14.csv`, 25 Nov 2026): 32 fitted of 128
places, one in each group of four. **Each converter serves two neighbouring arms** — U1 arms 1–2,
U2 arms 3–4, U3 arms 5–6, U4 arms 7–8, on the back between its two arms: its data line g (and its
PDMCLKg) takes group g of both arms — the first arm's microphone SELECT to GND, the second's to
MICVDD. Every place has its footprint and its SELECT jumper; the empty ones are stubs a few cm
long, harmless at 3.072 MHz (no terminator).

**The four lines into the H723's four SAI blocks, all targets:**

| petal | converter | SDOUT, 33 Ω → | H723 pin | SAI |
|---|---|---|---|---|
| 1 | U1 | PC1 (16) | SAI1_SD_A | SAI1 block A: SCK PE5 (4), FS PE4 (3) |
| 2 | U2 | PE3 (2) | SAI1_SD_B | SAI1 block B, synchronous to A |
| 3 | U3 | PD11 (58) | SAI4_SD_A | SAI4 block A: SCK PD13 (60), FS PD12 (59) |
| 4 | U4 | PE11 (41) | SAI4_SD_B | SAI4 block B, synchronous to A |

Each converter 8 slots × 16 bit, 192 kHz, BCLK 24.576 MHz (ratio 128), a target. The H723's SAI
as a target ≤ 50 MHz, setup 3.5 ns, hold 0 (Table 110).

**The PSSI out, 8 lines** (DS13313 Table 100: PDCK ≤ 50 MHz and ≤ 0.4 × HCLK — the HCLK ≥ 61.44
MHz; data valid ≤ 10 ns, held ≥ 4.5 ns): PDCK **PA6 (30)** ← U11 (the Báze's clock, 24.576 MHz);
D0 **PC6 (63)**, D1 **PC7 (64)**, D2 **PC8 (65)**, D3 **PC9 (66)**, D4 **PC11 (79)**, D5 **PD3
(84)**, D6 **PB8 (95)**, D7 **PB9 (96)** → J1, 33 Ω each. A frame (192 kHz) = 128 clocks = **128
byte-places**: 64 for the 32 samples (16 bit each), the rest the frame number, the head's state
and room — the layout in the protocol, to come. The SAIs' DMA fills the PSSI's; a FIFO underrun
is seen in the frame number and mended at the next PPS.

**The rest of U10:**

| pin | net | |
|---|---|---|
| PH0 (12) | OSC_IN ← U11, HSE in bypass | 24.576 MHz (DS13313 Table 31: 4–50 MHz); the core ~98.3 MHz (× 4 by PLL) while it only passes samples on, up to 546.8 MHz if it computes |
| PA8 (67) | **MCO1** → U12 | the HSE passed straight out: BCLK for the converters, edges remade on the head |
| PA5 (29) | **TIM2_CH1** → U13 | FSYNC: TIM2 counts 128 clocks, from a timer clock locked to the HSE |
| PA1 (23) | **TIM2_CH2** ← J1 PPS | resets TIM2 at the PPS: both heads start their frames together, within a timer tick |
| PA9 (68), PA10 (69) | **USART1** TX → J1, RX ← J1 | the Báze's commands, the head's answers, a new firmware (≤ 12.5 Mbit/s) |
| PB10 (46), PB11 (47) | **I2C2** SCL, SDA → U1–U4 | the converters' setup, 2.2 kΩ to +3V3 |
| PB1 (35) | SHDNZ → U1–U4 | 10 kΩ to GND: off until the H723 wakes them |
| PE15 (45) | LED, 1 kΩ | a sign of life |
| NRST (14) | ← J1 and J2, 0.1 µF to GND | the Báze can restart the head |
| BOOT0 (94) | 10 kΩ to GND | boot from flash; updates by its own loader over the UART |
| VDD 11, 27, 50, 75, 100 | +3V3 behind the ferrite, 0.1 µF at each, 4.7 µF once | |
| VDDA 21, VREF+ 20 | +3V3 through a ferrite bead, 1 µF + 0.1 µF | |
| VSS 10, 26, 49, 74, 99, VSSA 19 | GND | |
| VCAP 48, 73 | 2.2 µF ± 20 % each to GND, ESR < 100 mΩ (DS13313 Table 14) | |
| VBAT 6 | +3V3 | no RTC battery on the head |

**To check on the bench:** FSYNC's edge (TIM2, on a PLL clock) against BCLK's (MCO1) — it must
fall clear of the converters' setup and hold; if not, the compare moved by a tick (~10 ns: TIM2 at 98.3 MHz, 512 ticks a frame).

## Control

- The converters on the H723's **I2C2** (PB10/PB11), addresses 0x4C–0x4F (ADDR pins: U1 00, U2 01,
  U3 10, U4 11); **SHDNZ** of all four from PB1, 10 kΩ to GND. The Báze talks only to the H723,
  on its UART.

## A petal (×4: U1…U4, microphones MK1…MK32)

| pin (PCMD3180) | net |
|---|---|
| 1 AVDD | +1V8-Pn, 0.1 µF + 1 µF to AVSS |
| 2 AREG | **shorted to AVDD** (AVDD 1.8 V operation), 10 µF + 0.1 µF to AVSS |
| 3 VREF | 1 µF to AVSS |
| 4 AVSS | GND |
| 5 MICBIAS | MICVDD-n, 1 µF to AVSS; set to AVDD (≤ 20 mA, §6.3.4) |
| 6, 8, 10, 12 PDMDIN1…4 | DATA of microphone pairs 1…4 |
| 7, 9, 11, 13 PDMCLK1…4 | CLOCK of microphone pairs 1…4, 33 Ω at the pin; 3.072 MHz |
| 14 SHDNZ | SHDNZ |
| 15 ADDR1, 16 ADDR0 | the address, to GND or IOVDD |
| 17 SCL, 18 SDA | the H723's I2C2 (PB10, PB11) |
| 19 IOVDD | +3V3 from J1 (behind the ferrite), 0.1 µF |
| 20 GPIO1 | test point (all four are targets) |
| 21 SDOUT | its line, 33 Ω |
| 22 BCLK, 23 FSYNC | from U12 (BCLK) / U13 (FSYNC) |
| 24 DREG | 10 µF + 0.1 µF to GND |
| pad | GND |

**The microphones** (SPH0641LU4H-1: 1 DATA, 2 SELECT, 3 GROUND, 4 CLOCK, 5 VDD): pair k shares
PDMCLKk and PDMDINk, one SELECT to GND and one to MICVDD-n; VDD = MICVDD-n with **one 0.1 µF at each, C0G** — the sheet (SPH0641 Rev B §6): bypass near each VDD pin, and *"capacitors near the microphone should not contain Class 2 dielectrics"* (X7R/X5R are piezoelectric: they sing and pick up). The petal's 47 µF and the X7R parts kept away from the microphones, by the converter. A C0G 0.1 µF at JLCPCB (0603/0805) — **(m)**, to be found.
Bottom port, on the board's back, the sound through a hole (the coupons decide the hole and the
thickness). Converter settings for the firmware: 192 kHz, 8 slots × 16 bit, the low-latency
filter (DECI_FILT = 01), channels latched on the two clock edges per pair.

## The coupons

One petal (U1, its eight microphones) with the clocks, its own LDO and choke on its own small board — its one
TDM line into any SAI (an H723 or a DK) — in **0.6 mm** and **1.6 mm**, straight, countersunk and counterbored holes,
two microphones on each shape; a real leak (a nozzle) as the source. Whether the coupon plugs
onto the CNN647B (J5/J6) or is read by any board through a 5-pin cable: to be settled with the
mating connector.

## Datel — the knock (24 Nov 2026)

*Datel is Netopýr's tap mode (the owner, 24 Nov 2026): the same tool, the knock heard and the
hollows seen. Its output, J8, stands on the Báze for now (PQ5, TIM8_CH2).*

### The knocker's output

The owner: the knocker in a rod pressed to the surface; which actuator — a push
solenoid or a voice-coil exciter — is settled on the coupon. **One output drives either:**

| ref | part | net |
|---|---|---|
| J8 | 2-pin connector to the actuator in the rod's housing | pin 1 **SYS**, pin 2 **KNOCK** |
| Q1 | **AO3400A**, N-MOSFET 30 V 5.7 A, 48 mΩ at 2.5 V gate, SOT-23 — **LCSC C20917, basic** | drain KNOCK, source GND |
| D1 | **SS34**, Schottky 40 V 3 A, SMA — **LCSC C8678, basic** | across the coil: anode KNOCK, cathode SYS |
| R1, R2 | 100 Ω in the gate, 100 kΩ gate to GND | Q1 held off while the N6 boots |
| C | a C_P (47 µF aluminium polymer + 1 µF 50 V) at J8 | SYS's branch end |

**Gate from PQ5, TIM8_CH2** (freed by the MB1854): the pulse's length and repeat set in firmware —
one pulse of ~10–20 ms for a solenoid, short pulses for an exciter — and limited there, so a coil
is never left on. **The person's own hammer needs nothing:** the first loud arrival triggers.

