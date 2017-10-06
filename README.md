# MonsterBorgRC
Custom RC code for PiBorg's MonsterBorg

# Requirements
- ThunderBorg.py, upgraded to python3
- joystick
	- sudo apt-get install joystick
- A MonsterBorg
	- https://www.piborg.org/monsterborg
- A USB wireless controller, such as:
	- https://thepihut.com/collections/raspberry-pi-store/products/raspberry-pi-compatible-wireless-gamepad-controller

# Notes
- If the ThunderBorg can't be found, and it's finding board 00 instead, that's an issue with the Raspbian version. Running 'sudo rpi-update 5224108' will un-update it to a version that works. Hopefully they'll fix it soon!
- To get this to work with a PS3 controller, follow the instructions at https://www.piborg.org/rpi-ps3-help
