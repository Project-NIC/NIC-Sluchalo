<p align="center">
  <img src="NIC-Sluchalo.jpg" width="300" alt="Sluchalo"/>
</p>

★ N.I.C. ★

# NIC-Sluchalo

[English](README.md) · **Čeština** · [Русский](README.ru.md)

**Co je ve zdi, poznané podle stínu, který skrz ni vrhá Wi-Fi. Ruční hlava s deseti přijímači
Wi-Fi se otáčí na tyčce přitlačené k jedné straně zdi, malá krabička na druhé straně vysílá. Kabel, trubka nebo
ocelový profil mezi nimi pole zeslabí a hlava zmapuje kde. Každé nastavení i všechna surová data zůstávají otevřená tomu, kdo s ní pracuje.**

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![License: CERN-OHL-P v2](https://img.shields.io/badge/License-CERN--OHL--P%20v2-red.svg)](https://ohwr.org/cern_ohl_p_v2.txt)
![Version: 0.2 — on paper](https://img.shields.io/badge/version-0.2%20on%20paper-blue.svg)

> ⚠️ **Koncept — nic není postavené ani změřené.** U každého čísla je uvedeno, odkud pochází:
> z datasheetu, z publikované práce, z našeho vlastního výpočtu, nebo že není známé. Výpočty jsou
> modely — 2D a 3D FDTD a jednodušší fyzika — ne měření. Stín kabelu přes skutečnou zeď tímto
> způsobem zatím nikdo neviděl. Otázky a opravy jsou důvod, proč ho zveřejňujeme.

## Jak to funguje

- **Proč stín, a ne radar.** Signál projde zdí jen jednou. Nevzniká ozvěna od blízkého povrchu
  a vysílač neprosakuje do přijímače — dvě věci, které jednostranný radar oslepují.
- **Amplitudy, ne fáze.** Každý přijímač změří kanál téhož rámce na každé podnosné (CSI)
  s pevným ziskem. Každý přijímač jede na vlastním krystalu, takže se porovnávají jen amplitudy:
  na každém rámci přijímače navzájem, čímž zmizí vysílač a místnost; v každém přijímači rámce
  obou zkřížených antén vysílače proti sobě, čímž zmizí vlastní zisk přijímače; a během celé
  otáčky každý přijímač proti své kružnici. Vlna vysílače sama je referencí, která obraz zaostří,
  jako u hologramu.
- **Otáčka jako snímání.** Hlava se jednou otočí na tyčce přitlačené ke zdi, mimo svůj střed,
  takže každá z osmi antén kruhu opíše vlastní kružnici a dohromady vyplní kruh o průměru asi
  24 cm. Zdi se hlava nedotýká.
- **Samokritika.** Před otáčkou vyšle prostřední dvojice krátký rámec v každé polarizaci a každý
  přijímač změří, co k němu dorazilo — proti ťuknutí, vlhkosti a rozladění.
- **Síťové napětí jako zkoušečka.** V samostatném režimu, drženém jako zkoušečka, kapacitní
  snímač zvukem a sloupcem ukáže, kde je živý kabel nebo signál hledačky; nikdy netvrdí, že
  kabel pod napětím není.

## Jen tento jeden pokus

Detektory na trhu dávají všechno do jedné krabičky: Bosch D-tect 200 C spojuje radar s indukčním
snímačem a termokamery ukážou, kterým kabelem tekl proud. Sluchalo se o to nesnaží: je to jeden pokus
— jestli jde nakreslit stín, který Wi-Fi vrhá skrz zeď — a vedle něj obyčejná zkoušečka napětí.
Zbytek — hledačka kabelů, čtená nábojem i proudem, kov, ťukání, termokamera prolnutá s obyčejnou —
je NIC-Ariadna, samostatná ruční sonda, zatím nezveřejněná.

## Části

| část | co to je |
|---|---|
| **Iskra** | jiskra: vysílač za zdí, hotová deska se dvěma zkříženými anténami, které se střídají, svislou a vodorovnou |
| **Fonar** | lucerna: přístroj přiložený ke zdi — Valenki a Kolchoz |
| <img src="pictures/valenki.jpg" width="90"/><br/>**Valenki** | válenky: podvozek — gumová noha přitlačená ke zdi, tyčka a rukojeť; drží hlavu od zdi a kolmo k ní |
| <img src="pictures/kolchoz.jpg" width="90"/><br/>**Kolchoz** | kolchoz: hlava — všechno, co se točí na tyčce |
| <img src="pictures/levsa.jpg" width="90"/><br/>**Levša** | Leskovův levoruký kovář: konstrukce, všechno z kovu a plastu, co drží jednotky |
| **Brigáda** | brigáda: kruh osmi přijímačů, **Mužíků**, každý se svou anténou, **Kosou** |
| <img src="pictures/predseda.jpg" width="90"/><br/>**Předseda** | předseda: dvojice uprostřed v pravém úhlu — práce dvou Mužíků — se **Srpem** a **Molotem** v rukou, jedinými vysílači ve Fonaru, pro **Samokritiku** |
| **Kuranty** | kremelské hodiny: časová osa — jedna hrana na lince společné všem přijímačům |
| **Razvedčik** | zvěd: snímač úhlu hlavy na tyčce |
| **Iljič** | Iljičova žárovka: jednotka síťového napětí — kapacitní snímač s vlastním zesílením a pásmem, samostatný režim, drží se jako zkoušečka |
| **Gensek** | generální tajemník: jeden procesor nade vším — hlášení, úhel, obraz, displej, zvuk |
| **Pravda** | noviny: displej a tlačítka |
| **Kádrovák** | kádrovák: úložiště každého obrazu s jeho surovými daty; **Samizdat** je dostane do počítače |
| **Pajok** | příděl: dva články 18650 |
| **Karanténa** | karanténa: hlídá všechny jednotky, **Felčar** je kontroluje; při chybě přístroj přestane měřit |

## Hlava

| | |
|---|---|
| velikost | průměr asi 18 cm |
| kruh | **Brigáda**: osm koupených dvoupásmových antén (2,4 a 5 GHz), každá natočená radiálně |
| střed | **Předseda**: dvě stejné antény v pravém úhlu, kolem středu |
| tyčka | mezi středem a kruhem; jedna otáčka pokryje kruh o průměru asi 24 cm |
| značení | tužkou podle zářezů na okraji hlavy, když stojí |
| přijímače | deset hotových modulů ESP32-C5, každý na vlastním krystalu, každý připojený ke své anténě krátkým kabelem |
| Front | čelo ke zdi: kovový kotouč s tenkou izolační vrstvou a na ní antény — kotouč je jejich zemí a stíněním |
| Tyl | deska za ním: procesor, napájení, displej, zvuk |
| ke zdi | nedotýká se jí: **Valenki** ji drží od zdi; kde by se o zeď mohla otřít, má hlava filc |
| napájení | ze dvou článků 18650 asi tři hodiny |

Koncept z 28. 10. ([`concept.md`](concept.md), anglicky) popisuje dřívější hlavu — devět
vlastních patchů, jedny hodiny pro všechny, na pěně, posouvanou po zdi; kde se liší od úrovní,
platí úrovně ([`WHY.md`](WHY.md)). Rozložení hlavy se kreslí znovu pro koupené antény;
[`calc/ring8.py`](calc/ring8.py) ho má pro dřívější patche.

## Co nevíme

- **Jestli se skutečná zeď chová jako modely** — permitivita skutečné malty a omítky, mokré spáry
  a jestli 8bitové CSI s pevným ziskem udrží stabilně změnu amplitudy o 20–30 %.
- **Jestli samotné amplitudy, bez společných hodin, nakreslí skutečnou zeď** tak dobře jako tu
  v modelu.

Rozhodnou zkoušky popsané na konci [`concept.md`](concept.md).

## Co dál

Projekt roste po úrovních. Účel, požadavky, architektura, princip — hrubě spočítaná fyzika
každého bloku — i součástky, všude, kde to jde, koupené a hotové, jsou zavřené. Zbývá postavit
zkoušky a měřit.
autorům ESPARGOS a na fóra — a zkoušky postavíme, jakmile to půjde. Projekt poroste podle toho,
co ukážou, a tak daleko, jak dovolí čas a prostředky.

## Soubory

- [`purpose.md`](purpose.md) — co to dělá, pro koho a jak poznáme, že to funguje; jedna stránka, anglicky.
- [`requirements.md`](requirements.md) — co to musí umět, v rozsazích; anglicky.
- [`architecture.md`](architecture.md) — tělesa, jednotky a co mezi nimi teče; jména; anglicky.
- [`principle.md`](principle.md) — fyzika každého bloku, hrubě spočítaná, a co zbývá změřit; anglicky.
- [`parts.md`](parts.md) — součástky, každá s požadavkem, který plní; anglicky.
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
