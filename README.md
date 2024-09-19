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

Ohjelma on kehitetty macOS-ympäristössä (Apple Silicon) ja testattu yliopiston Cubbli Linux -koneissa. Ohjelman toimivuudesta muissa ympäristöissä ei ole tietoa, mutta sitä voi aina yrittää [Docker-ohjeilla](#dockerilla).

### Askel askeleelta

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
inv initdb
```

Alustettaessa tietokantaan luodaan käyttäjä 'admin@kauppakeskus.local' (salasana: 'supersecret').

Testaamista helpottamaan voidaan tietokantaan luoda testisisältöä. Tästä lisää [täällä](documentation/testaaminen.md).

Ohjelman ajaminen:

```
inv start
```

Tämän jälkeen siirry selaimella web-osoitteeseen http://127.0.0.1:8080/.

### Dockerilla

_Tähän tulee ohjeet sovelluksen ajamiseksi Dockerilla (jos aikaa riittää)._

## Testaaminen

Lue lisää [testaamisesta](documentation/testaaminen.md).

## Tiedossa olevat ongelmat / rajoitukset

- Syöttökenttien validointi sivulla, tai vähintään edes tieto siitä mitä kenttään odotetaan
- `inv format` (`autopep8`) ei tee kaikkia korjauksia; syy tuntematon, tutkittava
- Etusivulla kauppojen ja tuotteiden linkit puuttuvat
- Tuotelistaussivu on, mutta...
    - Ei osaa filtteröidä tuotteita
    - Ei osaa sivuttaa
    - Näyttää myyjän id:n, ei nimeä
    - Ostoskoritoiminnallisuus puuttuu

Muista opinnoista johtuen olen hieman jäljessä toteutuksen suhteen. Täytyy kiriä! :)
