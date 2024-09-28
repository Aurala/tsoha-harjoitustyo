# tsoha-harjoitustyo: Ostoskeskus-verkkokauppa

Tässä repositoriossa on Markus Auralan harjoitustyö kurssille [TKT20019 Tietokannat ja web-ohjelmointi](https://hy-tsoha.github.io/materiaali/).

## Aihe

Harjoitustyössä toteutan Flaskilla yksinkertaisen Ostoskeskus-nimisen verkkokaupan, jossa on seuraavanlaisia toiminnallisuuksia:

- Toteutettu: Käyttäjä voi rekisteröityä verkkokauppaan ja kirjautua sisään/ulos.
- Osittain toteutettu: Kirjautuneet käyttäjillä on ylläpitosivu, jonka kautta he voivat luoda verkkokaupan sisälle oman kauppansa.
- Ei toteutettu: Kirjautuneet käyttäjät voivat muokata ylläpitosivun kautta oman kauppansa valikoimaa, saatavuustietoja, jne.
- Osittain toteutettu: Kaikki käyttäjät voivat selata, etsiä ja katsella tuotteita.
- Osittain toteutettu: Kirjautuneet käyttäjät voivat lisätä kauppojen tuotteita ostoskoreihinsa ja tarvittaessa poistaa tuotteita niistä.
- Ei toteutettu: Kirjautunut käyttäjä voi tilata ostoskorinsa sisältämät tuotteet (maksutapana kuvitteellinen lasku, joka toimitetaan rekisteröinnissä annettuun osoitteeseen). 
- Ei toteutettu: Kirjautuneilla käyttäjillä on analytiikkasivu, josta he voivat seurata toteutuneita myyntejä ja varastosaldoja.

Toteutuksen status päivitetty 28.9.2024.

## Ajaminen

Ohjelma on kehitetty macOS-ympäristössä (Apple Silicon) ja testattu yliopiston Cubbli Linux -koneissa. Ensimmäisen vertaisarvioinnin perusteella ohjelman ajaminen [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/):n alla oli haasteellista, joten Windows-käyttäjille vahva suositus testata Cubbli Linux -koneella.

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

Suositeltavaa: testaamista helpottamaan voidaan tietokantaan luoda testisisältöä. Tästä lisää [täällä](documentation/testaaminen.md).

Ennen Ostoskeskuksen käynnistämistä on tehtävä vielä yksi pieni juttu. Projektin juureen tarvitaan tiedosto `.env`, jonka sisältö on seuraavanlainen:

```
SECRET_KEY="supersecret"
```

Avaimen sisällön voi määrittää vapaasti.

Ohjelman ajaminen:

```
inv start
```

Tämän jälkeen siirry web-selaimella osoitteeseen http://127.0.0.1:8080/.

## Testaaminen

Lue lisää [testaamisesta](documentation/testaaminen.md).

## Tiedossa olevat ongelmat / puutteet / rajoitukset

- Tietokantakyselyt olisi syytä siirtää johonkin funktioon koodin monistamisen sijaan; samalla virheenkäsittelyn lisääminen
- Syöttökenttien validointi sivulla, tai vähintään edes tieto siitä mitä kenttään odotetaan
- `inv format` (`autopep8`) ei tee kaikkia korjauksia; syy tuntematon, tutkittava
- Etusivulla kauppojen ja tuotteiden linkit puuttuvat
- Tuotelistaussivu on, mutta toistaiseksi...
    - Ei osaa filtteröidä tuotteita hakusanojen, kauppojen tai muidenkaan kriteerien perusteella
    - Ei osaa sivuttaa
    - Ostoskoritoiminnallisuus puuttuu
    - Hintojen lokalisointi locale-kirjastoa käyttäen

## Arvostelijalle tiedoksi

- Ohjelmoinnissa pyritty noudattamaan [Flask-projektin tutoriaalia](https://flask.palletsprojects.com/en/3.0.x/tutorial/) sekä kurssin ["Aineopintojen harjoitustyö: Ohjelmistotekniikka"](https://ohjelmistotekniikka-hy.github.io/) käytäntöjä
- Tekoälyä käytetty sparrauskumppanina, mutta koodia sillä ei ole tuotettu
- Grafiikka generoitu tekoälyllä, ei copyrightseja
- Käytän tässä harjoituksessa tietokantaa kuvien tallentamiseen; ei varmasti fiksuin ratkaisu oikeaan käyttöön, mutta kuvittelin tällä taklattavan ongelmia polkujen ja oikeuksien kanssa erilaisissa ympäristöissä
