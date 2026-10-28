# NIC-Sluchalo — what is in the wall, seen by the light of Wi-Fi

*Version 0.1, a concept, 28 Oct 2026. Nothing is built or measured yet. Every figure is marked by
where it comes from: **[sheet]** a datasheet or a maker's page, **[lit]** published measurements,
papers and makers' forum answers, **[calc]** our own calculation (the Python scripts in `calc/`,
which go with this page), **[open]** not known. The trials that decide whether it works are at the
end. Questions and corrections are the point of publishing it.*

## What it is for

A wall scanner tells what lies under a surface before it is drilled, cut, chased or broken into
**[sheet]**:

- **before drilling or chasing** — live cables, and water, heating and gas pipes, which cost a
  repair, or worse, when hit;
- **fixing things** — shelves, cabinets, a TV: the studs and profiles in drywall to fix into, the
  pipes to miss;
- **electrical work and renovation** — where the existing wiring runs when there are no drawings:
  from a socket or a box up, down or along; a UTP bundle in a server room's drywall;
- **reworking a building** — metal pipes, steel profiles, empty conduits, and in concrete the rebar.

The walls here are drywall with a cavity of up to 30 cm, and solid brick 10–60 cm thick with cables
in plastered grooves a few centimetres deep. The hand-held scanners on the market reach a groove by
their specification (Bosch D-tect 200 C: 200 mm in dry concrete, 80 mm in other walls, 18 433 Kč,
about €750 **[sheet]**) and are good machines; what they keep closed is the firmware — fixed modes
and thresholds, no raw data — so a wall that does not fit their presets leaves nothing to adjust.
What reaches further costs more than a small company will spend: a Proceq GP8000 GPR $14 120–22 240,
a MIRA A1040 ultrasonic tomograph about €30 000 **[sheet]**. This tool keeps every setting and its
raw data open to whoever uses it.

## The idea

**Light the wall from the far side and look for shadows on the near side.** The light is Wi-Fi that
is already there — the building's access points, the phones — or, where there is none, a small box
of our own on a table in the next room. The tool — a round head on a short handle, shaped like a
meat tenderiser — is pressed to the near side and slid or circled over it; it listens, and sends
only short frames between its own antennas to calibrate itself. Every Wi-Fi packet carries a known
preamble from which the receiver measures the channel on every subcarrier (the CSI); a metal object
between the sender and the receiver dims it. The tool shows the dimmed places as spots on its own
display, beeps over them, and the electrician marks them with a pencil by notches on the head's rim.

Why transmission and not a radar: the signal crosses the wall once, and there is no reflection from
the near surface and no leak from a transmitter beside the receiver — the two things that blind a
one-sided radar and that the expensive wall scanners spend their bandwidth on.

For masonry, sound shares the head, in the middle of the ring (*For masonry*). Heat — which cable
has carried a heavy load for an hour or more — is left to a thermal camera beside the tool for now
(*Heat*).

**The name.** Слухало (Sluchalo, the *ch* as in Scottish *loch*) is the companion in Afanasyev's
tale *The Flying Ship* who lies on the road with his ear pressed to the damp earth and hears
everything. NIC- marks the projects of our group, Project-NIC.

**The parts** go by nicknames in the same spirit: **Fonar** (the lantern) is the box that lights the
wall; **Kolchoz** (the collective farm) the ring of nine receivers that work as one; **Datel** —
Czech for woodpecker, after the Soviet Duga radar that the world called the Russian Woodpecker for
its tapping on shortwave — the acoustic head that taps the wall; **Gradusnik** (the thermometer) the
thermal sensor, postponed; **Razvedčik** (the scout) the optical sensors that track the position;
**Gensek** (the general secretary) the one processor over everything; **Pajok** (the ration) the
battery.

## The head: nine receivers in a ring, a crossed pair in the middle

Nine receivers in a ring and a crossed pair in the middle — eleven ESP32-C5s, each on its own
antenna port — on the face that slides on the wall. Three layouts were weighed, all with patches 29
mm wide at 45 mm between centres. The patch is narrowed from the usual 29 × 37 mm (`budget.py`) so
that nine fit a ring, and its length, 30 mm, is set by the match (below); in the ring as built that
leaves 16 mm between neighbours at their centres and 7.5 mm at their inner corners **[calc,
`array.py`]** — a choice against coupling; how much the neighbours still couple is not computed
**[open]**, and being fixed it is calibrated with the rest:

