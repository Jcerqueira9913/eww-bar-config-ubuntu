Aqui tens um `README.md` profissional, moderno e com estilo "Cyberpunk/Clean", pronto para o GitHub. Já deixei os espaços reservados para colares os teus prints e GIFs.

Cria um ficheiro chamado `README.md` na pasta do teu Eww e cola isto:

---

```markdown
# 🚀 Minha Eww Bar & Dashboard Custom

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Eww](https://img.shields.io/badge/Made%20with-Eww-ff79c6.svg)
![Linux](https://img.shields.io/badge/OS-Linux-orange.svg)

Uma configuração completa e personalizada para o **Eww (ElKowars wacky widgets)**.
Inclui uma barra superior dinâmica, um dashboard de notificações persistente e popups de controlo para Música, Wi-Fi e Bluetooth.

> **Estilo:** Minimalista / Dark / Neon Accents.

---

## ✨ Preview

![Barra Principal](link_para_tua_imagem_barra.png)

![Dashboard e Menus](link_para_tua_imagem_dashboard.png)

---

## 🛠️ Funcionalidades

* **🎵 Music Player Inteligente:**
    * Deteta automaticamente Spotify ou outros players via `playerctl`.
    * Mostra Título/Artista e controlos (Play/Pause/Next) diretamente na barra.
    * Popup dedicado com capa (ícone) e controlos avançados.
    * *Script Python robusto que ignora erros de leitura.*
* **🔔 Centro de Notificações:**
    * Histórico de notificações (não perdes nada se fores à casa de banho).
    * Botão "Limpar Tudo".
    * Script Python com Listener DBus em background.
* **📶 Conectividade:**
    * Menu **Wi-Fi**: Lista redes, mostra força do sinal e IP.
    * Menu **Bluetooth**: Lista dispositivos emparelhados, conecta/desconecta com um clique e interruptor Power On/Off.
* **💻 Sistema:**
    * Monitorização de CPU, RAM e Bateria.
    * Calendário e Relógio.

---

## 📦 Dependências

Para que tudo funcione corretamente, precisas de instalar estas ferramentas no teu sistema (Ubuntu/Debian/Arch):

### 1. Ferramentas Base
* **Eww** (Obviamente)
* `python3` (Para os scripts de lógica)
* `playerctl` (Para controlar a música)
* `socat` & `jq` (Utilitários comuns do Eww)
* **Nerd Fonts** (Para os ícones funcionarem. Recomendo: *JetBrains Mono Nerd Font*)

```bash
# Ubuntu/Debian
sudo apt install python3 playerctl jq socat

```

### 2. Bibliotecas Python

```bash
pip3 install dbus-python
# Ou via apt:
sudo apt install python3-dbus

```

---

## 🚀 Instalação

1. **Clonar o repositório:**
```bash
git clone [https://github.com/TEU_USER/TEU_REPO.git](https://github.com/TEU_USER/TEU_REPO.git) ~/.config/eww

```


2. **Dar permissão aos scripts:**
```bash
chmod +x ~/.config/eww/scripts/*

```


3. **Iniciar a barra:**
```bash
eww open bar

```



---

## ⚠️ Nota Importante sobre o Spotify

Se usas o Spotify instalado via **Snap** (Loja do Ubuntu), os widgets de música **não vão funcionar** devido às permissões de segurança (Sandbox).

**Solução Recomendada:** Desinstala o Snap e instala a versão oficial `.deb`:

```bash
# 1. Remover Snap
sudo snap remove spotify

# 2. Instalar Oficial
curl -sS [https://download.spotify.com/debian/pubkey_6224F9941A8AA7D1.gpg](https://download.spotify.com/debian/pubkey_6224F9941A8AA7D1.gpg) | sudo gpg --dearmor --yes -o /etc/apt/trusted.gpg.d/spotify.gpg
echo "deb [http://repository.spotify.com](http://repository.spotify.com) stable non-free" | sudo tee /etc/apt/sources.list.d/spotify.list
sudo apt-get update && sudo apt-get install spotify-client

```

---

## ⚙️ Iniciar com o Sistema

Para iniciar a barra e o script de notificações automaticamente:

1. Abre **Aplicações de Arranque** (Startup Applications).
2. Adiciona duas entradas:

| Nome | Comando |
| --- | --- |
| **Eww Daemon** | `eww daemon` |
| **Eww Bar** | `eww open bar` |
| **Eww Notifs** | `/home/TEU_USER/.config/eww/scripts/notifications.py` |

---

## 🤝 Contribuição

Sente-te à vontade para fazer fork, abrir issues ou sugerir melhorias!
---
