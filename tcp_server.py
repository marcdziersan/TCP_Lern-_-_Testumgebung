import socket
import time
import random
import math
import os
import ipaddress
import json

HOST = '0.0.0.0'
PORT = 5000

SHUTDOWN_COMMAND = "shutdown"
RESTART_COMMAND = "restart"

client_games = {}

database = {}

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
working_dir = ROOT_DIR

quiz_fragen = [
    {
        "frage": "Was ist ein gültiger Variablenname in Python?",
        "optionen": [
            "A) 1name", "B) _name", "C) def", "D) class"
        ],
        "antwort": "B"
    },
    {
        "frage": "Was ergibt 3 * 2 + 1?",
        "optionen": [
            "A) 7", "B) 9", "C) 8", "D) 5"
        ],
        "antwort": "A"
    },
    {
        "frage": "Was macht 'print(\"Hello\")'?",
        "optionen": [
            "A) Gibt 'Hello' aus", "B) Deklariert eine Funktion", "C) Macht nichts", "D) Wirft einen Fehler"
        ],
        "antwort": "A"
    }
]

quiz_status = {}

def verarbeite_befehl(befehl, client_ip):
    global working_dir

    befehl = befehl.strip()

    if befehl.lower() in ["hilfe", "help", "?"]:
        return (
            "Verfügbare Befehle:\n"
            "- hilfe: zeigt diese Übersicht\n"
            "- zeit: aktuelle Uhrzeit\n"
            "- zufall: zufällige Zahl zwischen 1-100\n"
            "- rechne <ausdruck>: einfache Berechnungen (auch sqrt())\n"
            "Mini Games:\n"
            "- wurf 3w6: würfelt 3 Würfel mit je 6 Seiten\n"
            "- lotto:1,2,3,4,5,6,9 → Tipp mit 6 Zahlen + Superzahl\n"
            "- zahlenstart: startet das Spiel 'Zahl erraten'\n"
            "- zahlen:<zahl>: gibt einen Tipp im Spiel ab\n"
            "Compendium:\n"
            "- info:<thema> – Kurzerklärung z. B. info:variablen\n"
            "- code:<thema> – Beispielcode z. B. code:helloworld\n"
            "- quiz:start – Starte ein Lernquiz\n"
            "- quiz:antwort X – Beantworte Quizfrage\n"
            "Datenbank:\n"
            "- db:add Name,Wert – fügt einen Eintrag hinzu\n"
            "- db:find Name – sucht einen Eintrag\n"
            "- db:delete Name – löscht einen Eintrag\n"
            "- db:list – zeigt alle Einträge\n"
            "- db:update Name,Wert – aktualisiert Eintrag\n"
            "- db:save / db:load – speichert/lädt Datenbank als JSON\n"
            "Netzwerk:\n"
            "- ping <ip>: simuliert Ping zu einer IP\n"
            "- whoami: zeigt eigene IP-Adresse\n"
            "- netstat: zeigt simulierte Verbindungen\n"
            "- subnet:<ip>/<prefix> – berechnet Subnetzinfos für IPv4 & IPv6\n"
            "Filesystem:\n"
            "- dir: zeigt Dateien und Ordner\n"
            "- dir /p: seitenweise Anzeige\n"
            "- mkf datei.txt: erstellt eine Datei\n"
            "- mko ordner: erstellt einen Ordner\n"
            "- delete datei.txt|ordner: löscht Datei oder Ordner\n"
            "- cd unterordner: wechselt in Unterordner\n"
            "- cd /: zurück zum Root\n"
            "Server:\n"
            "- shutdown / restart: Serversteuerung"
        )

    elif befehl.lower() == "zeit":
        return time.strftime("Aktuelle Uhrzeit: %H:%M:%S")

    elif befehl.lower() == "zufall":
        return f"Zufallszahl: {random.randint(1, 100)}"

    elif befehl.lower().startswith(("rechne ", "rechnen ")):
        ausdruck = befehl.lower().replace("rechne", "").replace("rechnen", "").strip()
        return rechne(ausdruck)

    elif befehl.lower().startswith("wurf "):
        return wuerfeln(befehl[5:].strip())

    elif befehl.lower().startswith("lotto:"):
        return lotto_pruefen(befehl[6:].strip())

    elif befehl.lower() == "zahlenstart":
        return starte_zahlenraten(client_ip)

    elif befehl.lower().startswith("zahlen:"):
        return pruefe_zahlenraten(befehl[7:].strip(), client_ip)

    elif befehl.lower().startswith("info:"):
        thema = befehl[5:].strip()
        return info_compendium(thema)

    elif befehl.lower().startswith("code:"):
        thema = befehl[5:].strip()
        return code_snippet(thema)

    elif befehl.lower() == "quiz:start":
        return quiz_start(client_ip)

    elif befehl.lower().startswith("quiz:antwort "):
        antwort = befehl[13:].strip().upper()
        return quiz_antwort(client_ip, antwort)

    elif befehl.lower().startswith("db:add "):
        return db_add(befehl[7:])

    elif befehl.lower().startswith("db:find "):
        return db_find(befehl[8:])

    elif befehl.lower().startswith("db:delete "):
        return db_delete(befehl[10:])

    elif befehl.lower() == "db:list":
        return db_list()

    elif befehl.lower().startswith("db:update "):
        return db_update(befehl[9:].strip())

    elif befehl.lower() == "db:save":
        return db_save()

    elif befehl.lower() == "db:load":
        return db_load()

    elif befehl.lower().startswith("ping "):
        ziel_ip = befehl[5:].strip()
        return simuliere_ping(ziel_ip)

    elif befehl.lower() == "whoami":
        return whoami(client_ip)

    elif befehl.lower() == "netstat":
        return netstat_simuliert(client_ip)

    elif befehl.lower().startswith("subnet:"):
        return subnet_rechner(befehl[7:].strip())

    elif befehl.lower().startswith("cd "):
        ziel = befehl[3:].strip()
        return wechsel_verzeichnis(ziel)

    elif befehl.lower().startswith("dir"):
        return verzeichnisse_auflisten(befehl)

    elif befehl.lower().startswith("mkf "):
        dateiname = befehl[4:].strip()
        return datei_erstellen(dateiname)

    elif befehl.lower().startswith("mko "):
        ordnername = befehl[4:].strip()
        return ordner_erstellen(ordnername)

    elif befehl.lower().startswith("delete "):
        ziel = befehl[7:].strip()
        return datei_oder_ordner_loeschen(ziel)

    elif befehl.lower().startswith("cat "):
        dateiname = befehl[4:].strip()
        return zeige_datei(dateiname)

    elif befehl.lower().startswith("write:"):
        return schreibe_datei(befehl[6:].strip())

    elif befehl.lower() == SHUTDOWN_COMMAND:
        return SHUTDOWN_COMMAND

    elif befehl.lower() == RESTART_COMMAND:
        return RESTART_COMMAND

    else:
        return "Unbekannter Befehl. Gib 'hilfe' ein für Optionen."

