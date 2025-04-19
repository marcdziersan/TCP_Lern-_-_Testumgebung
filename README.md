## 📦 `README.md` – **TCP Lern- & Testumgebung für Auszubildende**

# 🧠 TCP Lernserver – interaktive Ausbildung per Netzwerk

Ein voll funktionsfähiger TCP-Server mit grafischer und konsolenbasierter Clientanbindung – speziell für die Ausbildung von **Fachinformatiker:innen Anwendungsentwicklung** entwickelt.  
Ziel: Spielerisch und praktisch mit Themen wie Python, Netzwerk, Dateien, CMD-Befehlen und Mini-Spielen lernen – **im echten Client-Server-Umfeld!**

---

## 🚀 Features

| Kategorie          | Funktionen                                                  |
|--------------------|-------------------------------------------------------------|
| 📚 Lern-Compendium  | `info:`, `code:`, `quiz:start`, `quiz:antwort X`            |
| 🔢 Rechnen & Spiel  | `rechne`, `wurf`, `lotto`, `zahlenstart`, `zahlen:X`        |
| 🗂️ Dateibefehle      | `dir`, `mkf`, `mko`, `delete`, `cd`, `cat`, `write:`        |
| 🧠 Datenbank (CRUD) | `db:add`, `db:find`, `db:list`, `db:save`, `db:update`      |
| 🌐 Netzwerktools    | `ping`, `whoami`, `netstat`, `subnet:`                      |
| ✅ GUI & Console    | Konsolen-Client & moderne Tkinter-GUI mit Statusanzeige     |
| 🛠 Server-Steuerung | `restart`, `shutdown`, Live-Statusfarben im GUI             |

---

## 🖥 Aufbau

- `tcp_server.py` – Hauptserver mit allen Features
- `tcp_client.py` – CLI-Menü-Client zur Steuerung
- `tcp_gui.py` – Grafischer Client mit Antwortanzeige und Statusanzeige
- `tcp_suite.py` – Startet Server & GUI gemeinsam
- (Optional: Modularisierung in `utils.py`, `handler.py` etc. verfügbar)

---

## 🎯 Warum per TCP?

> Man könnte diese Logik auch ohne Server in einzelnen Programmen realisieren – aber…

**Das Lernen mit TCP bringt echten Mehrwert:**

- 🧠 **Netzwerkverständnis** fördern: Socket-Kommunikation verstehen  
- 🧪 **Multi-Client-Fähigkeit** simulieren  
- 🔁 **Restart/Shutdown**-Steuerung live erleben  
- 🧩 Trennung von Client & Server = echte Architektur wie in der Praxis  
- 🛜 Vorbereitung auf spätere Server-/Service-Entwicklung

---

## 🎓 Lernziele

- **Python-Grundlagen interaktiv lernen** (Variablen, Funktionen, Rechnen, etc.)
- **CMD-ähnliche Dateibefehle** testen und umsetzen
- **Datenbanklogik (CRUD)** spielerisch verstehen
- **Quizzes & Info-Module** mit Bewertungssystem
- **Einfache Netzwerkgrundlagen begreifen**
- **Client-Server-Architektur praktisch erleben**

---

## ✅ Starten

```bash
# TCP Suite starten (empfohlen)
python tcp_suite.py
```

Oder einzeln:

```bash
# Server starten
python tcp_server.py

# Separat Client oder GUI öffnen
python tcp_client.py
python tcp_gui.py
```

---

## 🧠 Beispielbefehle

```txt
hilfe
zeit
zufall
rechne 5+5*2
wurf 3w6
lotto:1,2,3,4,5,6,9
zahlenstart
zahlen:50
info:variablen
quiz:start
quiz:antwort A
db:add Max,25
db:update Max,30
ping 8.8.8.8
subnet:192.168.1.0/24
cd unterordner
cat datei.txt
```

---

## ❤️ Für wen ist das gedacht?

- Azubis Fachinformatik AE/SE
- Informatikunterricht mit Fokus auf praktische Anwendungen
- Dozierende oder Schulungen im Bereich Python & Netzwerke
- Jede:r, der interaktiv Lernen & Entwickeln will

---

## 📄 Lizenz

MIT – Frei nutzbar, anpassbar, erweiterbar.

---

## 📌 Hinweis

> Dieses Projekt wurde bewusst **als TCP-Netzwerkserver** umgesetzt – für maximalen Lerneffekt und Realitätsnähe.
> 
> Es zeigt, wie man einfache, didaktische Inhalte als echtes Client-Server-System **modular, skalierbar und interaktiv** gestaltet.

```
