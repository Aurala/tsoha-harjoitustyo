# Ajaminen Poeetryllä

Siirrytään koodin sisältävään hakemistoon ja ajetaan komento:

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

Ennen Ostoskeskuksen käynnistämistä on tehtävä vielä kaksi pientä juttua:

1. Projektin juureen tarvitaan tiedosto `.env`, jonka sisältö on seuraavanlainen:

```
SECRET_KEY="supersecret"
```

Avaimen sisällön voi määrittää vapaasti.

2. Tietokannan tiedot määritetään tiedostoon `config.py`:

```
SQLALCHEMY_DATABASE_URI = "postgresql:///markusaurala"
```

[Kurssiohjeiden](https://hy-tsoha.github.io/materiaali/osa-2/#tietokannan-k%C3%A4ytt%C3%A4minen) mukaisesti vaihda osoitteeseen oma käyttäjätunnuksesi.

Sitten ohjelman voikin käynnistää:

```
inv start
```

Tämän jälkeen siirry web-selaimella osoitteeseen http://127.0.0.1:8080/.
