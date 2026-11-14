# NIC-Sluchalo — the purpose

*Level 1 of the project, closed on 13 Nov 2026: what it does, for whom, and how we know it works. No parts and no numbers
here — those are in the levels below, for now in [`concept.md`](concept.md).*

## What it does

It shows what lies in a wall before the wall is drilled, chased or broken into. A hand-held head
is pressed to one face of the wall and slid over it. From the other face the wall is lit by Wi-Fi —
a small box of ours in the next room, or the network the building already has. What is in the wall
casts a shadow, and the tool draws the shadows as **a picture of the wall on its own display**, the
way an X-ray shows a piece of material or a thermal camera a facade.

Into the same picture it can lay the mains hum: where there is voltage on a cable, or current in
it.

## The picture, not a verdict

The tool does not decide what a thing is. It shows the wall as a surface with its own grain — the
joints, the stones, the noise — and in it the shapes that do not belong to the grain: a stripe
where a conduit runs, something darker inside it where the copper is. A person reads the shapes,
as with a thermal camera, where nobody needs the temperatures: noise never draws the same
rectangle over every window, and it never draws a straight stripe from a socket to the ceiling.

So the contrast and the thresholds are in the user's hands, and beside the tool goes a book of
examples — pictures of known walls with what was in them — from which reading it is learnt.

## For whom

The electrician and the tradesman at a renovation with no drawings, who need to know where the
cables and the pipes run. The small company that will not buy a ground radar. And anyone who minds
the closed firmware of the scanners on sale: here every setting and all the raw data stay open.

## What it looks for

Cables, metal pipes, steel profiles, bundles of data cables, the rebar in concrete — and whatever
else dims the field enough to show, such as a thick-walled conduit. Nothing is promised about what
does not show.

## What it is not

- Not a one-sided radar: it needs the other face of the wall. A radar may follow later.
- It may show that a cable is live; it never says that one is not. Silence is no proof, and the
  tool replaces neither a voltage tester nor safe working practice.
- Heat — which cable has carried a load — is postponed.
- Not an app on a phone.

## How we know it works

1. On a wall whose contents are known, the picture shows the cable as a shape where the cable is —
   at every pass, the same.
2. Where there is nothing, the picture shows only the wall's grain.
3. This holds on drywall and on plastered brick.
4. A person who did not build the tool reads the picture after the book of examples.

Before anything is built, cheap trials with two boards decide. If the radio does not pass, the
project stops and the results are published.
