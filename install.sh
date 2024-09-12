#!/bin/env bash

# INITIAL CHECKS ==============================================================
# Check if script is run as root (using sudo)
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (using sudo)."
  exit 1
fi
# If script is run as root, continue with the rest of the script


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt install python3 python3-venv -y
cd $SCRIPT_DIR
python3 -m venv .venv
.venv/bin/pip3 install RPi.GPIO spidev gpiozero pillow numpy matplotlib lgpio psutil hurry.filesize docker pi-ina219

sudo tee "/lib/systemd/system/e-paper.service" > /dev/null <<EOF
[Unit]
Description=e-Paper Service
#
# Restart if service fails but terminate retries if repeated start-up error
StartLimitIntervalSec=60
StartLimitBurst=5

[Service]
# Edit path if necessary
WorkingDirectory=$SCRIPT_DIR
# Create logs in username or remove for root
#User=epaper
# Edit path if necessary
ExecStart=$SCRIPT_DIR/.venv/bin/python3 $SCRIPT_DIR/e-paper.py
# Restart on failure after 5 seconds
Restart=always
RestartSec=5

[Install]
; # Wait until network target, but app will retry on failure to connect
WantedBy=default.target
EOF

sudo systemctl enable e-paper
sudo systemctl daemon-reload
