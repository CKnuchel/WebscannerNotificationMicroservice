
# Microservices Projekt Checkliste

## Übersicht

## Reihenfolge der Implementierung

### 1. MySQL Datenbank
- [x] Erstellen der Datenbank mit den notwendigen Tabellen
- [x] Sicherstellen, dass die Datenbank korrekt läuft und zugänglich ist


### 2. Authentication Service (Fast API)
- [x] Projekt einrichten
- [x] Verbindung zur MySQL-Datenbank herstellen
- [x] Dockerfile erstellen
- [x] Endpunkte für Benutzerregistrierung und -anmeldung erstellen
- [x] Hashen der Passwörter (z.B. mit BCrypt)
- [x] JWT-Authentifizierung einrichten
- [x] Endpunkte sichern (Login/Register)
- [x] Service in `docker-compose.yml` hinzufügen

### 3. Message Queue (RabbitMQ)
- [x] RabbitMQ im Docker Compose definieren und starten
- [x] Sicherstellen, dass RabbitMQ läuft und zugänglich ist

### 4. Scraping Services (Python (BS4))
- [x] Python Projekt für Scraper einrichten
- [x] Verbindung zur MySQL-Datenbank herstellen
- [x] Dockerfile erstellen
- [x] Scraper für die erste Webseite implementieren
- [x] Gescrapte Daten in der Datenbank speichern
- [x] Nachricht an RabbitMQ senden bei neuen Daten
- [x] Scraping Services containerisieren
- [x] Services in `docker-compose.yml` hinzufügen

### 5. API Gateway (FastAPI oder Spring Boot)
- [ ] API Gateway Projekt einrichten
- [ ] Verbindung zur MySQL-Datenbank und RabbitMQ herstellen
- [ ] Dockerfile erstellen
- [ ] Endpunkte für die Verwaltung der gescrapten Daten erstellen
- [ ] Endpunkte für Benutzerinformationen und Authentifizierung erstellen
- [ ] JWT-Authentifizierung einrichten
- [ ] Endpunkte sichern
- [ ] API Gateway containerisieren
- [ ] Service in `docker-compose.yml` hinzufügen

### 6. Notification Service (Python, mit Firebase?)
- [ ] Python Projekt für den Notification Service einrichten
- [ ] Verbindung zu Firebase herstellen
- [ ] Dockerfile erstellen
- [ ] Logik zum Empfangen von Nachrichten aus RabbitMQ implementieren
- [ ] Benachrichtigungen über Firebase senden
- [ ] Notification Service containerisieren
- [ ] Service in `docker-compose.yml` hinzufügen

## Weiterentwicklung
- [x] FastAPI (Auth) Konfiguration in .env
- [x] MySQL Port nicht gegen aussen Exposen

## Projektstruktur

```
project-root/
├── .env
├── docker-compose.yml
├── database/
│   └── Dockerfile
├── message-queue/
│   └── Dockerfile
├── authentication-service/
│   ├── Dockerfile
│   ├── src/
│   ├── config/
│   └── tests/
├── scraping-service-1/
│   ├── Dockerfile
│   ├── src/
│   ├── config/
│   └── tests/
├── scraping-service-2/
│   ├── Dockerfile
│   ├── src/
│   ├── config/
│   └── tests/
├── api-gateway/
│   ├── Dockerfile
│   ├── src/
│   ├── config/
│   └── tests/
├── notification-service/
│   ├── Dockerfile
│   ├── src/
│   ├── config/
│   └── tests/
└── README.md
```


