<p align="center">
  <img src="datel.jpg" width="420" alt="Datel"/>
</p>

# Datel — the acoustic camera

**Where a gas under pressure escapes, seen as a spot over the camera's picture: 32 microphones
hear the leak's hiss — steam, oxygen, argon, nitrogen, compressed air — and draw where it comes
from. And a knock: which patch of plaster, tile or laminate rings hollow.** Named after the
woodpecker, which knocks and listens.

> ⚠️ **A concept — nothing built, nothing measured.** The figures come from the parts' datasheets
> and our own calculations (`calc/`); the microphone holes, the matching at ultrasound and the
> real range are measured on a test board with one petal first.

## How it works

- **A sparse array of 32 MEMS microphones** in four petals of eight, the camera in the middle, an
  aperture of about 20 cm. Delay-and-sum beamforming over a band: a leak's hiss is broadband, so
  the true source stays where it is while the array's ghosts move with frequency and are averaged
  away; CLEAN-SC takes a loud source out to show a weaker one.
- **Ultrasound first:** a leak's jet is loudest high up, where the hall's machines are quiet; the
  band is set on the tool anywhere from ~0.2 to ~86 kHz — 25–45 kHz for a hissing hole, a few kHz
  for a coupling that only blows. A spectrum of the spot under the cursor shows which.
- **The tap:** a sprung pin beside the camera, struck by a small actuator while four rubber feet
  hold the tool to the surface — the same force every time, the same distance, the knock on the
  axis; the picture shows the patches that ring round it.
- **The picture, not a verdict:** the camera's view at the display's resolution, ten frames a
  second, the map laid over it; a photo keeps what the display shows and the map's numbers. No
  sound is recorded.

## The build

| | |
|---|---|
| microphones | 32 × Knowles SPH0641LU4H-1 (PDM, to 80 kHz), 0.1 µF C0G at each |
| converters | 4 × TI PCMD3180 (8 PDM channels each, TDM), 192 kHz, one master clock of 24.576 MHz |
| processor | STM32N647 on Alientek's ATK-CNN647B core board — Cortex-M55 at 800 MHz with Helium, an NPU, the camera pipeline and the display controller; the four converters on its four SAI lines |
| camera | an OV5647 module of the Raspberry Pi kind on a longer flex, ~90–120° lens, cropped to the view |
| display | up to 7", RGB, behind a plastic window, no touch; buttons |
| power | a 1S sodium-ion pack, TI BQ25628 charger, two TPS63020 buck-boosts in forced PWM; each petal its own TPS7A2018 and a 33 µH choke into an aluminium polymer |
| lights | four LEDs round the camera and the display's backlight, each on a TPS61169 dimmed to a DC current — nothing switched in the band |
| also | microSD, USB-C, an ESP32-S31 module for Wi-Fi to a phone and Bluetooth headphones |

## What is not known

- **The microphones' matching above 20 kHz** and what the hole in the board does to it — the
  calibration per channel is planned, its quality is measured.
- **The real range** on a real leak in a real hall with its reflections — `calc/leak.py` puts a
  0.2 mm hole at 6 bar at ~3 m in a hall, roughly, from a model.
- **The tool's own sound** at a few centimetres — supplies, the display, the case.

## Files

- [`purpose.md`](purpose.md) — what it does, for whom, and how we know it works.
- [`WHY.md`](WHY.md) — why things changed.
- [`calc/`](calc) — the scripts, Python 3 (numpy for `acam.py`): the array and its ghosts
  (`acam.py`), the processor's load and the bus (`compute.py`), the air's loss (`air.py`), the
  microphone's hole (`port.py`, `membrane.py`), the supplies (`supply.py`, `surge.py`,
  `power.py`, `sodium.py`), a leak against the ear (`leak.py`).
