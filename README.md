# Python Scripts Repository

Tento repozitář obsahuje sbírku jednoduchých Python skriptů, které jsem vytvořil pro různé účely. Každý skript se nachází ve svém vlastním adresáři a má specifické zaměření.

## Obsah

### 1. Webscrapping-news
Tento skript provádí jednoduchý web scraping zpravodajských stránek za účelem získání aktuálních titulků nebo článků. Skript je napsán v Pythonu s využitím knihoven jako `aiohttp`, `BeautifulSoup` a `tkinter`.

#### Použití:
- Pro spuštění skriptu je potřeba mít nainstalovaný Python a potřebné knihovny.
- Skript stáhne a zobrazí aktuální zprávy z definovaných zpravodajských webů.

### 2. Info
Tento skript poskytuje detailní informace o systému, instalaci Pythonu a nainstalovaných Python balíčcích.

### 3. Jednoduchá kalkulačka
Tento skript poskytuje jednoduchou kalkulačku s grafickým uživatelským rozhraním (GUI) vytvořenou pomocí knihoven `tkinter` a `ttk`. Kalkulačka umožňuje provádět základní matematické operace, jako je sčítání, odčítání, násobení a dělení, a také pokročilé funkce jako závorky a mocniny.

#### Funkce:
- Základní matematické operace: sčítání, odčítání, násobení, dělení.
- Pokročilé funkce: závorky `(`, `)`, exponentace `^`.
- Moderní vzhled pomocí `ttk` pro lepší uživatelský zážitek.

### 4. Snake
Tento skript je jednoduchá verze hry Snake (Had), napsaná pomocí knihovny `pygame`. Hráč ovládá hada, který se pohybuje po obrazovce a sbírá jídlo. Každé snědené jídlo hada prodlouží a zvyšuje jeho rychlost. Hra končí, pokud had narazí do stěny nebo do svého těla.

#### Funkce:
- Ovládání pomocí šipek (nahoru, dolů, vlevo, vpravo).
- Tři úrovně obtížnosti: lehká, střední a těžká.
- Pauza (stiskem klávesy "P").
- Nejvyšší skóre se ukládá do souboru `highscore.txt`.

### 5. Hangman
Tento skript představuje klasickou hru Hangman (Šibenice), kde hráč hádá písmena slova na základě zvoleného jazyka. Hra obsahuje tři různé jazykové možnosti: čeština, angličtina a ukrajinština. Cílem je uhodnout celé slovo před vypršením počtu životů.

#### Funkce:
- Podpora více jazyků: čeština, angličtina a ukrajinština.
- Výběr náhodného slova ze slovníku pro každý jazyk.
- 6 životů na uhádnutí slova.
- Hra se ovládá zadáváním písmen přes konzoli.



## Jak začít

1. Klonujte tento repozitář do svého počítače:

   ```sh
   git clone https://github.com/FoxDeFacto/PyrhonScripts.git
   ```

2. Nainstalujte potřebné Python balíčky pro spuštění skriptů:

   ```sh
   pip install -r requirements.txt
   ```

3. Spusťte skripty pomocí Pythonu:

   ```sh
   python <název_skriptu>.py
   ```

## Požadavky

- Python 3.6 nebo novější
- Knihovny uvedené v souboru `requirements.txt`
