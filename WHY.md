# NIC-Sluchalo — why closed levels were reopened

## 13 Nov 2026 — levels 2 and 3, reopened the day they were closed; closed again on 14 Nov

Levels 1 to 3 were closed in the morning. Working through level 4 the same day, the owner changed
how the head is moved and held, and the calculations changed what it needs. Level 1, the
purpose, stands as closed.

**What changed, and why**

| # | change | why |
|---|---|---|
| 1 | The head is turned about a rod, not slid over the wall. | The owner: a small picture is enough, best taken by turning; then "na kraji udělat čep a točit kolem něj", then the plain form — a grip, a rod with a rubber tip, the head a disc on it turned by the other hand. `picture.py`: about its centre the head draws only a ring, about a rod off the centre a full disc. |
| 2 | The head's angle is measured on the rod; the optical-flow sensors go. | With a turn only the angle is wanted. The owner: "any magnetic sensor"; the sensor stays in even if the radio can give the angle too. |
| 3 | Eight patches around Předseda, each at its full width; ten receivers, not eleven. | The owner's question and decision. The nine were for a head that slides under a sender of unknown field; a turned head takes every direction anyway. Eight fit the middle's square, Datel's eight microphones, and the full patch; in the model they draw what nine did. |
| 4 | Iljič is a capacitive plate only, on the processor's own converter, gain and band adjustable. | The owner. The coil, the rods and the tracer's signal went to a project of their own, NIC-Ariadna. |
| 5 | The foam spacer goes; the head does not touch the wall. Valenki is the undercarriage: a wide foot on the rod, pressed to the wall and standing firm. Where the turning head, Kolchoz, may brush the wall it wears hard smooth felt. | The owner: foam grips and is soft; good felt slides on paint and scuffs nothing. |
| 6 | The receivers are levelled from the pass itself; sending between the chips is no longer the only way. | `picture.py`, `samokritika.py`: over a whole turn an uncalibrated head draws the same picture once each receiver is levelled against its own circle. Whether Samokritika by sending stays a required step is the owner's to say. |

A thought, not a change: a small motor to turn the head.

**What stops holding below, to be worked off before anything new**

| where | what no longer holds | state |
|---|---|---|
| `requirements.md` | the picture's size and how it is taken; one hand holding and one marking; the hum "voltage, current, or both" | rewritten; closed again on 14 Nov 2026 |
| `architecture.md` | Kolchoz as a ring of nine; Razvedčik as optical sensors; Iljič's form; Valenki as foam; the body; the steps to a picture; the names, now in three tiers | rewritten; closed again on 14 Nov 2026 |
| level 4, the principle and its scripts — not yet published | — written on the new head | holds |
| `calc/ring8.py` | — | the new head's layout, published with this |
| `calc/array.py` | the ring of nine as the layout | replaced by `ring8.py`; kept as the record of the three layouts weighed |
| `calc/patch_fdtd.out` | the patch 30 × 29 mm under 15 mm of foam | done: the 30 × 37 mm patch tuned, `calc/patch8.out` |
| `calc/head.py` and its outputs | the head's ground plane 167 mm across on foam; the spacer's choice | redone for the head as decided: `head8.py` (the disc, both bands; the gap) — level 4, closed 14 Nov 2026 |
| `calc/acoustics.py`, Datel in the concept | the microphones' pipes through the foam; the knock's rod resting on the wall under a head that slides | gone through: `datel8.py` — level 4, closed 14 Nov 2026 |
| `calc/budget.py` | the head's size and weight with foam and sheet; eleven C5s in the power and the data rates; the optical sensors' current | redone: `body.py` — level 4, closed 14 Nov 2026 |
| `calc/cpu.py` | eleven receivers; the stroke's focusing | redone: `cpu8.py` — level 4, closed 14 Nov 2026 |
| `concept.md` | *The head* (nine, the foam, the notches), *The electronics* (eleven chips, 22 UART lines, optical sensors, the calibration's "both ways cancels the paths"), *The trials* (the foam in the microwave; the clock trial's second question) | not edited: the concept is the record of 28 Oct; the levels replace it as they close |
| `README.md` and its Czech and Russian | *The parts* and *The head* tables | brought up to date with levels 3 and 4, 14 Nov 2026 |
| the trials and the questions as posted | the foam and the optical sensors in them | to be gone through |

## 14 Nov 2026 — level 3 reopened: no shared clock; closed again the same day