def rechne(ausdruck):
    try:
        ausdruck = ausdruck.replace("sqrt", "math.sqrt")
        erlaubte_zeichen = "0123456789+-*/(). mathsqrt"
        if any(c not in erlaubte_zeichen for c in ausdruck.replace(" ", "")):
            return "Ungültige Zeichen im Ausdruck."
        ergebnis = eval(ausdruck, {"__builtins__": None, "math": math})
        return f"Ergebnis: {ergebnis}"
    except Exception as e:
        return f"Fehler bei der Berechnung: {e}"

def wuerfeln(eingabe):
    try:
        if "w" not in eingabe:
            return "Format: <anzahl>w<seiten> z. B. 3w6"

        anzahl_str, seiten_str = eingabe.lower().split("w")
        anzahl = int(anzahl_str)
        seiten = int(seiten_str)

        if anzahl < 1 or seiten < 2 or anzahl > 100:
            return "Ungültige Eingabe. Max. 100 Würfel, min. 2 Seiten."

        würfe = [random.randint(1, seiten) for _ in range(anzahl)]
        summe = sum(würfe)
        würfe_str = ", ".join(str(w) for w in würfe)
        return f"Würfe: {würfe_str}\nSumme: {summe}"

    except Exception as e:
        return f"Fehler beim Würfeln: {e}"

