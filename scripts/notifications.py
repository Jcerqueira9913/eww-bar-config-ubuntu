#!/usr/bin/env python3
import json
import os
import sys
import subprocess
try:
    import dbus
    from dbus.mainloop.glib import DBusGMainLoop
    from gi.repository import GLib
except ImportError:
    # Se falhar silenciosamente, o Eww nao crasha
    sys.exit(1)

# Caminho absoluto para garantir que funciona sempre
LOG_FILE = os.path.expanduser("~/.config/eww/scripts/notifications.json")
MAX_NOTIFICATIONS = 10

def update_eww(n_list):
    # Escreve no ficheiro
    with open(LOG_FILE, 'w') as f:
        json.dump(n_list, f)
    # Avisa o Eww imediatamente
    subprocess.run(["eww", "update", "notifications_json=" + json.dumps(n_list)])

def load_notifications():
    if not os.path.exists(LOG_FILE): return []
    try:
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    except: return []

def handle_notification(bus, msg):
    args = msg.get_args_list()
    # Indices do DBus: 0:App, 3:Titulo, 4:Corpo
    if len(args) >= 4:
        title = str(args[3])
        body = str(args[4])

        if not title: return

        # Carrega lista atual
        current = load_notifications()

        # --- CORREÇÃO DE DUPLICADOS ---
        # Se a última notificação for igual a esta, ignora
        if len(current) > 0:
            last = current[0]
            if last['title'] == title and last['body'] == body:
                return
        # ------------------------------

        new_notif = {"title": title, "body": body}

        # Insere no topo e corta os antigos
        current.insert(0, new_notif)
        current = current[:MAX_NOTIFICATIONS]

        update_eww(current)

if __name__ == "__main__":
    # Comando para limpar
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        update_eww([]) # Grava lista vazia
        sys.exit(0)

    # Inicia o Listener
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
    bus.add_message_filter(handle_notification)

    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        pass