# NIC-Sluchalo — the architecture

*Level 3 of the project: the blocks and what passes between them. No part types, no packages, no
processors — those are level 5, and for now in [`concept.md`](concept.md). What the tool is for is
in [`purpose.md`](purpose.md), what it must do in [`requirements.md`](requirements.md).*

## Two things

**Fonar**, the sender, stands behind the wall. **The head** is held against the near face. Nothing
joins them but radio.

```mermaid
flowchart LR
  subgraph F[Fonar — behind the wall]
    FA[Serp<br/>upright] ~~~ FB[Molot<br/>level]
  end
  F -. frames through the wall .-> K
  subgraph H[the head]
    K[Kolchoz<br/>ring of nine receivers<br/>+ Předseda in the middle] -->|reports| G[Gensek<br/>the one processor]
    C[Kuranty<br/>the clock] --> K
    C --> G
    D[Datel<br/>knock + microphones] <--> G
    R[Razvedčik<br/>optical sensors] -->|motion| G
    I[Iljič<br/>the hum sensor] -->|50 Hz signal| G
    G --> S[Pravda<br/>display, buttons]
    G <--> M[Kádrovák<br/>the store]
    P[Pajok<br/>battery] --> K & G
  end
  K -. channel, start, stop .-> F
```

## The blocks

| block | what it does | what it does not |
|---|---|---|
| **Fonar** | sends frames through the wall from two crossed senders taking turns, **Serp** and **Molot**; every frame says which of them it came from and carries a counter; goes to the channel the head names | measure anything; know anything about the wall |
| **Kolchoz** | the ring of nine receivers, each with its own antenna facing the wall; each measures the channel of every frame and sends a reduced report | compute the picture; keep anything |
| **Předseda** | the crossed pair in the middle of the ring, two receivers more; listens as the nine do, and leads the calibration: it sends first, then each of the nine in turn | — |
| **Kuranty** | the clock: one source for all eleven receivers and for Gensek, so that their phases can be compared and everything counts the same time | — |
| **Datel** | taps the wall through the middle of the head and hears its surface with a ring of microphones, the head held still | work while the head moves |
| **Razvedčik** | watches the wall's surface and reports how the head has moved over it | know where on the wall the head is in absolute terms |
| **Iljič** | the hum sensor: picks up the mains' field at the wall — voltage, current, or both | say that a cable is dead |
| **Gensek** | the one processor: tells the receivers what to do, collects their reports, the motion, the microphones and the hum; computes the layers of the picture; draws them; stores them; takes the user's settings | any radio work |
| **Pravda** | the display and the buttons: show the picture; set the contrast, the thresholds and the layer | — |
| **Kádrovák** | the store: keeps every picture with its raw data; gives them to a computer | — |
| **Pajok** | the battery and its charging; one supply for the radios, one for the rest | — |
| **Gradusnik** | the thermal sensor — postponed, nothing reserved for it | — |

## What passes between them

| from | to | what | over what |
|---|---|---|---|
| Fonar | Kolchoz, Předseda | frames: Serp or Molot, a counter | radio, through the wall |
| the head | Fonar | channel, start, stop | radio, the same kind of frame |
| Předseda, Kolchoz | each other | Samokritika's frames, receiver to receiver | radio, across the head's face |
| Kuranty | each receiver, Gensek | one frequency, lines of equal length | a line each, from one buffer |
| Gensek | each receiver | channel, gain, start on a common edge, calibrate, send; a new program | a serial link each; a reset and a start line shared by all |
| each receiver | Gensek | a report for every frame: which frame, the channel measured, reduced | the same serial link |
| Gensek | Datel | the knock's timing | a drive signal |
| Datel | Gensek | the microphones' streams | digital streams and their clock |
| Razvedčik | Gensek | motion since the last reading | a serial bus |
| Iljič | Gensek | the amplified field | an analog signal |
| Gensek | Pravda | the picture | a parallel bus |
| Pravda | Gensek | the user's settings | lines |
| Gensek | Kádrovák | pictures with raw data | — |
| Kádrovák | a computer | Samizdat: the pictures out; programs in | a cable |
| Pajok | everything | two supplies | — |

## How a picture comes to be

1. **Samokritika** — Předseda sends, the ring listens, then each receiver in turn: the
   receivers' own phases fall out. Done again after every change of channel, because a receiver
   locks to a new channel at a new phase.
2. **Scan** — Fonar sends; every receiver reports every frame; Gensek divides receiver by
   receiver, so that whatever the sender did falls out and the wall is left.
3. **Place** — Razvedčik's motion says where each report was taken.
4. **Draw** — the radio layer grows under the hand; the hum layer lies on it; the sound layer is
   added where the head stood still and knocked.
5. **Keep** — the picture and what it was made from go to Kádrovák.

## The body

Two boards, one behind the other. **Front** faces the wall: the antennas, the receivers right
behind them, Kuranty, the microphones, the optical sensors. **Tyl**, behind it, carries Gensek,
the power, the knock and Pravda. Between Front and the wall, **Valenki**: a foam spacer with a
sheet that slides; on the rim, notches to mark the wall by.

## The names

In the spirit of the tale the tool is named after, and meant as a joke. They are settled here and
not changed below this level.

| name | from | what it is |
|---|---|---|
| **Fonar** | the lantern | the sender behind the wall |
| **Serp**, **Molot** | the sickle, the hammer | Fonar's two senders, crossed |
| **Kolchoz** | the collective farm | the ring of nine receivers that work as one |
| **Předseda** | Czech: its chairman | the crossed pair in the middle |
| **Kuranty** | the Kremlin's chimes | the one clock everything goes by |
| **Samokritika** | self-criticism | the calibration over the air: each speaks in turn, the others listen |
| **Datel** | Czech: the woodpecker, after the Duga radar | the knock and the microphones |
| **Razvedčik** | the scout | the optical sensors that follow the head's movement |
| **Iljič** | Ilyich's lamp, the electrification | the mains-hum sensor |
| **Gensek** | the general secretary | the one processor |
| **Pravda** | the newspaper | the display and the buttons |
| **Kádrovák** | Czech: the keeper of everyone's file | the store of pictures and raw data |
| **Samizdat** | what gets out | taking the pictures out to a computer |
| **Pajok** | the ration | the battery |
| **Front**, **Tyl** | the front, the rear | the board at the wall, the board behind it |
| **Valenki** | felt boots | the foam and its sliding sheet |
| **Bukvar** | the primer | the book of examples the picture is learnt from |
| **Gradusnik** | the thermometer | the thermal sensor, postponed |

## The words

| word | meaning |
|---|---|
| frame | one radio packet from a sender |
| report | what one receiver measured on one frame, reduced, as it goes to Gensek |
| layer | one kind of picture of the same piece of wall: radio, hum, sound |
| picture | the layers together, with the raw data they were made from |
| pass | one movement of the head that yields a picture — a turn on the spot, or a stroke |
| grain | what the wall itself shows in a picture: joints, stones, noise |

## Open at this level

- **A turn or a stroke** — whether Razvedčik must give the path or only the angle (level 4, with
  the three cases of the head computed side by side).
- **Iljič's form** — a plate for voltage, a loop for current, or both; one sensor or several
  around the head.
- **How often the channel can change**, with a calibration after each change.
