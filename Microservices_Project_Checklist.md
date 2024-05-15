
# Microservices Projekt Checkliste

## Übersicht

Dieses Projekt umfasst mehrere Microservices, die in Docker-Containern ausgeführt werden. Die Hauptkomponenten sind:
1. MySQL Datenbank
2. Authentication Service (Spring Boot)
3. Scraping Services (Python)
4. API Gateway (Python oder Java)
5. Notification Service (Python, mit Firebase)
6. Message Queue (RabbitMQ)

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

#### Erweiterungen
- [ ] Rollen integrieren

### 3. Message Queue (RabbitMQ)
- [ ] RabbitMQ im Docker Compose definieren und starten
- [ ] Sicherstellen, dass RabbitMQ läuft und zugänglich ist

### 4. Scraping Services (Python)
- [ ] Python Projekt für Scraper einrichten
- [ ] Verbindung zur MySQL-Datenbank herstellen
- [ ] Dockerfile erstellen
- [ ] Scraper für die erste Webseite implementieren
- [ ] Gescrapte Daten in der Datenbank speichern
- [ ] Nachricht an RabbitMQ senden bei neuen Daten
- [ ] Weitere Scraper für verschiedene Webseiten implementieren
- [ ] Scraping Services containerisieren
- [ ] Services in `docker-compose.yml` hinzufügen

### 5. API Gateway (Python oder Java)
- [ ] API Gateway Projekt einrichten
- [ ] Verbindung zur MySQL-Datenbank und RabbitMQ herstellen
- [ ] Dockerfile erstellen
- [ ] Endpunkte für die Verwaltung der gescrapten Daten erstellen
- [ ] Endpunkte für Benutzerinformationen und Authentifizierung erstellen
- [ ] JWT-Authentifizierung einrichten
- [ ] Endpunkte sichern
- [ ] API Gateway containerisieren
- [ ] Service in `docker-compose.yml` hinzufügen

### 6. Notification Service (Python, mit Firebase)
- [ ] Python Projekt für den Notification Service einrichten
- [ ] Verbindung zu Firebase herstellen
- [ ] Dockerfile erstellen
- [ ] Logik zum Empfangen von Nachrichten aus RabbitMQ implementieren
- [ ] Benachrichtigungen über Firebase senden
- [ ] Notification Service containerisieren
- [ ] Service in `docker-compose.yml` hinzufügen

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

## Allgemeine Hinweise
- [ ] Versionierung: Nutze Git für die Versionskontrolle
- [ ] Dokumentation: Halte die Dokumentation aktuell, insbesondere die API-Dokumentation
- [ ] Tests: Schreibe Unit-Tests und Integrationstests für alle Services
- [ ] CI/CD: Implementiere eine CI/CD-Pipeline für automatisiertes Bauen, Testen und Deployment

## Starten der Services
- [ ] Stelle sicher, dass Docker und Docker Compose installiert sind
- [ ] Starte alle Services mit dem Befehl:

```sh
docker-compose up --build
```

- [ ] Überprüfe die Logs und stelle sicher, dass alle Services korrekt gestartet sind

## Weiterentwicklung
- [ ] Neue Features: Plane und implementiere neue Features in kleinen, überschaubaren Schritten
- [ ] Code Reviews: Führe regelmäßige Code Reviews durch, um die Codequalität hoch zu halten
- [ ] Performance: Überwache die Performance der Services und optimiere sie bei Bedarf

Viel Erfolg bei der Umsetzung deines Projekts!
