import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import { Extension } from 'resource:///org/gnome/shell/extensions/extension.js';

export default class StopRecordingExtension extends Extension {
    enable() {
        this._fileMonitor = null;
        this._file = null;

        const path = '/tmp/stop_gnome_rec';
        this._file = Gio.File.new_for_path(path);

        try {
            this._fileMonitor = this._file.monitor(Gio.FileMonitorFlags.NONE, null);

            this._fileMonitorSignal = this._fileMonitor.connect('changed', (monitor, file, otherFile, eventType) => {
                if (eventType === Gio.FileMonitorEvent.CREATED || eventType === Gio.FileMonitorEvent.CHANGED) {
                    
                    this._stopRecording();

                    // Limpa o ficheiro gatilho
                    GLib.timeout_add(GLib.PRIORITY_DEFAULT, 100, () => {
                        try { this._file.delete(null); } catch (e) {}
                        return GLib.SOURCE_REMOVE;
                    });
                }
            });
        } catch (e) {
            console.error('[StopRec] Erro ao iniciar monitor:', e);
        }
    }

    disable() {
        if (this._fileMonitor) {
            if (this._fileMonitorSignal) {
                this._fileMonitor.disconnect(this._fileMonitorSignal);
                this._fileMonitorSignal = null;
            }
            this._fileMonitor.cancel();
            this._fileMonitor = null;
        }
        this._file = null;
    }

    _stopRecording() {
        let success = false;

        if (Main.screenshotUI) {
            try {
                if (typeof Main.screenshotUI.stopScreencast === 'function') {
                    Main.screenshotUI.stopScreencast();
                    success = true;
                } else if (typeof Main.screenshotUI._stopScreencast === 'function') {
                    Main.screenshotUI._stopScreencast();
                    success = true;
                }
            } catch (e) {
                console.error('[StopRec] Falha no ScreenshotUI:', e);
            }
        }
    }
}