def lotto_pruefen(eingabe):
    try:
        teile = [int(x.strip()) for x in eingabe.split(",") if x.strip().isdigit()]
        if len(teile) != 7:
            return "Bitte genau 6 Zahlen + 1 Superzahl angeben, z. B. lotto:1,2,3,4,5,6,9"

        tipp_zahlen = set(teile[:6])
        super_tipp = teile[6]

        if len(tipp_zahlen) != 6 or any(n < 1 or n > 49 for n in tipp_zahlen) or not (0 <= super_tipp <= 9):
            return "Ungültige Zahlen. Tipp: 6x 1–49 + Superzahl 0–9"

        ziehung = set(random.sample(range(1, 50), 6))
        super_ziehung = random.randint(0, 9)

        richtige = tipp_zahlen & ziehung
        super_richtig = (super_tipp == super_ziehung)

        antwort = (
            f"Lottoziehung: {sorted(ziehung)} + Superzahl: {super_ziehung}\n"
            f"Dein Tipp:     {sorted(tipp_zahlen)} + Superzahl: {super_tipp}\n"
            f"Richtige Zahlen: {len(richtige)} ({sorted(richtige)})\n"
        )

        if super_richtig:
            antwort += "Superzahl stimmt ✔️\n"
        else:
            antwort += "Superzahl falsch ❌\n"

        if len(richtige) == 0 and not super_richtig:
            antwort += "Leider kein Glück gehabt."
        else:
            antwort += "Nicht schlecht! 🍀"

        return antwort

    except Exception as e:
        return f"Fehler bei Lotto-Auswertung: {e}"

def starte_zahlenraten(ip):
    client_games[ip] = {
        "zahl": random.randint(1, 100),
        "versuche": 3
    }
    return "Spiel gestartet! Rate eine Zahl von 1 bis 100. Du hast 3 Versuche. (z. B. zahlen:50)"

def pruefe_zahlenraten(tipp_str, ip):
    if ip not in client_games:
        return "Starte ein neues Spiel mit 'zahlenstart'"

    spiel = client_games[ip]

    try:
        tipp = int(tipp_str)
    except:
        return "Ungültiger Tipp. Bitte eine Zahl senden (z. B. zahlen:42)"

    spiel["versuche"] -= 1

    if tipp == spiel["zahl"]:
        del client_games[ip]
        return f"✅ Richtig! Die Zahl war {tipp}. Glückwunsch!"

    if spiel["versuche"] == 0:
        richtige_zahl = spiel["zahl"]
        del client_games[ip]
        return f"❌ Leider verloren. Die richtige Zahl war {richtige_zahl}."

    if tipp < spiel["zahl"]:
        return f"❌ Zu niedrig! Noch {spiel['versuche']} Versuche."
    else:
        return f"❌ Zu hoch! Noch {spiel['versuche']} Versuche."

def info_compendium(thema):
    if thema == "variablen":
        return (
            "🔹 Variablen in Python:\n"
            "- Speichern Werte unter einem Namen\n"
            "- Beispiel:\n"
            "  name = 'Anna'\n"
            "  zahl = 5\n"
            "  preis = 4.99\n"
            "- Datentypen wie str, int, float, bool werden automatisch erkannt."
        )
    elif thema == "funktionen":
        return (
            "🔹 Funktionen in Python:\n"
            "- Wiederverwendbare Codeblöcke mit einem Namen\n"
            "- Beispiel:\n"
            "  def begruessung(name):\n"
            "      print(f'Hallo, {name}!')\n"
            "  begruessung('Max')"
        )
    else:
        return f"Keine Info zum Thema '{thema}' verfügbar."

def code_snippet(thema):
    if thema == "helloworld":
        return (
            "🖥️ Python Hello World:\n"
            "--------------------------\n"
            "print('Hello, World!')\n"
            "--------------------------\n"
            "→ Gibt einfach einen Text auf der Konsole aus."
        )
    else:
        return f"Kein Beispiel zu '{thema}' vorhanden."

def quiz_start(ip):
    quiz_status[ip] = {"frage": 0, "punkte": 0}
    return quiz_zeige_frage(ip)

def quiz_zeige_frage(ip):
    status = quiz_status.get(ip)
    if not status or status["frage"] >= len(quiz_fragen):
        return "🎉 Quiz beendet. Starte neu mit quiz:start"
    
    frage = quiz_fragen[status["frage"]]
    text = f"🧠 Frage {status['frage'] + 1}:\n{frage['frage']}\n" + "\n".join(frage["optionen"])
    return text + "\n\nAntwort mit: quiz:antwort <A/B/C/D>"

