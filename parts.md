# NIC-Sluchalo — the parts

The types, packages and processors, each with the requirement it meets. No pin assignments yet.
Bought, ready-made and certified wherever there is a choice (the owner: "všechno z koupených
dílů"). Where a figure is marked **to confirm**, it is named from what is known and is checked
against its maker's datasheet before the part is bought.

## Rys — the receivers and their antennas

| part | type | how many | meets |
|---|---|---|---|
| receiver (a Mužík; two in Předseda) | **Espressif ESP32-C5-WROOM-1U** — the module with a U.FL connector and its own 48 MHz crystal; N4 (4 MB flash) or N8R8 (8 MB flash, 8 MB PSRAM, unused) as stock allows. 18.0 × 21.2 × 3.3 mm, castellated pins; EN, GPIO28, GPIO27, UART0 and an SPI slave brought out (datasheet v1.3, Table 3-2) — **the Mužíci report on three SPI buses, three to a bus, each with its chip select (which is also its boot strap) and a ready line; Serp and Molot on a UART each**; one reset for all | 10 | CSI on 2.4 and 5 GHz (esp-csi lists the C5); a certified radio, nothing opened — Espressif's EU technical conformity document for the WROOM-1U (RED: safety, health, EMC, radio — EN 300 328, EN 301 893, EN 300 440, all passed; tested with a PCB antenna as its accessory), with FCC (5 GHz), ISED, KCC and MIC beside it; every line of a receiver's interface |
| antenna (a Kosa; Serp and Molot) | **Ezurio dual-band FlexPIFA 001-0016** — 2400–2480 and 4900–5900 MHz, linear, 38.5 × 12.7 × 2.5 mm, U.FL, 100 mm cable (160–250 mm variants) | 10 | dual-band; made to sit over metal (Front's disc); linear, so the picture's directions hold |

## Rys — Gensek and the units round it

| part | type | meets |
|---|---|---|
| Gensek | **ST STM32N647** (Cortex-M55 at 800 MHz with Helium, an NPU, 4.2 MB SRAM; six SPI, ten U(S)ARTs, SDMMC, USB, two 12-bit ADCs; no op-amps) on **Alientek's ATK-CNN647B core board** (45 × 32 mm, its own memories and supplies, two 80-pin connectors) — the same core board as Datel's, on the same base: power, display, card, USB, buttons | the eleven receivers' reports on three SPI buses and two UARTs; the picture's arithmetic with room to spare; the recognition left on 13 Nov within reach of the NPU |
| Pravda | an **RGB TFT up to 7″** on the core board's display connector, no touch, behind a plastic window; **buttons**; the backlight fed by a TI TPS61169 whose PWM input it turns into a DC current, dark while the head turns | its own display, no phone; the display is the largest single load (`body.py`) |
| Matjugalnik | **Analog Devices (Maxim) MAX98357A** on the processor's SAI, and **Bluetooth headphones** through the communication module while Iljič measures — — a class-D amplifier fed digitally by I2S from the processor, no DAC between; a small speaker; tone and loudness in software; off while Iljič measures, its switching lying in Iljič's band; 2.5–5.5 V, 3.2 W into 4 Ω at 5 V, 2.4 mA quiescent (Analog Devices); fed from the cells, somewhat less | a sound worth listening to all day |
| Kádrovák | a **microSD card** on the SDMMC | every picture with its raw data, ~5 MB a turn |
| Samizdat | **USB-C** on the base, to the processor's own USB | pictures out, programs in |
| Razvedčik | **ams AS5600** on a ready-made board, a diametric magnet in Kuří nožka: 12 bits, ±1° from the best line over a turn, 0.015° rms noise (datasheet v1-06); a 3.3 V supply mode by its own LDO, the range **to confirm** in its electrical table | the head's angle to about a degree — ±1° is the bound, and a fixed curve can be measured once and taken out |
| Iljič | a **plate in Front's insulating face** into **TI TLV9062** (the dual of NIC-Heimdall's TLV9061; CMOS input, rail to rail, 1.8–5.5 V, 10 MHz, ~0.5 mA a section, input bias ~0.5 pA — distributors' figures, TI's SBOS839 to confirm): one half a **charge amplifier with its feedback switched, 100 / 10 / 1 pF**, the other a **second stage of ×1 or ×10**, then **the processor's own op-amp as a programmable gain** — ×1 as a follower, ×2/4/8/16, inverting −1/−3/−7/−15 (STM32H7A3 OPAMP; its bandwidth to read in DS13195), then its ADC; the gain set so that the signal fills half to four-fifths of the ADC (Iljič is a mode of its own, held like a tester — `WHY.md` 16); an LED by the plate shows where it senses; several tracers' frequencies picked out at once in software; a narrow filter in software for the rest | `calc/iljic_amp.py`: the plate's charge gives 0.2 mV to 0.7 V at 10 pF — 70 dB — so the gain is switched; with these steps eight of the nine cases fill 44–80 % of a 1.8 V ADC, mains through a damp wall 21 % at the most gain; the charge amplifier's noise gain is 3 at 10 pF, 21 at 1 pF, so 10 MHz holds it to 3 MHz and 0.5 MHz — ample at 125 kHz. The LTC6268 Heimdall uses (16.5 mA a section) was left for this: ~30 times less current The N6 has no op-amps, so the fine gain is a **Microchip MCP6S21** PGA (1–32, SPI) after the ×1/×10 stage, into the N6's 12-bit ADC with its hardware oversampling. |
| Kuranty | one timer edge from Gensek fanned out by **two TI LMK1C1108** clock buffers to every receiver, caught by each C5's timer through ETM (ESP-IDF, *ETM*, *GPTimer*) | one time base, all receivers within nanoseconds |
| Pajok | **a 1S sodium-ion pack** (its size not chosen yet — cells change by the half-year), **TI BQ25628** charger on USB-C, **two TI TPS63020 buck-boosts** in forced PWM — one for the core board, one for the receivers and the rest; the same supply as Datel's | ~5–6 W; ~0.8 h per sodium 18650 of today |
| the communication module | **Espressif ESP32-S31-WROOM-1** (Wi-Fi 2.4 GHz, classic Bluetooth and LE Audio; an ESP32-MINI-1 as the fallback) — off while Rys measures | pictures to a phone; Bluetooth headphones for Iljič (the C5 has Bluetooth LE only) |
| Karanténa | **no part**: Felčar is firmware | — |

## Iskra — the sender

| part | type | how many | meets |
|---|---|---|---|
| sender | **ESP32-C5-WROOM-1U**, as in Rys — one upright, one level, taking turns; one leads the hops (channels 1, 36, 165) | 2 | two polarizations; frames Rys can name; licence-free bands |
| antenna | **Ezurio dual-band FlexPIFA 001-0016** on a small aluminium plate, one upright, one level | 2 | the same antenna as Rys's; EIRP capped in software below 20 dBm with its gain counted |
| power | a **USB power bank** | 1 | a box with nothing to build |

## Levša — the construction

| part | type | meets |
|---|---|---|
| Front's disc | **aluminium, at least 3 mm** (threads for the screws), about 177 mm across, drilled for the cables (3–4 mm, beside each antenna) and for Kuří nožka | the antennas' ground and the shield; the frame everything is screwed to |
| Front's face | **polycarbonate 2 mm** (the maker recommends 1.5 mm over metal; 2 mm sheet is easier to get) | the antennas' spacer over metal |
| Kuří nožka | a **rod with a rubber foot**, its **bearing** in the disc, a **friction clutch**, the **magnet** for Razvedčik | the axis; stands firm on the wall; a turn by hand without slipping |
| felt | **hard, smooth, synthetic felt** ~5 mm where the head may brush the wall | slides on paint, marks nothing; synthetic, since damp wool is lossy at 2.4 GHz — the microwave test first |
| housing | to be drawn | — |

## For the trials, before the head

| part | type | for |
|---|---|---|
| receiver and sender | **Seeed XIAO ESP32-C5** (bare chip, own crystal, U.FL) | the wall trials |
| antennas | the same FlexPIFA, on an aluminium plate | the trials as the head will see them |

## Open

- **The prices and stock** of every part, at ordering (WROOM-1U-N8R8: $7.93 at Mouser, $4.19 at LCSC
  when in stock, 14 Nov 2026).
- The AS5600's supply range at 3.3 V, in its electrical table.
- **Memory**: the picture in four groups of subcarriers, or memory on the FMC beside the display.
