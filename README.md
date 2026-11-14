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
- **Amplitudes, not phases.** Every receiver measures the channel of the same frame on every
  subcarrier (the CSI), its gain held fixed. Every receiver runs on its own crystal, so only the
  amplitudes are compared: on each frame the receivers against one another, which removes the
  sender and the room; in each receiver the frames of the sender's two crossed antennas against
  each other, which removes the receiver's own gain; and over a whole turn each receiver against
  its own circle. The sender's own wave is the reference that focuses the picture, as in a
  hologram.
- **A turn as the scan.** The head turns once on a rod held to the wall, off its own centre, so
  each of the eight antennas of the ring draws its own circle and together they fill a disc
  about 24 cm across. The head does not touch the wall.
- **Samokritika.** Before a turn the middle pair sends a short frame in each polarization and
  every receiver measures what arrives — against knocks, damp and drift.
- **The mains voltage, as a layer.** A capacitive sensor in the head shows where a live cable
  is; it never says that one is dead.
- **For masonry, a knock.** A buzzer disc taps the wall through a plastic rod in the middle;
  eight microphones around it hear the wall's surface wave before the sound through the air.

## The parts

| part | what it is |
|---|---|
| **Iskra** | the spark: the sender behind the wall, a ready-made board with two crossed antennas taking turns, upright and level |
| **Fonar** | the lantern: the tool held to the wall — Valenki and Kolchoz |
| **Valenki** | the felt boots: the undercarriage — a rubber foot pressed to the wall, a rod and a grip; it holds the head off the wall and square to it |
| **Kolchoz** | the collective farm: the head — everything that turns on the rod |
| **Levša** | Leskov's left-handed smith: the construction, all of metal and plastic that holds the units |
| **Brigáda** | the work brigade: the ring of eight receivers, the **Mužíci**, each with its antenna, its **Kosa** (scythe) |
| **Předseda** | the chairman (Czech): the pair in the middle, at right angles — the work of two Mužíci — with **Serp** and **Molot** in its hands, the only senders in Fonar, for **Samokritika** |
| **Kuranty** | the Kremlin's chimes: the time base — one edge on a line shared by all receivers |
| **Datel** | the woodpecker: the knock and the eight microphones |
| **Razvedčik** | the scout: the sensor of the head's angle on the rod |
| **Iljič** | Ilyich's lamp: the mains-voltage unit — a capacitive sensor with its own gain and band, a layer of the picture |
| **Gensek** | the general secretary: one processor over everything — the reports, the angle, the knock, the picture, the display |
| **Pravda** | the newspaper: the display and the buttons |
| **Kádrovák** | the keeper of files (Czech): the store of every picture with its raw data; **Samizdat** takes them out to a computer |
| **Pajok** | the ration: two 18650 cells |
| **Karanténa** | quarantine: the watch over every unit, its **Felčar** the checks; on a fault the tool stops |
| **Gradusnik** | the thermometer: a thermal sensor, postponed — a thermal camera beside the head does it for now |

## The head

| | |
|---|---|
| size | about 18 cm across |
| the ring | **Brigáda**: eight bought dual-band antennas (2.4 and 5 GHz), each turned radially |
| the middle | **Předseda**: two of the same antennas at right angles, beside the knock's rod |
| the rod | between the middle and the ring; one turn covers a disc about 24 cm across |
| marking | a pencil by notches on the head's rim, once it has stopped |
| the receivers | ten ready-made ESP32-C5 modules, each on its own crystal, each joined to its antenna by a short cable |
| Front | the face towards the wall: a metal disc with a thin insulating face, the antennas on it — their ground and the shield behind them |
| Tyl | the board behind it: the processor, the power, the knock, the display |
| against the wall | it does not touch: **Valenki** holds it off; felt on the head where it may brush the wall |
| power | about three hours from two 18650 cells |

The concept of 28 Oct ([`concept.md`](concept.md)) describes the earlier head — nine patches of
our own, one clock for all, on foam, slid over the wall; where it differs from the levels, the
levels hold ([`WHY.md`](WHY.md)). The head's layout is redrawn for the bought antennas;
[`calc/ring8.py`](calc/ring8.py) has it for the earlier patches.

## What is not known

- **Whether a real wall behaves as the models do** — the permittivity of real mortar and
  plaster, wet joints, and whether 8-bit CSI with a fixed gain holds a change of 20–30 % in
  amplitude steadily.
- **Whether the amplitudes alone, with no clock in common, draw a real wall** as well as they
  draw the modelled one.
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
