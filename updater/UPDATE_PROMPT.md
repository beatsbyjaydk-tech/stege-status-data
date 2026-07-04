# Ugentlig data-opdatering — Stege Status

Du opdaterer `data.json` i dette repo (Stege Status TV-tavle). Målet: friske
åbningstider + korrekte markeds-datoer for byen Stege på Møn.

## Gør følgende
1. Læs nuværende `data.json`. Bevar schemaet 1:1 (felter, rækkefølge, `id`'er,
   `logo`- og `brand`-felter). Fjern ALDRIG et sted.
2. Re-research via web hver butiks aktuelle åbningstider og ret `hours` hvis de
   har ændret sig (index 0=mandag … 6=søndag; `null` = lukket den dag):
   - REMA 1000, Netto, 365discount, SuperBrugsen Lendemark (supermarkeder)
   - XL-BYG (byggemarked) · Matas (personlig pleje)
   - Øbageren (bageri — tider er historisk usikre, verificér grundigt)
   - Delfino Pizzaria, Saftig (spisesteder)
   Behold/ajourfør `closures` (ferie o.l.), fx Delfinos sommerlukning.
3. Re-research Stege-markeder og opdatér `markets`:
   - `recurring`: Tirsdagsmarked i Stege — kører om sommeren (starter typisk
     første tirsdag i juli, ~6 tirsdage). Sæt `seasonFrom`/`seasonTo` til de
     korrekte datoer for INDEVÆRENDE år (10:00–17:00 medmindre andet oplyses).
   - `dates`: konkrete enkelt-markeder med kendt dato (fx Møns Kræmmermarked på
     Dyrskuepladsen, lokale lørdags-torvemarkeder, Sildemarked, Æblefestival,
     Lyserød Lørdag). Tilføj kommende bekræftede datoer; FJERN datoer der ligger
     i fortiden. Hver dag = ét objekt med `date`,`open`,`close`,`title`,`location`.
   Find KUN datoer du kan bekræfte fra en kilde. Gæt ikke.
4. Sæt `meta.updated` til dagens dato (YYYY-MM-DD) og `meta.generatedBy` til
   "weekly-agent".
5. Skriv den opdaterede `data.json` (gyldig JSON, samme struktur).

Kør derefter `updater/update.sh` — eller hvis du er selve update-scriptets agent,
så bare skriv filen; scriptet committer og pusher.

Vær konservativ: hellere beholde en eksisterende korrekt værdi end at indføre en
usikker ændring. Ingen andre filer end `data.json` må ændres.
