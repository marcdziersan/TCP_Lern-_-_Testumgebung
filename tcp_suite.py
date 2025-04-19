import subprocess
import time
import sys
import os

def starte_server():
    return subprocess.Popen([sys.executable, "tcp_server.py"])

def starte_client():
    subprocess.call([sys.executable, "tcp_gui.py"])

if __name__ == "__main__":
    print(">> Starte Server...")
    server = starte_server()
    time.sleep(1)

    print(">> Starte Client...")
    try:
        starte_client()
    except KeyboardInterrupt:
        print("Abbruch durch Benutzer.")
    finally:
        print(">> Beende Server...")
        server.terminate()
        server.wait()
        print(">> Server gestoppt.")
