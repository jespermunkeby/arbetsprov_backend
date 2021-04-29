# arbetsprov backend

## Specifikation

Med hjälp av valfritt programmeringsspråk ska en objektorienterad modell för ett parkeringsgarage byggas. Bilar "stämplar in" när de kommer och "stämplar ut" när de åker. I samband med att de åker får de betala för den tid de stått parkerade. Priset för att parkera är 12 SEK för varje påbörjad timme. Den parkeringsansvarige på kommunen vill kunna ta ut en förteckning över vilka bilar (inklusive registreringsnummer) som har stått parkerade under en viss tidsperiod, samt hur mycket inkomsten är för den önskade tidsperioden.

## Modellen i stora drag
Det finns många saker som skulle kunna göras annorlunda med lite mer tid, men det jag främst fokuserat på är en långsiktig lösning. I problemet vill man lagra loggar på parkerade bilar i en odefinerad tid framöver, vilket gör att databasen är ständigt växande. När man sedan vill hämta från databasen gäller det då att sökanropet inte är allt för beroende av storleken av databasenn (antalet bil-loggar på den), för att garantera långsiktig prestanda. 

### FakeIntervalTree
Datastrukturen jag valt för att adressera problemet är ett [intervall-träd](https://en.wikipedia.org/wiki/Interval_tree#Centered_interval_tree). Intervallrädet har en tidskomplexitet för sökning av ett intervall av **~O(log n)** (n är antalet parkerings-loggar), vilket är "i stort sett konstant", åtminstonde om man jämför med en filter av en databas, vilket är **O(n)**. Det finns standardmässiga implementationer av intervallräd att hitta på github eller att implementera själv, men p.g.a. tidsbegränsningen har jag skapat klassen "FakeIntervalTree" som är just det - ett fejkat intervallträd. FakeIntervalTree har endast metoder som går att implementera på ett "riktigt" intervallträd, men har inte samma prestanda.

### ParkingGarage
ParkingGarage är den huvudsakliga klassen i min modell av systemet. Den har en intern klocka, en log på bilar som är parkerade just nu, samt en backlog på bilar som tidigare har varit parkerade. Bilar läggs till i loggen av parkerade med metoden enter(lic_plate) och förs över från loggen av parkerade till backlog med metoden exit(lic_plate). Metoden get_summary(datetime_from, datetime_to) ger en dictionary med tjänade pengar och info om alla bilar som varit eller är parkerade någoon gång under intervallet mellan datetime_from och datetime_to.

## Mina avslutande kommentarer
Jag vet inte om jag förstått uppgiften rätt, eller lyckats beskriva den på ett dugligt sätt, men här är det som jag jobbade på i alla fall. Svarar gärna på frågor, bara att slå en pling eller skicka ett mail isåfall

Mvh,
Jesper



