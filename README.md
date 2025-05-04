# Kortų žaidimas "Karas"

## Įvadas

### a. Kokia tai programa?

Tai skaitmeninė klasikinio kortų žaidimo „Karas“ versija. Du žaidėjai (du žmonės arba vienas žmogus ir kompiuteris) žaidžia su sumaišyta standartine 52 kortų kalade. Kiekviename raunde abu žaidėjai traukia po kortą – laimi 
aukštesnė korta. Lygiųjų atveju prasideda „karas“, kurio metu traukiamos papildomos kortos, kad būtų nustatytas nugalėtojas. Žaidimas tęsiasi tol, kol išnaudojama kaladė, o žaidėjas, laimintis daugiausiai raundų, 
paskelbiamas nugalėtoju.

### b. Kaip paleisti programą?

1. Įrašykite kodą į failą, pvz., `WAR.py`.

2. Terminale arba komandų eilutėje paleiskite šį scenarijų:
```
python WAR.py
```
3. Vykdykite nurodymus, kad įvestumėte žaidėjų vardus ir pasirinktumėte, ar žaisti prieš kompiuterį.

Norėdami paleisti unit testus:
```
python WAR.py test
```

### c. Kaip naudoti programą?

Paleidus žaidimą, jūsų bus paprašyta įvesti vardus ir nurodyti, ar norite žaisti prieš kompiuterį.
- Norėdami žaisti raundą, paspauskite bet kurį klavišą (išskyrus „q“).
- Norėdami anksčiau išeiti iš žaidimo, bet kuriuo metu paspauskite „q“.
- Programa registruoja kiekvieną raundą ir rodo rezultatą.
- Rezultatai išsaugomi faile `game_results.txt`, pagal tuos rezultatus rodo paskutinius tris laimėtojus.

## Struktūros analizė

### a. Paaiškinkite, kaip programa apima (įgyvendina) funkcinius reikalavimus.
- **4 OOP kolonos:**
- Klasės `Card`, `Deck`, `Player` ir `Game` visos naudoja inkapsuliaciją(apibūdina duomenų ir metodų, kurie dirba su duomenimis, sujungimą viename vienete.).
- Abstrakcija(principas, kurio esmė – paslėpti klasės ar funkcijos vidines įgyvendinimo detales, o vartotojui parodyti tik esmines funkcijas.) yra `CardFactory` klasėje.
- Paveldėjimas( leidžia kurti naujas klases (poklasius), kurios paveldi savybes ir elgseną iš esamų klasių (superklasių). Tai skatina pakartotinį kodo naudojimą ir padeda užmegzti ryšius tarp klasių.) yra naudojamas Klasėje `Player`, jis turi subklasę `ComputerPlayer`,
- Polymorfizmas(programavimo koncepcija, leidžianti metodui atlikti skirtingas užduotis, priklausomai nuo objekto, su kuriuo jis dirba, net jei objektai yra skirtingų tipų.) naudojamas `Card` klasėje `__lt__` ir `__gt__` operatoriuose.
- **Kompozicija:** `Game` klasė turi `Deck` ir `Players`, o `Deck` klasė turi `Card` objektus.
- **Kortų kaladės kūrimas:** `Deck` klasė, naudodama "Factory" design patern, sukuria 52 kortų kaladę ir ją sumaišo.
- **Kortų palyginimai:** Klasė `Card` įgyvendina `__lt__` ir `__gt__`, kad palygintų kortelių vertes.
- **Žaidimo mechanika:** Klasė `Game` tvarko pagrindinę logiką, įskaitant raundo eigą, rezultatų stebėjimą ir nugalėtojo nustatymą.
- **Karo logika:** Įdiegta realistiška karo mechanika – kiekvienam karo scenarijui traukiamos trys užverstos kortos ir viena užversta.
– **Žaidėjo sąveika:** Palaiko žmonių tarpusavio arba žmonių ir kompiuterio žaidimus su dinamine įvestimi.
– **Pastovumas:** Žaidimo rezultatai registruojami byloje, kad būtų galima juos saugoti.
– **Unit test:** „unittest“ modulis apžvelgia pagrindinę logiką: kortų palyginimą, kaladės dydį ir nugalėtojo nustatymą.