| | 3 × 3 square | ring of 8 around a ninth | **ring of 9** |
|---|---|---|---|
| head across | ~165 mm | ~155 mm | ~167 mm |
| neighbours under λ/2 = 61 mm at 2.44 GHz (for finding a sender's direction by phase) | yes | yes | yes |
| directions of the field covered | 1, or 2 as a checkerboard | 4 | **9, every 20°** |
| a cable at the worst angle: the field along it, as a share of the best case | 0 %, or 50 % | 86 % | **97 %** |
| free middle | none | a 30 mm annulus | **a disc 103 mm across** |

With the sender's two linear turns known, every layout here keeps the full shadow of a cable at any
angle **[calc, `array.py`]**; the nine directions matter for a sender whose field is not known. Six
around one would make every triangle equal (the radius equal to the neighbours' distance) and need
eight C5s; it was weighed and left: the distances need not be equal — they are known, and the
calibration cancels them (*The electronics*) — and nine leave more room in the middle and more
receivers for the phase.

**The ring of nine with every patch turned radially.** A thin cable shadows only the field along it
(below); nine radial patches pick out nine directions of the field 20° apart, so a cable at any
angle is within 10° of one of them — no turning the tool for the second polarization, and which
patches see the dip tells the cable's direction. The field along the cable must come from the
sender, though: our box sends from two crossed antennas in turn; an access point's field reaches the
wall through the room's reflections, partly depolarized — how much is **[open]**. The free middle
takes **the crossed pair**: one square patch fed twice at right angles, each feed to its own C5, no
switch. It sends the calibration frames to the ring (*The electronics*) and, listening, measures
both components of the arriving field, on the same clock — the field's polarization, which mixes
into the radial patches' phases. Through its centre, where its field is nearly nil, goes a small
hole for Datel's rod — 2 mm of hard plastic, which loads the patch far less than metal would (*For
masonry*). Around it: the two optical-flow sensors that track the position over the wall, as in a
computer mouse, and — for masonry — the microphones' openings around the exciter. **The first head
is 2.4 GHz only:** the patches are cut for it, and a dual-band patch is **[open]**.

**The patches do not touch the wall** **[calc, `patch_fdtd.py`, output in `patch_fdtd.out`]**. A
small 3D FDTD of the 2.44 GHz patch (on FR4 1.6 mm, probe-fed) with a 30 mm wall slab in front of it
and an air gap between; without the wall the full 29 × 37 mm patch resonates at 2.475 GHz, the
ring's 29 × 29 mm one at 2.488 GHz:

| the wall | gap to the patch | 29 × 37 mm | shift | 29 × 29 mm | shift |
|---|---|---|---|---|---|
| ITU brick, εr 3.9 | 0 mm | 2.190 GHz | −11.5 % | 2.187 GHz | −12.1 % |
| very dry, εr 3.0 | 0 mm | 2.263 GHz | −8.6 % | | |
| wet, εr 6.1 (9 % moisture **[lit]**) | 0 mm | 2.027 GHz | −18 % | | |
| ITU brick | 2 mm | 2.462 GHz | −0.5 % | 2.469 GHz | −0.8 % |
| ITU brick | 5 mm | 2.488 GHz | +0.5 % | 2.498 GHz | +0.4 % |
| wet | 5 mm | 2.472 GHz | −0.1 % | | |
| ITU brick | 10 mm | 2.495 GHz | +0.8 % | | |

Pressed onto the wall a patch falls out of the Wi-Fi band; 5 mm away it barely moves, wet or dry,
and 2 mm away dry — its fringing field reaches only about as far as the board is thick. So **a
spacer** covers the patches. How thick is set by the standing wave in front of the board (*The head
itself*): **15 mm of foam, with a hard sheet of 1 mm on its face that slides on the wall.** To the
radio the foam is nearly air — cross-linked polyethylene foam has εr 1.03–1.06 and tan δ 0.0001
**[sheet]** — and it weighs about 15 g. **The foam is the sound-insulating kind put into cars and
wrapped round ultrasonic cleaners**, in sheets stacked to 15 mm. Best is closed-cell polyethylene or
EPDM: the hand squeezes it by under 1 %, about 0.1 mm — 30 kg/m³ polyethylene foam takes 35–65 kPa
to lose a quarter of its thickness **[sheet]**, a hand of 20 N on the whole face presses 0.9 kPa
**[calc]**, and the sheet spreads it. Soft open-cell acoustic foam gives more, how much is
**[open]**; a millimetre more or less in the spacer barely moves the standing wave (*The head
itself*). Not the butyl mats, whose aluminium foil is metal, and nothing faced with foil. A
microwave oven is the test for the rest — it works at 2.45 GHz: a piece without foil beside a cup of
water for half a minute, and a foam that stays cold does not drink the signal; black foam must pass
it too, for the carbon some foams carry is what RF absorbers are made of. The sheet is natural
polyethylene or polypropylene — they slide, εr 2.2–2.3 and low loss **[lit]** — not a black
antistatic grade, whose carbon is lossy. It changes the cable's dip by a tenth of a dB at most,
polycarbonate no more (*The head itself*). Solid plastic right on the patch, by contrast, is itself
a load, as the εr 3.0 row shows. The model's cells are 1 mm; the length is set by the match (below).
**The acoustic head's quiet is kept at the microphones, not by the spacer:** each microphone sits on
its own island of the antenna board's back, cut free by slots and held by thin bridges, the slots
filled with foam, so the board's vibration reaches it weakly, and hears the wall through a pipe
across the board and the foam (*For masonry*); which microphones and how they are best mounted is
**[open]**. The spacer then serves the radio alone. How far the board's copper sits from the wall
matters more than the tuning, though (*The head itself*, below).

**The match** **[calc, `patch_fdtd.py s11`]** — the probe as a current source, the input impedance
its voltage over that current, S11 against 50 Ω; patches 29 mm wide. First **the head as built** —
the patch on layer 1 over its ground on layer 3, 1.28 mm of FR4, 15 mm of foam (and 20 mm for
comparison), lime-cement plaster:

| patch length | in front of it | feed in from the edge | best match | S11 | −10 dB band | at 2412 / 2442 / 2472 MHz |
|---|---|---|---|---|---|---|
| **30 mm** | **15 mm of light foam (εr 1.05), then plaster** | **8 mm** | **2.445 GHz** | **−23.6 dB** | **55 MHz** | **−9.5 / −23.2 / −10.1 dB** |
| 30 mm | 15 mm of dense foam (εr 1.2), then plaster | 8 mm | 2.421 GHz | −26.0 dB | 55 MHz | −19.9 / −12.9 / −6.1 dB |
| 30 mm | 20 mm of light foam (εr 1.05), then plaster | 8 mm | 2.445 GHz | −19.4 dB | 48 MHz | −8.9 / −19.1 / −9.6 dB |
| 30 mm | 20 mm of dense foam (εr 1.2), then plaster | 8 mm | 2.421 GHz | −21.0 dB | 48 MHz | −17.8 / −12.3 / −5.9 dB |
| 30 mm | 20 mm of air, then plaster | 8 mm | 2.453 GHz | −18.9 dB | 48 MHz | −7.3 / −15.6 / −11.7 dB |
| 30 mm | 20 mm of air, then plaster | 7 mm | 2.453 GHz | −13.2 dB | 44 MHz | −7.0 / −11.8 / −11.1 dB |
| 29 mm | 20 mm of air, then plaster | 8 mm | 2.528 GHz | −22.9 dB | 52 MHz | −1.7 / −2.6 / −4.9 dB |
| 30 mm | 20 mm of air, no wall | 8 mm | 2.449 GHz | −15.9 dB | 44 MHz | −7.1 / −14.4 / −10.1 dB |

Then the earlier cases on a plain 1.6 mm board, for comparison:

| patch length | in front of it | feed in from the edge | best match | S11 | −10 dB band | at 2412 / 2442 / 2472 MHz |
|---|---|---|---|---|---|---|
| 29 mm | nothing | 8 mm | 2.508 GHz | −20.6 dB | 60 MHz | −2.9 / −4.8 / −8.8 dB |
| 30 mm | nothing | 8 mm | 2.432 GHz | −18.0 dB | 60 MHz | −12.8 / −15.7 / −8.2 dB |
| 30 mm | 5 mm of air, then brick | 8 mm | 2.442 GHz | **−32.5 dB** | 66 MHz | **−11.6 / −32.5 / −11.1 dB** |

**On the head's board a patch 30 mm long, fed 8 mm in, under 15 mm of light foam matches 54 Ω at
2.445 GHz**, channels 1, 6 and 11 at −9.5, −23.2 and −10.1 dB, its band 55 MHz at −10 dB. Dense foam
pulls it to 2.421 GHz; 20 mm of foam or air give much the same; lifted off the wall it moves by 4
MHz only (computed at 20 mm), so the calibration made with the head lifted holds on the wall. The
thinner board narrows the band from the 60–66 MHz of a plain 1.6 mm board, which costs the edge
channels at most half a dB of signal under light foam, 1.2 dB under dense foam until the patch is
trimmed. A millimetre of length moves the match by 75 MHz, so the foam bought decides the last
tenths — dense foam wants the patch about 0.3 mm shorter — and they are trimmed on the bench with
the feed **[open]**: 7 mm in gives 73 Ω, 8 mm 54–59 Ω, so 50 Ω lies at 8–9 mm.

**How a measurement goes.** The sender is behind the wall: an access point found by its address, or
our box. The head is pressed to the wall and moved; the optical sensors give its position, the
receivers the shadows. **The shadow is the ratio between the receivers on the same packet:**
whatever the sender does — power control, beamforming, a rate change — divides out, which is why
there is a radio for every antenna and not one radio switched between them. Between strokes, with
the head lifted, the middle calibrates the ring. Our box sends about 1000 packets a second; an
access point's beacons come about ten a second, more when one receiver joins it and pings it, as
Espressif's example does. Two senders in different directions, or the box moved once, tell **near
face from far face**: inside the brick the ray bends to at most 30°, so an object 3 cm in front of
the receiver moves its shadow by up to 1.8 cm between a sender straight behind and one at a grazing
angle, one 25 cm in front by up to 15 cm **[calc]** — not a depth, but which side's groove; the
depth comes from focusing the stroke (*The stroke as an aperture*). Each sender's direction comes
from the phase across the ring (*The electronics*). The display shows the spots over a threshold
taken against the wall's own background; a beep over a spot; a pencil mark at the notches.

## Why it should work — the numbers

**The wall** **[lit, calc]**. ITU brick (ITU-R P.2040-3) costs 22.7 dB/m at 2.44 GHz and 25.9 dB/m
at 5.5 GHz: 60 cm once through is 13.6 / 15.5 dB. Two layers of plasterboard cost 0.5 dB at 2.44
GHz, 1 dB at 5.5. Damp brick costs far more: solid brick measured at 1–6 GHz **[lit]** loses 13 dB/m
dry (εr 3.06, σ 0.014 S/m), 60 dB/m at 3 % moisture (3.6, 0.07) and 109 dB/m at 9 % (6.1, 0.166)
**[calc]** — 36 dB and 66 dB through 60 cm. In practice here a damp socket is rare, about one in a
hundred, so the dry wall is the typical case and the wet one the exception the tool must recognise
(*Wet joints*).

**The link** **[calc, `budget.py`]**. A sender of 20 dBm EIRP (the EU limit at 2.4 GHz), 3 m of air,
60 cm of ITU brick and a patch of 3 dBi (assumed) leave −40 dBm at the receiver, 55 dB over the
noise of a 20 MHz channel (noise figure 6 dB assumed) — on every subcarrier, since signal and noise
split alike. 10 m away 44 dB, through 60 cm of damp brick 32 dB. Thermal noise is not the limit;
whether the C5's int8 CSI with a fixed gain holds a 2–3 dB dip steadily is **[open]**.

**An ideal shadow** **[calc, `shadow.py`]** — how much a cylinder in homogeneous brick dims the
field 2, 5, 10, 20, 30 cm behind it (2D, exact series):

| object | 2.44 GHz, field along it | across | 5.5 GHz, along | across |
|---|---|---|---|---|
| a cable, Ø 5 mm | −5.0 / −2.9 / −1.9 / −1.3 / −1.1 dB | ≈ 0 | −5.0 / −2.9 / −2.0 / −1.3 / −1.1 | −0.4 … −0.2 |
| an empty conduit, Ø 25 mm | −3.9 / −2.5 / −1.7 / −1.2 / −1.0 | −1.6 / −2.9 / −2.4 / −1.8 / −1.5 | −45 / −10 / −6.1 / −3.9 / −3.1 | −7.1 / −24 / −13 / −7.1 / −5.3 |
| a metal pipe, Ø 32 mm | −25 / −11 / −6.9 / −4.5 / −3.6 | −9.7 / −2.8 / −2.2 / −1.6 / −1.4 | −30 / −14 / −9.0 / −5.9 / −4.6 | −11 / −6.6 / −4.8 / −3.4 / −2.7 |

A shadow is a few centimetres wide only within about 5 cm of the object; deeper it spreads, and the
phase refocuses it, as Holl & Reinhard's holography does. The cable's shadow needs the field along
the cable — hence the radial ring. Figures such as −45 dB at 5.5 GHz are single-frequency nulls at
one point.

**Drywall** **[calc, `shadow.py`]**: in the air of the cavity a Ø 5 mm cable dims the field along it
by 5.3 dB 2 cm behind it, 3.0 dB at 5 cm, 2.0 dB at 10 cm, 1.4 dB at 20 cm; a metal pipe by 24 / 9.6
/ 6.0 / 3.9 dB. A cable lying on the board is found from that side; one in the middle of a 30 cm
cavity is at the edge, and the tool goes to whichever side is nearer. An empty plastic conduit in
air shows almost nothing, only its cable. The studs are steel profiles almost always (99 % in
practice here), a strong shadow every 40–62.5 cm: they are among the things to find, the tool learns
their shadow first, and a cable within a few centimetres of one may hide in it; foil-faced
insulation blocks the light altogether.

**A real wall** **[calc, `wall_fdtd.py`, output in `wall_fdtd.out`]** — a 2D FDTD of solid brick
(290 × 140 × 65 mm, 10 mm bed joints, a collar joint in every other course of the 29 cm wall), 15 mm
of plaster each side, the wave from the far side, the field read at points 2 mm in front of the near
face. The groove 40 × 30 mm filled with plaster, the cable in its middle; the conduit Ø 25 mm in a
45 × 40 mm groove. No measured permittivity of mortar or plaster was found **[open]**: the plaster
is taken as gypsum (εr 2.5, σ 0.01 S/m) or as lime-cement like ITU concrete (εr 5.2, σ 0.09 S/m);
the mortar is bracketed by εr 2.5, 5.0 and, wet, 8.0. The code was first checked against the series:
the field 5 cm behind a cable in homogeneous brick, −3.0 dB against −2.9 dB.

At 2.4 GHz, three channels averaged (2412, 2442, 2472 MHz), the field along the cable:

| wall | plaster | mortar | joints, peak to peak | the empty groove | the cable in it, against the plain wall | against the same groove empty |
|---|---|---|---|---|---|---|
| 14 cm | gypsum | εr 5.0 | 0.7 dB | −3.1 dB | −5.6 dB | **−3.3 dB** |
| 14 cm | lime-cement | εr 5.0 | 0.4 dB | −2.1 dB | −2.0 dB | **−2.7 dB** |
| 14 cm | gypsum | wet, εr 8.0 | **5.9 dB** | −1.0 dB | −1.6 dB | −0.9 dB |
| 29 cm | gypsum | εr 5.0 | 2.1 dB | −2.9 dB | −5.3 dB | **−3.0 dB** |
| 29 cm | lime-cement | εr 5.0 | 1.8 dB | −2.1 dB | −1.9 dB | **−2.4 dB** |
| 29 cm | gypsum | wet, εr 8.0 | **8.4 dB** | −1.2 dB | −2.0 dB | −2.0 dB |

With mortar up to εr 5 the cable shows **2.4–3.3 dB below the same groove empty**, and 2–6 dB below
the plain wall: the groove itself, filled with a plaster unlike the brick, is a dip of 2–3 dB —
where the grooves are, the cables are — and the joints stay at 0.4–2.1 dB. **With wet mortar the
joints rise to 6–8 dB.** Which plaster and mortar real walls have is the first thing the trials
measure.

**The typical wall here** — lime-cement plaster, cables 2–3 cm deep — three channels averaged: a
cable 20 or 25 mm from the face shows **−3.3 dB** against the same groove empty in a 14 cm wall
(joints 0.4 dB), **−2.9 dB** in a 29 cm one (joints 1.8 dB); against the plain wall −2.4 to −2.8 dB
**[calc, `wall_fdtd.out`]**.

**Wet joints** **[calc, `joints.py`, output in `joints.out`]** — the same wall scanned along a line,
three channels at 2.4 GHz. Wet mortar, εr 8 against the brick's 3.9, gathers the wave like a light
pipe through the wall: the near face is bright over the joints and dark between them. A horizontal
cable lies along them: in its groove at a joint it stands out by 15 dB against the same groove
empty, mid-brick by under 1 dB. Evenly laid joints divide out — the scan folded over one course, its
median taken as the pattern, leaves 1 dB of the 6 — but joints 7–13 mm thick do not, from the scan
alone. A vertical cable crosses the bed joints, which are the same in every row of the map and
divide out row by row; across it lie the head joints, and in a 14 cm stretcher wall it still shows
3.0–4.4 dB against the same groove empty. A 29 cm wall's header bond cannot be drawn in 2D — its
head joints become walls through the whole thickness — and waits for 3D **[open]**. So in a wet wall
a horizontal cable can hide; but the joints' pattern itself tells a wet wall — 0.4–3 dB dry, 6–8 dB
wet — and the tool can say so.

Single frequencies, gypsum plaster, mortar εr 2.5–5.0 and once damp brick, against the same wall
without the groove:

| wall | band | joints alone, peak to peak | the cable in its groove, along | across | conduit + cable, along / across |
|---|---|---|---|---|---|
| 14 cm | 2.44 GHz | 0.2–0.9 dB | −5.2 to −5.5 dB | ≈ 0 | −7.0 to −7.7 / −0.8 to −2.4 dB |
| 14 cm | 5.5 GHz | **11–44 dB** | lost in the joints | lost | lost |
| 29 cm | 2.44 GHz | 1.1–2.5 dB | −5.4 to −8.1 dB | −0.4 to −0.8 | −6.8 to −11 / −2.1 to −2.8 dB |
| 29 cm | 5.5 GHz | 3.7–5.8 dB | −9.8 to −29 dB | −2.2 to −3.0 | −18 to −49 / −13 to −16 dB |

At 5.5 GHz the 75 mm courses are longer than the wavelength in air: in a thin wall they scatter the
wave sideways like a grating, and averaging five channels from 5.18 to 5.82 GHz still left 21 dB of
pattern; in the thick wall the loss damps the grating, and 5 GHz gives large but unstable dips — −10
to −29 dB on the mortar's value alone. **So 2.4 GHz is the band for masonry, 5 GHz a later bonus**,
once there is a dual-band patch. Not modelled: head joints, irregular joints, the third dimension.

**The head itself** **[calc, `head.py`, output in `head_depth.out`, `head_cdepth.out`]**. The
antenna board's ground plane — its copper, no plate of its own; 35 µm of copper reflects as a plate
does — is as wide as the head and a couple of centimetres from the wall. It reflects the wave back
into the wall: a standing wave stands between the copper and the wall, and a cable near one of its
nulls barely changes the amplitude. In 2D the patch cannot be drawn, so what it would see is taken
as the field along the cable in its plane, over its 29 mm; the cable against the same groove empty,
14 cm wall, mortar εr 5, 2.44 GHz; the foam as εr 1.2, tan δ 0.001 — the dense end; light foam lies
between it and air. The amplitude alone, on the typical wall (lime-cement plaster, cables 20–30 mm
from the face):

| between the board and the wall | cable 20 mm from the face | 25 mm | 30 mm |
|---|---|---|---|
| no ground plane (an antenna backed by absorber) | −3.1 dB | −3.0 dB | −2.4 dB |
| 5 mm of air | **−0.8 dB** | −2.0 dB | −2.7 dB |
| 10 mm of foam | −1.3 dB | −2.7 dB | −2.7 dB |
| 15 mm of foam | −1.8 dB | −2.9 dB | −2.5 dB |
| 20 mm of foam | −2.2 dB | −2.8 dB | −2.1 dB |
| 25 mm of foam | −2.5 dB | −2.6 dB | −1.7 dB |
| 20 mm of air | −2.1 dB | −2.8 dB | −2.1 dB |
| 20 mm of foam with 1 mm of polyethylene on its face | −2.3 dB | −2.8 dB | −2.1 dB |
| 20 mm of foam with 1 mm of polycarbonate on its face | −2.3 dB | −2.9 dB | −2.1 dB |

On gypsum plaster (εr 2.5 against 5.2) the wave stands elsewhere, and the 20 mm that suits
lime-cement nearly loses a cable 2 cm deep: −0.5 dB. With a ground plane there is always some wall
and some depth where the amplitude nearly vanishes. **The phase does not vanish with it.** The
receivers measure the complex field; the change a cable makes in amplitude and phase together, as a
share of the field — an amplitude dip of 2.5 dB alone is a 25 % change:

| between the board and the wall | gypsum, cable 20 mm | 30 mm | 40 mm | lime-cement, 20 mm | 25 mm | 30 mm |
|---|---|---|---|---|---|---|
| no ground plane | 33 % | 40 % | 37 % | 30 % | 32 % | 29 % |
| **15 mm of foam** | **29 %** | **31 %** | **43 %** | **19 %** | **29 %** | **31 %** |
| 20 mm of foam | 16 % | 37 % | 39 % | 23 % | 30 % | 30 % |
| 25 mm of foam | 3 % | 38 % | 34 % | 25 % | 30 % | 28 % |
| 30 mm of foam | 11 % | 37 % | 29 % | 26 % | 29 % | 26 % |

**15 mm of foam is taken: the spacer that keeps every cable on both plasters, 19 % at worst**
(lime-cement, a cable 2 cm deep), against 29 % with no ground plane at all; 25 mm would lose a cable
2 cm under gypsum (3 %). A hard sheet on the foam adds a tenth of a dB. An antenna backed by
absorber instead of a ground plane — as GPR antennas are, a shielded bow-tie in an absorber-lined
cavity — has no standing wave and stays the way out if the trials find 19 % too little; it costs the
absorber, and the receivers behind it on coax. So the trials measure with a ground plane behind the
antenna — foil standing in for the board's copper — and not only with bare boards.

**The stroke as an aperture** **[calc, `budget.py`]**. As the head slides, the wave scattered by a
cable reaches each receiver with a phase that turns with the head's position — the "Doppler" of the
motion. With the phase on one clock, the sender's own phase taken out on every packet by the
receivers' ratio, and the position from the optical sensors, the packets of a whole stroke add up as
one antenna as long as the stroke: synthetic aperture, as radar and GPR migrate their hyperbolas. It
asks little of the timing — at 20 cm/s the phase turns at most 3.2 times a second, 311 packets a
turn at 1000 a second — and much of the position: within λ/8 in brick, 8 mm, better 4 mm, where an
optical mouse drifts 1–2 % of the stroke, 3–6 mm over 30 cm **[open]**. What it gives is focus: the
shadow of a deep object pulled sharp again, and its depth — for an object 3 cm deep a stroke of 20
cm focuses to about 6 mm in depth, of 30 cm to about 2 mm; 10 cm deep, to 6 and 3 cm (4λ(d/A)²,
rough).

## The electronics

The electronics are assembly; what is hard is in the physics (*Known and not known*).

- **Two boards, and no coax** **[calc, `budget.py`]**. **The antenna board carries the radios too,**
  as ESPARGOS's sensor board carries its eight ESP32-S2 chips beside their antennas **[lit]**. An
  ordinary 4-layer board, 1.6 mm (JLCPCB's 7628 stack-up: 0.2 mm, 1.065 mm, 0.2 mm **[sheet]**), all
  its parts on the back, so a machine assembles it in one pass:
  - layer 1, facing the wall: the patches;
  - layer 2: empty under them;
  - layer 3: an unbroken ground — the patches' ground and the shield against the room behind the
    operator;
  - layer 4, the back: each ESP32-C5 right behind its patch, its match a few millimetres from a via
    that goes straight up through the board to the patch's feed point. The via is the probe: no coax
    and no connector, nothing whose phase moves when the head is handled. The 50 Ω trace there is
    0.38 mm wide over layer 3. The oscillator, the clock buffer and its star, the eight microphones
    and the two optical sensors (each over a hole through the board, the foam and its sheet) are on
    this layer too — the sensors there look at the wall from 17 mm and their own height, inside
    their 15–35 mm.

  Between layers 1 and 3 lie 1.28 mm of FR4, not 1.6, so the patch is cut for that (*The match*).
  **The electronics board** sits 11 mm behind, on a 2 × 25 pin header, with no RF on it: the H7A3,
  the power, Datel's drive and its disc, and the display on top. Through the header: eleven UARTs
  (22 lines), one shared EN and one shared boot line, the microphones' clock and four data lines,
  the optical sensors' SPI (five lines), the 48 MHz clock for the H7A3, the antenna board's 3.3 V,
  and ground. Whether the bare chip can be had for machine assembly is **[open]**; the 0.4 mm pitch
  of its QFN and the 0201 parts of its match are not for a hand iron.
- **The receivers:** eleven ESP32-C5 — nine in the ring, two on the crossed pair. For the trials,
  Seeed XIAO ESP32-C5 boards (21 × 17.8 mm, a U.FL socket, about $7 **[sheet]**); for the head, the
  bare chip with its flash inside, the ESP32-C5HF4 (QFN48, 6 × 6 mm, 4 MB **[sheet]**), since the
  shared clock replaces the crystal a module carries. Each then needs its own RF match (Espressif's
  checklist: a CLC network close to the chip, 0201 parts, 50 Ω traces **[sheet]**), which goes
  straight to its patch's via (above). The ESP32-C5 is Espressif's dual-band Wi-Fi 6 chip (2412–2484
  and 5180–5885 MHz, no 6 GHz) and its best CSI chip: int8 I/Q, 242 subcarriers in HE20 **[sheet]**.
  The receive gain is fixed with Espressif's `esp_csi_gain_ctrl`, or the AGC would lift a shadowed
  packet back up. Each module computes its CSI and reduces it before sending: raw HE20 CSI with its
  legacy part is about 640 B a packet, and eleven modules at 1000 packets a second would make 7.0
  MB/s **[calc]**; averaged over 16 groups of subcarriers on the module, the report is about 0.4
  Mbit/s a receiver **[calc]**.
- **The rest — one processor for everything but the radios: an STM32H7A3.** Cortex-M7 at 280 MHz
  with a double-precision FPU, about 1.4 MB of RAM, an 8-channel DFSDM plus a 2-input DFSDM2, a
  PSSI, two SAIs, six SPIs, two 16-bit ADCs, three 12-bit DAC channels, two op-amps, an LCD-TFT
  controller with Chrom-ART, and no radio of its own **[sheet]**. It collects the eleven reports,
  fuses the position, runs the acoustic head and draws the display. Its load, at half a
  multiply-accumulate a cycle **[calc, `cpu.py`]**: a phase image of 50 × 50 points from eleven
  receivers and 64 groups of subcarriers 25 %, the stroke's focusing back-projected from a tenth of
  the packets 8 %, the amplitude map 1 %, the acoustic lock-in 2 %, the band energies 5 % — 40 % all
  at once.
- **The links:** each ESP32-C5 on a UART of its own — the C5's UART runs to 5 MBaud, the H7A3 has
  ten U(S)ARTs to 10 Mbit/s **[sheet]**. A reduced report of 0.4 Mbit/s needs about half a megabaud,
  so the eleventh goes on the H7A3's low-power UART, which a forum reports at tens of Mbit/s from a
  fast clock **[lit]** (an SPI if not). The microphones go on the DFSDM. **Flashing the eleven:**
  the C5's ROM loads a program over UART0 when GPIO28 is held low at reset, with GPIO27 high
  **[sheet]**; one shared EN line and one shared boot line let the H7A3 put all eleven into the
  loader at once and send the same image down all eleven UARTs together; the H7A3 takes its own
  program and theirs over USB. **One clock for the processor too:** the clock buffer's twelfth
  output drives the H7A3's HSE input (4–50 MHz **[sheet]**), so the microphones' clock, the knock's
  timer and the radios all count the same 48 MHz.
- **The display:** a 5″ 800 × 480 TFT with an SSD1963 controller and its own frame memory, on an
  8080-style parallel bus, which the H7A3's FMC drives as a memory bank — so no frame buffer in the
  H7A3's RAM (773 Kč, about €31, sold for Arduino **[sheet]**). **Not a phone:** it would have to be
  kept in flight mode a hand's width from the antennas, and the tool would hang on an app for every
  phone; a 5″ panel is cheaper than that. A beeper, buttons.
- **Two optical-flow sensors** that work 15–35 mm from the surface — a mouse's sensor wants it
  within a couple of millimetres — such as the PixArt PAA5100JE on SPI, 242 frames a second, up to
  1.14 m/s at 25 mm, 6 mA **[sheet]**; how far they drift over plaster is **[open]**.
- **Power** **[calc, `budget.py`]**: the eleven C5s receiving 87 mA each by the datasheet, taken as
  100 mA with their CSI work, the H7A3 64–133 mA, the rest small — 4.2 W at 3.3 V, with the display
  (assumed 1.5 W) 5.7 W. **Pajok** is two 18650 cells in parallel: about three hours. At one cell's
  voltage, 3.0–4.2 V, there is nothing to balance; a one-cell charger fills them over USB-C; at
  their end they give 2.2 A, 1.1 A a cell. Two buck-boost converters make the 3.3 V — TI's TPS63021,
  fixed 3.3 V, 2 A from 2.5 V up, switching at 2.4 MHz **[sheet]**. One feeds the antenna board (1.1
  A, 1.5 A while a C5 sends), one the rest (0.6 A with the display); both sit on the electronics
  board, behind the antenna board's ground.
- **Each C5 by Espressif's checklist** **[sheet]**: 10 µF on its analog rail, 1 µF and 0.1 µF on its
  I/O rails, 10 kΩ and 1 µF delaying CHIP_PU, a pull-up on GPIO28, and a supply good for at least
  600 mA for one chip. That is a peak, not the 87 mA it draws listening, so eleven on one 2 A
  converter must not start their radios together: the H7A3 starts them one after another over their
  UARTs, and the RF calibration each runs at its start **[sheet]** falls on one at a time. Once they
  run, the shared boot line can carry one start edge to all eleven — a strapping pin is an ordinary
  pin after reset **[sheet]**.
- **One clock for all eleven — the phase from the first build.** A module with its own crystal
  cannot compare phase with its neighbours, so the eleven C5s run from one 48 MHz source through a
  fan-out buffer: the same frequency on every chip and no drift between them; a common start on one
  clock edge lines up their timing. The clock goes as a star on the antenna board's back: the
  oscillator and the buffer beside Datel's hole in the middle, and from the buffer one branch to
  each chip, each driven from its own output and terminated at the source; the branches are
  meandered to the longest one's length, all on the same layer, with the meander's turns far enough
  apart not to shorten it. The buffer can be TI's CDCLVC1112: one LVCMOS input, twelve outputs, 50
  ps between them, under 100 fs of added jitter **[sheet]** — eleven for the C5s, the twelfth for
  the H7A3. A millimetre of trace is 6–7 ps, which the PLL turns into 5–6° of the 2.44 GHz carrier
  **[calc, `budget.py`]**: the skew itself is calibrated out; equal lengths on one layer make it
  drift alike. Whether the ESP32-C5 runs from an external clock is **[open]**, and decides the
  board: its datasheet calls XTAL_P/N the input for a crystal *or oscillator*, Espressif's checklist
  calls the crystal compulsory — 48 MHz only, within ±10 ppm, more than 500 mV at the pins, a 24 nH
  inductor in series on XTAL_P **[sheet]**, and nothing on a clock fed in — and says the same of the
  ESP32-S2, which ESPARGOS clocks from one source. The board above is drawn for bare chips fed so; a
  dev board with its crystal taken off and the clock fed in answers it first **[open]**.
- **Plan B, if the C5 will not run from an outside clock: a raw I/Q radio.** The receiver need not
  speak Wi-Fi; it needs the signal. Microchip's AT86RF215IQ gives 13-bit I/Q at up to 4 MS/s over
  LVDS, at 2.4 GHz and below 1 GHz, from a 26 MHz TCXO or crystal **[sheet]** — so one shared
  reference is its ordinary use. Eleven of them would feed a small FPGA, as the open CaribouLite
  board pairs one with an iCE40 **[lit]**. The price: our own sender only — a known tone or chirp,
  anywhere in the band, 4 MHz at a time — so no access point and no 5 GHz; RF layout of our own; and
  an FPGA. Bluetooth direction-finding chips (nRF52833 and the like) give I/Q only during a packet's
  tone extension, 16–160 µs **[lit]**, narrower still.
- **What one clock does not fix** **[lit]**. A packet's CSI phase carries three errors: the carrier
  offset turns the whole packet by a random angle, the timing offset tilts it across the subcarriers
  (both removed by fitting a line), and the PLL's starting phase — which ESPARGOS found changes
  after every reset and every change of channel, "every time the PLL has to acquire a new frequency
  lock". One clock and one start edge keep the chips together in time, but each PLL still locks at
  its own phase. The amplitude carries none of these errors and stays the robust fallback; only the
  gain must be fixed.
- **The phase reference as ESPARGOS does it — not taken here.** There each receiver's RF switch
  alternates between its antenna and a reference — Wi-Fi frames from one more chip, split to all
  receivers by a resistive divider — and every receiver is re-calibrated against it after each
  retune and as the temperature drifts; ESPARGOS published no residual error and no calibration
  interval **[open]**. But a switch in every receiver's path has its own loss and phase, unequal
  from part to part and drifting with temperature — in an instrument, one more thing to calibrate.
- **The calibration over the air — the one taken, with no switch anywhere:** the crossed pair in the
  middle sends short frames, one feed and then the other. It is equally far from all nine, so the
  paths agree by symmetry and each receiver's offset falls out, its antenna and feed included; every
  radial patch gets at least half the power (−3 dB) from one of the two feeds, and its phase follows
  its angle, which is known. The receivers stay linear and radial, as the shadow needs. Then each
  chip sends in turn and the others listen: the paths are the same both ways, so pairs of
  measurements cancel them, as large MIMO arrays are calibrated. Whether the C5 keeps its phase
  between sending and listening on one channel is **[open]**; between strokes the head is lifted
  anyway, and lifted or on the wall the patch's tune moves by 4 MHz (*The match*). The distances
  need not all be equal — in a plane only three points can be — but they are known: 65.8 mm from the
  middle to each, 45.0, 84.6, 113.9 and 129.6 mm between ring antennas, each class alike by
  symmetry; a millimetre of path is 2.9° at 2.44 GHz, the board places the antennas to about a tenth
  of one, 0.3°, and sending both ways cancels the paths altogether **[calc, `array.py`]**.
- **Fonar, the sender box:** two ESP32-C5 boards (XIAO, as for the trials), one for each
  polarization, each with its own plain dipole on a pigtail, held at right angles, both parallel to
  the wall — one upright, one level. They take turns, 500 frames a second each, one wire between
  them saying whose turn it is; every frame carries which antenna sent it and a counter. The frames
  are ESP-NOW, as Espressif's `csi_send` example sends them for CSI **[lit]**, up to 1470 bytes
  **[sheet]**. No switch, no RF layout, nothing to calibrate: whatever the sender does divides out
  of the ratio between the receivers on the same packet, and only its polarization counts — which
  the frame names. The head talks back over the same ESP-NOW: channel, start, stop. A USB power bank
  feeds it; its power is set so that with the dipole's gain it stays within 20 dBm EIRP. Whether its
  frames can go out at an HE rate — the 242 subcarriers — or only at legacy OFDM's 52 is **[open]**.
- **The body** **[calc, `budget.py`, rough]**: the head 167 mm across. The foam weighs about 15 g,
  its sheet 21 g, the two boards 130 g, the cells 94 g, the display about 100 g — about 0.36 kg
  before the housing; the cells go in the handle. The 5.7 W leave through the back and the rim,
  about 13 K over the room outside and more inside, with no fan; the boards warm for a while after
  switching on, and the calibration between strokes follows them.

## For masonry: sound in the middle

The free middle of the ring takes an acoustic head for masonry. Not for drywall: sound does not
cross the air cavity. **Only the exciter touches the wall; the receivers are microphones that hear
it through the air** — in the head through pipes that open at the wall's face — as the
professionals' contactless systems do **[lit]**:

- Groschup & Grosse (TU München, 2015): 35 MEMS microphones on one board, 20 mm above concrete, a 9
  mm steel ball as the hammer; the array picked the slab's resonance out more clearly than a
  measurement microphone, as clearly as an accelerometer.
- Gucunski et al. (2016): a hexagon of six air-coupled microphones around a central solenoid hammer,
  scanning bridge decks for delamination.
- Zhu & Popovics: air-coupled sensors hear the surface waves that leak from the solid into the air,
  with sensitivity comparable to contact sensors; Song & Popovics (2019) imaged near-surface damage
  in concrete with a MEMS ultrasonic microphone array, entirely without contact.

**The exciter** — a tap, a piezo knock, or a tone:

- **The tap.** A steel ball's contact time sets how high it reaches: a 9 mm ball about 39 µs and 32
  kHz, a 3 mm ball 13 µs and 97 kHz (on concrete; plaster is softer and slower) **[lit, calc]** —
  for hollow plaster, and for the groove's depth with a small ball. A 9 mm ball tapped at 1 m/s
  brings 1.5 mJ **[calc]**.
- **The knock.** A piezo disc pressed through a tip, its voltage switched on hard, held, and
  switched off hard, a few times a second: each edge is one broadband knock, the hold time does not
  matter. It is far weaker than the ball: ½CV² is the electrical energy of an edge — 5.3 µJ at 15 V
  on a 47 nF buzzer, about 14 µJ in a professional point-contact probe, the ACS S1802 **[calc]** —
  and only part of it reaches the wall. The edge's speed sets how high the knock reaches: for a ~47
  nF buzzer, 10 Ω in series reach about 340 kHz, 100 Ω 34 kHz, 1 kΩ 3.4 kHz **[calc]**. In a linear
  wall a slow knock's answer is the fast one's, low-passed — a filter in software gives the same —
  so a slow edge helps only where the high part does harm: the disc's own high ringing, the click
  through the air. The disc's own resonances (2.6 kHz for a 27 mm buzzer, 45 kHz for a 50 mm disc
  **[sheet]**) decide what comes out strongest.
- **The tone.** A 40 kHz bolt-clamped transducer from an ultrasonic cleaner, sold as 50–60 W and
  driven at a few watts **[sheet]**, with a steel or aluminium rod 6.3 cm long — half a wavelength
  at 40 kHz **[calc]** — that keeps it in tune and touches the wall at one rounded point. Sent as
  bursts, or as a chirp, so that arrivals can be told apart.

**Run by the main processor, on one clock.** The acoustic head is not run by the ESP32-C5s but by
the STM32H7A3 (*The electronics*), which drives the exciter and listens, so the exciter and every
microphone run on one clock.

- **Digital microphones, not an analog front end.** PDM MEMS microphones share one clock line, two
  on each data line: they are sampled at the same instant by construction, with no multi-channel ADC
  and its anti-alias filters. A part that exists: Knowles SPH0641LU4H-1, bottom port, an ultrasonic
  mode at a clock of 3.072–4.8 MHz, SNR 64.3 dB(A) **[sheet]** — an audio-band figure; its noise at
  40–80 kHz is not published **[open]** — sold on breakout boards as 100 Hz–80 kHz **[sheet]**. The
  H7A3 takes PDM directly: the DFSDM (8 channels) or the SAI in PDM mode (up to six microphones
  each, by ST's forum **[lit]**), set up in ST's AN5027 **[sheet]**. Not every MCU reaches the
  ultrasonic clock — the nRF5340's PDM stops at 1.333 MHz, by Nordic's forum **[lit]**.
- **Reading them and what is computed.** Each PDM line can come in through the DFSDM or the SAI,
  which decimate in hardware, or through a plain SPI whose clock is the microphones' clock — the bit
  stream then filtered in software (ST's AN5027 covers all three) **[sheet]**. The DFSDM is the
  documented way (an 8-microphone array on an STM32H743 is reported on ST's forum **[lit]**); the
  PSSI, the H7A3's parallel 8/16-bit input, could take eight or sixteen microphone lines in one
  clock and leave the bits to be sorted in software — nobody has published it **[open]**. No heavy
  audio analysis is needed: for a knock, the energy in a few wide bands in a time window after it;
  for the tone, a lock-in — each microphone's samples multiplied by the processor's own sine and
  cosine and averaged — which gives amplitude *and* phase for two multiplications a sample. Phase is
  free here because the processor makes the tone itself.
- **Two independent knobs** for the knock: the **voltage** sets how far the disc moves — its
  strength — from a small boost converter (3.3 V up to 5–30 V); the **edge** sets how high its
  spectrum reaches, by the resistor in series (a few, each with its own transistor, chosen by the
  processor) timed by a hardware timer. The electrical energy, ½CV² an edge whatever the resistor,
  stays in milliwatts at most, no heatsink **[calc]**. Tone bursts and chirps come from the H7A3's
  own 12-bit DAC through an external amplifier — its on-chip op-amps cannot drive a 47 nF disc, 85 Ω
  at 40 kHz **[calc]**, let alone the cleaner transducer.
- **Divide, do not regulate — by what is already there,** no sensor on the exciter. *When* it
  knocked is the timer's own edge: the disc's delay behind its voltage is the same every knock, and
  the delays across the ring need no start at all. *How hard* it knocked — the head pressed harder,
  the disc warmer, the battery lower — is the same for all eight microphones, so each is divided by
  the ring's median, as the radio divides its receivers by each other; what is left is where the
  wall answers differently on one side. For the tone exciter, later, its drive current through a
  small resistor shows what went in, and its phase against the voltage where the stack resonates.

**Datel in the head** **[calc, `acoustics.py`]**:

- **The exciter for the first build is the knock:** a plain buzzer disc under the electronics board,
  a hard plastic rod glued to its centre, through the hole in the middle patch to the wall, about 28
  mm. **The disc sits on a ring of soft foam,** and the foam holds the rod on the wall: the disc
  itself is far too stiff for that — at least 20 N a millimetre at its centre, so the 0.05–0.15 mm
  the spacer's foam gives under the hand would put 1–3 N on the rod, where a millimetre of acetal 28
  mm long buckles at 0.5–1.9 N **[calc]**. On foam of 0.5 N a millimetre, pressed 2 mm, the rod
  rests on the wall with about 1 N, and the spacer changes that by a fifteenth; the rod is **2 mm
  thick** (it buckles at 7.6–30 N), slides in its hole through the board, the foam and the sheet,
  and its rounded tip, just out of the sheet, drags on the wall as the head slides. On its foam the
  disc knocks against its own mass, as an inertial exciter does, above about 80 Hz **[calc, assumed
  foam]**; along its length the rod rings at 26, 53 and 79 kHz, the same every knock. Small, cheap,
  broadband. Plastic is softer than steel, so the contact lasts longer and the knock reaches less
  high — how high, trial P3 shows. A rod on the wall scrapes as the head slides, so **Datel listens
  with the head held still** for a moment; the radio scans while it moves. The 40 kHz stack comes
  later if the bursts prove worth it (trial P4): through plastic its half-wave rod would be 1.8 cm
  of acetal or 2.1 cm of PEEK, lossy; 6.3 cm of aluminium otherwise.
- **The drive**, the two knobs above made concrete: a small boost from 3.3 V to 15–30 V, a
  transistor to charge the disc through one of three resistors (10 Ω, 100 Ω, 1 kΩ), one to discharge
  it, a hardware timer of the H7A3 to time them. Nothing measures the knock itself (*Divide, do not
  regulate*).
- **The microphones:** eight PDM microphones on a ring around the tip, 25–45 mm out, in the annulus
  left free between the middle patch and the ring's patches (18–48 mm). There the wall's surface
  wave arrives after 14–59 µs and the sound through the air after 73–131 µs, so the two are apart in
  time. Each sits on its own island of the antenna board's back, over a hole through the board, and
  hears the wall through that hole and a pipe through the foam and its sheet, 16.6 mm together
  (*Sound pipes*, below). On the H7A3's DFSDM: four data lines, two microphones on each, one clock.
- **The middle hole** carries the rod alone. The pencil marks by notches on the head's rim, two
  pairs on its two axes: a spot under the middle lies where the lines between opposite notches
  cross.

**What it hears** **[lit, calc, `acoustics.py`]**:

- Surface (Rayleigh) waves at 40 kHz have a wavelength of 1.9–4.6 cm in brick and reach about one
  wavelength deep — the depth of a plastered groove.
- Fired clay brick carries P-waves at 1430–3100 m/s, a masonry panel with its joints 1584 m/s; shear
  waves about 0.6 of that, surface waves about 0.92 of shear. Every wall is measured first, by the
  delay across the ring.
- Sound straight through the air from the exciter travels at 343 m/s, slower than any wave in the
  brick: after a knock or a tone burst the ring of microphones tells it apart by its arrival; a
  continuous tone cannot, and leans on the foam. A collar of absorbing foam around the exciter's rod
  and around each microphone's pipe damps it — as the professional enclosures do with foam and
  baffles.
- **A void reflects everything with the sign inverted** (brick has 5 900–12 800 times the acoustic
  impedance of air); a flat face of copper reflects 0.78–0.89 with the same sign; mortar at most a
  third — the joints that make a grating for 5 GHz radio are weak mirrors for sound. These hold for
  faces larger than the wavelength, 2–5 cm: a conduit's hollow or a pipe answers by its sign; a
  cable a few millimetres across is a small scatterer and answers weakly, whatever its metal.
- What the microphone hears is the surface's motion: 1 nm at 40 kHz radiates 74 dB SPL, 0.1 nm 54 dB
  **[calc]**, against a microphone noise of about 30 dB SPL in the audio band **[sheet]**. How far
  the wall moves a few centimetres from the exciter is **[open]**.
- The microphones listen a few centimetres from the exciter, not at it: there its own ringing would
  cover the wall's answer, unless the pulse were shorter than the echo — 30–73 µs from 3 cm
  **[calc]**.
- **Sound pipes** **[calc, `acoustics.py`]**: the microphones sit on the antenna board's back and
  hear the wall through pipes across the board and the foam. One 1–2 mm across carries a single
  plane wave up to 100–200 kHz and loses 0.5–1.5 dB a centimetre to its walls; its length rings at
  odd quarter-waves — the head's 16.6 mm, closed at the microphone, at 5, 15, 26, 36 kHz and on —
  fixed and alike in all eight, so divided out with the ring's median, or damped by a fine mesh in
  the pipe. The microphone's own port is a fraction of a millimetre; the pipe narrows to it.
- Hollow plaster is what the tap finds best.
- No attenuation figure for brick at 25–100 kHz was found **[open]**; over a few centimetres it
  should not limit.

## Heat: what has carried current shows through the plaster

**Postponed:** not in the head for now — a thermal camera held beside it does the same — and the
sensor below can come back later.

A cable under load warms the plaster over it, an overloaded or undersized one most of all. It needs
no transmitter, and it tells what the shadow cannot: which cable has carried a heavy load for an
hour or more. Computed **[calc, `thermal.py`]** for a 2D section through 29 cm of solid brick, still
room air on both faces, a steady load (CYKY is the Czech PVC-sheathed installation cable, like NYM):

| | heat in the cable | the plaster over it, cable 25 mm deep |
|---|---|---|
| CYKY 3 × 1.5, one phase, 10 A | 2.7 W/m | +1.4 K |
| CYKY 3 × 1.5, one phase, 16 A | 6.9 W/m | +3.7 K |
| CYKY 3 × 2.5, one phase, 16 A | 4.2 W/m | +2.3 K |
| CYKY 5 × 4, three phases, 25 A | 9.7 W/m | +5.1 K |

Per watt a metre the rise is 0.67 K with the cable 15 mm deep, 0.53 K at 25 mm, 0.44 K at 35 mm, in
a band 8, 11 and 14 cm wide at half height. Half of it comes in 0.7 h, 90 % in 7 h. So a cable that
has carried 10 A for an hour or more stands out well above a cheap sensor's noise; one that carries
5 A gives a third of a kelvin, about what a wall's own patchiness gives **[open]**. The same picture
shows heating and hot-water pipes, underfloor heating, a cold-water pipe while it runs, and damp
patches, which evaporation keeps cooler.

- **The sensor: Waveshare's long-wave 80 × 62 module** **[sheet]** — I²C for its registers, SPI for
  the data, up to 25 frames a second, NETD 150 mK, 45° or 90°, 5 V at 61 mA, about $96. At a metre
  with 45° it sees 83 cm of wall, a centimetre a pixel **[calc]**. A frame is 10 kB. Inside is
  Meridian Innovation's SenXor MI0802 with its MI48 processor, shutterless **[sheet]**; its sibling
  MI0801 with the MI48 is sold on Midas's MTP-8062 board (LCSC), and Meridian announced a
  cost-optimised 50 × 50, the Cheetah — a cheaper source is likely, not yet priced **[open]**.
- **How it is used:** from a metre or two away, before the head goes onto the wall — an overview of
  where the warm lines run, then the head over them. Pressed to the wall it sees nothing: too close
  for its lens, and the head's own warmth is in the way. Should it come back into the head, it needs
  an opening of its own beside the middle, which is Datel's; most plastics are opaque at 8–14 µm.
- **Bands, not spots:** the search starts where a cable must start — a socket, a switch, a box — and
  follows the warm band that leaves it, mostly straight up, down or along. A band is a line; a
  wall's own spots (anchors, damp, a radiator's glow) are blobs. The tool draws the band's middle as
  a line over the picture. The band is about 11 pixels wide at a metre, so a fit finds its middle
  far finer than a pixel: 3 mm from one frame for a 3 × 1.5 cable at 10 A, 1.3 mm at 16 A
  **[calc]**, the cable 25 mm deep, the sensor's own noise only — in the picture; the pencil mark
  comes from the head on the wall. The tool works from one picture, with no before-and-after
  difference; how a wall's own spots compare with a cable's band is **[open]** (the trials).
- **What it does not do:** see a cable without current, or give the conductor's temperature — the
  plaster's rise is a small part of it. A cable warmer than its neighbours is a reason to call an
  electrician, not a measurement.

## What it stands on

The figures in this table are as published **[lit]**.

| work | what it showed | what is taken |
|---|---|---|
| ESPARGOS (Univ. Stuttgart) | eight ESP32-S2 on one 40 MHz clock and a 2.4 GHz phase reference: phase-coherent CSI | the shared clock and the chips on the antennas' board; their switched reference was weighed and the calibration over the air taken instead |
| WiProfile (MobiCom 2024) | the shadow of an object between two Wi-Fi cards at 5.3 GHz; outline within 1 cm | dividing the CSI by a reference channel; inverting the diffraction |
| Holl & Reinhard (PRL 2017) | a hologram from an ordinary router at 5 GHz; a metal cross from its shadow | phase-referenced back-propagation; subtracting the unshadowed field (the dark-field step) |
| Supélec planar camera, 2.45 GHz | a plane wave on one side, a 32 × 32 receiving array right behind the object | the dense array pressed behind the object |
| SiWa (MobiCom 2021) | a UWB radar module on a Raspberry Pi swiped on the wall: rebar and pipe to 10 cm, median error 0.2–0.7 cm | the bar to beat; the model for a later one-sided radar |
| RASCAN (Bauman Univ.) | holographic radar 1.6–6.8 GHz, wires in concrete, to 35 cm | the bar to beat |
| MIRA A1040, Pundit 250 Array | ultrasonic arrays on concrete, 40–50 kHz, dry point contact; Politecnico di Milano reads the echoes by their sign | reading void and metal by the echo's sign |
| Groschup & Grosse; Gucunski et al.; Song & Popovics | MEMS microphones above concrete, a tapping or ultrasonic exciter: delamination and near-surface damage without contact | the acoustic head: one exciter touching, microphones in a ring |

A related idea at a larger scale is the KrakenSDR passive radar: five cheap receivers on one clock,
phase-aligned by a built-in noise source, tracking aircraft by the light of FM and DVB-T **[lit]**.

## Why not … — the paths looked at and left

- **Buy one?** See *What it is for*: the good ones keep their firmware and their raw data closed,
  and what reaches further costs a car.
- **A cheap 24 or 60 GHz radar module?** The cheapest give presence firmware and no raw data; those
  with raw data and several antennas (Infineon BGT60, TI IWR6843, Acconeer A121) work at 60 GHz,
  where 10 cm of concrete costs 162 dB there and back **[calc]** (brick is not tabulated that high).
  Behind drywall alone they might see — 12.5 mm of plasterboard costs 9.9 dB there and back
  **[calc]** — but SiWa found 24 and 77 GHz radars did not get into its walls **[lit]**; for drywall
  a trial worth having, for masonry no.
- **A UWB chip, with more antennas and more bandwidth?** Qorvo's DW3220 has two antenna ports and
  gives each one's channel impulse response, the angle to about ±5° **[sheet]**, at 6.5 or 8 GHz,
  500 MHz wide — a nanosecond's resolution. But brick costs 27 dB/m there, and the joints, against a
  wavelength in brick of 19–23 mm, scatter worse than at 5.5 GHz (*A real wall*) **[calc]**. Kept
  with the later one-sided radar, as SiWa's was UWB.
- **A one-sided radar first?** The surface reflection and the transmitter's leak are far stronger
  than a cable's echo; separating them needs gigahertz of bandwidth and a coherent front end. Cheap
  SDRs struggled with exactly that (LimeSDR Mini: leak and instability **[lit]**). SiWa shows a UWB
  module works to 10 cm; it is kept for later.
- **One Wi-Fi chip as a radar?** It cannot listen while it transmits; the echo from the back of 60
  cm brick returns after 7.9 ns **[calc]**, the switch takes microseconds.
- **Depth from the delay?** One way through the wall the delay resolves c/B: one 20 MHz channel 15 m
  in air; the ESP32-C5's EU 5 GHz channels stitched together 43 cm in air, 22 cm in brick
  **[calc]**. Which face a cable lies under comes from the shadows' parallax, and how deep from
  focusing the stroke (*The stroke as an aperture*).
- **Stitching channels on unsynchronised chips?** Every retune starts the PLL at a random phase
  (ESPARGOS); MIT's Chronos needed packets exchanged both ways to cancel the offsets; a 2025 thesis
  at TU Berlin could not reproduce channel-stitched ranging on the ESP32 or the Intel AC9260
  **[lit]**.
- **The nRF7002?** It takes an external TCXO **[sheet]**, but its raw samples come only from the
  radio-test firmware, and every chip needs a host. The ESP32-C5 gives CSI officially.
- **An SDR transceiver (LMS7002M, AD9361)?** Fine-pitch or BGA, an FPGA; the LMS7002M stops at 3.8
  GHz **[sheet]**. Kept for the later radar.
- **Bluetooth direction finding?** Its receivers switch antennas within one packet, so the IQ
  samples are phase-coherent — but only from a sender that adds the direction-finding tone, which no
  access point or phone in the building does, and over one 2 MHz channel, where the wall's pattern
  cannot be averaged over frequency.
- **The sender's direction from arrival times?** Across the ring a wave arrives at most 0.43 ns
  apart **[calc]**; the C5 samples every 50 ns, stamps packets to the microsecond, and each module
  runs on its own crystal **[sheet]**. The direction is in the carrier's phase — 1° is 1.1 ps, 0.34
  mm of path **[calc]** — and that needs one clock and the calibration (*The electronics*); noise
  allows far under a degree, multipath and calibration leave one or two (ArrayTrack 1.3° **[lit]**).
  Inside the brick the ray bends to at most 30°, so even a sender up by the ceiling moves a shadow 3
  cm deep by under 2 cm, and a few degrees are enough.
- **Locating the tool from the signal alone?** The best Wi-Fi angle, ArrayTrack's, is about 1.3°
  **[lit]**: 2.3 cm at 1 m from the sender, 11 cm at 5 m **[calc]**. Optical-flow sensors cost
  little and do better.
- **A phone as the display?** It would sit in flight mode a hand's width from the antennas (*The
  electronics*).
- **5 GHz alone in masonry?** A thin brick wall's joints act as a grating there (above).
- **A higher frequency for thin cables?** 20 or 60 GHz does not cross masonry, and is not needed: 2
  cm behind a cable 2.4 GHz gives −5 dB along it, 5 cm behind −3 dB **[calc]**.
- **The middle of a 45–60 cm wall?** A cable there dims the field at the near face by about 1 dB
  **[calc]**, smeared over decimetres; radar tomography of 76 cm masonry resolved only anomalies of
  10 cm and more **[lit]**. Out of scope.
- **Ultrasound alone?** It cannot cross drywall's cavity.
- **Contact tips on every acoustic receiver?** Not needed: microphones a few millimetres to 2 cm
  above the wall hear the leaky surface waves, as the contactless systems show. Only the exciter
  touches.
- **The cheap 40 kHz air transducers (HC-SR04 and the like) pressed to the wall?** Matched to air,
  narrow-band, ringing long. As receivers *in the air* above the wall, with a 40 kHz tone, they
  might serve — unmeasured.
- **Patches pressed straight onto the wall?** They detune by 9–18 % (above); 5 mm of air keeps them
  within about half a percent, and the standing wave sets the spacer at 15 mm.
- **A square of nine?** One polarization only, or two at 50 % in the worst case, and no free middle
  (*The head*).
- **Circular polarization on every receiver?** Every cable angle is seen, but only part of the field
  along the cable: a −5 dB shadow shows as −1.8 dB at worst, where the ring of radial patches keeps
  all of it **[calc, `array.py`]**.
- **One chip with several receivers?** Chips with two or more receivers are made for speed, for
  laptops and routers, and sit on PCIe or SDIO with a Linux host; the small ones for
  microcontrollers have one. NXP documents CSI for its 2 × 2 chips only under Linux **[sheet]**, and
  Espressif's first 2 × 2, the ESP32-E22, does not document CSI yet **[sheet]**; the H7A3 has no MMU
  for the Linux they want. Router chips, four to eight receivers in step, keep their CSI behind SDKs
  and NDAs or research patches on older parts **[lit]**, and want watts and room. Revisited when a
  two-receiver chip gives CSI to a microcontroller.
- **An ordinary camera for an overview?** It shows what the eye sees; a photo of the wall for the
  customer is a phone's job.
- **A finer thermal camera, 160 × 120 or more, for a sharper line?** The wall blurs the warmth into
  a band 8–14 cm wide **[calc]**, whatever the sensor; at a centimetre a pixel the line is already
  found to millimetres in the picture. A finer sensor would see a whole wall from further back at
  the same centimetre a pixel — a matter of price, not of the line.
- **The cheaper Melexis MLX90640?** 32 × 24 on I²C, £50 on a Pimoroni breakout **[sheet]**; at 55°
  it gives 3.3 cm a pixel at a metre **[calc]**, the band only 3–4 pixels wide.

## Known and not known

- **From datasheets:** the ESP32-C5's bands, CSI format, gain control, antenna switching, its
  loader; the module's crystal; the nRF7002's TCXO input; the H7A3's peripherals; the clock buffer,
  the converters, the board's stack-up.
- **Computed, to be measured:** every shadow above; the ring's polarization coverage; the patch
  against the wall and its match; the ultrasonic timings; the warmth over a loaded cable.
- **Open, for the Wi-Fi:** the permittivity of mortar and plaster — wet mortar raises the joints'
  pattern to 6–8 dB and can hide a horizontal cable (*Wet joints*); how damp walls are at socket
  height; head joints and joints that are not regular, in 3D; the standing wave between the board's
  ground and a real wall (*The head itself*); how the microphones are best kept quiet on the board;
  how much of an access point's field arrives with the other polarization; whether int8 CSI with a
  fixed gain holds steadily a change of 20–30 % — a dip of 2–3 dB, or the same in phase; whether the
  ESP32-C5 runs from an external clock, keeps its phase between sending and listening, and how long
  a calibration holds; how far the optical sensors drift over plaster; the patch's last tenths of a
  millimetre on the bench, and a dual-band patch for 5 GHz; whether the bare ESP32-C5HF4 can be had
  for machine assembly.
- **Open, for the sound and the heat:** how a 2 mm plastic rod on foam couples to plaster, and how
  high its knock reaches; how far the wall's surface moves a few centimetres from the exciter; the
  SPH0641LU4H-1's noise at 40–80 kHz and whether its ultrasonic mode holds up to 80 kHz in practice;
  whether the H7A3's DFSDM takes eight of them at the ultrasonic clock; the attenuation of brick at
  25–100 kHz; how patchy a real wall looks to a thermal sensor, with radiators, sun and draughts.

## What we ask

1. Has anyone run the ESP32-C5 (or the S2 or S3) from an external clock? How was XTAL_P driven?
2. Does the ESP32-C5 keep its phase between sending and listening on one channel?
3. Has anyone measured a Wi-Fi CSI shadow of a cable or pipe through a wall?
4. Measured permittivity of lime-cement mortar and plaster at 2.4 GHz?
5. Can the ESP32-C5 send frames of its own at an HE rate, so that the CSI has its 242 subcarriers?
6. A dual-band 2.4/5 GHz patch, 15 mm from a wall, that someone has built?
7. Dry-point-contact ultrasound on brick or plaster: what came back?
8. Air-coupled microphones on brick masonry rather than concrete: has anyone tried?
9. Thermal images of loaded cables in plastered brick: how much did they show, and after how long?

## The trials

Short sets decide whether it is worth building, each cheaper than the next.

- **Wi-Fi:** two ESP32-C5 boards, one sending and one listening, a laptop, foil behind the listening
  antenna at 15 mm of foam as the head will have it; a cable, a UTP bundle and a conduit behind
  drywall and in a grooved brick wall, on lime-cement and on gypsum plaster; both polarizations at
  the sender and at the receiver, the gain fixed; 2.4 GHz, and 5 GHz on the kits' dual-band
  antennas. Passed when the cable shows a repeatable dip of at least 2 dB where it is, above the
  wall's own pattern there (expected figures in *A real wall* and *The head itself*). Then the
  building's own access point as the sender.
- **The clock:** two C5 dev boards with their crystals taken off, fed from one 48 MHz oscillator,
  both listening to one sender. Passed when the phase between them holds, packet after packet and
  after a retune once calibrated, and when a C5 keeps its phase between sending and listening on one
  channel. This decides the board (*The electronics*); if it fails, plan B.
- **Sound:** Datel's knock — a buzzer with its plastic rod — and a steel ball by hand, on bricks
  with and without a conduit and on plaster that sounds hollow; an ultrasonic microphone a few
  millimetres above, and 50 mm PZT discs as a contact reference. Passed when the microphone hears
  the wall over the airborne sound and the conduit or the hollow changes the pattern. The 40 kHz
  cleaner transducer with its 6.3 cm rod after it, if bursts promise more.
- **Heat**, on the side: any thermal camera a metre from a plastered wall over a known cable, its
  circuit loaded by a 2 kW heater for a few hours; expected a band about 11 cm wide, about 1 K warm
  over 3 × 1.5 once settled, half of it within the first 0.7 h **[calc]**.

If neither the Wi-Fi nor the sound passes, the project stops, and the results join the *Why not*
list above.

## The scripts

Every **[calc]** figure comes from a script in `calc/`, attached to this post — Python 3, numpy, and
scipy where noted. `materials.py` holds every material constant; the rest:

| script | what it gives | runs |
|---|---|---|
| `budget.py` | wall losses, damp brick, wavelengths, range resolution, parallax, the link, data rates, the boards' stack, power, patch and disc sizes | at once |
| `array.py` | the three layouts of nine and their polarization coverage | at once |
| `shadow.py` | a cylinder's shadow in brick and in air, the exact 2D series (scipy) | a minute or two |
| `wall_fdtd.py` | the real wall, 2D FDTD; output in `wall_fdtd.out` | tens of minutes a wall |
| `joints.py` | the joints' pattern along a scan, dry and wet, and what divides it out; output in `joints.out` | tens of minutes a case |
| `head.py` | the head's ground plane against the wall, the spacer, the cable's depth, the amplitude and the phase; output in `head.out`, `head_depth.out`, `head_cdepth.out` | tens of minutes a case |
| `patch_fdtd.py` | the patch against the wall, its resonance and its match, 3D FDTD; output in `patch_fdtd.out` | a quarter of an hour to an hour a case |
| `acoustics.py` | speeds, wavelengths, reflections, echo times, the tap and the knock, sound levels, sound pipes, Datel's rod | at once |
| `thermal.py` | the warmth over a loaded cable and how finely the sensor finds it (scipy); output in `thermal.out` | half a minute |
| `cpu.py` | the processor's load | at once |

## Acknowledgements

To the AI assistant Claude (Anthropic), for its great help with this project.

## Sources

- What wall scanners are for: [Bosch CZ, detektory](https://www.bosch-professional.com/cz/cs/detektory-131501-ocs-c/), [Estav](https://www.estav.cz/cz/11285.neriskujte-provrtani-elektrickeho-vedeni-pouzijte-detektor-kabelu), [Cal Poly on the D-tect 200 C](https://grandavehousing.calpoly.edu/news/bosch-d-tect-200-c)
- Bosch D-tect 200 C: [Bosch CZ](https://www.bosch-professional.com/cz/cs/products/detektor-d-tect-200-c-0601081600), [depths](https://www.bosch-professional.com/ge/en/products/wallscanner-d-tect-200-c-0601081600); Walabot: [CNX](https://cnx-software.com/?p=26641), [Core Electronics](https://core-electronics.com.au/walabot-developer.html); Proceq GP8000: [Gilson](https://www.globalgilson.com/gpr-live), [Screening Eagle](https://www.screeningeagle.com/en/inspection/efficient-ground-penetrating-radar-for-concrete); MIRA A1040: [IndiaMART](https://www.indiamart.com/proddetail/a1040-mira-mira-ultrasonic-concrete-tomography-2851104290655.html)
- Materials: ITU-R P.2040-3 Table 3 via [MathWorks](https://www.mathworks.com/help/comm/ref/buildingmaterialpermittivity.html); damp solid brick 1–6 GHz [PMC13165532](https://pmc.ncbi.nlm.nih.gov/articles/PMC13165532/); gypsum plaster blocks [PMC10703195](https://pmc.ncbi.nlm.nih.gov/articles/PMC10703195/); solid brick and joints [Estav](https://www.estav.cz/cz/4880.vazby-cihelneho-pohledoveho-zdiva/gallery?thumbs=1)
- ESP32-C5: [datasheet v1.5](https://documentation.espressif.com/esp32-c5_datasheet_en.pdf); ESP32-C5-MINI-1/1U datasheet v1.4; CSI: [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/v6.1/esp32c5/api-guides/wifi-driver/wifi-vendor-features.html), [esp-csi](https://github.com/espressif/esp-csi), [esp_csi_gain_ctrl](https://components.espressif.com/components/espressif/esp_csi_gain_ctrl/versions/0.1.5/readme); antennas: [PHY guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c5/api-guides/phy.html); checklist: [C5](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c5/schematic-checklist.html), [S2](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s2/schematic-checklist.html)
- Seeed XIAO ESP32-C5: [CNX Software](https://www.cnx-software.com/2026/01/16/xiao-esp32-c5-a-tiny-usb-c-iot-board-with-dual-band-wifi-6-bluetooth-5-0-le-zigbee-and-thread-connectivity/), [Core Electronics](https://core-electronics.com.au/seeed-studio-xiao-esp32-c5.html)
- ESPARGOS: [arXiv 2408.16377](https://arxiv.org/abs/2408.16377), the phase after a retune and the reference [arXiv 2502.09405](https://arxiv.org/abs/2502.09405); CSI phase sanitisation [arXiv 1708.07129](https://arxiv.org/pdf/1708.07129), [arXiv 2205.00973](https://arxiv.org/pdf/2205.00973); WiProfile: [HAL](https://hal.science/hal-04783812); Holl & Reinhard: [arXiv 1612.03194](https://arxiv.org/abs/1612.03194); Supélec camera: [summary](https://www.es.mdu.se/pdf_publications/1089.pdf); SiWa: [arXiv 2110.14279](https://arxiv.org/abs/2110.14279); RASCAN: [Ivashov 2018](https://flore.unifi.it/retrieve/e398c37e-6201-179a-e053-3705fe0a4cff/Culture_2018_Ivashov_Eng.pdf); KrakenSDR: [rtl-sdr.com](https://www.rtl-sdr.com/unleash-the-krakensdr-5-channel-coherent-capable-rtl-sdr-coming-soon-direction-finding-passive-radar/)
- Chronos: [NSDI 2016](https://www.usenix.org/conference/nsdi16/technical-sessions/presentation/vasisht); TU Berlin 2025: [TKN](https://www.tkn.tu-berlin.de/bib/huenecke2025study/); LimeSDR Mini as a radar: [BYU](https://scholarsarchive.byu.edu/etd/9027); ArrayTrack: [report](https://cs.princeton.edu/~kylej/papers/UCL-CS-RN-11-19.pdf); masonry tomography: [Wendrich 2008](https://opus4.kobv.de/opus4-bam/files/111/diss47_vt.pdf); nRF7002: [product specification v1.1](https://media.distrelec.com/Web/Downloads/_m/an/NRF7002-QFAA-R_eng_man.pdf); LMS7002M: [datasheet](https://www.mouser.com/datasheet/2/982/LMS7002M-Data-Sheet-v3.1r00-1600568.pdf)
- STM32H7A3: datasheet DS13195 Rev 8 (ST)
- Two-receiver chips: NXP AN14011 Rev. 10.2 (CSI on Linux, June 2026); Espressif ESP32-E22 (announced at CES 2026); router CSI: Nexmon CSI (seemoo-lab)
- Thermal sensors: Waveshare 80 × 62 [wiki](https://www.waveshare.com/wiki/Thermal_Camera_HAT), [RobotShop](https://www.robotshop.com/products/waveshare-long-wave-ir-thermal-imaging-camera-module-80-x-62-pixels-ir-array), [MI0802 datasheet](https://files.waveshare.com/wiki/common/MI0802--Datasheet--v1.0.1.pdf); Midas MTP-8062 [LCSC](https://www.lcsc.com/product-detail/C17582838.html); Meridian Cheetah 50 × 50 [EE Times Asia](https://www.eetasia.com/meridian-innovation-unveils-new-generation-of-thermal-imaging-sensor); MLX90640 [Pimoroni](https://shop.pimoroni.com/products/mlx90640-thermal-camera-breakout); copper resistances IEC 60228; the faces' surface resistance ISO 6946
- Digital microphones: Knowles SPH0641LU4H-1 [datasheet](https://akizukidenshi.com/goodsaffix/SPH0641LU4H-1.PDF), [breakout](https://eu.robotshop.com/products/digital-mems-microphone-breakout-board-sph0641lu4h-1); PDM on STM32: [AN5027](https://www.st.com/resource/en/application_note/an5027-interfacing-pdm-digital-microphones-using-stm32-mcus-and-mpus-stmicroelectronics.pdf), [ST community](https://community.st.com/stm32-mcus-products-25/array-of-pdm-microphones-best-bus-interface-120416); nRF5340 PDM limit: [DevZone](https://devzone.nordicsemi.com/f/nordic-q-a/114214/maximum-pdm-clock-frequency-supported-by-nrf5340/499750)
- Contactless acoustics: Groschup & Grosse 2015 [PMC4541815](https://pmc.ncbi.nlm.nih.gov/articles/PMC4541815/); Gucunski et al. 2016 [CETRA](https://cetra.grad.hr/ocs/index.php/cetra4/cetra2016/paper/view/576); Zhu & Popovics [thesis, Illinois 2008](https://www.ideals.illinois.edu/items/5377), [air-coupled surface-wave NDT](https://experts.illinois.edu/en/publications/application-of-air-coupled-sensors-to-surface-wave-ndt-in-concret/); Song & Popovics 2019 [DOI 10.3390/app9153005](https://doi.org/10.3390/app9153005); a 40 kHz 50 W cleaner stack [SiliconChip](https://siliconchip.com.au/Shop/7/5629), 60 W [Probots](https://probots.co.in/40khz-60w-adjustable-ultrasonic-cleaning-transducer.html); Knowles ultrasonic MEMS microphone [knowles.com](https://www.knowles.com/resource-news-details/new-product-ultrasonic-mems-microphone)
- Ultrasound: brick-making clay 2700–3100 m/s [Academia](https://www.academia.edu/35534451/Evaluation_of_correlation_between_physical_properties_and_ultrasonic_pulse_velocity_of_fired_clay_samples); dry clay bricks 1430–2143 m/s [Materials 2024](https://doi.org/10.3390/ma17061353); [Buildings 2022](https://doi.org/10.3390/buildings12081069); masonry joints [ASCE](https://ascelibrary.com/doi/10.1061/%28ASCE%29MT.1943-5533.0000547), [real.mtak.hu](https://real.mtak.hu/202129/1/606-article-p61.pdf); mortars [MATEC 2024](https://doaj.org/article/a5d49007b2b14a1690749222b7cd3190); MIRA in practice [Structural 218](https://doi.org/10.12917/STRU218.18); ACS S1802 [ACS](https://acs-international.com/instruments/transducers/low-frequency-50-to-300-khz/dry-point-contact-transducers/single/s1802/); Pundit 250 Array [DirectIndustry](https://directindustry.com/prod/proceq/product-7242-1871923.html); ULB piezo discs [ULB](https://structuraldynamics.ulb.be/ultrasonic-monitoring-of-concrete-using-embedded-piezoelectric-transducers/)
- *The Flying Ship* (Летучий корабль): [nukadeti.ru](https://nukadeti.ru/skazki/letuchij_korabl)
