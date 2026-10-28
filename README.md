<p align="center">
  <img src="NIC-Sluchalo.jpg" width="300" alt="Sluchalo"/>
</p>

★ N.I.C. ★

# NIC-Sluchalo

**English** · [Čeština](README.cs.md) · [Русский](README.ru.md)

**What is in a wall, seen by the shadow Wi-Fi casts through it. A hand-held head with eleven
Wi-Fi receivers slides along one face of the wall; a small box on the other side sends. A cable,
a pipe or a steel stud between them dims the field, and the head maps where. For masonry it also
taps the wall and listens. Every setting and all the raw data stay open to whoever uses it.**

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![License: CERN-OHL-P v2](https://img.shields.io/badge/License-CERN--OHL--P%20v2-red.svg)](https://ohwr.org/cern_ohl_p_v2.txt)
![Version: 0.1 — concept](https://img.shields.io/badge/version-0.1%20concept-blue.svg)

> ⚠️ **A concept — nothing built, nothing measured.** Every figure is marked by where it comes
> from: a datasheet, published work, our own calculation, or not known. The calculations are
> models — 2D and 3D FDTD and simpler physics — not measurements. Nobody has yet seen a cable's
> shadow through a real wall this way. Questions and corrections are why it is published.

## How it works

- **Why a shadow, not a radar.** The signal crosses the wall once. There is no echo from the
  near surface and no transmitter leaking into the receiver — the two things that blind a
  one-sided radar.
- **The ratio between receivers.** Every receiver measures the channel of the same packet on
  every subcarrier (the CSI). Dividing one receiver by another removes everything the sender
  does — its power, its phase, its rate — and leaves the wall.
- **Phase from the first build.** All eleven receivers run from one 48 MHz clock. The crossed
  pair in the middle calibrates the ring over the air, between strokes, with no switch anywhere.
- **The stroke as an aperture.** As the head slides, the phase along the stroke focuses: a cable
  3 cm deep is placed to about 6 mm in depth over a 20 cm stroke.
- **For masonry, a knock.** A buzzer disc taps the wall through a plastic rod in the middle;
  eight microphones around it hear the wall's surface wave before the sound through the air.

## The parts

| part | what it is |
|---|---|
| **Fonar** | the lantern: the sender behind the wall, two ESP32-C5 boards with crossed dipoles taking turns, 1000 frames a second |
| **Kolchoz** | the collective farm: the ring of nine receivers that work as one, and the crossed pair in the middle |
| **Datel** | the woodpecker: the knock and the eight microphones |
| **Razvedčik** | the scout: two optical-flow sensors that track the head over the wall |
| **Gensek** | the general secretary: one STM32H7A3 over everything — the reports, the position, the knock, the display |
| **Pajok** | the ration: two 18650 cells |
| **Gradusnik** | the thermometer: a thermal sensor, postponed — a thermal camera beside the head does it for now |

## The head

| | |
|---|---|
| size | 167 mm across; about 0.36 kg before the housing |
| the ring | nine patches 30 × 29 mm on a circle of 65.8 mm radius, 45 mm apart, each turned radially |
| the middle | one square patch fed twice at right angles, on two receivers; a hole through its centre for the knock's rod |
| marking | a pencil by notches on the head's rim, two pairs on its two axes |
| the receivers | eleven ESP32-C5, as bare chips on the back of the antenna board, each fed straight up to its patch by a via — no coax |
| the boards | the antenna board, 4 layers, 1.6 mm; the electronics board 11 mm behind it |
| against the wall | 15 mm of foam, a 1 mm polyethylene sheet on its face that slides |
| power | about 5.7 W; about three hours from the cells |

Details, sources and every figure: [`concept.md`](concept.md).

## What is not known

- **Whether the ESP32-C5 runs from an outside 48 MHz clock.** Its documents call the crystal
  compulsory. This decides the board; a raw-I/Q radio is the plan B.
- **Whether a real wall behaves as the models do** — the permittivity of real mortar and
  plaster, wet joints, and whether 8-bit CSI with a fixed gain holds a change of 20–30 % in
  amplitude and phase steadily.
- **Whether the knock and the microphones hear anything useful** through dry contact on plaster.

The trials that decide it are at the end of [`concept.md`](concept.md).

## What next

Version 0.1 is the concept in one document, with its scripts beside it; the parts get folders of
their own only in later versions. Next we send our questions — to Espressif, to the authors of
ESPARGOS, to the forums on radio and on non-destructive testing — and build the trials as soon as
we can. The project grows with what they show, and as far as time and means allow.

## Files

- [`concept.md`](concept.md) — the whole concept: what it is for, the head, why it should work,
  the electronics, the sound, the heat, the paths left and why, what is not known, the trials.
- [`calc/`](calc) — the scripts behind every calculated figure, Python 3 with numpy (scipy for
  two of them), and their outputs. `budget.py`, `array.py`, `acoustics.py` and `cpu.py` run at
  once; the FDTD models take minutes to an hour a case.

Software under the MIT licence ([`LICENSE`](LICENSE)); the hardware design under the CERN-OHL-P v2
([`LICENSE-HW`](LICENSE-HW)).

## Acknowledgements

To the AI assistant Claude (Anthropic), for its great help with this project.

★ Viva La Resistánce ★
