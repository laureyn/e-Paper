#!/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt install python3 python3-venv -y
cd $SCRIPT_DIR
python3 -m venv .venv
.venv/bin/pip3 install RPi.GPIO spidev gpiozero pillow numpy matplotlib lgpio psutil hurry.filesize docker pi-ina219

sudo cp e-paper.service /lib/systemd/system/
sudo systemctl enable e-paper