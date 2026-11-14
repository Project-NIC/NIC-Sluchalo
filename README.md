<p align="center">
  <img src="NIC-Sluchalo.jpg" width="300" alt="Sluchalo"/>
</p>

★ N.I.C. ★

# NIC-Sluchalo

**English** · [Čeština](README.cs.md) · [Русский](README.ru.md)

**What is in a wall, seen by the shadow Wi-Fi casts through it. A hand-held head with ten
Wi-Fi receivers turns on a rod held to one face of the wall; a small box on the other side sends. A cable,
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
- **One clock for all ten receivers.** They run from one 48 MHz source, so their phases can be
  compared. Over a whole turn the receivers are levelled against one another from the pass
  itself; they can also calibrate one another over the air — **Samokritika** — with no switch
  anywhere.
- **A turn as the scan.** The head turns once on a rod held to the wall, off its own centre, so
  each of the eight antennas of the ring draws its own circle and together they fill a disc
  about 24 cm across. The head does not touch the wall.
- **The mains voltage, as a layer.** A capacitive sensor in the head shows where a live cable
  is; it never says that one is dead.
- **For masonry, a knock.** A buzzer disc taps the wall through a plastic rod in the middle;
  eight microphones around it hear the wall's surface wave before the sound through the air.

## The parts

| part | what it is |
|---|---|
| **Fonar** | the lantern: the sender behind the wall, two ESP32-C5 boards with crossed dipoles taking turns — **Serp** and **Molot** — 1000 frames a second |
| **Valenki** | the felt boots: the undercarriage — a rubber foot pressed to the wall, a rod and a grip; it holds the head off the wall and square to it |
| **Kolchoz** | the collective farm: the head — everything that turns on the rod |
| **Brigáda** | the work brigade: the ring of eight receivers that work as one |
| **Předseda** | its chairman (Czech): the crossed pair in the middle, which leads the calibration over the air — **Samokritika** |
| **Kuranty** | the Kremlin's chimes: the one 48 MHz clock everything goes by |
| **Datel** | the woodpecker: the knock and the eight microphones |
| **Razvedčik** | the scout: the sensor of the head's angle on the rod |
| **Iljič** | Ilyich's lamp: the mains-voltage unit — a capacitive sensor with its own gain and band, a layer of the picture |
| **Gensek** | the general secretary: one STM32H7A3 over everything — the reports, the position, the knock, the display |
| **Pravda** | the newspaper: the display and the buttons |
| **Kádrovák** | the keeper of files (Czech): the store of every picture with its raw data; **Samizdat** takes them out to a computer |
| **Pajok** | the ration: two 18650 cells |
| **Gradusnik** | the thermometer: a thermal sensor, postponed — a thermal camera beside the head does it for now |

## The head

| | |
|---|---|
| size | 176 mm across |
| the ring | **Brigáda**: eight patches 30 × 37 mm on a circle of 69.5 mm radius, 53 mm apart, each turned radially |
| the middle | one square patch fed twice at right angles, on two receivers; a hole through its centre for the knock's rod |
| the rod | 35 mm from the centre, between the middle patch and the ring; one turn covers a disc about 24 cm across |
| marking | a pencil by notches on the head's rim, once it has stopped |
| the receivers | ten ESP32-C5, as bare chips on the back of the antenna board, each fed straight up to its patch by a via — no coax |
| the boards | **Front**, the antenna board, 4 layers, 1.6 mm; **Tyl**, the electronics board, 11 mm behind it |
| against the wall | it does not touch: **Valenki** holds it 15 mm off; felt on the head where it may brush the wall |
| power | about three hours from two 18650 cells (5.7 W was computed for eleven receivers) |

The head as decided on 13 Nov 2026: [`calc/ring8.py`](calc/ring8.py), its patch in
`calc/patch8.out`. The concept of 28 Oct ([`concept.md`](concept.md)) describes the earlier head —
nine in the ring, on foam, slid over the wall; where it differs from the levels, the levels hold
([`WHY.md`](WHY.md)).

## What is not known

- **Whether the ESP32-C5 runs from an outside 48 MHz clock.** Its documents call the crystal
  compulsory. This decides the board; a raw-I/Q radio is the plan B.
- **Whether a real wall behaves as the models do** — the permittivity of real mortar and
  plaster, wet joints, and whether 8-bit CSI with a fixed gain holds a change of 20–30 % in
  amplitude and phase steadily.
- **Whether the knock and the microphones hear anything useful** through dry contact on plaster.

The trials that decide it are at the end of [`concept.md`](concept.md).

## What next

The project is grown level by level. The purpose, the requirements and the architecture are
closed; the physics is being computed block by block. The concept of 28 Oct stays as the record
of where it began. Our questions are out — to Espressif, to the authors of ESPARGOS, to the
forums — and the trials are built as soon as we can. The project grows with what they show, and
as far as time and means allow.

## Files

- [`purpose.md`](purpose.md) — what it does, for whom, and how we know it works, on one page.
- [`requirements.md`](requirements.md) — what it must do, in ranges.
- [`architecture.md`](architecture.md) — the bodies, the units and what passes between them; the names.
- [`WHY.md`](WHY.md) — why closed levels were reopened, and what that changed below.
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
