<p align="center">
  <img src="NIC-Sluchalo.jpg" width="300" alt="Sluchalo"/>
</p>

★ N.I.C. ★

# NIC-Sluchalo

[English](README.md) · **Čeština** · [Русский](README.ru.md)

**Co je ve zdi, poznané podle stínu, který skrz ni vrhá Wi-Fi. Ruční hlava s jedenácti přijímači
Wi-Fi se posouvá po jedné straně zdi, malá krabička na druhé straně vysílá. Kabel, trubka nebo
ocelový profil mezi nimi pole zeslabí a hlava zmapuje kde. U zděných stěn do zdi navíc ťuká
a poslouchá. Každé nastavení i všechna surová data zůstávají otevřená tomu, kdo s ní pracuje.**

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![License: CERN-OHL-P v2](https://img.shields.io/badge/License-CERN--OHL--P%20v2-red.svg)](https://ohwr.org/cern_ohl_p_v2.txt)
![Version: 0.1 — concept](https://img.shields.io/badge/version-0.1%20concept-blue.svg)

> ⚠️ **Koncept — nic není postavené ani změřené.** U každého čísla je uvedeno, odkud pochází:
> z datasheetu, z publikované práce, z našeho vlastního výpočtu, nebo že není známé. Výpočty jsou
> modely — 2D a 3D FDTD a jednodušší fyzika — ne měření. Stín kabelu přes skutečnou zeď tímto
> způsobem zatím nikdo neviděl. Otázky a opravy jsou důvod, proč ho zveřejňujeme.

## Jak to funguje

- **Proč stín, a ne radar.** Signál projde zdí jen jednou. Nevzniká ozvěna od blízkého povrchu
  a vysílač neprosakuje do přijímače — dvě věci, které jednostranný radar oslepují.
- **Poměr mezi přijímači.** Každý přijímač změří kanál téhož paketu na každé podnosné (CSI).
  Vydělením jednoho přijímače druhým zmizí všechno, co dělá vysílač — jeho výkon, jeho fáze,
  jeho rychlost — a zůstane zeď.
- **Fáze od první stavby.** Všech jedenáct přijímačů běží z jednoho taktu 48 MHz. Zkřížená
  dvojice uprostřed kalibruje kruh vzduchem, mezi tahy, bez jediného přepínače.
- **Tah jako apertura.** Jak hlava klouže, fáze podél tahu zaostřuje: kabel 3 cm hluboko se při
  tahu dlouhém 20 cm určí v hloubce zhruba na 6 mm.
- **U zdiva ťuknutí.** Bzučákový disk ťuká do zdi plastovou tyčinkou uprostřed; osm mikrofonů
  kolem ní uslyší povrchovou vlnu zdi dřív než zvuk, který jde vzduchem.

## Části

| část | co to je |
|---|---|
| **Fonar** | lucerna: vysílač za zdí, dvě desky ESP32-C5 se zkříženými dipóly, které se střídají, 1000 rámců za sekundu |
| **Kolchoz** | kolchoz: kruh devíti přijímačů, které pracují jako jeden, a zkřížená dvojice uprostřed |
| **Datel** | datel: ťukání a osm mikrofonů |
| **Razvedčik** | zvěd: dva optické snímače pohybu, které sledují hlavu po zdi |
| **Gensek** | generální tajemník: jeden STM32H7A3 nade vším — hlášení, poloha, ťukání, displej |
| **Pajok** | příděl: dva články 18650 |
| **Gradusnik** | teploměr: tepelný snímač, odložený — zatím to zastane termokamera vedle hlavy |

## Hlava

| | |
|---|---|
| velikost | průměr 167 mm; bez krabice asi 0,36 kg |
| kruh | devět patchů 30 × 29 mm na kružnici o poloměru 65,8 mm, 45 mm od sebe, každý natočený radiálně |
| střed | jeden čtvercový patch napájený dvakrát v pravém úhlu, na dvou přijímačích; jeho středem prochází díra pro tyčinku ťukání |
| značení | tužkou podle zářezů na okraji hlavy, dva páry na dvou osách |
| přijímače | jedenáct ESP32-C5 jako holé čipy na zadní straně anténní desky, každý napájí svůj patch prokovem přímo nahoru — žádný koax |
| desky | anténní deska čtyřvrstvá, 1,6 mm; deska elektroniky 11 mm za ní |
| ke zdi | 15 mm pěny, na jejím líci 1 mm polyetylenové fólie, která klouže |
| napájení | asi 5,7 W; z článků asi tři hodiny |

Podrobnosti, zdroje a všechna čísla: [`concept.md`](concept.md) (anglicky).

## Co nevíme

- **Jestli ESP32-C5 poběží z vnějšího taktu 48 MHz.** Jeho dokumentace označuje krystal za
  povinný. Rozhoduje to desku; záložním plánem je rádio s přímými I/Q vzorky.
- **Jestli se skutečná zeď chová jako modely** — permitivita skutečné malty a omítky, mokré spáry
  a jestli 8bitové CSI s pevným ziskem udrží stabilně změnu 20–30 % v amplitudě a fázi.
- **Jestli ťukání a mikrofony uslyší něco užitečného** přes suchý kontakt na omítce.

Rozhodnou zkoušky popsané na konci [`concept.md`](concept.md).

## Co dál

Verze 0.1 je koncept v jednom dokumentu a vedle něj skripty; vlastní složky dostanou části až
v dalších verzích. Teď rozešleme otázky — Espressifu, autorům ESPARGOS a na fóra o rádiové technice
a nedestruktivním zkoušení — a postavíme zkoušky, jakmile to půjde. Projekt poroste podle toho, co
ukážou, a tak daleko, jak dovolí čas a prostředky.

## Soubory

- [`concept.md`](concept.md) — celý koncept, anglicky: k čemu je, hlava, proč by to mělo fungovat,
  elektronika, zvuk, teplo, opuštěné cesty a proč, co nevíme, zkoušky.
- [`calc/`](calc) — skripty za každým spočítaným číslem, Python 3 s numpy (dva z nich se scipy),
  a jejich výstupy. `budget.py`, `array.py`, `acoustics.py` a `cpu.py` doběhnou hned; modely FDTD
  počítají minuty až hodinu na případ.

Software pod licencí MIT ([`LICENSE`](LICENSE)); návrh hardwaru pod CERN-OHL-P v2
([`LICENSE-HW`](LICENSE-HW)).

## Poděkování

AI asistentovi Claude (Anthropic) za velkou pomoc s tímto projektem.

★ Viva La Resistánce ★
