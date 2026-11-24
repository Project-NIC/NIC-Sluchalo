# Datel — why things changed

| # | what changed | why |
|---|---|---|
| 1 | **The purpose reopened the day it was closed (23 Nov 2026):** no raw recording kept with the picture; the picture saved, compressed, and nothing more. Below it nothing was closed; `boards.md` (the requirement of a card for 6 MB/s gone) and `calc/compute.py` brought to it. The raw stream stays only as the bench's live link to a PC during the development. | The owner: "na kartu se nenahrává … max komprimovaný obraz". |
| 2 | **The camera: ST's MB1854 (IMX335, ToF, IMU) → a Raspberry Pi OV5647 module on a longer flex (24 Nov 2026)** | The picture only has to show where the sound is: the display's 800 × 480 at 10–15 fps. The owner: "vezmi to běžné – stačí". **An OV2640 (ESP32-CAM) was weighed** — its own ISP would spare the N6's tuning — and left for the long cable the camera needs to the honeycomb's middle: its parallel bus, eight lines and a clock at full swing without grounds between them, would cross-talk and radiate past the microphones; CSI-2's low-swing pairs with grounds between run 15–50 cm. |
