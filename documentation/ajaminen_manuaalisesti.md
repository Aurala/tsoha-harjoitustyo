# Ajaminen manuaalisesti

Siirrytään koodin sisältävään hakemistoon ja luodaan virtuaaliympäristö:

```
python3 -m venv venv
```

Aktivoidaan virtuaaliympäristö:

```
source venv/bin/activate
```

Asennetaan tarvittavat riippuvuudet:

```
pip install -r requirements.txt
```

Alustetaan tietokanta:

```
flask --app app init-db
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
flask run
```

Tämän jälkeen siirry web-selaimella osoitteeseen http://127.0.0.1:5000/.
