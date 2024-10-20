# tsoha-harjoitustyo: Ostoskeskus-verkkokauppa

Tässä repositoriossa on Markus Auralan harjoitustyö kurssille [TKT20019 Tietokannat ja web-ohjelmointi](https://hy-tsoha.github.io/materiaali/).

Dokumentti päivitetty: 20.10.2024

## Aihe

Harjoitustyössä toteutan Flaskilla yksinkertaisen Ostoskeskus-nimisen verkkokaupan, jossa on seuraavanlaisia toiminnallisuuksia:

- Toteutettu: Käyttäjä voi rekisteröityä verkkokauppaan ja kirjautua sisään/ulos.
- Toteutettu: Kirjautuneilla käyttäjillä on ylläpitosivu, jonka kautta he voivat aktivoida verkkokaupan sisällä oman kauppansa.
- Toteutettu: Kirjautuneet käyttäjät voivat muokata ylläpitosivun kautta oman kauppansa valikoimaa, saatavuustietoja, jne.
- Toteutettu: Kaikki käyttäjät voivat selata, etsiä ja katsella tuotteita.
- Toteutettu: Kirjautuneet käyttäjät voivat lisätä kauppojen tuotteita ostoskoreihinsa ja tarvittaessa poistaa tuotteita niistä.
- Toteutettu: Kirjautunut käyttäjä voi tilata ostoskorinsa sisältämät tuotteet (maksutapana kuvitteellinen lasku, joka toimitetaan rekisteröinnissä annettuun osoitteeseen).
- Toteutettu (paitsi varastosaldot, jotka löytyvät muualta): Kirjautuneilla käyttäjillä on analytiikkasivu, josta he voivat seurata toteutuneita myyntejä ~~ja varastosaldoja~~.

Toteutettu = perustoiminnallisuus löytyy, mutta hifisteltävää olisi. Lista [täällä](#tiedossa-olevat-ongelmat--puutteet--rajoitukset).

## Ajaminen

Ohjelma on kehitetty macOS-ympäristössä (Apple Silicon) ja testattu yliopiston Cubbli Linux -koneissa. Vertaisarvioinnin perusteella ohjelman ajaminen [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/):n alla oli haasteellista, joten Windows-käyttäjille vahva suositus testata Cubbli Linux -koneella.

Ohjelma käyttää PostgreSQL-tietokantaa. Kehityskoneella on ollut käytössä [Postgres.app](https://postgresapp.com/) v2.7.8 default-asetuksilla. Cubbli Linux -koneilla PostgreSQL tein PostgreSQL-asennuksen [asennusskriptiä](https://hy-tsoha.github.io/materiaali/osa-2/#tietokannan-k%C3%A4ytt%C3%A4minen) käyttäen.

### Askel askeleelta

Alla on linkit ohjeisiin ohjelman ajamiseen manuaalisesti tai Poetryn avulla. Ensimmäinen askel on kummassakin vaihtoehdossa sama eli projektin kloonaus omaan ympäristöön.

- [Ajaminen manuaalisesti](documentation/ajaminen_manuaalisesti.md)
- [Ajaminen Poetryn avulla](documentation/ajaminen_poetryn_avulla.md)

## Testaaminen

Lue lisää [testaamisesta](documentation/testaaminen.md).

## Tiedossa olevat ongelmat / puutteet / rajoitukset

- Monessa paikassa, kuten tietokantakyselyissä ja syötteen validoinnissa, on koodia, joka olisi syytä siirtää johonkin funktioon/apuluokkaan koodin monistamisen sijaan
- `inv format` (`autopep8`) ei tee kaikkia korjauksia - syy tuntematon, joten tein korjauksia käsin
- Syötteiden katkaiseminen tietyn mittaisiksi ennen tallentamista

## Arvostelijalle tiedoksi

- Ohjelmoinnissa pyritty noudattamaan myös [Flask-projektin tutoriaalia](https://flask.palletsprojects.com/en/3.0.x/tutorial/) sekä kurssin ["Aineopintojen harjoitustyö: Ohjelmistotekniikka"](https://ohjelmistotekniikka-hy.github.io/) käytäntöjä
- Tekoälyä käytetty sparrauskumppanina, mutta koodia sillä ei ole tuotettu
- Grafiikka generoitu tekoälyllä, ei copyrightseja
- Käytän tässä harjoituksessa tietokantaa kuvien tallentamiseen; ei varmasti fiksuin ratkaisu oikeaan käyttöön, mutta kuvittelin tällä taklattavan ongelmia polkujen ja oikeuksien kanssa erilaisissa ympäristöissä
