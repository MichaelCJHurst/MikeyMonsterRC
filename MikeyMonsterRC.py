#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable """
import time
import os
import sys
import pygame
from   Classes.MikeyMonster import JoystickSettings, MikeyMonster, PowerSettings

def connect_joystick(mikey_monster):
	""" Connects to a joystick """
	while True:
		try:
			try:
				pygame.joystick.init()
				# Attempt to setup the joystick
				if pygame.joystick.get_count() < 1:
					# No joystick, set LEDs to blue
					mikey_monster.set_leds(0, 0, 1)
					pygame.joystick.quit()
					time.sleep(0.1)
				# There is a joystick, attempt to initialise
				else:
					return pygame.joystick.Joystick(0)
			except Exception as ex:
				# Failed to connect joystick, set LEDs to blue
				mikey_monster.set_leds(0, 0, 1)
				pygame.joystick.quit()
				print(str(ex))
				time.sleep(0.1)
		except KeyboardInterrupt:
			# Cancelled searching
			print("User aborted :'(")
			mikey_monster.disable_failsafe()
			mikey_monster.set_leds(0, 0, 0)
			sys.exit()

def main():
	""" Run when the program starts """
	# Redirect the output to standard error, to ignore some pygame errors
	sys.stdout = sys.stderr
	# Set up the MikeyMonster
	joystick_settings = JoystickSettings()
	power_settings    = PowerSettings()
	mikey_monster     = MikeyMonster(joystick_settings, power_settings)
	# If there was an error, exit
	if mikey_monster.result.success is False:
		print(mikey_monster.result.error_msg)
		print(mikey_monster.result.errors)
		sys.exit()
	# Output the battery details
	output_battery(mikey_monster.get_battery_details())
	# Remove the need for a GUI window
	os.environ["SDL_VIDEODRIVER"] = "dummy"
	# Init pygame and wait for a joystick
	pygame.init()
	# Connect to a joystick, if there is one, and then initiate it
	print("Waiting for joystick, press CTRL+C to abort")
	joystick = connect_joystick(mikey_monster)
	joystick.init()
	print("Found a joystick")
	# Use the LEDs like normal
	mikey_monster.led_show_battery(True)
	# This deals with the inputs
	try:
		print("Press CTRL+C to quit")
		drive_left      = 0.0
		drive_right     = 0.0
		running         = True
		had_event       = False
		# Loop indefinitely
		while running:
			# Get the latest events from the system
			had_event = False
			events = pygame.event.get()
			# Handle each event
			for event in events:
				# print(event)
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.JOYBUTTONDOWN:
					had_event = True
				elif event.type == pygame.JOYAXISMOTION:
					had_event = True
				# If there was an event
				if had_event:
					# Read axis positions (-1 to +1)
					if joystick_settings.invert_left_axis:
						drive_left = joystick.get_axis(joystick_settings.left_axis)
					else:
						drive_left = -joystick.get_axis(joystick_settings.left_axis)
					if joystick_settings.invert_right_axis:
						drive_right = joystick.get_axis(joystick_settings.right_axis)
					else:
						drive_right = -joystick.get_axis(joystick_settings.right_axis)
					# Check for button presses
					if joystick.get_button(joystick_settings.slow_button):
						drive_left  *= joystick_settings.slow_factor
						drive_right *= joystick_settings.slow_factor
					# Set the motors to the new speeds
					mikey_monster.drive(drive_left, drive_right)
	except KeyboardInterrupt:
		# CTRL+C exit, so quit gracefully
		mikey_monster.turn_off()

def output_battery(battery):
	""" Outputs the status of the battery """
	print("Battery monitoring settings:")
	print("    Minimum  (red)     %02.2f V" % (battery["minimum"]))
	print("    Half-way (yellow)  %02.2f V" % ((battery["minimum"] + battery["maximum"]) / 2))
	print("    Maximum  (green)   %02.2f V" % (battery["maximum"]))
	print("")
	print("    Current voltage    %02.2f V" % (battery["current"]))
	print("")

if __name__ == "__main__":
	main()
