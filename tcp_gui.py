import socket
import tkinter as tk
from tkinter import scrolledtext

HOST = "127.0.0.1"
PORT = 5000

def set_status(color):
    status_canvas.itemconfig(status_rect, fill=color)

def sende_befehl(befehl):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(befehl.encode())
            antwort = s.recv(4096).decode().strip()

            if "neu gestartet" in antwort.lower():
                set_status("orange")
                log.delete("1.0", tk.END)
                log.insert(tk.END, f">> {befehl}\n<< {antwort}\n")
                starte_reconnect_loop()
                return

            set_status("green")
            log.delete("1.0", tk.END)
            log.insert(tk.END, f">> {befehl}\n<< {antwort}\n")

    except Exception as e:
        set_status("red")
        log.delete("1.0", tk.END)
        log.insert(tk.END, f"Fehler: {e}\n")

    eingabe.delete(0, tk.END)

def sende_manuell():
    befehl = eingabe.get().strip()
    if befehl:
        sende_befehl(befehl)

def versuche_verbindung():
    """Wird periodisch aufgerufen nach restart"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.5)
            s.connect((HOST, PORT))
            s.sendall(b"hilfe")
            antwort = s.recv(4096).decode().strip()

            set_status("green")
            log.delete("1.0", tk.END)
            log.insert(tk.END, f"<< Server wieder erreichbar\n<< {antwort}\n")
            return  # erfolgreich, kein weiterer Versuch nötig
    except:
        root.after(2000, versuche_verbindung)  # erneut versuchen in 2s

def starte_reconnect_loop():
    root.after(2000, versuche_verbindung)

# GUI-Aufbau
root = tk.Tk()
root.title("TCP GUI Client")

frame = tk.Frame(root)
frame.pack(pady=5)

eingabe = tk.Entry(frame, width=50)
eingabe.pack(side=tk.LEFT, padx=(10, 5))
eingabe.bind("<Return>", lambda event: sende_manuell())

# 🟡 Status-Anzeige (kleines Quadrat)
status_canvas = tk.Canvas(frame, width=20, height=20, highlightthickness=1, highlightbackground="gray")
status_canvas.pack(side=tk.LEFT, padx=(0, 10))
status_rect = status_canvas.create_rectangle(2, 2, 18, 18, fill="gray")

# Senden-Button
sende_button = tk.Button(root, text="Senden", command=sende_manuell)
sende_button.pack(pady=5)

# Log-Anzeige
log = scrolledtext.ScrolledText(root, width=60, height=20)
log.pack(padx=10, pady=10)

# Beim Start automatisch "hilfe" senden
root.after(500, lambda: sende_befehl("hilfe"))

root.mainloop()
