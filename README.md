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

### Docker

xxx

### Manuaalisesti

Kun projekti on kopioitu haluttuun paikkaan, siirrytään koodin sisältävään hakemistoon ja ajetaan komento:

```
poetry install
```

Ellei Poetryä ole asennettuna jo, asennusohjeet löytyvät [täältä](https://python-poetry.org/docs/#installing-with-the-official-installer).

```
poetry shell
```

Tietokannan alustaminen:

```
xxx
```

Ohjelman ajaminen:

```
inv start
```

## Testaaminen

xxx

## Tiedossa olevat ongelmat / rajoitukset

- xxx
