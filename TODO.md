## TODO

### Scraper

- [ ] Erstellen eines Ordner für die Basisdefinitionen des Scrapers

  - [ ] Definition der Schemas für die Datenbank
        - Wird anschliessend 1 zu 1 in jedem Scraper verwendet um ein konstantes Datenformat zu gewährleisten
    - [ ] Definition der Datenbankzugriffe
      - Jeder Scraper soll die gleichen Methoden verwenden um Daten in die Datenbank zu schreiben
    - [ ] Definition des Scrapers
      - Jeder Scraper soll die gleichen Methoden verwenden um Daten zu sammeln
      - Somit muss für jeden Scraper nur die Definition der zu sammelnden Daten und die URL angepasst werden
    - [ ] Definition der Modelle
      - Jeder Scraper soll die gleichen Methoden verwenden um Daten zu verarbeiten
      - Somit muss für jeden Scraper nur die Definition der zu verarbeitenden Daten angepasst werden
    - [ ] Definition der API
      - Jeder Scraper soll die gleichen Methoden verwenden um Daten abzurufen
      - Somit muss für jeden Scraper nur die Definition der abzurufenden Daten angepasst werden
      - Im Main muss nur der Prefix der API angepasst werden

### RabbitMQ

- [ ] Definition erstellen, wie die Daten von den Scrapern an RabbitMQ gesendet werden
  - [ ] Definition des Exchanges, Queue und Routing Key

### Notification

- [ ] Definition wie die Daten von RabbitMQ an die Notification API gesendet werden
  - [ ] Definition des Exchanges, Queue und Routing Key

- [ ] Definition der Subscriptions der unterschidlichen Benutzer
  - [ ] Definition des Datenbankmodells

- [ ] Integration von Firebase (Push Notifications - Mobile)
- [ ] Integration von Email (Email Notifications - Desktop)

inegration Webapp (Browser Notifications - Desktop)

- [ ] Verwenden von Websockets um die Daten in Echtzeit zu erhalten
  - [ ] Daten ungelesen markieren bis der Benutzer sie gelesen hat
    Umsetzungsidee:
    - [ ] Benutzer erhält eine Benachrichtigung
    - [ ] Benutzer öffnet die Benachrichtigung
    - [ ] Benachrichtigung wird als gelesen markiert
    - [ ] Benachrichtigung wird aus der Liste der ungelesenen Benachrichtigungen entfernt
    - [ ] Liste mit Status wird getrackt mittels Websockets und in der Datenbank gespeichert
