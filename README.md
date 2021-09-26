# Tech Inventory
Tech Inventory on sovellus, jossa voi pitää inventaariota esitystekniikan laitteista. Inventaarioon voi lisätä uusia laitteita, olemassa olevia laitteita voi muokata ja vanhoja laitteita voi poistaa. Tech Inventoryssä voi myös luoda tuotantoja, joihin laitteita voidaan varata. Näin sovelluksesta voi tarkistaa, milloin mitkäkin laitteet ovat vapaana ja milloin käytössä.

[Välipalautus 2](https://raw.githubusercontent.com/JuanitoSebastian/tsoha-techinv/main/documentation/Välipalautus2.md)

### Sovelluksen ominaisuudet
* Tunnuksen luominen ja sen avulla sovellukseen kirjautuminen.
  * Normaalit käyttäjät voivat muokata vain itse lisäämiään laitteita ja perua vain omia varauksia.
  * Ylläpitäjät voivat muokata minkä tahansa laitteen tietoja ja perua muiden tekemiä varauksia.
* Laitteita voi lisätä inventaarioon
  * Laitteista voi lisätä tietoja, kuten valmistajan sekä laitteen sarjanumeron.
* Laitteita voi varata tuotantoihin
  * Tuotannolla on kesto (alku pvm - päättymis pvm). 
  * Yksittäisen laitteen voi merkata osaksi tuotantoa. Tällöin laite on varattu tuotannon alusta loppuun saakka, eikä sitä voi varata enää toisiin tuotantoihin.

## Tietokanta
Alustava relaatiokaavio tietokannasta.
![Diagram of Database](https://raw.githubusercontent.com/JuanitoSebastian/tsoha-techinv/main/documentation/TechInv_DbDiagram.png)