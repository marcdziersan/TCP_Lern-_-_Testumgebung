import socket

HOST = '127.0.0.1'
PORT = 5000

def sende_befehl(befehl):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(befehl.encode())
            data = s.recv(1024).decode()
            print(f"\n<< Antwort vom Server:\n{data}")
    except Exception as e:
        print(f"Fehler: {e}")

def zeige_menue():
    print("\n===== TCP Client Menü =====")
    print("1. Hilfe anzeigen")
    print("2. Uhrzeit abfragen")
    print("3. Zufallszahl abfragen")
    print("4. Server neustarten")
    print("5. Server beenden")
    print("6. Eigener Befehl")
    print("0. Beenden")
    return input("Auswahl: ")

def client_starten():
    while True:
        auswahl = zeige_menue()
        if auswahl == "1":
            sende_befehl("hilfe")
        elif auswahl == "2":
            sende_befehl("zeit")
        elif auswahl == "3":
            sende_befehl("zufall")
        elif auswahl == "4":
            sende_befehl("restart")
        elif auswahl == "5":
            sende_befehl("shutdown")
            break
        elif auswahl == "6":
            custom = input("Befehl eingeben: ")
            sende_befehl(custom)
        elif auswahl == "0":
            print("Client beendet.")
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    client_starten()