def quiz_antwort(ip, antwort):
    status = quiz_status.get(ip)
    if not status:
        return "Bitte starte zuerst mit quiz:start"

    frage_index = status["frage"]
    if frage_index >= len(quiz_fragen):
        return "🎉 Du hast das Quiz bereits beendet."

    aktuelle = quiz_fragen[frage_index]
    if antwort.upper() == aktuelle["antwort"]:
        status["punkte"] += 1
        feedback = "✅ Richtig!"
    else:
        feedback = f"❌ Falsch. Richtige Antwort: {aktuelle['antwort']}"

    status["frage"] += 1

    if status["frage"] >= len(quiz_fragen):
        gesamt = len(quiz_fragen)
        punkte = status["punkte"]
        del quiz_status[ip]
        return f"{feedback}\n\n🎉 Quiz beendet!\nDein Ergebnis: {punkte} von {gesamt} Punkten."
    else:
        return f"{feedback}\n\n" + quiz_zeige_frage(ip)

def db_add(eingabe):
    try:
        name, wert = eingabe.split(",", 1)
        name = name.strip()
        wert = wert.strip()
        if name in database:
            return f"Eintrag '{name}' existiert bereits."
        database[name] = wert
        return f"Eintrag hinzugefügt: {name} → {wert}"
    except Exception:
        return "Fehler beim Hinzufügen. Format: db:add Name,Wert"

def db_find(name):
    name = name.strip()
    if name in database:
        return f"{name} → {database[name]}"
    else:
        return f"'{name}' nicht gefunden."

def db_delete(name):
    name = name.strip()
    if name in database:
        del database[name]
        return f"Eintrag '{name}' wurde gelöscht."
    else:
        return f"'{name}' nicht gefunden."

def db_list():
    if not database:
        return "Datenbank ist leer."
    return "Inhalte:\n" + "\n".join(f"{k} → {v}" for k, v in database.items())

def db_update(eingabe):
    try:
        name, wert = eingabe.split(",", 1)
        name = name.strip()
        wert = wert.strip()
        if name not in database:
            return f"Eintrag '{name}' existiert nicht."
        database[name] = wert
        return f"Eintrag aktualisiert: {name} → {wert}"
    except Exception:
        return "Fehler beim Aktualisieren. Format: db:update Name,Wert"

def db_save():
    try:
        pfad = os.path.join(working_dir, "db.json")
        with open(pfad, "w") as f:
            json.dump(database, f, indent=2)
        return "📁 Datenbank wurde gespeichert (db.json)."
    except Exception as e:
        return f"Fehler beim Speichern: {e}"

def db_load():
    try:
        pfad = os.path.join(working_dir, "db.json")
        if not os.path.exists(pfad):
            return "Keine gespeicherte Datenbank gefunden."
        with open(pfad, "r") as f:
            geladen = json.load(f)
            database.clear()
            database.update(geladen)
        return f"📥 Datenbank wurde geladen ({len(database)} Einträge)."
    except Exception as e:
        return f"Fehler beim Laden: {e}"

def simuliere_ping(ip):
    # Einfach simuliert – kein echter Netzwerkping
    try:
        socket.inet_aton(ip)
        return f"Pinging {ip} mit 32 Bytes Daten:\nAntwort von {ip}: Zeit <1ms\nPing erfolgreich."
    except socket.error:
        return "Ungültige IP-Adresse."

def whoami(client_ip):
    return f"🌐 Deine IP-Adresse: {client_ip}"

def netstat_simuliert(client_ip):
    # Einfach simulierte Netstat-Ausgabe
    return (
        "Aktive Verbindungen:\n"
        f"Proto  Lokale Adresse        Remote-Adresse       Status\n"
        f"TCP    {client_ip}:random    127.0.0.1:5000        ESTABLISHED\n"
        f"TCP    {client_ip}:random    8.8.8.8:80            TIME_WAIT"
    )

def subnet_rechner(eingabe):
    try:
        netz = ipaddress.ip_network(eingabe, strict=False)
        return (
            f"📡 Subnetz-Berechnung für {eingabe}:\n"
            f"- Netzadresse: {netz.network_address}\n"
            f"- Broadcast:   {getattr(netz, 'broadcast_address', '—')}\n"
            f"- Hosts:       {netz.num_addresses}\n"
            f"- Netzmaske:   {netz.netmask if hasattr(netz, 'netmask') else netz.prefixlen}\n"
            f"- Präfix:      /{netz.prefixlen}"
        )
    except Exception as e:
        return f"❌ Ungültige IP/Subnetz-Eingabe: {e}"

