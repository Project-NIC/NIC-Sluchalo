# NIC-Sluchalo — the principle

*Level 4 of the project, begun on 13 Nov 2026 and not closed: for every block the physics and a
rough calculation, always as a script in [`calc/`](calc). No part numbers. Every figure lives in
its script's output; this page says what the figures mean and points at them. The blocks and
their names are in [`architecture.md`](architecture.md).*

| block | its script | state |
|---|---|---|
| Fonar, the wall, the shadow | `budget.py`, `shadow.py`, `wall_fdtd.py`, `joints.py` | as in [`concept.md`](concept.md) |
| Kolchoz's antennas | `head.py`, `patch_fdtd.py`, `array.py` | as in the concept; the coupling between patches not computed |
| **the pass and the picture** | **`picture.py`** | **below** |
| Samokritika | — | to be scripted |
| Kuranty | `budget.py` | as in the concept |
| Datel | `acoustics.py` | as in the concept |
| the angle of the head | `picture.py` | below |
| **Iljič** | **`hum.py`** | **below** |
| Gensek's load | `cpu.py` | to be redone once the picture's arithmetic is settled |
| Pajok | `budget.py` | as in the concept |

## The pass: the head is turned, not slid

Eleven receivers are eleven points; a picture is a few hundred. The rest comes from moving the
head, and the simplest movement is a turn: a rod with a rubber tip is pressed to the wall with one
hand, the head — a disc on that rod — is turned about it with the other. The rod is plastic and
stands off the head's centre, so that each of the nine patches of the ring lies at its own
distance from it and draws its own circle.

## The picture

`picture.py` draws what the head would show of six walls for four ways of moving it. It is a
model and not a wall: a plane wave through brick, each object the exact field of a cylinder, the
wall's grain made up to the size `joints.py` found for dry mortar, the patch taken as an average
over its own area. It leaves out the wall's surface and the head's ground plane (`head.py` has
those), the room, the wall's own change of polarization, the other channels and 5 GHz. It shows
what a way of moving the head can give at best. The figures are in `calc/picture.out`.

![every wall, every way of moving the head](calc/picture_moves.png)

*Left, what is in the wall; then the head turned about its centre, about a rod a third of the way
out, about a rod on its rim, and slid. Amplitude only, both senders.*

![what each thing adds](calc/picture_adds.png)

*The cable that turns, the rod a third out (above) and on the rim (below), one thing changed at a
time.*

What the model says:

1. **About its own centre the head draws a ring and nothing else** — all nine patches run on one
   circle.
2. **About a rod off the centre it fills a disc.** A third of the way out the disc is the smaller
   and the denser; on the rim it is half as wide again, and coarser.
3. **A single cable a few centimetres deep is a faint line, about as strong as the wall's own
   grain.** It is seen because it is straight and long and the grain is not — which is what the
   purpose asks of the picture. A conduit and a pipe are strong.
4. **Both senders are needed.** With Serp alone every object that runs the other way is gone.
5. **The grain is the limit, not the noise.** Ten times the noise changes nothing, and one turn
   gives the same picture as three.
6. **The angle can come from the radio alone**: Serp and Molot are linear and the nine patches
   radial, so the ring's pattern turns with the head. In the model the error stays within a degree
   or two and the picture is the same as with a sensor. The model has no wall that turns the
   polarization, so this is the best case.
7. **The phase earns its keep on deep objects.** Carried back through the wall, a cable ten
   centimetres deep comes out of the grain; at three centimetres it adds nothing, and under a
   strong grain it harms — though the grain's phase here is a guess.
8. **A receiver's leftover gain error draws a ring about the rod**, and a stripe along a slide.
   Nothing in a wall runs in circles about our rod, so the rings can be levelled out receiver by
   receiver; a stripe along a slide looks like a pipe.
9. **Two cables four centimetres apart are not told apart** — and here the model is weak as well:
   it adds the two fields and leaves out what one cable does to the other.

Where the rod stands is left to the prototype, which takes the rod in several places. Open:
whether the rings are levelled; the same pictures with the head's
ground plane and the wall's surface in them.

## Iljič: the mains hum and a tracer's signal

Two sensors and several frequencies. **A plate** in the head's ground plane takes the electric
field: the voltage on a cable, whether current flows or not. **A coil** takes the magnetic field:
the current. What frequency is listened to is Gensek's choice, not the sensor's — 50 Hz for the
mains themselves, or the tens of kilohertz to a megahertz that a cable tracer's sender puts on a
cable from a socket. `hum.py` is a rough calculation of both, to the order of magnitude; its
figures are in `calc/hum.out`, and the cable's sizes, the wall's conductivity and the tracer's
volts and milliamps in it are assumed, not taken from a sheet.

What it says:

1. **A wall is a conductor to slow fields and an insulator to fast ones**, and where it changes
   over depends on its damp: a few hertz for a bone-dry wall, tens of kilohertz for an ordinary
   one, megahertz for a damp one.
2. **Where the wall conducts, the plate goes blind.** At 50 Hz it reads well only through a dry
   wall; through an ordinary one it keeps a few per cent, through a damp one nothing. This is the
   known weakness of every voltage pen.
3. **A higher frequency reads through a damper wall**: at 125 kHz an ordinary wall is no
   obstacle and a damp one costs about half; at 1 MHz not even the damp one does. And the current
   into the plate grows with the frequency itself.
4. **The plate sees a cable wide** — one to four tens of centimetres, wider the deeper it lies
   and the more the wall conducts. It says *here is a live cable*, not where to the centimetre.
5. **The coil sees it narrow**, about as wide as it is deep, but it needs current: an ampere of
   load at 50 Hz gives a signal only a few times above a room's own hum, while a tracer's few
   milliamps at its high frequency give far more.

So the three modes the owner asked for — a tracer's probe, an inductive sensor, a capacitive one
on 50 Hz — are these two sensors and a choice of frequency. For a tracer to be read, its
frequency and the form of its code must be known; neither is yet.

Open: the tracer's frequency and code (UNI-T UT25CL, the owner's); where on the head the plate
and the coil sit — on the axis they give a number, off it they draw a circle as the head turns;
what the head's own converters and radios put into them.
