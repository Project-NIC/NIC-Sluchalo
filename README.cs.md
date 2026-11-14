<p align="center">
  <img src="NIC-Sluchalo.jpg" width="300" alt="Sluchalo"/>
</p>

★ N.I.C. ★

# NIC-Sluchalo

[English](README.md) · **Čeština** · [Русский](README.ru.md)

**Co je ve zdi, poznané podle stínu, který skrz ni vrhá Wi-Fi. Ruční hlava s deseti přijímači
Wi-Fi se otáčí na tyčce přitlačené k jedné straně zdi, malá krabička na druhé straně vysílá. Kabel, trubka nebo
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
- **Jedny hodiny pro všech deset přijímačů.** Běží z jednoho taktu 48 MHz, takže se jejich fáze
  dají porovnat. Při celé otáčce se přijímače srovnají navzájem z přejezdu samotného; umějí se
  i zkalibrovat vzduchem — **Samokritika** — bez jediného přepínače.
- **Otáčka jako snímání.** Hlava se jednou otočí na tyčce přitlačené ke zdi, mimo svůj střed,
  takže každá z osmi antén kruhu opíše vlastní kružnici a dohromady vyplní kruh o průměru asi
  24 cm. Zdi se hlava nedotýká.
- **Síťové napětí jako vrstva.** Kapacitní snímač v hlavě ukáže, kde je živý kabel; nikdy
  netvrdí, že kabel pod napětím není.
- **U zdiva ťuknutí.** Bzučákový disk ťuká do zdi plastovou tyčinkou uprostřed; osm mikrofonů
  kolem ní uslyší povrchovou vlnu zdi dřív než zvuk, který jde vzduchem.

## Části

| část | co to je |
|---|---|
| **Fonar** | lucerna: vysílač za zdí, dvě desky ESP32-C5 se zkříženými dipóly, které se střídají — **Serp** a **Molot** — 1000 rámců za sekundu |
| **Valenki** | válenky: podvozek — gumová noha přitlačená ke zdi, tyčka a rukojeť; drží hlavu od zdi a kolmo k ní |
| **Kolchoz** | kolchoz: hlava — všechno, co se točí na tyčce |
| **Brigáda** | brigáda: kruh osmi přijímačů, které pracují jako jeden |
| **Předseda** | jeho předseda: zkřížená dvojice uprostřed, která vede kalibraci vzduchem — **Samokritiku** |
| **Kuranty** | kremelské hodiny: jedny hodiny 48 MHz, podle kterých jde všechno |
| **Datel** | datel: ťukání a osm mikrofonů |
| **Razvedčik** | zvěd: snímač úhlu hlavy na tyčce |
| **Iljič** | Iljičova žárovka: jednotka síťového napětí — kapacitní snímač s vlastním zesílením a pásmem, jedna z vrstev obrazu |
| **Gensek** | generální tajemník: jeden STM32H7A3 nade vším — hlášení, poloha, ťukání, displej |
| **Pravda** | noviny: displej a tlačítka |
| **Kádrovák** | kádrovák: úložiště každého obrazu s jeho surovými daty; **Samizdat** je dostane do počítače |
| **Pajok** | příděl: dva články 18650 |
| **Gradusnik** | teploměr: tepelný snímač, odložený — zatím to zastane termokamera vedle hlavy |

## Hlava

| | |
|---|---|
| velikost | průměr 176 mm |
| kruh | **Brigáda**: osm patchů 30 × 37 mm na kružnici o poloměru 69,5 mm, 53 mm od sebe, každý natočený radiálně |
| střed | jeden čtvercový patch napájený dvakrát v pravém úhlu, na dvou přijímačích; jeho středem prochází díra pro tyčinku ťukání |
| tyčka | 35 mm od středu, mezi prostředním patchem a kruhem; jedna otáčka pokryje kruh o průměru asi 24 cm |
| značení | tužkou podle zářezů na okraji hlavy, když stojí |
| přijímače | deset ESP32-C5 jako holé čipy na zadní straně anténní desky, každý napájí svůj patch prokovem přímo nahoru — žádný koax |
| desky | **Front**, anténní deska, čtyřvrstvá, 1,6 mm; **Tyl**, deska elektroniky, 11 mm za ní |
| ke zdi | nedotýká se jí: **Valenki** ji drží 15 mm od zdi; kde by se o zeď mohla otřít, má hlava filc |
| napájení | ze dvou článků 18650 asi tři hodiny (5,7 W bylo spočítáno pro jedenáct přijímačů) |

Hlava, jak byla rozhodnuta 13. 11. 2026: [`calc/ring8.py`](calc/ring8.py), její patch
v `calc/patch8.out`. Koncept z 28. 10. ([`concept.md`](concept.md), anglicky) popisuje dřívější
hlavu — devět v kruhu, na pěně, posouvanou po zdi; kde se liší od úrovní, platí úrovně
([`WHY.md`](WHY.md)).

## Co nevíme

- **Jestli ESP32-C5 poběží z vnějšího taktu 48 MHz.** Jeho dokumentace označuje krystal za
  povinný. Rozhoduje to desku; záložním plánem je rádio s přímými I/Q vzorky.
- **Jestli se skutečná zeď chová jako modely** — permitivita skutečné malty a omítky, mokré spáry
  a jestli 8bitové CSI s pevným ziskem udrží stabilně změnu 20–30 % v amplitudě a fázi.
- **Jestli ťukání a mikrofony uslyší něco užitečného** přes suchý kontakt na omítce.

Rozhodnou zkoušky popsané na konci [`concept.md`](concept.md).

## Co dál

Projekt roste po úrovních. Účel, požadavky a architektura jsou zavřené; fyzika se počítá blok po
bloku. Koncept z 28. 10. zůstává jako záznam, odkud se vyšlo. Otázky jsou rozeslané — Espressifu,
autorům ESPARGOS a na fóra — a zkoušky postavíme, jakmile to půjde. Projekt poroste podle toho,
co ukážou, a tak daleko, jak dovolí čas a prostředky.

## Soubory

- [`purpose.md`](purpose.md) — co to dělá, pro koho a jak poznáme, že to funguje; jedna stránka, anglicky.
- [`requirements.md`](requirements.md) — co to musí umět, v rozsazích; anglicky.
- [`architecture.md`](architecture.md) — tělesa, jednotky a co mezi nimi teče; jména; anglicky.
- [`WHY.md`](WHY.md) — proč se zavřené úrovně znovu otevřely a co to změnilo níž; anglicky.
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
