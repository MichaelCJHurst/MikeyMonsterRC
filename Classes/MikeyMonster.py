#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable, using the ThunderBorg library """
import Classes.ThunderBorg    as ThunderBorg
import Classes.MikeyFunctions as MikeyFunctions

class JoystickSettings(object):
	""" The object which contains the settings for the joystick """
	def __init__(self, left_axis = 1, right_axis = 2, slow_button = 8, slow_factor = 0.5):
		""" Contains the settings for the joystick """
		self.left_axis = left_axis
		self.invert_left_axis = False
		self.right_axis = right_axis
		self.invert_right_axis = False
		self.slow_button = slow_button
		self.slow_factor = slow_factor
		self.interval = 0.00

class MikeyMonster():
	""" Controls the MonsterBorg """
	def __init__(self, joystick):
		""" Sets up the ThunderBorg, which is used by the MonsterBorg """
		init_error = "Couldn't initialise the MikeyMonster"
		self.joystick = joystick
		# Setup the ThunderBorg
		self.thunderborg = ThunderBorg.ThunderBorg()
		self.thunderborg.Init()
		# Check that a ThunderBorg chip can be found
		self.result = self._find_chips()
		print(self.result)
		# If there was an error, return
		if self.result.success is False:
			self.result.error_msg = init_error
			return

	def _find_chips(self):
		""" Scans for ThunderBorgs """
		if not self.thunderborg.foundChip:
			boards = ThunderBorg.ScanForThunderBorg()
			# If no board was found, state so
			if len(boards) == 0:
				return MikeyFunctions.mikeyresult_error(
					"Couldn't find the ThunderBorg",
					("No ThunderBorg was found")
				)
			else:
				error = "No ThunderBorg at address " + self.thunderborg.i2cAddress +", but at: "
				error = error + ", ".join(boards)
				return MikeyFunctions.mikeyresult_error("Couldn't find the ThunderBorg", (error))
		# Return a success
		return MikeyFunctions.mikeyresult_success()
