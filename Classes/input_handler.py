#!/usr/bin/env python3
# coding: Latin-1
""" Contains the InputHandler functionality """
from   Classes.mikey_monster import JoystickSettingsClass, MikeyMonsterClass, PowerSettingsClass

class InputHandlerClass():
    """ Acts as a bridge between all the different parts """
    def __init__(self):
        """ Initialises the variables """
        self.joystick_settings = JoystickSettingsClass()
        self.power_settings    = PowerSettingsClass()
        self.mikey_monster     = MikeyMonsterClass(self.joystick_settings, self.power_settings)
        self.drive_left        = 0.0
        self.drive_right       = 0.0
        self.horizontal        = 0
        self.vertical          = 0

    def get_battery_details(self):
        """ Returns the battery details """
        return self.mikey_monster.get_battery_details()

    def execute_move(self, joystick):
        """ Reads and executes any valid input """
        self.manage_event(joystick)
        self.perform_move()

    def turn_left(self):
        """ Deals with thurning left """
        # If not moving, move
        if self.vertical > -0.05 and self.vertical < 0.05:
            self.drive_left  = self.horizontal  * self.power_settings.max_power
            self.drive_right = -self.horizontal * self.power_settings.max_power
        # If moving, take the deduction
        else:
            self.drive_left *= 1.0 + (2.0 * self.horizontal)

    def turn_right(self):
        """ Deals with turning right """
        # If not moving, move
        if self.vertical > -0.05 and self.vertical < 0.05:
            self.drive_left    = self.horizontal * self.power_settings.max_power
            self.drive_right = -self.horizontal    * self.power_settings.max_power
        # If moving, take the deduction
        else:
            self.drive_right *= 1.0 - (2.0 * self.horizontal)

    def manage_event(self, joystick):
        """ Deal with any inputted event """
        # Read axis positions (-1 to +1)
        self.get_joystick_inputs(joystick)
        self.drive_left = self.drive_right = -self.vertical
        # Deal with turning left
        if self.horizontal < -0.05:
            self.turn_left()
        # Turning right
        elif self.horizontal > 0.05:
            self.turn_right()
        # Check for button presses
        if joystick.get_button(self.joystick_settings.slow_button):
            self.drive_left  *= self.joystick_settings.slow_factor
            self.drive_right *= self.joystick_settings.slow_factor

    def get_horizontal_axis(self, joystick):
        """ Sets the self.horizontal axis """
        if self.joystick_settings.invert_right_axis:
            self.horizontal = -joystick.get_axis(self.joystick_settings.right_axis)
        self.horizontal = joystick.get_axis(self.joystick_settings.right_axis)

    def get_vertical_axis(self, joystick):
        """ Sets the self.vertical axis """
        if self.joystick_settings.invert_left_axis:
            self.vertical = -joystick.get_axis(self.joystick_settings.left_axis)
        self.vertical = joystick.get_axis(self.joystick_settings.left_axis)

    def get_joystick_inputs(self, joystick):
        """ Sets both the horizontal and vertical axis """
        self.get_horizontal_axis(joystick)
        self.get_vertical_axis(joystick)

    def perform_move(self):
        """ Performs the actual movement """
        self.mikey_monster.drive(self.drive_left, self.drive_right)
