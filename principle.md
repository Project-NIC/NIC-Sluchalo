# NIC-Sluchalo — the principle

*Level 4 of the project, closed on 14 Nov 2026: for every block the physics and a rough calculation,
always as a script in [`calc/`](calc). No part numbers — those are level 5. The bodies, the units and
their names are in [`architecture.md`](architecture.md).*

> **What these figures are.** Rough calculations, made to choose between ways of building the tool,
> not to promise what it will see. The wall is a model: a slab, or a 2D section through it, at single
> frequencies, with handbook or assumed values for brick, mortar and plaster, and objects that are
> straight cylinders. The antennas are taken as the field summed along their length; the room, the
> user and the third dimension are left out. Each script says what it leaves out. Where a figure
> matters, it is there to be measured: **only the trials on real walls give the real values**, and
> the trials are at the end of [`concept.md`](concept.md).

## The blocks and their scripts

| block | script | what it says |
|---|---|---|
| Iskra, the wall, the shadow | `budget.py`, `shadow.py`, `wall_fdtd.py`, `joints.py` | as in the concept: what a wall costs, the shadow of a cable, the joints' pattern |
| the face of the head | `layout.py` | where the antennas and the rod sit — below |
| the pass and the picture | `picture.py`, `nosync.py` | a turn about a rod, and the picture drawn from amplitudes alone — below |
| the head against the wall | `head8.py` | how far the head may stand off, and the depths each band sees — below |
| Samokritika | `samokritika.py` | below |
| behind the antennas | `absorber.py` | below |
| Iljič | `hum.py` | below |
| Pajok, the body, the frames | `body.py` | below |
| Gensek | `cpu8.py` | below |

Each script prints into the `.out` file of its own name; that file is the home of its figures.

## The pass: the head is turned about Kuří nožka

Ten receivers are ten points; a picture is a few hundred. The rest comes from moving the head, and
the simplest movement is a turn: Kuří nožka, a rod with a rubber foot, is pressed to the wall with
one hand, and Kolchoz, a disc on it, is turned with the other. The rod stands off the head's
centre, so that each antenna of the ring lies at its own distance from it and draws its own circle
(`picture.py`, `picture_moves.png`):

- about its own centre the head would draw a ring and nothing else — all eight on one circle;
- about a rod off the centre it fills a disc; slid instead, a receiver's leftover gain error draws
  a stripe along the stroke that looks like a pipe, while about a rod it draws rings that nothing in
  a wall imitates and that the levelling takes out;
- **both of Iskra's senders are needed**: with the upright one alone, everything that runs the other
  way is gone;
- the grain of the wall, not the noise, is the limit: ten times the noise changes nothing, and one
  turn draws what three do.

## The picture without a shared clock

Every receiver runs on its own crystal. The phase between two receivers is then new in every frame
and worth nothing; what is left of a frame is the amplitude each receiver measured on every
subcarrier, its gain held fixed. `nosync.py` (`nosync.out`, `nosync.png`) makes the reports exactly
so — each receiver's gain a few dB off, a random phase in every frame for every receiver, the sender
and the room changing by 2 dB from frame to frame — and draws the picture three ways:

1. **Levelled.** On each frame the receivers are set against one another, so the sender and the
   room fall out; over a whole turn each receiver is set against its own circle, so its gain falls
   out.
2. **Focused, as an in-line hologram.** The wall is lit by Iskra's own wave, nearly the same over
   the whole head. A cable adds its wave to it, and the change in amplitude is the part of the
   cable's wave in step with the light — Gabor's hologram, with the light itself as the reference
   instead of a clock of ours. That part can be carried back through the wall.
3. **Self-scaled.** No levelling at all: Iskra's upright frame and its level one follow each other
   within a millisecond and reach the same receiver at the same gain, so their ratio in one receiver
   has no gain in it. Against what a bare wall would give at that antenna's angle, it shows where the
   field along one direction is changed.

How far an object stands out of the rest of the wall, in dB, against the spread of the rest:

| | levelled | focused | self-scaled |
|---|---|---|---|
| one cable, 3 cm deep | −1.8 / 2.0 | −1.5 / 1.5 | −1.3 / 2.0 |
| a 60 mm conduit with a cable in it | −7.4 / 10.3 | −2.9 / 6.7 | −6.0 / 6.5 |
| two cables 4 cm apart | −0.6 / 2.0 | −0.6 / 1.5 | −0.3 / 2.1 |
| a cable that turns | −2.2 / 2.8 | −1.6 / 2.2 | −2.4 / 2.9 |
| a 22 mm metal pipe | −4.3 / 4.8 | −3.1 / 3.4 | −3.1 / 4.5 |
| one cable, 10 cm deep | −0.4 / 1.4 | −0.4 / 0.8 | −0.3 / 1.6 |

