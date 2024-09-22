# Testaaminen

## Testisisällön luominen

Testisisältö ajetaan sisään tietokantaan:

```
inv populatedb
```

Testisisällön luominen on suositeltavaa. jotta ohjelmaan tutustuakseen tarvitse rekisteröidä tunnuksia, luoda kauppoja ja tuotteita. Luotava sisältö on kuvattu alla.

## Testisisällön uusiminen

Pääset aina takaisin lähtöpisteeseen näillä komennoilla:

```
inv initdb
```

```
inv populatedb
```

Huomio:
- Kaikki tietokantaan tehdyt muutokset tuhoutuvat
- `inv populatedb` pitää aina ajaa välittömästi tietokannan initialisoinnin jälkeen

## Testisisältö

### Käyttäjätunnukset

| käyttäjätunnus | salasana |
| -------------- | -------- |
| iines@mailinator.com | iines |
| hannu@mailinator.com | hannu |
| pelle@mailinator.com | pelle |

### Muu testisisältö

Kaikille käyttäjille muodostuu automaattisesti verkkokauppa, joka on aktivoitu. Kussakin verkkokaupassa on yksi tuote kuvauksineen, tuotekuvineen yms.
