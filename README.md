# Měřicí aplikace

Jedná se o aplikaci pro zobrazení měřených dat. Po spuštění main.py se zobrazí obrazovka rozdělená do tří částí: části s uživatelem, grafem a tlačítky.

Po kliknutí na tlačítko Nový uživatel lze zadat jméno, příjmení a věk uživatele. Uživatel se uloží do databáze, zároveň se informace o nově vzniklém uživateli objeví na hlavní obrazovce aplikace a přidají se do comboboxu se seznamem uživatelů.

Po klepnutí na tlačítko měřit se začne zobrazovat graf s měřenými hodnotami v reálném čase, zároveň se zobrazuje okamžitá hodnota signálu.
Tlačítkem Pozastavit lze měření pozastavit, další tlačítka slouží pro ukládání do excelu a vymazání grafu.

Jako vstup slouží signál z bluetooth modulu HC-05, který je připojený k Arduinu. Měřenou hodnotou je zde napětí na potenciometru.

V repozitáři bluetooth je uložena aplikace pro připojení k Arduinu, ve složce demo se nachází excelovský soubor a modul logic.py upravený pro spuštění aplikace bez připojeného Arduina - stačí tyto dva soubory přidat do k souborům ve složce bluetooth.

<img width="649" alt="app" src="https://github.com/user-attachments/assets/ebb65d57-d49a-48b4-b5fc-fb83f6b3a373" />


To do:
  * ukládání měřených dat do databáze, současně s tím průběžné promazávání obrazovky
  * možnost nastavení svislé a vodorovné osy grafu
  * analýza dat - průměrná hodnota, energie a výkon signálu, spektrum
  * řízení dalších zařízení nebo programů snímaným signálem - zpětnovazební systém
  * ...
