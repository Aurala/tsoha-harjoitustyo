# tsoha-harjoitustyo: Ostoskeskus-verkkokauppa

Tässä repositoriossa on Markus Auralan harjoitustyö kurssille [TKT20019 Tietokannat ja web-ohjelmointi](https://hy-tsoha.github.io/materiaali/).

## Aihe

Harjoitustyössä toteutan Flaskilla yksinkertaisen Ostoskeskus-nimisen verkkokaupan, jossa on seuraavanlaisia toiminnallisuuksia:

- Käyttäjä voi rekisteröityä verkkokauppaan ja kirjautua sisään/ulos.
- Kirjautuneet käyttäjillä on ylläpitosivu, jonka kautta he voivat luoda verkkokaupan sisälle oman kauppansa.
- Kirjautuneet käyttäjät voivat muokata ylläpitosivun kautta oman kauppansa valikoimaa, saatavuustietoja, jne.
- Kaikki käyttäjät voivat selata, etsiä ja katsella tuotteita.
- Kirjautuneet käyttäjät voivat lisätä kauppojen tuotteita ostoskoreihinsa ja tarvittaessa poistaa tuotteita niistä.
- Kirjautunut käyttäjä voi tilata ostoskorinsa sisältämät tuotteet (maksutapana kuvitteellinen lasku, joka toimitetaan rekisteröinnissä annettuun osoitteeseen).
- Kirjautuneilla käyttäjillä on analytiikkasivu, josta he voivat seurata toteutuneita myyntejä ja varastosaldoja.

## Ajaminen

Valmistelen Docker-tiedoston, jonka avulla arvioijat voivat ajaa Ostoskeskusta lokaalisti.

## Testaaminen

Valmistelen skriptin, joka luo tietokantaan kaksi käyttäjää (Tiku ja Taku) sekä molemmille omat kaupat esimerkkituotteineen.
