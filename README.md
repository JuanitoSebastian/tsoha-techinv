# Tech Inventory
Tech Inventory on sovellus, jossa esitystekniikkaa omistava yritys voi ylläpitää listaa inventaariosta. Sovellukseen voi kirjata milloin laitteet ovat käytössä ja milloin varastossa vapaana, tämän ansioista sovelluksesta voi kätevästi tarkistaa onko laitteita vapaana tietyille päiville.

Sovelluksen ominaisuuksia ovat:
* Tunnuksen luominen ja niiden avulla kirjautuminen sovellukseen.
  * Normaalit käyttäjät voivat muokata vain itse lisäämiään laitteita ja perua vain omia varauksia.
  * Ylläpitäjät voivat muokata minkä tahansa laitteen tietoja ja perua muiden tekemiä varauksia.
* Laitteita voi lisätä inventaarioon
  * Laitteista voi lisätä tietoja, kuten valmistajan sekä laitteen sarjanumeron.
* Laitteita voi varata tuotantoihin
  * Tuotannolla on kesto (alku pvm - päättymis pvm). 
  * Yksittäisen laitteen voi merkata osaksi tuotantoa. Tällöin laite on varattu tuotannon alusta loppuun saakka, eikä sitä voi varata enää toisiin tuotantoihin.
  