#!/usr/bin/env gjs

const GLib = imports.gi.GLib;
const Gio = imports.gi.Gio;
const System = imports.system;

// Tenta importar a biblioteca moderna
let GLibUnix = null;
try {
    GLibUnix = imports.gi.GLibUnix;
} catch (e) {}

// Conectar ao DBus
const bus = Gio.bus_get_sync(Gio.BusType.SESSION, null);

const proxy = Gio.DBusProxy.new_sync(
    bus,
    Gio.DBusProxyFlags.NONE,
    null,
    "org.gnome.Shell.Screencast",
    "/org/gnome/Shell/Screencast",
    "org.gnome.Shell.Screencast",
    null
);

print("A iniciar gravação...");

try {
    proxy.call_sync(
        "Screencast",
        new GLib.Variant("(sa{sv})", ["", {}]), 
        Gio.DBusCallFlags.NONE,
        -1,
        null
    );
    print("Gravação a correr (PID: " + System.programInvocationName + ")...");
} catch (e) {
    print("Erro ao iniciar: " + e.message);
    System.exit(1);
}

const loop = new GLib.MainLoop(null, false);

function stop() {
    try {
        print("A parar...");
        proxy.call_sync("StopScreencast", null, Gio.DBusCallFlags.NONE, -1, null);
    } catch (e) {}
    loop.quit();
    return GLib.SOURCE_REMOVE;
}

// === LÓGICA DE SINAIS CORRIGIDA ===
function adicionar_sinal(sinal, callback) {
    // Tenta o método novo (SEM PRIORIDADE) - Ubuntu 22.04/24.04
    if (GLibUnix && typeof GLibUnix.add === 'function') {
        try {
            return GLibUnix.add(sinal, callback);
        } catch (e) {}
    }
    
    // Tenta o método antigo (COM PRIORIDADE) - Fallback
    try {
        return GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, sinal, callback);
    } catch (e) {
        // Se ambos falharem, não faz nada (o script corre mas só fecha com kill -9)
    }
}

// 15 = SIGTERM, 2 = SIGINT
adicionar_sinal(15, stop);
adicionar_sinal(2, stop);

loop.run();
