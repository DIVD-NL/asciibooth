#!/bin/bash

if [[ $(cat /etc/*release*|grep bookworm|wc -l) -gt 0 ]]; then
	# Raspberry Pi 

	# Install ascii-image-converter
	if [[ 
		! -e /etc/apt/sources.list.d/ascii-image-converter.list && 
		$(grep "deb [trusted=yes] https://apt.fury.io/ascii-image-converter/ /" | wc -l ) -le 0
	]]; then
		echo 'deb [trusted=yes] https://apt.fury.io/ascii-image-converter/ /' | sudo tee /etc/apt/sources.list.d/ascii-image-converter.list
		sudo apt update
		sudo apt install -y ascii-image-converter
	fi

	apt install python3-picamera2 vim cups python3-flask git figlet python3-cups
	(cd systemd;./install.sh)
fi

