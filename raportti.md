# Raportti

### Resurssien valinta

Valitsin Fastapi-kehyksen ja Pythonin, koska ne olivat tulleet kurssilla tutuiksi ja mahdollistivat näin keskittymisen itse rajapinnan toteutukseen.

FastAPI tarjosi selkeän tavan rakentaa REST rajapintoja, sekä automaattisen dokumentaation mikä helpotti rajapintojen testaamista ja kehitystä.

Tietokannankerrokseksi valitsin SQLModelin ja tietokannaksi SQLiten, koska myös nämä olivat tulleet kurssilla tutuiksi, mutta myös koska ne olivat helppoja ottaa käyttöön.

### Endpointien polkusuunnittelu

Endpointien suunnittelua ohjasi aluksi paperille tehty hahmotelma, jonka avulla mallinsin resurssien välisiä suhteita ennen varsinaista toteutusta. Tämän avulla pystyin arvioimaan, onko rajapinnan rakenne looginen ja helposti ymmärrettävä.

Toteutusvaiheessa hyödynsin REST-periaatteita ja suunnittelin endpointit kuvaamaan selkeästi projektin keskeisiä resursseja, kuten lohkoja, antureita ja mittauksia. Tavoitteena oli rakentaa yhtenäinen ja looginen rakenne, jossa endpointit ovat helposti ymmärrettäviä ja ennakoitavia.

### Mitä minä opin

Opin paljon uutta ja hyödyllisiä asioita. Enum oli yksi uusi asia, johon törmäsin. Aluksi pystyin kirjoittamaan mitä vain, kuten "Aktiivinen", "EI" tai "Banaani", mutta ymmärsin, ettei se ole kovin kannattava ratkaisu. Tämän kautta törmäsin enumiin ja siihen, miten sillä saadaan "lukittua" tilat, jolloin vastauksista ja rajapinnasta tulee selkeämpi.

Yksi suurimmista asioista, mitä opin projektia tehdessä, oli miten voin tehdä tietokantakyselyitä funktion sisällä määrittelemieni mallien perusteella, esim. (AnturiMittausResponse), jolloin pystyin palauttamaan samassa vastauksessa useamman kyselyn tulokset.

Samaan ideaan liittyen opin myös yhdistämään useista tietokantatauluista haettua dataa ja muodostamaan niistä listamuotoisia vastauksia funktion sisällä.

Opin muodostamaan listamuotoisia vastauksia funktioissa ja palauttamaan ne osana API responsea.

Opin hakemaan yksittäisen mittauksen ja sen viimeisimmän arvon käyttämällä max-funktiota ja lambdaa.

Tämä projekti vahvisti myös osaamistani monilla osa-alueilla. Taulujen luonti ja niiden käyttö: olen projektissa toteuttanut API response -mallit vielä Out-tyylillä, mutta jatkossa käytän nimeämistä, kuten AnturiResponse AnturiOutin sijasta. Ymmärsin paremmin taulujen haun jälkeen niiden validointia sekä sitä, mitkä virhekoodit ovat oikeasti järkeviä käyttää.

### Keinoälyn käyttö

Hyödynsin keinoälyä projektin aikana tukena oppimisessa ja ongelmanratkaisussa. Käytin sitä erityisesti käsitteiden selittämiseen, koodin toiminnan ymmärtämiseen sekä omien ratkaisujeni varmistamiseen.

Käytin keinoälyä myös tekstin selkeyttämiseen README- ja raporttiosioissa, mutta kaikki varsinainen toteutus, suunnittelu ja koodi on tehty itsenäisesti.