# 📁 CMD-Dateibefehle
def verzeichnisse_auflisten(befehl):
    try:
        eintraege = os.listdir(working_dir)
        eintraege.sort()
        if "/p" in befehl:
            seiten = [eintraege[i:i+5] for i in range(0, len(eintraege), 5)]
            seiten_text = "\n\n".join(["\n".join(seite) for seite in seiten])
            return f"Inhalt (Seitenweise):\n{seiten_text}"
        else:
            return "Inhalt:\n" + "\n".join(eintraege)
    except Exception as e:
        return f"Fehler bei dir: {e}"

def datei_erstellen(name):
    try:
        pfad = os.path.join(working_dir, name)
        with open(pfad, 'w') as f:
            f.write("")
        return f"Datei '{name}' wurde erstellt."
    except Exception as e:
        return f"Fehler beim Erstellen der Datei: {e}"

def ordner_erstellen(name):
    try:
        pfad = os.path.join(working_dir, name)
        os.makedirs(pfad, exist_ok=True)
        return f"Ordner '{name}' wurde erstellt."
    except Exception as e:
        return f"Fehler beim Erstellen des Ordners: {e}"

def datei_oder_ordner_loeschen(name):
    try:
        pfad = os.path.join(working_dir, name)
        if os.path.isfile(pfad):
            os.remove(pfad)
            return f"Datei '{name}' wurde gelöscht."
        elif os.path.isdir(pfad):
            os.rmdir(pfad)
            return f"Ordner '{name}' wurde gelöscht."
        else:
            return f"'{name}' wurde nicht gefunden."
    except Exception as e:
        return f"Fehler beim Löschen: {e}"

# 📂 Ordnerwechsel
def wechsel_verzeichnis(ziel):
    global working_dir
    if ziel == "/":
        working_dir = ROOT_DIR
        return f"Wechsel zu Root: {working_dir}"

    neuer_pfad = os.path.abspath(os.path.join(working_dir, ziel))

    if os.path.isdir(neuer_pfad) and neuer_pfad.startswith(ROOT_DIR):
        working_dir = neuer_pfad
        return f"Wechsel zu: {os.path.relpath(working_dir, ROOT_DIR)}"
    else:
        return "Ungültiger Ordner oder Zugriff verweigert."

def zeige_datei(name):
    try:
        pfad = os.path.join(working_dir, name)
        if not os.path.isfile(pfad):
            return f"Datei '{name}' existiert nicht."

        with open(pfad, 'r') as f:
            inhalt = f.read()
            if not inhalt:
                return f"Datei '{name}' ist leer."
            return f"Inhalt von '{name}':\n\n{inhalt}"

    except Exception as e:
        return f"Fehler beim Lesen: {e}"

def schreibe_datei(eingabe):
    try:
        if "|" not in eingabe:
            return "Format: write:datei.txt|Inhalt"

        dateiname, text = eingabe.split("|", 1)
        pfad = os.path.join(working_dir, dateiname.strip())

        with open(pfad, 'a') as f:
            f.write(text.strip() + "\n")

        return f"Inhalt wurde in '{dateiname.strip()}' geschrieben."

    except Exception as e:
        return f"Fehler beim Schreiben: {e}"

# 🔁 Server-Loop
def server_starten():
    global server_running
    print(f"TCP-Server läuft auf {HOST}:{PORT}")
    print(f"Arbeitsverzeichnis: {working_dir}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while server_running:
            conn, addr = s.accept()
            with conn:
                print(f"Verbindung von {addr}")
                data = conn.recv(1024).decode()
                print(f"Empfangen: {data}")

                client_ip = addr[0]
                antwort = verarbeite_befehl(data, client_ip)
                if antwort == SHUTDOWN_COMMAND:
                    conn.sendall(b"Server wird beendet.\n")
                    server_running = False
                elif antwort == RESTART_COMMAND:
                    conn.sendall(b"Server wird neu gestartet...\n")
                    return True
                else:
                    conn.sendall(antwort.encode() + b"\n")
    return False

# ▶️ Starten
server_running = True
while server_running:
    do_restart = server_starten()
    if do_restart:
        print(">> Neustart des Servers...\n")
        time.sleep(1)
    else:
        print(">> Server wurde beendet.")