All three draw the walls; a single cable is about as strong as the wall's grain and is seen because
it is straight and long and the grain is not — as the purpose asks of the picture. Self-scaled needs
nothing of the receivers' gains and is the most robust. **What the absence of phase costs is depth**:
a cable 10 cm deep is weak in all three. With a clock shared by all receivers, the phase could focus
it further (`picture.py`); that is the variant for later, if a C5 is ever easy to clock from outside.

## The face

`layout.py` (`layout.out`, `layout.png`) places everything on Front for the bought antenna — the
Ezurio dual-band FlexPIFA, 38.5 × 12.7 mm, made to sit over metal — keeping the maker's 5 mm beside
every antenna and round every hole: the eight of the ring, radial, on a circle of 64 mm; Předseda's
two at right angles as a pinwheel round the middle, which leaves the middle free; Kuří nožka 32
mm out, in the quarter the pinwheel leaves free. (The layout still keeps the middle and eight places
by the ring for Datel, which went to NIC-Ariadna on 14 Nov — `WHY.md` 17; they cost the ring nothing.) **The head is 177 mm across**, and a turn covers a disc about 23 cm across.
Předseda off the centre costs nothing: Samokritika no longer needs the symmetry, and its two antennas
draw two circles instead of one (a run with four antennas round the middle drew the same picture).

## The head against the wall

The antennas sit on Front's metal disc, over a thin insulating face, 15 mm from the wall. The disc
is their ground and the shield behind them; it also makes a standing wave with the wall. `head8.py`
puts the head into the concept's 2D wall model — a section through the wall, gypsum plaster, the
cable in a groove — and asks what the cable changes in the field the antenna sums
(`head8_disc.out`, `head8_disc5.out`): amplitude in dB, and in brackets amplitude and phase together.

| cable deep | channel 1 | channel 6 | channel 11 | channel 36 | channel 165 |
|---|---|---|---|---|---|
| 20 mm | −1.6 (28 %) | −1.4 (29 %) | −1.1 (29 %) | +2.4 (40 %) | +17.6 (749 %) |
| 25 mm | −0.4 (5 %) | −0.4 (5 %) | −0.5 (6 %) | +15.5 (497 %) | +7.9 (149 %) |
| 30 mm | −0.6 (23 %) | −0.8 (28 %) | −1.4 (31 %) | +4.8 (76 %) | −2.9 (42 %) |
| 35 mm | −2.0 (36 %) | −2.3 (41 %) | −2.9 (43 %) | −1.7 (23 %) | −2.0 (57 %) |
| 40 mm | −3.0 (38 %) | −3.4 (41 %) | −3.8 (42 %) | −1.3 (58 %) | +1.4 (26 %) |

- The 2.4 GHz band has **weak depths**: at 30 mm the amplitude barely moves though the field changes
  by a quarter, and at 25 mm the cable hardly shows at all. Its three channels lie too close together
  to fill them.
- The 5 GHz band sees exactly there, strongly — **but as a brightening as often as a shadow**: its
  standing wave has nodes close together, and near one a cable can raise the field many times over.
  The two bands cover each other's weak depths, and **the picture shows change either way, not
  darkness alone**, as self-scaling does. At 5 GHz the model is coarse — a millimetre's grid against
  26 mm of wavelength in brick — and has no joints, which the concept found to scatter there in a thin
  wall: the figures say where, not how much.
- **How closely the head must keep its distance** (`head8.out`, run for the earlier patch head, whose
  ground plane the disc matches within a tenth of a dB on channel 6): from 13 to 17 mm what a cable
  changes moves by a few per cent. A millimetre or two, a degree of tilt — the bound the requirements
  set — is kept with room to spare.

## Samokritika

Before a turn Předseda swings Serp, then Molot: a short frame in each polarization, and every Mužík
measures how much arrives. Set against the state stored when the tool was last known good, it shows
what a knock, damp or a shifted antenna has done to each Mužík — Gensek scales by it, and Felčar
takes it as a check. With no shared clock it says nothing of delays; and it needs no symmetry, since
each Mužík is set against itself. The picture does not hang on it: the turn's own scaling draws it
without. Neighbours lie 5 cm and more apart, and a sender reaches them easily.

`samokritika.py` holds what was computed for the phase, for the variant with a shared clock: sending
both ways alone does not give the receivers against one another; the ring's symmetry does, to the
accuracy of that symmetry — paths 3 % uneven cost 0.7°, 10 % cost 2.5°.

## Behind the antennas

