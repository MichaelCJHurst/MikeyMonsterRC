#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable """
import time
import os
import sys
import pygame
from   Classes.MikeyMonster import JoystickSettings, MikeyMonster

def main():
	""" Run when the program starts """
	# Redirect the output to standard error, to ignore some pygame errors
	sys.stdout = sys.stderr
	# Set up the MikeyMonster
	joystick      = JoystickSettings()
	mikey_monster = MikeyMonster(joystick)
	print(str(mikey_monster.result))

if __name__ == "__main__":
	main()
