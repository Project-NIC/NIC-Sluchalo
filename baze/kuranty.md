# Kuranty — every clock of the Báze and its heads

*25 Nov 2026 (the owner: "kuranty můžou být v bázi… kompletní soupis všech hodin, nejvíc je
vytváří báze").* The time's whole chain, from the one oscillator to the last converter.

## The one clock

| clock | where it is made | goes to | why |
|---|---|---|---|
| **24.576 MHz** | **the N6, no crystal of our own** (the owner, 25 Nov 2026): **I2S3's master clock (MCK) on PC7**, straight from a kernel PLL kept for audio — **independent of the core** (the N6 may run at any speed, or be slowed) **and of the PSSI** (off for a head on its UART only, the clock still runs); SPI3/I2S3 otherwise unused, its data pins left unassigned → U11 | H1, H2 (pin 5 — the heads' OSC_IN), the N6's PSSI PDCK (PD5), the N6's TIM1_ETR (PD0) | one clock for all, the PLL's output divided down |
| **PPS, 1 Hz** | the N6's **TIM1 counting that clock itself** on its ETR (PD0): 24 576 000 counts (÷ 375 ÷ 65 536), out on TIM1_CH1 **PE9** → U12 | H1, H2 (pin 7) | the epoch, every head's frame 0; independent of the core too; every second or more rarely |

## On each head (`../netopyr/schematic.md`)

| clock | made from | goes to |
|---|---|---|
| **HSE 24.576 MHz** | the cable's clock → U11 → OSC_IN (PH0), bypass | the H723's PLL: the core ~98.3 MHz (up to 546.8) |
| **PDCK 24.576 MHz** | the cable's clock → U11 → PA6 | the head's PSSI: its data on the master clock |
| **BCLK 24.576 MHz** | **MCO1 (PA8)** — the HSE passed out → U12 | U1–U4, SAI1/SAI4 SCK |
| **FSYNC 192 kHz** | **TIM2** (÷ 128, reset by the PPS on PA1), out on PA5 → U13 | U1–U4, SAI1/SAI4 FS |
| **PDM 3.072 MHz** | inside each PCMD3180 (BCLK ÷ 8) | its eight microphones |


## The rest of the Báze

| clock | where | note |
|---|---|---|
| **3.072 MHz** to the audio microphone | the N6's **ADF1_CCK0 (PE2)**, from the same audio PLL as the 24.576 MHz (÷ 8) | MK1, the IM69D130 — in step with the heads |
| the N6's own | the CNN647B's 48 MHz crystal (HSE) and 32.768 kHz (LSE) — the module's, its pins not on J5/J6 | its core (any speed), its NPU, its buses; the audio clock from a kernel PLL of its own |
| the ESP's own | on its module | Wi-Fi, Bluetooth |
| the camera's own | on the Pi camera module | its pixel clock; CSI-2's lanes |
| UARTs, SPIs | the N6's PLLs | asynchronous to the audio — the UARTs within ±2 % of their rates |

## Why it holds together

- Every sample of every microphone on every head is taken on an edge of the **one** 24.576 MHz:
  the heads differ only by their wiring's few ns (0.01° at 40 kHz) — constant, calibrated away.
- The PPS starts both heads' FSYNC within a timer tick (~10 ns, the head's TIM2 at 98.3 MHz — 512 ticks a frame); between PPS they cannot drift,
  being counted from the same clock.
- **To see on the bench:** each head's FSYNC against its BCLK (a timer's edge against MCO's).
