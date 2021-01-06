
ARDCLI=arduino-cli
PORT=/dev/cu.usbmodem14201

build: Servo.alib core
	arduino-cli compile --fqbn arduino:avr:uno arduino

flash: build
	$(ARDCLI) upload -p $(PORT) --fqbn arduino:avr:uno arduino

core:
	$(ARDCLI) core install arduino:avr

%.alib:
	$(ARDCLI) lib install $(@:%.alib=%)