**What changed, and why.** The head was to run all its receivers from one 48 MHz clock, so that
their phases could be compared (the owner, 27 Oct). Three things undid it the same day. The
ESP32-C5 has no clock input; Espressif's checklist calls its crystal compulsory; the one attempt
on record to run eight C5s from a shared clock (a DigiKey forum thread, June 2026) failed to boot
and found no fix. Even with a shared clock, every chip's synthesizer locks at a new phase after
each reset and change of channel (the ESPARGOS authors). And level 4's `nosync.py` showed that a
head with **every receiver on its own crystal**, its phases thrown away, draws the same pictures
from the amplitudes alone — scaled within each receiver by the ratio of the sender's upright frame to its level one,
levelled over the turn, and focused as an in-line hologram with the sender's own wave as its reference.
What it loses is sharpness in depth. So (the owner: "přesně, beru to, tlač to tam natvrdo"):

| # | change | why |
|---|---|---|
| 7 | Every receiver runs on its own crystal; there is no shared clock. **Kuranty** becomes the time base: one edge from Gensek on a shared line, caught by each chip's timer. | Above. A shared clock may come back with bare chips, only to sharpen depth. |
| 8 | The radio layer is drawn from the amplitudes: self-scaled, levelled, focused. Samokritika checks gains only. | `nosync.py`. |
| 9 | A receiver is a unit with one interface — each of Brigáda's eight **Mužíci**, and Předseda's two, which do the work of two Mužíci: an antenna input of 50 ohm, a serial link, the reset and boot lines, the sync line, 3.3 V — so that a ready-made module can be one now and a bare chip later. The first head is built from ready-made, certified modules, each joined to its antenna by a short cable (the antennas: entry 13). | Ready-made modules need no work on the radio and keep their certification; nothing in them has to be opened. |
| 10 | **Karanténa** is the watch over every unit, its **Felčar** the checks; on a fault the tool declares it and stops. | The owner. |
| 11 | **Names:** Sluchalo is the project; **Fonar** is now the tool held to the wall (Valenki and Kolchoz); the sender behind the wall is **Iskra**; **Serp** and **Molot** are Předseda's two halves, the only senders in Fonar. Iskra's two senders are simply upright and level. | The owner: the project and its parts named apart, as in NIC-Strelka; Předseda hands out the calibration. |
| 12 | **Samokritika** is a regular step of every pass: Předseda swings Serp, then Molot; every Mužík measures what arrives, against the state last known good. Amplitudes only. | The owner: it calibrates the antennas against knocks, damp and detuning, and gives Felčar its check. |
| 13 | **Every antenna is bought** — the receivers', Předseda's and Iskra's — dual-band, 2.4 GHz and the whole 5 GHz band, 50 ohm, on a short cable to its module. No antenna of our own: Front becomes a carrier for bought antennas, turned radially. Předseda sends; every sender's power is capped in software so that its EIRP stays under the 20 dBm of the band. | The owner: an antenna of our own varies from piece to piece, a bad one radiates into its neighbours, and one that holds 50 ohm over 2.4 GHz and all of 5 GHz is beyond what we would design and could not have measured; a bought antenna of a type its maker certifies with modules is the smaller evil. |
| 14 | A name added, none changed: **Kuří nožka** — Valenki's rod with its rubber foot, the axis the head turns on. | The owner: the head turns on it as Baba Yaga's hut turns on its chicken leg; old Czech slang calls such a widened end a chicken leg. |
| 15 | A unit added: **Matjugalnik**, the sound — what the picture and Iljič show, by ear, in a tone and loudness the user sets; silent while Iljič measures. | The owner: a day with a bought tracer's crude squeal is wearing, and with the display off its fine changes are lost; a sound worth listening to. |

**What stops holding below**

| where | what no longer holds | state |
|---|---|---|
| `architecture.md` | Kuranty as one clock; the steps to a picture; Předseda's part in calibration; the body | rewritten with entries 11–13 and the names Kosa and Levša; closed again on 14 Nov 2026 |
| level 4, not yet published | the clock lines on the board (`body.py`, *Kuranty*); the receivers' phase as the way to depth | the clock kept as the record of a variant left (`principle.md`, *Computed and left*); level 4 closed 14 Nov 2026 |
| the trials | the clock trial as the trial that decides the board | it decides only the later, sharper variant |
| level 4: `ring8.py`, `calc/patch8.out`, `coupling8.py`, `head8.py` | the patch 30 × 37 mm, its tuning, its coupling, the ground plane behind it, the ring's spacing set by the patch's width | redone with the FlexPIFA: `layout.py`, `head8.py`; the patch scripts kept as the record — level 4 closed 14 Nov 2026 |
| `concept.md`, `calc/patch_fdtd.py`, `head.py` | the head's own patches and ground plane | the concept's record; not edited |
