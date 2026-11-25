# The Báze — the main board every tool plugs into, as a netlist

*Built 25 Nov 2026 (the owner: "postav tu strukturu, báze a netopýr") from the acoustic camera's first
schematic. Written as nets, to be drawn in KiCad.* Sources in
the makers' datasheets, named where used: Alientek ATK-CNN647B V1.0
schematic, DS14791 Rev 2 (the N6), DS13313 Rev 5 (the STM32H723), BQ25628, TPS63020; calculations
in `calc/`; every clock of the Báze and its heads in `kuranty.md`. Parts marked **(m)** are chosen
from memory, their sheets still to read.

**The Báze** carries the CNN647B core board (the STM32N647) on its two 80-pin connectors J5, J6,
the power from one cell with its charger, the USB-C, the card, the communication module, the
camera's connector, the buttons, the lights — and **the heads' ports**: two head ports H1 and H2
(the raw data on the N6's one PSSI, 8 + 8 lines), an I2C port, its own sensors (the air, the distance, the motion, a microphone). The display plugs into
the core board's own RGB LCD connector (its J4). A tool is the Báze and the head behind its front
mask — Netopýr's microphones (`../netopyr/`), later others.

## Power — from one cell, no 5 V anywhere

**25 Nov 2026:** the petals (their LDOs U21, U25–U27, chokes L1–L4, C_P) now stand **on Netopýr's head**, fed
by the head port's +3V3 (pins 1–4) from U23 — written here as they were until this section is
split; the head's side in `../netopyr/schematic.md`.

| ref | part | job |
|---|---|---|
| BT1 | **a 1S pack with its own protection (PCM) — sodium-ion intended** (the owner, as on other projects; Li-ion fits the same board) | sodium ~2.5–3.9 V (curve, `calc/sodium.py`), Li-ion 3.0–4.2 V; the BQ25628's charge voltage and VBAT_UVLO set to the chemistry |
| J1 | USB-C, power only (CC1/CC2 5.1 kΩ to GND) | charging |
| U20 | **TI BQ25628** (SLUSEG4C, Feb 2025; **WQFN-18, 2.5 × 3 mm**) — the owner, 24 Nov 2026: no ball package | a 2 A switching charger with NVDC power path, BATFET 15 mΩ, **from the battery 6 A continuous, 10 A for 50 ms**; charge voltage **3.50–4.80 V** (Li-ion 4.2 V, sodium 3.65/3.90 V); **the BATFET opens below VBAT_UVLO, 2.2 V or 1.8 V** (a sodium cell's floor); a 12-bit ADC — the charge counted by the N6 from it; I2C, INT, QON (the power button) |
| U22 | **TI TPS63020DSJR** (VSON-14, 3 × 4 mm; LCSC C15483) — 2 A at 3.3 V from VIN > 2.5 V, 1.8–5.5 V in | **the core board's feed: SYS → 3.9 V → J5 VCC_5V**, a divider sets it |
| U23 | **TPS63020DSJR**, the same part | **our board's 3.3 V**: the camera (VDD_CAM) and the four analog LDOs' inputs — the converters' IOVDD and the clocks are not on it, they take the N6's own VDD_3V3 (below) |
| U21, U25–U27 | **TI TPS7A2018PDBVR, SOT-23-5, LCSC C963430** (the TPS7A20 family; SBVS338H), **one per petal, on the petal** (the owner, 24 Nov 2026: each branch its own LDO and its own choke), 1 µF ceramic in and out | **+1V8A-P1…P4** straight from **U23's 3.3 V** — 1.5 V across each, so its PSRR is the sheet's (stated at VIN = VOUT + 1.0 V), at ~18 mA its better column (20 mA: 75 dB to 100 kHz) |
| L1–L4, C | 33 µH SWPA3015S330MT (C68342) + **C_P** (47 µF aluminium polymer + 1 µF 50 V, below), one per petal, behind its LDO | +1V8-P1…P4 |
| L5, C | the same | +3V3-CLK for the oscillator and the clock buffers, from the core board's VDD_3V3 (J5 pin 5) |

- **One polymer and one ceramic for the whole board** (the owner, 24 Nov 2026): **C_P = Panasonic
  SP-Cap EEFCT1C470R**, 47 µF **16 V**, aluminium polymer, 40 mΩ at 100 kHz, 7.3 × 4.3 mm,
  **LCSC C139571** (stock to be seen at ordering) **+ 1 µF 50 V X7R 0805, Samsung
  CL21B105KBFNNNE, LCSC C28323**(basic; −4 % at 6.9 V on Samsung's curve, so
  ~1 µF at our 1.8–4.8 V). **Aluminium, not tantalum:** tantalum dislikes current surges (the
  cell's connection, SYS). **47 µF, not more:** against a ceramic that keeps perhaps half of its
  value at the working voltage, a polymer's 47 µF is 47 µF — and it does not sing; and 47 µF stays
  under the TPS7A20's **200 µF effective output maximum** (SBVS338H, Recommended Operating
  Conditions, note 3). **At the microphones only one 0.1 µF C0G each** (the sheet: no Class 2
  dielectrics near them). **One C_P at each regulator and one at each branch's end** (the owner: a
  branch's track is an inductance at these frequencies):

| place | the sheet's word | C_P |
|---|---|---|
| SYS (U20's output, U22/U23's inputs) | BQ25628 (SLUSEG4C): C_SYS **20–500 µF**, its loop made for ≥ 10 µF ceramic | 1× |
| U22's output, 3.9 V | TPS63020 (SLVS916I, table 1): 2×22 … ≥ 100 µF, "a larger output capacitor less critical" | 1× |
| J5, the core board's input (the branch's end) | the same net | 1× — the N6's and the display's bursts |
| U23's output, 3.3 V | as U22 | 1× |
| the four LDOs' common input on the microphone board (the branch's end) | TPS7A20: C_IN ≥ 1 µF, no maximum | **1×** for all four (the owner, 24 Nov 2026); each LDO keeps its own 1 µF at its pin |
| each petal LDO's output, behind its choke | TPS7A20: C_OUT effective ≤ 200 µF | 4× (47 + 1 + the LDO's own 1 µF) |
| each petal's 1.8 V end, at its converter and microphones — **only if the track is long** (the owner) | the same LDO: 2 × 48 + 1 ≈ 97 µF < 200 | 4×, settled at the layout |
| the camera's connector (the branch's end) | U23's net | 1× |
| after L5, the clocks | the core board's VDD_3V3 | 1× |
| VBUS, BAT | VBUS up to 18 V; USB's inrush; the cell is the bulk | none |

  **The camera shares the LDOs' C_P** (the owner, 24 Nov 2026: keep one if the surges allow it;
  `calc/surge.py`): a camera step of 0.1–0.5 A moves U23's 3.3 V by ~6–30 mV (TPS63020 fig. 21,
  ~60 mV per amp), by 18–92 mV even if the capacitors alone held it for 20 µs — the camera's 3.3 V
  and the LDOs' 2.0 V floor untouched; behind an LDO (75 dB) and a petal's LC it is **0.6–2.8 µV**
  at the 1.8 V, a camera line-rate ripple (~60 kHz) **~2 nV**. One is enough; a second only if the
  camera's current (the OV5647 module's, to be read) proves far above 0.5 A.
  **11 × C_P** (15 with the petals' ends); **on the microphone board 5 for the analog** (9 with
  the ends), and the camera's and the clocks' if they sit on it. The ceramics the sheets ask for stay beside them: the BQ25628's (VBUS 1 µF, PMID
  10 µF, SYS ≥ 10 µF, BAT 10 µF, REGN **10 µF 50 V, C13585** in place of the sheet's 4.7 µF — the owner, 24 Nov 2026: one part; ~8 µF at REGN's ~4.6 V, more than the sheet's, an LDO's usual safe side, to be checked against TI's EVM — BTST 47 nF), the TPS63020s' input and their 2 × 22 µF
  output (its loop is compensated for them), the TPS7A20s' 1 µF out, the converters' AVDD
  0.1 + 1 µF, AREG and DREG 10 µF. The petal's filter with C_P: −31 / −41 / −50 dB at 25 / 45 /
  80 kHz (`calc/supply.py`'s LC, 33 µH 0.82 Ω, 40 mΩ). **Room:** if the 7.3 × 4.3 mm parts do not fit between the cells, the petals take KEMET T520B476M010ATE035
  (tantalum polymer, 47 µF 10 V, 35 mΩ, case B 3.5 × 2.8 mm, LCSC C141441): no surge there, the
  LDO and the choke limit it.
- **Each petal its own LDO and its own choke** (the owner, 24 Nov 2026): the 3.3 V runs to the
  petals and is made 1.8 V on each, so no analog rail crosses the board; a petal's fault or its
  converter's switching current stays on its own LDO; each LDO at ~18 mA, its quieter column.
- **U22 and U23 with PS/SYNC tied to VIN: power-save off, fixed 2.4 MHz PWM** (SLVS916I, pin 13).
  In power save at a light load a buck-boost switches in bursts at kHz to tens of kHz — inside our
  band, both as ripple and as its coil and capacitors singing beside the microphones. PWM costs a
  few mA at light load and keeps every harmonic at 2.4 MHz and above. (The BQ25628's own PFM at
  light load likewise switched off in its registers, if it has the bit — to read.)
- **Each branch on its own regulator** (the owner, 24 Nov 2026): the core board on U22, our 3.3 V
  on U23, each petal's 1.8 V on its own LDO and choke behind U23 — so a cell of any chemistry, down to its floor,
  leaves every rail where it was set, and one branch's load never moves another's. **No ball
  package on our board** (the owner): the BQ25190 (WCSP only) gave way to the BQ25628 and two
  buck-boosts, all leaded or QFN.
- **The rails against the parts' windows** (the owner, 24 Nov 2026: margins for heat, and the
  LDO's headroom for its noise rejection — "the more you want cut, the more voltage across it"):

| rail | the part's window | what it gets | margin |
|---|---|---|---|
| converters' AVDD, 1.8 V mode (AREG shorted) | **1.70–1.90 V** (SBASA14A §5.3) | 1.80 V ± 1.5 % (its LDO), less ~15 mV in a choke: **1.76–1.81 V** | 60 mV low, 90 mV high |
| microphones' VDD (= MICBIAS = AVDD) | 1.62–3.6 V (SPH0641 Rev B) | 1.76–1.81 V | 140 mV low |
| converters' IOVDD, 3.3 V mode | 3.0–3.6 V | the core board's VDD_3V3 (RT9013-33 from 3.9 V) | ~0.3 V either way |
| each analog LDO's headroom | dropout ≤ 205 mV (1.5–2.5 V out); PSRR stated at VIN = VOUT + 1.0 V | **1.5 V** (3.3 → 1.8) | the PSRR as the sheet gives it |

  **The analog cannot go to 2.0 V:** the converter's 1.8 V mode ends at 1.90 V and its 3.3 V mode
  starts at 3.0 V — nothing between. So the margin is taken from the LDO's headroom instead:
  **The analog LDOs fed from U23's 3.3 V directly, the 2.2 V buck dropped** — 1.5 V across it, past the 1.0 V
  its PSRR (75 dB to 100 kHz, 40–45 dB at 1 MHz) is stated at; they cost ~(3.3 − 1.8) × 4 × 18 mA
  ≈ 0.11 W (27 mW each) against ~0.03 W through the buck, ~4 % of the tool.
- **Why 3.9 V into the core board** (the owner: keep margins for temperature): its RT9013-33 needs
  ~3.3 V plus its dropout (~0.25 V at 500 mA, more when hot) and its LCD module's own 3.3 V LDO the
  same; 3.9 V leaves ~0.35 V, every part on that net is rated to 5.5 V or more (TMI3113, RT9013,
  XC6206), and the display's backlight driver sees 3.9 V instead of 5. **The analog's LDO** is fed
  3.3 V, not a pre-regulated 2.2 V (the table below). **The converters' IOVDD and the clocks at 3.3 V** match
  the N6's own pins (VDD_3V3 on the core board); a lower rail there would cross the levels.
- **The budget** (`calc/power.py`): ~0.55 A from the cell at 3.7 V with a 4.3" display, ~0.86 A at
  3.0 V with a 7" — far inside the BQ25628's 6 A; U22 carries the core board's share (~0.35–0.5 A
  at 3.9 V) against its 2 A, U23 ours (the camera and the analog's ~72 mA).
- **Its I2C** on the core board's I2C2 (PD4/PD14) — **address 0x6A** (SLUSEG4C §8.5; the converters, now on the heads, on their own I2C); **INT** to **PE15** (EXTI 15)
  (J5); **QON** to the tool's power button (ship mode and wake).
- **The core board's VCC_5V (J5 pins 1–3) from U22 at 3.9 V.** Everything on the core board is made from
  VCC_5V by parts that run from a cell (Power.SchDoc): TMI3113 buck → VDDSMPS_1V8 (2.7–5.5 V,
  TOLL), RT9013-18/-33 → VDD_1V8 / VDD_3V3, XC6206P182/P332 → VDDA_1V8_AON / VDD_3V3_VDD. Fed a
  steady 3.9 V by U22, the two 3.3 V rails hold to the cell's floor (no longer following it down).
- **The converters' AVDD at 1.8 V** (SBASA14A: AVDD 1.8 V with AREG shorted to AVDD), so their
  analog and, through MICBIAS = AVDD, the microphones (1.62–3.6 V, their sheet measured at 1.8 V)
  stay steady to the cell's end. Each petal its own TPS7A2018 on U23's 3.3 V, then its own LC
  (`calc/supply.py`: −32 / −42 / −52 dB at 25 / 45 / 80 kHz). Load ~18 mA a petal (11.3 mA the
  converter, 8 × ~0.85 mA the microphones) — ~72 mA, ~15 mV in each choke.
- **The converters' IOVDD and the clocks at 3.3 V from the core board's VDD_3V3** (J5 pin 5) —
  the same rail as the N6's pins, so the levels match; the clock part behind L5.
- **Warnings, from the core board's schematic:**
  - **Its USB-C (J1 there) has VBUS wired straight to VCC_5V** (Devices.SchDoc) — in our build,
    **that port must not be plugged in**: it would push 5 V back into U22's output. Programming over SWD
    (J2 there: PA13, PA14) or with the cell removed; charging only at our J1.
  - **The display's backlight is fed VCC_5V** (its connector J4, pins 39–40) — so the cell's
    voltage. Whether Alientek's RGB LCD module lights from 3.0–4.2 V: **open**, its schematic.
  - **VBAT (J5)** goes to the N6's VBAT through a BAT54C with VDD_3V3; left open here (the cell's
    4.2 V is above VBAT's range).

## The camera

**A Raspberry Pi camera module with the OmniVision OV5647** (the owner, 24 Nov 2026: "vezmi to
běžné – stačí"): an old phone's 5 MP sensor, 2-lane MIPI CSI-2, one 3.3 V supply (its regulators on
the module), I2C address 0x36, VGA binned at up to ~90 fps — the display's 800 × 480 at 10–15 fps
is all it is asked for; a lens chosen to the array's field of view. Its init tables are open
(Linux's `ov5647.c`); the N6's ISP tuned for it by us.

**J7, a 15-pin, 1.0 mm FPC connector** — the Pi camera's own, so a stock module and its stock cable
plug in — **placed right beside J6** (the CSI pairs a few millimetres on our board, the flex
carrying them to the camera in the honeycomb's middle). Its pins, from the Raspberry Pi's
published pinout (raspberrypi.com, *Camera Module hardware*: the 15-pin table, CAM_IO0 "typically an
active-high power enable", **SCL and SDA pulled up to 3.3 V on the host** — so **2.2 kΩ to
VDD_CAM on SCL and SDA on our board**); a module draws **up to ~300 mA** at peak (Arducam's
OV5647 figure), inside `calc/surge.py`'s sweep:

| J7 | net |
|---|---|
| 1, 4, 7, 10 | GND (between the pairs) |
| 2, 3 | CSI_D0N, CSI_D0P (J6) |
| 5, 6 | CSI_D1N, CSI_D1P (J6) |
| 8, 9 | CSI_CKN, CSI_CKP (J6) |
| 11 | CAM_IO0, the module's enable — **PQ3** (J5) |
| 12 | CAM_IO1 (its LED or spare) — **PQ4** (J5) |
| 13, 14 | **I2C4: PE13 SCL, PE14 SDA** (J5, so labelled) |
| 15 | VDD_CAM, 3.3 V from U23, with the camera's C_P |

The pairs 100 Ω differential, short on our board, ground between them; **the flex to the camera a stock Pi camera cable of the length the case wants** (15 cm and longer are sold — the owner, 24 Nov 2026: the OV5647 on a longer flex; `WHY.md` 2). **The module as small as is sold** (the owner, 24 Nov 2026: in a small build, to fit the honeycomb's middle — the 5 cm hole of `calc/acam.py`): the Pi camera board's ~25 × 24 mm fits; the "spy" builds — sensor and lens on a module of ~9 × 9 mm at the end of their own flex — fit with room. Bought with its flex length and a ~90–120° lens. **PQ0, PQ1, PQ2 went to the base** (the communication module and the status LED; PQ5 to the knocker)
(the MB1854's ToF and IMU are gone).

## The heads' ports (25 Nov 2026)

The owner, 25 Nov 2026, after the afternoon's weighing (the working notes): **each head
sends its raw data on 8 lines of the N6's PSSI; two heads share it, H1 the low byte, H2 the high**;
every head on the Báze's one clock and its PPS; its commands on a UART of its own. The heads are
one board, plugged into either port; the ports differ only in where the Báze wires them.

**The PSSI, 16 lines, a receiving target** (DS14791 §3.28, Table 95: ≤ 100 MHz, setup 3.5 ns, hold
0.5 ns): PDCK **PD5** ← the Báze's clock (U11), so the data run on the master clock itself —
**24.576 MHz**. A head sends on its edge (the H723's PSSI: valid ≤ 10 ns, held ≥ 4.5 ns, DS13313
Table 100); the N6 latches **on the same edge one period later** (CKPOL set so): the data, out
≤ ~14 ns after the Báze's edge with the cable both ways, are taken at 40.7 ns — ~27 ns of setup,
~6 ns of hold. A frame (192 kHz) is 128 clocks: **128 byte-places a head**, 64 of them its 32
samples, the rest its frame number, its state and room (`../netopyr/schematic.md`, *The head*).

| PSSI | N6 pin (connector) | | PSSI | N6 pin (connector) |
|---|---|---|---|---|
| **H1** D0 | PD7 (J5-69) | | **H2** D8 | PE1 (J6-61) |
| D1 | PC6 (J6-63) | | D9 | PF0 (J6-54) |
| D2 | PE0 (J5-64) | | D10 | PB14 (J5-52) |
| D3 | PA4 (J6-23) | | D11 | PD9 (J6-62) |
| D4 | PE8 (J5-65) | | D12 | PD12 (J5-43) |
| D5 | PE5 (J5-70) | | D13 | PG7 (J6-65) |
| D6 | PB6 (J6-26) | | D14 | PD3 (J6-67) |
| D7 | PB7 (J5-62) | | D15 | PD11 (J5-35) |

- **A head missing reads zeros:** 100 kΩ to GND on each of the sixteen lines, at the Báze.
- **One head or two:** set at the start-up talk — the PSSI on 8 lines (H1 alone) or 16 (both);
  H2 alone on 16 lines, its low byte zeros.
- **Splitting the two heads' bytes:** the 32-bit word in memory is [H1 low, H2 low, H1 high, H2
  high]; the DMA's byte exchange (SBX on the STM32's GPDMA — to confirm in RM0486) makes it
  [H1's sample | H2's sample]; Helium's VLD2 parts the half-words into two streams as it loads
  them for the FFT.
- To make D9 and D13 free: **the communication module leaves UART9 (PF0, PF1)** for SPI2 (*The
  card, the communication module* below), and **button 4 moves from PG7** (the buttons since inductive, on I2C2, their interrupt on PG4).

**Per head:**

| | UART (TX → head, RX ← head) | NRST (open drain, 10 kΩ to 3.3 V) |
|---|---|---|
| **H1** | **USART1**: TX PF13 (J6-34), RX PF12 (J6-33) | PF15 (J6-36) |
| **H2** | **USART6**: TX PG14 (J5-53), RX PB8 (J5-63) | PF7 (J6-38) |

**The clock and the PPS** (`kuranty.md`) — **made by the N6, no crystal of our own, the SAIs and
the timers' clocks left alone** (the owner, 25 Nov 2026): **I2S3's MCK on PC7** (J6-64) — a kernel
PLL for audio, 24.576 MHz, independent of the core and of the PSSI → **U11** (LMK1C1108): H1, H2,
PD5 (the PSSI's PDCK), **PD0 (TIM1_ETR)**, a test point, through 33 Ω each. **PPS = TIM1_CH1 on
PE9**, TIM1 counting the clock itself (÷ 375 ÷ 65 536) → **U12** (LMK1C1104 **(m)**): H1, H2, a
test point.

**The head connector, H1 and H2 alike, 2 × 15, 1.27 mm, shrouded, keyed** (the owner, 25 Nov 2026:
the power together, a ground beside every signal; a flat cable ≤ ~15 cm, straight):

| pin | net | pin | net |
|---|---|---|---|
| 1 | +3V3 | 2 | +3V3 |
| 3 | +3V3 | 4 | +3V3 |
| 5 | CLOCK 24.576 MHz → | 6 | GND |
| 7 | PPS → | 8 | GND |
| 9 | D0 ← | 10 | GND |
| 11 | D1 ← | 12 | GND |
| 13 | D2 ← | 14 | GND |
| 15 | D3 ← | 16 | GND |
| 17 | D4 ← | 18 | GND |
| 19 | D5 ← | 20 | GND |
| 21 | D6 ← | 22 | GND |
| 23 | D7 ← | 24 | GND |
| 25 | UART head → Báze | 26 | GND |
| 27 | UART Báze → head | 28 | GND |
| 29 | NRST → | 30 | GND |

The power filtered where it enters each board — 10 µF + 0.1 µF at the connector on both ends, on
the head a ferrite bead (≥ 1 A) and from it a star to the H723 and the converters' LDOs — rather
than steering the return current; all thirteen grounds are one return. No ESD parts on these
connectors (the owner: plugged once, inside the box); ESD only where a hand or an outside cable
reaches (USB-C, the buttons, the knocker's output).

**No UART port left outside:** UART7 is the rangefinder's, USART2 the communication module's (*The
Báze's own sensors*, *The card, the communication module*); I2C1 (PH9, PE6) the SHT45's. **Q1, an I2C port** —
JST SH 4-pin, Qwiic's pinout (GND, 3V3, SDA, SCL): I2C2 PD4/PD14, shared with the charger, the
EEPROM and the touch controller. **The N6's four SAIs are free.**

## The lights — the display's backlight and the scene's four LEDs (24 Nov 2026)

The owner: one part for both, its own switching stage and inductor, the current held, dimmed by a
PWM it turns into a DC level — no chopped LED current, nothing to sing. **TI TPS61169DCKR**, LCSC
**C71045** (SC-70-5; a boost LED driver, 2.7–5.5 V in, 40 V 1.8 A switch, 1.2 MHz, its 204 mV
reference chopped by the CTRL pin's PWM and filtered — analog dimming, TI's sheet SNVSA40B: "eliminates
the audible noise"; CTRL low = off). **Two of them:**

| ref | job | nets |
|---|---|---|
| U30 | **the display's backlight** — a display **without its own backlight driver**, its LED string(s) on our board | VIN **SYS**; LED string to its FB; R_FB = 0.204 V / I_LED (e.g. 3 strings × 20 mA → 3.4 Ω); **CTRL from PD13, TIM4_CH2** |
| U31 | **the scene: four white LEDs in series** (~12 V), **60–90° beam**, around the camera on the front | VIN **SYS**; R_FB for ~100–150 mA (1.36–2.04 Ω, ~1.2–1.8 W at full); **CTRL from PF1, TIM4_CH3** (moved from PH9, 25 Nov 2026) |

Around each, from TI's sheet (SNVSA40B §7.2.2: L 4.7–10 µH, C_IN ≥ 1 µF, **C_OUT 1–10 µF**;
OVP 36–39 V; switch limit **1.2 A minimum**):
- **L: Sunlord SWPA4030S100MT, 10 µH, I_sat 2.4 A, 1.5 A rated, DCR 130 mΩ, 4 × 4 × 3 mm,
  shielded — LCSC C38117, extended** (the family of the petals' SWPA3015S330MT; no basic 10 µH
  power inductor found). Peak current at a 3.0 V cell: ~0.8 A for the scene's
  1.8 W, ~0.7 A for a 1.5 W backlight — under the 1.2 A minimum limit.
- **D: SS210, 100 V 2 A Schottky, SMA — LCSC C14996, basic** (MDD; 0.85 V at 2 A) — the sheet
  asks its reverse voltage above the open-LED protection (39 V); the SS34's 40 V is too close.
- **C_OUT: 2 × 10 µF 50 V X5R 1206, Samsung CL31A106KBHNNNE — LCSC C13585, basic** (Samsung's DC-bias curve: **3.7 µF each at 12 V, 1.4 at
  25 V**) — so ~7.4 µF on the scene's 12 V and ~2.8 µF on a 25 V backlight, against the sheet's
  1–10 µF and equation 6's ~1.9 µF for 50 mV of ripple (the owner: larger is welcome, within the
  sheet's 10); **no polymer here**: the sheet allows 10 µF at most for
  the loop, and the LED current being DC, a ceramic on this node has nothing in our band to sing.
- **C_IN: 10 µF 50 V (C13585, 8.7 µF at 4.2 V) at the VIN pin + the C_P** at the input (SYS's branch end).
- **No choke on the output:** an LC there would sit inside the current loop. **A ferrite bead
  and 100 nF at the display's connector** instead, for the cable's edges (tens of MHz); the
  1.2 MHz ripple is ~50 mV, invisible as light and far above the band.

**The PWM at 100 kHz** — the top of TI's 5–100 kHz, above the band; only a logic level, the LED
current itself DC. The four LEDs: **(m)**, a 3030/3535 white with a 60–90° lens, or a 120° part
behind a small reflector — to be found at JLCPCB.

## The card, the communication module, the reserve (24 Nov 2026)

The owner: a microSD; **no wired headphones and no mains antenna** — headphones by Bluetooth
through the communication module, the mains' period from the discharges themselves.

| block | part | nets |
|---|---|---|
| **microSD** — photos, settings, calibrations | push-push microSD socket **(m)**, 47 kΩ pull-ups on CMD and D0–D3, 100 nF + a 10 µF 50 V (C13585) at its 3.3 V | **SDMMC1** (the N6's own card controller, 4 bits — not SPI): CK **PC12**, CMD **PH2**, D0 **PC8**, D1 **PC9**, D2 **PC10**, D3 **PC11**; card detect **PC13**; 3.3 V from the core board's VDD_3V3 |
| **the communication module** — Wi-Fi to a phone, Bluetooth headphones | **Espressif ESP32-S31-WROOM-1** (PCB antenna at the case's edge; Wi-Fi 6 2.4 GHz, **classic Bluetooth (A2DP) and LE Audio**, 3.0–3.6 V; datasheet pre-release v0.5, 24 Nov 2026) — **pads also for an ESP32-MINI-1** (classic Bluetooth + Wi-Fi 2.4 GHz), one of the two fitted, as stock allows. Not a C5: the C5 has Bluetooth LE only, no A2DP and no LE Audio (ESP-IDF's BLE overview) | **SPI2 (the owner, 25 Nov 2026: "přes SPI") — ESP-Hosted's SPI: SCK PF2 (J5-29), MOSI PG8 (J5-27), MISO PD6 (J5-26), CS PC1 (J5-28); HANDSHAKE PF10 (J6-40, EXTI 10), DATA-READY PF14 (J6-35, EXTI 14); EN PQ0, BOOT PQ1** (each module's own strap pin, from its sheet); **and USART2 to its UART0** (TX PG3, RX PF6 — its loader and console; the owner, 25 Nov 2026); ~10–20 Mbit/s of Wi-Fi instead of a UART's few; 3.3 V from U23 with its C_P; in Rys off while it measures, on for Iljič's headphones |
| **reserve** | — | **every N6 pin left free brought to a row of pads** (a 2.54 mm header's footprint, unfitted) beside the core board — the owner, 24 Nov 2026: the board right the first time, a later wire a jumper and not a new order; **a status LED on PQ2** |

## The base — the same in NIC-Sluchalo (24 Nov 2026)

**The power is the base's whole** (the owner, 24 Nov 2026: one supply, one core board, one display,
one battery connector for both; only what is inside differs): the cell, BQ25628, U22 (3.9 V to
the core board), U23 (our 3.3 V), the C_P at each regulator, the USB-C, and U30 for the display.
**One battery connector for a 1S pack, sodium-ion** — the same charger and voltages, only the charge current set in the
BQ25628's register to the pack. **U23's load** (*25 Nov 2026: now two heads ~2 × 0.35 A, the camera, the module, the rangefinder — ~1.3 A at a peak; the budget redone in the check of that day, the working notes*): Datel ~0.3–0.5 A (the camera, the four petal LDOs,
the module); Rys ~1.1–1.5 A peak (eleven receivers mostly listening, the module off while
measuring) — within the TPS63020's 2 A at 3.3 V from a cell above 2.5 V (SLVS916I), ~75 % at
Rys's peak. **On sodium** (the reason the supply is a charger and two buck-boosts at all — 24 Nov 2026): the BQ25628 charges to 3.5–4.8 V (sodium's 3.65 or 3.90 V) and opens its BATFET
at 2.2 or 1.8 V; the TPS63020 runs from 1.8 V and gives its 2 A at 3.3 V from **above 2.5 V** —
sodium curve calls 2.5 V empty, so every rail holds to the end. **The pack is not chosen
now** (the owner, 24 Nov 2026: cells change by the half-year) — only its rough reach: on today's
sodium, ~4–4.5 Wh an 18650, Datel (~2 W) runs ~2 h and Rys (~5–6 W) ~0.8 h per such cell. **Inside, each its own:** Netopýr's head (behind its port: its H723, the petals' LDOs, chokes, PCMD3180s, microphones), J7, U31 and J8; Rys the receivers, Kuranty's buffers, Iljič, the amplifier and AS5600.

The owner, 24 Nov 2026: **both tools on the same board** — the CNN647B and the same base under it;
only what each tool hears is its own (here the petals and the camera, in NIC-Sluchalo the ten
receivers; Rys's schematic (not yet published)). The base, drawn once and used by both:

| block | what | N6 pins (connector) |
|---|---|---|
| power | BQ25628, U22 (3.9 V → J5 VCC_5V), U23 (our 3.3 V), the C_P scheme — the Power section above | I2C2 **PD4/PD14**, INT **PE15**, QON the power button |
| USB | our J1 USB-C **with its data**: D+/D− to the N6's **OTG1** (J5, near pin 19: OTG1_HSDM/HSDP — exact pins **(m)**), its VBUS to U20 and, through a divider, to OTG1_VBUS (level **(m)**); the core board's own USB-C (OTG2) never plugged | OTG1 |
| buttons | **eight, inductive** (the owner, 25 Nov 2026): **▲ ▼ ◄ ► and OK in the middle, ESC, MENU, the trigger** (on the side, under the forefinger) — a coil on the board under each, a thin metal plate in the case's wall pressed in by a few µm; no hole, gloves and water no matter; **two TI LDC2114 (m)**, four channels each, I2C, their addresses set apart by a pin **(m)**; on the core board's 3.3 V | **I2C2** PD4/PD14; **INTB → PG4** (J6-42, EXTI 4) and **PG6** (J6-41, EXTI 6), side by side |
| the power button | **a Hall switch, TI DRV5032ZEDBZR** (~1.6 µA, open drain), fed from the cell, **a magnet in a sprung button** in the wall — sealed too; its output to the BQ25628's **QON** (wakes it from ship mode) and, through 10 kΩ, to **PG5** (J6-71, EXTI 5 — five-volt tolerance to confirm) to tell a short press from a long | QON, PG5 |
| programming | the core board's own SWD (its J2: PA13, PA14, NRST) | — |
| microSD | SDMMC1, as above — the same in both tools | PC8–PC12, PH2, PC13 |
| communication module | as above — the same in both tools | SPI2 PF2/PG8/PD6/PC1, PF10, PF14, PQ0, PQ1 |
| status LED | — | PQ2 |
| display | on the core board's RGB LCD connector (J4 there), fed VCC_5V = 3.9 V; no touch layer (the owner's thought) | LTDC, on the core board |
| display's backlight | **U30, TPS61169** (The lights, above) — part of the base, the same display in both tools | PWM **PD13** (TIM4_CH2) |

## The Báze's own sensors (25 Nov 2026)

The owner, 25 Nov 2026: the air's temperature and humidity ("teplota s vlhkostí je super") and a
**laser rangefinder with a red dot, a small module with its own optics, mounted in the chassis**.

| ref | part | nets |
|---|---|---|
| U40 | **SHT45 in a probe on a cable** (the owner, 25 Nov 2026: "šulín", screwed in, a cable) — a threaded probe body (M8 or M12 **(m)**) through the case's wall, the sensor out in the air; the **SHT45-AD1F** (its PTFE membrane against dust and water) **(m)**; ±0.1 °C, ±1 % RH | **J9**, JST SH 4-pin on the Báze (3V3, GND, SDA, SCL) → **I2C1**: SCL **PH9** (J5-72), SDA **PE6** (J5-71), 2.2 kΩ pull-ups, **100 kHz** (a cable up to ~1 m); for the air's absorption of ultrasound (`../netopyr/calc/air.py`) |
| U41 | **Benewake TF40** (chosen 25 Nov 2026; its datasheet named) — a visible red laser, 0.04–40 m (90 % reflectivity), accuracy ±2 mm, resolution 1 mm, **3.3 V supply, UART at 3.3 V** (9600 baud by default) — figures from its datasheet as quoted, size and current to read from the sheet itself; the fallback a JRT module (635 nm, < 1 mW, 0.03–40 m, TTL, 49 × 25 × 13 mm) | **UART7**: TX **PH3** (J6-57), RX **PG11** (J6-53); its supply through a load switch (U46), EN from **PD1** (J6-56), off until wanted |
| U42 | **ST LSM6DSV16X (m)** — accelerometer and gyroscope; its own orientation (SFLP), its finite-state machine and machine-learning core; **two programmable interrupts** (wake, still, tilt, tap, fall, an FSM/MLC result) that wake the N6 from Stop; on the core board's 3.3 V, alive while the N6 sleeps; rigid on the board near its middle | **SPI5**: SCK **PH5** (J6-32), MOSI **PH7** (J5-30), MISO **PH8** (J5-31), CS **PH6** (J5-32); **INT1 → PB2** (J5-36, EXTI 2), **INT2 → PE3** (J5-38, EXTI 3) — the group together on J5 |
| U43 | **InfiRay Tiny1-C** (the owner, 25 Nov 2026) — a thermal camera core, **256 × 192**, ~25 frames/s, a lens of ~56° to match the camera (OV5647 ~54 × 41°); **above the propeller**, beside the rangefinder, its axis parallel to the camera's; behind a **germanium window** (or an open hole — glass and plastics are opaque to it); figures from memory, its sheet to read | **USB, the N6's OTG2 as a host (UVC)**: D− **OTG2_HSDM (J5-13)**, D+ **OTG2_HSDP (J5-14)** — the core board's own USB-C on OTG2 never plugged; its supply through a load switch **U47 (TPS22918 (m))**, EN **PE12** (J5-44) — **if it wants 5 V** (its sheet), a small boost **(m)** behind the switch, there being no 5 V on the Báze |

- **Its optics** (`konstrukce/valenki.md`): two openings in the mask before its two lenses, a
  baffle between them (else the window's reflection blinds the receiver), or none of glass at
  all; its axis parallel to the camera's and close to it, screwed to the face; the dot seen in the
  picture calibrates the offset once.
- The UART port U1 is the module's now; no free UART left outside.
- **The thermal camera's picture is laid on the camera's** — the parallax of a few cm taken out by
  the rangefinder's distance; its firmware a USB host with a UVC class on the N6 (ST's USBX).

## Switching the power — sleep, self-off, off (25 Nov 2026)

The owner, 25 Nov 2026: a self-off and a whole off, the regulators and the switches under the
N6's hand for the current's sake.

| what | how it is switched | N6 pin (connector) |
|---|---|---|
| **U23**, our 3.3 V (the camera, the module, the rangefinder, the probe, the heads' feed) | its EN (TPS63020): 100 kΩ to SYS — on at power-up — pulled low by the N6 (open drain) to switch it off | **PF11** (J6-31) |
| **head H1's +3V3** (pins 1–4) | a load switch **U44, TI TPS22918 (m)**, off by a pull-down until the N6 lets the head up | **PQ7** (J5-55) |
| **head H2's +3V3** | **U45, TPS22918 (m)** | **PQ6** (J5-56) — beside H1's |
| the rangefinder U41 | **U46, TPS22918 (m)** | PD1 (J6-56) |
| the communication module | its EN | PQ0 (as before) |
| the camera | its enable | PQ3/PQ4 (as before) |
| the display's backlight | U30's EN/PWM | PD13 (as before) |
| **the whole tool** | **the BQ25628's ship mode** by I2C — its BATFET opens, the cell's drain ~µA; left by the power button (QON) or the charger's plug | I2C2 |

- **Alive while the N6 sleeps** — on the core board's own 3.3 V, not on U23: the IMU (U42), the
  buttons' LDC2114s, the power button's Hall switch (on the cell itself).
- **Sleep = the N6's Stop** (its RAM kept): woken by any EXTI — the IMU's INT1/INT2, the buttons'
  INTBs, the power button. (Standby is not used: the module brings out one wake-up pin, PC13, the
  card's detect.)
- **Self-off, in steps:** the IMU reports stillness and no button for N minutes → the backlight
  off → U23 and the heads off, the N6 in Stop → after M more minutes **ship mode** — off; on again
  only by the power button or the charger. A long press of the power button: the data saved, then
  ship mode.

## The audio microphone (25 Nov 2026)

The owner, 25 Nov 2026: one audio microphone for every tool, on the Báze, through **ADF1** — the
N6's filter made for one PDM microphone, with its sound-activity detector (a wake on a voice or a
sound at little current).

| ref | part | nets |
|---|---|---|
| MK1 | **Infineon IM69D130** (PDM; 28 Hz low roll-off, response to 15 kHz in its Table 2, measured 20 Hz – 20 kHz; 69 dB(A); sheet v1.0), its hole anywhere in the case | CLOCK ← **ADF1_CCK0 PE2** (J5-39), DATA → **ADF1_SDI0 PB0** (J5-37), SELECT to GND, VDD +3V3 with 0.1 µF |

Its clock 3.072 MHz (≤ 3.3 MHz, its normal mode 2.9–3.3) from the ADF's kernel clock — the same
audio PLL as the heads' 24.576 MHz (÷ 8), so it is in step with them (`kuranty.md`).

## J5 and J6, pin by pin (24 Nov 2026)

**25 Nov 2026:** the Báze column follows *The heads' ports* above (the PSSI, the heads' UARTs and
NRSTs, the clock out on PC7 (I2S3_MCK), the PPS, the module on SPI2, the buttons' interrupts on PG4/PG6, the IMU on SPI5, the power switches).

Read from the CNN647B schematic's connector page (Pinout.SchDoc: each net label beside its pin's
designator, J5 and J6 two rows of 40, pin 1 facing 80). Both tools on the one footprint: the
Báze column for the Báze with Netopýr's heads, the Rys column for Rys; "pad" is a spare N6 pin to the
row of pads. **PA3, PB3, PD8, PD10** reach the core board's LCD connector too (TIM16_CH1 and the
touch panel's PEN, MISO, CS) and are left alone; **PH8** is an ordinary pin (BOOT0 has its own,
J5-50). The power pins: J5-1…3 VCC_5V (U22's 3.9 V), J5-4 VDD_1V8 and J5-5 VDD_3V3 (outputs of
the core board), J5-6 VREFP, J5-7 VBAT, the GND pins between the pairs.

| pin | net / N6 | Báze (with Netopýr's heads) | Rys |
|---|---|---|---|
| J5-1 | VCC_5V | U22 3.9 V | U22 3.9 V |
| J5-2 | VCC_5V | U22 3.9 V | U22 3.9 V |
| J5-3 | VCC_5V | U22 3.9 V | U22 3.9 V |
| J5-4 | VDD_1V8 | — | — |
| J5-5 | VDD_3V3 | the core board's 3.3 V: IOVDD, clocks, SD | the core board's 3.3 V: SD, AS5600 |
| J5-6 | VREFP | — | — |
| J5-7 | VBAT | — | — |
| J5-8 | NLED_EN | — | — |
| J5-9 | PWR_ON | — | — |
| J5-10 | NRST_EX | — | — |
| J5-11 | NRST | — | — |
| J5-12 | GND | GND | GND |
| J5-13 | OTG2_HSDM | USB D− → U43 (Tiny1-C), host — **the core board's own USB-C (also on OTG2) never to be plugged** | — (core board USB-C, never plugged) |
| J5-14 | OTG2_HSDP | USB D+ → U43, host | — (core board USB-C, never plugged) |
| J5-15 | GND | GND | GND |
| J5-16 | OTG2_VBUS | — (OTG2 a host; the core board's USB-C never plugged) | — (core board USB-C) |
| J5-17 | OTG2_ID | — | — |
| J5-18 | GND | GND | GND |
| J5-19 | OTG1_HSDM | USB D− | USB D− |
| J5-20 | OTG1_HSDP | USB D+ | USB D+ |
| J5-21 | GND | GND | GND |
| J5-22 | OTG1_VBUS | USB VBUS sense (divider) | USB VBUS sense (divider) |
| J5-23 | OTG1_ID | — | — |
| J5-24 | UCPD1_CC2 | — | — |
| J5-25 | UCPD1_CC1 | — | — |
| J5-26 | PD6 | ESP SPI2 MISO | pad |
| J5-27 | PG8 | ESP SPI2 MOSI | pad |
| J5-28 | PC1 | ESP SPI2 CS | CS M7 |
| J5-29 | PF2 | ESP SPI2 SCK | SPI2 SCK |
| J5-30 | PH7 | SPI5 MOSI → U42 | SPI5 MOSI |
| J5-31 | PH8 | SPI5 MISO ← U42 | pad |
| J5-32 | PH6 | SPI5 CS → U42 | pad |
| J5-33 | PE15 | BQ25628 INT | BQ25628 INT |
| J5-34 | PD13 | backlight PWM (TIM4_CH2) | RDY M8 |
| J5-35 | PD11 | H2 PSSI D15 | SPI2 MISO |
| J5-36 | PB2 | U42 INT1 (EXTI 2) | SAI1 SD_A → MAX98357A |
| J5-37 | PB0 | ADF1_SDI0 ← MK1 | SAI1 FS_A |
| J5-38 | PE3 | U42 INT2 (EXTI 3) | CS M1 |
| J5-39 | PE2 | ADF1_CCK0 → MK1 (the audio microphone) | SPI4 SCK |
| J5-40 | PC2 | pad (SAI1 SCK_A — the clock's fallback) | SAI1 SCK_A |
| J5-41 | PD14 | I2C2 SCL (+ Q1) | I2C2 SCL |
| J5-42 | PD4 | I2C2 SDA (+ Q1) | I2C2 SDA |
| J5-43 | PD12 | H2 PSSI D12 | RDY M7 |
| J5-44 | PE12 | U43's power switch EN (U47) | pad |
| J5-45 | PE11 | pad | RDY M6 |
| J5-46 | PE14 | I2C4 SDA (camera) | CS PGA |
| J5-47 | PE13 | I2C4 SCL (camera) | pad |
| J5-48 | PG10 | — (core board LED0) | — (core board LED0) |
| J5-49 | PA6 | — (BOOT1) | spare SPI6 MISO (BOOT1) |
| J5-50 | BOOT0 | — (core board) | — (core board) |
| J5-51 | PQ0 | COMM EN | COMM EN |
| J5-52 | PB14 | H2 PSSI D10 | CS M6 |
| J5-53 | PG14 | H2 USART6 TX | spare SPI6 MOSI |
| J5-54 | PB13 | pad | spare SPI6 SCK |
| J5-55 | PQ7 | H1 power switch EN (U44) | pad |
| J5-56 | PQ6 | H2 power switch EN (U45) | pad |
| J5-57 | PQ5 | KNOCK (TIM8_CH2) | pad |
| J5-58 | PQ4 | CAM_IO1 | BOOT-P |
| J5-59 | PQ3 | CAM_IO0 | EN-RX (Q1 gate) |
| J5-60 | PQ2 | status LED | status LED |
| J5-61 | PQ1 | COMM BOOT | COMM BOOT |
| J5-62 | PB7 | H1 PSSI D7 | SPI4 MOSI |
| J5-63 | PB8 | H2 USART6 RX | RDY M3 |
| J5-64 | PE0 | H1 PSSI D2 | CS M5 |
| J5-65 | PE8 | H1 PSSI D4 | Serp TX (USART3) |
| J5-66 | PB9 | pad | CS M4 |
| J5-67 | PD5 | PSSI PDCK ← U11 (the clock) | Mužíci TX (USART2, broadcast) |
| J5-68 | PD0 | TIM1_ETR ← U11 (the clock, counted for the PPS) | Molot RX (UART4) |
| J5-69 | PD7 | H1 PSSI D0 | SPI2 MOSI |
| J5-70 | PE5 | H1 PSSI D5 | CS M3 |
| J5-71 | PE6 | I2C1 SDA ↔ U40 (SHT45) | pad |
| J5-72 | PH9 | I2C1 SCL → U40 (SHT45) | RDY M4 |
| J5-73 | PC12 | SD CK | SD CK |
| J5-74 | PC11 | SD D3 | SD D3 |
| J5-75 | PC10 | SD D2 | SD D2 |
| J5-76 | PC8 | SD D0 | SD D0 |
| J5-77 | PC9 | SD D1 | SD D1 |
| J5-78 | PH2 | SD CMD | SD CMD |
| J5-79 | GND | GND | GND |
| J5-80 | GND | GND | GND |
| J6-1 | PN7 | — (XSPI, core board) | — (XSPI, core board) |
| J6-2 | PN12 | — (XSPI, core board) | — (XSPI, core board) |
| J6-3 | PO1 | — (XSPI, core board) | — (XSPI, core board) |
| J6-4 | PO3 | — (XSPI, core board) | — (XSPI, core board) |
| J6-5 | PP8 | — (XSPI, core board) | — (XSPI, core board) |
| J6-6 | PP9 | — (XSPI, core board) | — (XSPI, core board) |
| J6-7 | LTDC_R2 = PB5 | display (core board) | display (core board) |
| J6-8 | LTDC_R3 = PB4 | display (core board) | display (core board) |
| J6-9 | LTDC_R5 = PA15 | display (core board) | display (core board) |
| J6-10 | LTDC_R6 = PF8 | display (core board) | display (core board) |
| J6-11 | LTDC_R7 = PG9 | display (core board) | display (core board) |
| J6-12 | LTDC_G2 = PA1 | display (core board) | display (core board) |
| J6-13 | LTDC_G3 = PA0 | display (core board) | display (core board) |
| J6-14 | LTDC_G5 = PB12 | display (core board) | display (core board) |
| J6-15 | LTDC_G6 = PB11 | display (core board) | display (core board) |
| J6-16 | LTDC_G7 = PB10 | display (core board) | display (core board) |
| J6-17 | LTDC_B2 = PA12 | display (core board) | display (core board) |
| J6-18 | LTDC_B3 = PA11 | display (core board) | display (core board) |
| J6-19 | LTDC_B4 = PA10 | display (core board) | display (core board) |
| J6-20 | LTDC_B5 = PA9 | display (core board) | display (core board) |
| J6-21 | LTDC_B6 = PA8 | display (core board) | display (core board) |
| J6-22 | LTDC_B7 = PA2 | display (core board) | display (core board) |
| J6-23 | PA4 | H1 PSSI D3 | CS M2 |
| J6-24 | LTDC_CLK = PA5 | display (core board) | display (core board) |
| J6-25 | LTDC_DE = PG13 | display (core board) | display (core board) |
| J6-26 | PB6 | H1 PSSI D6 | SPI4 MISO |
| J6-27 | TP_CS = PD10 | — (core board LCD) | — (core board LCD) |
| J6-28 | TP_MISO = PD8 | — (core board LCD) | — (core board LCD) |
| J6-29 | TP_PEN = PB3 | — (core board LCD) | — (core board LCD) |
| J6-30 | TIM16_CH1 = PA3 | — (core board LCD) | — (core board LCD) |
| J6-31 | PF11 | U23 EN (open drain) | MAX98357A SD_MODE |
| J6-32 | PH5 | SPI5 SCK → U42 (IMU) | SPI5 SCK |
| J6-33 | PF12 | H1 USART1 RX | SPI5 MISO |
| J6-34 | PF13 | H1 USART1 TX | pad |
| J6-35 | PF14 | ESP DATA-READY | RDY M9 |
| J6-36 | PF15 | H1 NRST | pad |
| J6-37 | PF5 | pad | Iljič gain 1 |
| J6-38 | PF7 | H2 NRST | Iljič gain 2 |
| J6-39 | PF4 | pad | Iljič ADC1_INP18 |
| J6-40 | PF10 | ESP HANDSHAKE | Iljič ×1/×10 |
| J6-41 | PG6 | LDC2114 #2 INTB (EXTI 6) | button 3 |
| J6-42 | PG4 | LDC2114 #1 INTB (EXTI 4) | button 1 |
| J6-43 | GND | GND | GND |
| J6-44 | CSI_CKN | J7 CSI |  |
| J6-45 | CSI_CKP | J7 CSI |  |
| J6-46 | GND | GND | GND |
| J6-47 | CSI_D1N | J7 CSI |  |
| J6-48 | CSI_D1P | J7 CSI |  |
| J6-49 | GND | GND | GND |
| J6-50 | CSI_D0N | J7 CSI |  |
| J6-51 | CSI_D0P | J7 CSI |  |
| J6-52 | GND | GND | GND |
| J6-53 | PG11 | UART7 RX ← U41 | pad |
| J6-54 | PF0 | H2 PSSI D9 | COMM TX (UART9) |
| J6-55 | PF1 | scene LEDs PWM (TIM4_CH3) | COMM RX (UART9) |
| J6-56 | PD1 | U41 power switch EN (U46) | Molot TX (UART4) |
| J6-57 | PH3 | UART7 TX → U41 (the rangefinder) | pad |
| J6-58 | PE7 | pad | pad |
| J6-59 | PE9 | PPS (TIM1_CH1) → U12 | Kuranty (TIM1_CH1) |
| J6-60 | PE10 | pad | RDY M5 |
| J6-61 | PE1 | H2 PSSI D8 | RDY M1 |
| J6-62 | PD9 | H2 PSSI D11 | Serp RX (USART3) |
| J6-63 | PC6 | H1 PSSI D1 | CS M8 |
| J6-64 | PC7 | the clock out (I2S3_MCK) → U11 | pad |
| J6-65 | PG7 | H2 PSSI D13 | button 4 |
| J6-66 | PD15 | pad | CS M9 |
| J6-67 | PD3 | H2 PSSI D14 | RDY M2 |
| J6-68 | PG3 | ESP USART2 TX (its UART0: loader, console) | pad |
| J6-69 | PF6 | ESP USART2 RX | Mužíci RX (USART2) |
| J6-70 | PF3 | pad | pad |
| J6-71 | PG5 | the power button (Hall), its press (EXTI 5) | button 2 |
| J6-72 | PC13 | SD detect | SD detect |
| J6-73 | PA14 | SWD (core board) | SWD (core board) |
| J6-74 | PA13 | SWD (core board) | SWD (core board) |
| J6-75 | PP10 | — (XSPI, core board) | — (XSPI, core board) |
| J6-76 | PP14 | — (XSPI, core board) | — (XSPI, core board) |
| J6-77 | PP13 | — (XSPI, core board) | — (XSPI, core board) |
| J6-78 | PP12 | — (XSPI, core board) | — (XSPI, core board) |
| J6-79 | PP11 | — (XSPI, core board) | — (XSPI, core board) |
| J6-80 | PP15 | — (XSPI, core board) | — (XSPI, core board) |

## Open before drawing

- The mating connector of J5/J6 (the owner has an idea).
- The display: **up to 7"** (the owner, 24 Nov 2026), an Alientek-pinout RGB module on the core board's J4 **whose backlight LEDs come out to our U30** (no driver of its own) — 7" at 1024 × 600 stays under the LTDC's XGA; its backlight at the core board's feed voltage, one module on the bench.
- The scene's four LEDs; a display whose backlight comes out bare; the TF40's sheet; the LDC2114's, LSM6DSV16X's, TPS22918's, DRV5032's sheets; RTC across ship mode (a coin cell or a supercapacitor on VBAT, or the time from the phone).
- **The owner's thoughts of 24 Nov 2026, waiting for his word**: four LEDs, DC-driven; the
  knocker (piezo rod, solenoid, voice-coil exciter or the person's hammer); the buttons' kind.
