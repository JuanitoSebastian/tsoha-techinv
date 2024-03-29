# Tech Inventory
![Screenshot of Tech Inventory](https://raw.githubusercontent.com/JuanitoSebastian/tsoha-techinv/main/documentation/techinv_screen.png)
Tech Inventory on sovellus, jossa voi pitää inventaariota esitystekniikan laitteista. Inventaarioon voi lisätä uusia laitteita, olemassa olevia laitteita voi muokata ja vanhoja laitteita voi poistaa. Tech Inventoryssä voi myös luoda tuotantoja, joihin laitteita voidaan varata. Näin sovelluksesta voi tarkistaa, milloin mitkäkin laitteet ovat vapaana ja milloin käytössä.

## Sovelluksen ominaisuudet
* Tunnuksen luominen ja sen avulla sovellukseen kirjautuminen.
  * Normaalit käyttäjät voivat muokata vain itse luomiaan laitteita tai tuotantoja
  * Ylläpitäjät voivat muokata minkä tahansa laitteen tai tuotannon tietoja
* Laitteita ja tuotantoja voi lisätä sekä poistaa järjestelmästä
  * Laitteista voi lisätä tietoja, kuten valmistajan sekä laitteen sarjanumeron.
* Laitteita ja tuotantoja voi muokata
  * Luodun laitteen mallin nimeä voi muokata ja valmistajaa voi muuttaa
  * Luodun tuotannon nimeä ja ajankohtaa voi muokata
* Laitteita voi varata tuotantoihin
  * Tuotannolla on kesto (alku pvm - päättymis pvm). 
  * Yksittäisen laitteen voi merkata osaksi tuotantoa. Tällöin laite on varattu tuotannon alusta loppuun saakka, eikä sitä voi varata enää toisiin tuotantoihin.

## Sovelluksen käyttäminen
Tech Inventoryä voi testata [Herokussa](https://tsoha-techinv.herokuapp.com/). 

## Sovelluksen lopullinen tilanne
Sain toteutettua lähes kaikki toiminnot, jotka projektin alussa kirjasin tavoitteiksi. Olen tyytyväinen työni lopputuloksesta, ja minusta sovelluksesta tuli oikein hyvä. Projektin loppupuolella huomasin, että alkoi kasvaa aika suureksi, eikä minulla riittäny aika hioa kaikkia sovelluksen toimintoja sellaiseksi kuin olisin halunnut. Etenkin laitteiden varaamisessa olisi mielestäni yhä työstettävää.

### Tietokanta
![Diagram of Database](https://raw.githubusercontent.com/JuanitoSebastian/tsoha-techinv/main/documentation/techinv_db.png)
Tietokanta koostuu 11 taulusta.

### Ulkoasu
Toteutin sovelluksen ulkoasun manuaalisesti ilman kirjastoja. Kirjoitin tyylit käyttämällä .scss, jotka käänsin [Sassilla](https://sass-lang.com/) normaaliksi .css:ksi.