#!/usr/bin/env python3
import sys
import signal
import gi
import os

# Importar bibliotecas do GNOME
gi.require_version('Gio', '2.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gio, GLib

# Configurações do DBus
BUS_NAME = "org.gnome.Shell.Screencast"
OBJECT_PATH = "/org/gnome/Shell/Screencast"
INTERFACE_NAME = "org.gnome.Shell.Screencast"

def main():
    # 1. Conectar ao DBus da Sessão
    bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
    
    proxy = Gio.DBusProxy.new_sync(
        bus,
        Gio.DBusProxyFlags.NONE,
        None,
        BUS_NAME,
        OBJECT_PATH,
        INTERFACE_NAME,
        None
    )

    # 2. Definir função de paragem
    loop = GLib.MainLoop()

    def stop_recording(signum, frame):
        try:
            print("A parar gravação...", flush=True)
            proxy.call_sync(
                "StopScreencast",
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None
            )
            print("Guardado em ~/Vídeos.", flush=True)
        except Exception as e:
            print(f"Nota ao parar: {e}", flush=True)
        
        loop.quit()

    # 3. Capturar sinais (Ctrl+C ou kill)
    signal.signal(signal.SIGTERM, stop_recording)
    signal.signal(signal.SIGINT, stop_recording)

    # 4. Iniciar Gravação
    print("A iniciar...", flush=True)
    try:
        # O segredo: Passar GLib.Variant explícito para não haver erro de tipos
        # (sa{sv}) -> String (template), Array de Dicionário (opções)
        params = GLib.Variant('(sa{sv})', ("", {}))
        
        proxy.call_sync(
            "Screencast",
            params,
            Gio.DBusCallFlags.NONE,
            -1,
            None
        )
        print("Gravação ativa.", flush=True)
    except Exception as e:
        print(f"ERRO FATAL: {e}", flush=True)
        sys.exit(1)

    # 5. Manter script vivo
    loop.run()

if __name__ == "__main__":
    main()
