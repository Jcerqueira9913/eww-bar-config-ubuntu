#!/bin/bash

# Colors for pretty output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Configuration
# The folder inside your repo where extension.js and metadata.json are located
SRC_DIR="./gnome_extension" 
EXTENSIONS_DIR="$HOME/.local/share/gnome-shell/extensions"

echo -e "${YELLOW}>>> Starting GNOME Recording Control Extension installation...${NC}"

# 2. Validation
if [ ! -d "$SRC_DIR" ]; then
    echo -e "${RED}ERROR: Directory '$SRC_DIR' not found.${NC}"
    echo "Please make sure you are running this script from the root of the repository."
    exit 1
fi

if [ ! -f "$SRC_DIR/metadata.json" ]; then
    echo -e "${RED}ERROR: 'metadata.json' not found inside '$SRC_DIR'.${NC}"
    exit 1
fi

# 3. Extract UUID from metadata.json
# Uses grep/sed to parse JSON without needing 'jq' installed
UUID=$(grep -oP '"uuid":\s*"\K[^"]+' "$SRC_DIR/metadata.json" 2>/dev/null || sed -n 's/.*"uuid": *"\([^"]*\)".*/\1/p' "$SRC_DIR/metadata.json")

if [ -z "$UUID" ]; then
    echo -e "${RED}ERROR: Could not read UUID from metadata.json.${NC}"
    exit 1
fi

echo -e "Detected Extension UUID: ${GREEN}$UUID${NC}"
DEST_PATH="$EXTENSIONS_DIR/$UUID"

# 4. Installation
if [ -d "$DEST_PATH" ]; then
    echo -e "${YELLOW}Warning: Extension already exists. Updating files...${NC}"
fi

mkdir -p "$DEST_PATH"
cp "$SRC_DIR/extension.js" "$DEST_PATH/"
cp "$SRC_DIR/metadata.json" "$DEST_PATH/"

# If you add a license later, uncomment this:
# [ -f "$SRC_DIR/LICENSE" ] && cp "$SRC_DIR/LICENSE" "$DEST_PATH/"

echo -e "${GREEN}Files successfully copied to: $DEST_PATH${NC}"

# 5. GNOME Shell Reload Logic
echo -e "\n${YELLOW}IMPORTANT:${NC} GNOME Shell needs to be restarted to detect the new extension."

# Check session type
SESSION_TYPE=$XDG_SESSION_TYPE

if [ "$SESSION_TYPE" == "x11" ]; then
    echo -e "X11 Session detected. I can restart GNOME automatically for you (Screen will flash)."
    read -p "Do you want to restart GNOME and enable the extension now? (y/N): " choice
    
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        echo -e "Restarting GNOME Shell..."
        
        # Restart Shell
        killall -HUP gnome-shell
        
        # Wait for Shell to reload
        echo "Waiting for GNOME to return..."
        sleep 5 
        
        # Enable Extension
        gnome-extensions enable "$UUID"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}>>> Success! Extension installed and enabled.${NC}"
        else
            echo -e "${RED}>>> Could not enable extension automatically.${NC}"
            echo "Please try running: gnome-extensions enable $UUID"
        fi
    else
        echo -e "${YELLOW}Installation done. Please restart your session (Logout/Login) to enable it.${NC}"
    fi
else
    # Wayland handling
    echo -e "${YELLOW}Wayland detected. Cannot restart shell without logging out.${NC}"
    echo -e "1. Please Logout and Login."
    echo -e "2. Then run: ${GREEN}gnome-extensions enable $UUID${NC}"
fi