The FlexPIFA is made to sit over metal; the disc behind it is its ground and keeps out the room, the
hand and the head's own electronics. No absorber goes between the antennas: it would muffle
Samokritika across the face. `absorber.py` (`absorber.out`) keeps what was found on absorbers, should
one be wanted at the rim: from behind, household aluminium foil stops what matters (some 50 dB in
the foil alone, the seams deciding); from the front, about 30 mm of carbon foam on foil returns about
−20 dB at 2.4 GHz and −12 to −14 dB at 5.5 GHz, while films stacked within 5 mm of the foil do
nearly nothing (the foil shorts the field there) — thin absorbers are magnetic sheets.

## Iljič

`hum.py` (`hum.out`): a plate that senses the field at the wall, from 50 Hz to 1 MHz, through walls
from bone dry to damp.

1. A wall conducts slow fields and insulates fast ones; where it changes over depends on its damp —
   a few hertz bone dry, tens of kilohertz ordinary, megahertz damp.
2. Where the wall conducts, the plate goes blind: at 50 Hz it reads well only through a dry wall.
3. A higher frequency reads through a damper wall — at 125 kHz an ordinary wall is no obstacle; so
   Iljič's band is the user's to set, 50 Hz for the mains, a tracer's frequency where one is at hand.
4. The plate sees a cable wide — one to four tens of centimetres. It says *here is a live cable*, not
   where to the centimetre.

The coil and the tracer went to NIC-Ariadna; `hum.py` keeps both halves as they were computed.

## The body: power, weight, frames

`body.py` (`body.out`): ten receivers, the processor, Razvedčik, Iljič and the display draw
about **5.4 W — about 3.4 h** from two 18650 cells. Front's aluminium, 3 mm at least for the screws'
threads, weighs about 200 g; the head before its modules, antennas and housing about 470 g. Off the
wall it sheds its heat from both faces, about 8 K over the room.

**A turn needs few frames.** The outermost antenna, 95 mm from the rod, moves 8 to 30 cm/s in a turn
of eight to two seconds; a frame every eighth of a wavelength in brick wants **ten to forty frames a
second from each sender**. At a hundred, the whole channel as the chip measures it is half a megabit
a second a receiver — the receivers send it raw, and the raw data the purpose promises are the
reports themselves.

Each receiver's own 48 MHz crystal has harmonics in the 2.4 GHz band: the 50th at 2400 MHz, just
below channel 1, the 51st at 2448 MHz, between channels 6 and 11 — none inside the three channels
Iskra uses.

## Gensek

`cpu8.py` (`cpu8.out`) counts what `picture.py` does, for a turn of four seconds at a hundred frames
a second from each sender, the subcarriers in sixteen groups. **Time is no trouble**: putting every
report into the picture takes half a per cent of the processor while the head turns; at the end of
the turn levelling, solving and focusing take about three quarters of a second. **Memory binds**: a turn's reduced reports are about a megabyte and the picture's
sums two more, against about 1.4 MB in the processor — four groups of subcarriers fit, or memory
beside it; for the parts. The raw reports, five megabytes a turn, go straight to Kádrovák.

## Not computed

- **How much one antenna hears its neighbour.** There is no model of the FlexPIFA here; Samokritika
  measures it on the first head.
- **The FlexPIFA's own pattern and the purity of its polarization** over the disc — taken as a line
  summing the field along it.
- **The third dimension, the room and the user**, and at 5 GHz the joints.

## Computed and left

On the way to the head as decided, three things were computed and then left; their scripts stay as
the record, and [`WHY.md`](WHY.md) says why:

- **Our own patches** — `ring8.py` (the ring of eight patches 30 × 37 mm), `patch8.out` (the patch
  tuned: −32 dB at 2.437 GHz, 55 MHz wide), `coupling8.py` (neighbours −32 to −39 dB, a ring patch
  and the middle −40 to −45 dB). Left for bought antennas.
- **A clock shared by all receivers** — the clock lines need no matching, a fixed skew being levelled
  out and its drift hundredths of a degree per kelvin (`body.py`); the phase calibration by symmetry
  (`samokritika.py`). Left: the C5 has no clock input and the one attempt on record failed.
- **Foam as a spacer and absorbers between the antennas** — above. Left for Valenki holding the head
  off the wall and for the disc.
- **Datel, the knock and its eight microphones** — moved to NIC-Ariadna on 14 Nov 2026 (`WHY.md` 17).
  What was computed for it here stays as its record: the knock in the middle, the microphones 64 mm
  out, the head 15 mm off the wall — the wall's surface wave reaches them 65 to 114 µs before the
  sound through the air (`datel8.py`, `acoustics.py`); `body.py` and `cpu8.py` still count it.
