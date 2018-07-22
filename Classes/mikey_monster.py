#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable, using the ThunderBorg library """
import Classes.ThunderBorg3    as thunderborg

class MikeyMonsterException(Exception):
    """ Manages any exceptions raised by MikeyMonster """
    pass

class JoystickSettingsClass(object):
    """ The object which contains the settings for the joystick """
    def __init__(
            self,
            left_axis = 1,
            right_axis = 3,
            slow_button = 8,
            fast_button = 9,
            light_button = 2
    ):
        """ Contains the settings for the joystick """
        self.left_axis         = left_axis
        self.invert_left_axis  = False
        self.right_axis        = right_axis
        self.invert_right_axis = False
        self.slow_button       = slow_button
        self.slow_factor       = 0.5
        self.fast_button       = fast_button
        self.light_button      = light_button
        self.open_grip         = 0
        self.close_grip        = 1
        self.base_acw          = 7
        self.base_cw           = 6
        self.shoulder_up       = 15
        self.shoulder_down     = 13
        self.elbow_up          = 16
        self.elbow_down        = 14
        self.wrist_up          = 4
        self.wrist_down        = 5
        self.stop_stop_please_stop = 3
        self.interval          = 0.00

class PowerSettingsClass(object): # pylint: disable=R0903
    """ Contains the power settings """
    def __init__(self, voltage_in = 12.00, voltage_out = 11.4):
        """ Contains the settings for the POWAAHH! """
        self.voltage_in  = float(voltage_in)
        self.voltage_out = float(voltage_out)
        # Set up the power limits
        if self.voltage_out > self.voltage_in:
            self.max_power = 1.0
        else:
            self.max_power = self.voltage_out / self.voltage_in

class MikeyMonsterClass():
    """ Controls the MonsterBorg """
    def __init__(self, joystick, power):
        """ Sets up the ThunderBorg, which is used by the MonsterBorg """
        self.failsafe = False
        self.joystick = joystick
        self.power    = power
        # Setup the ThunderBorg
        self.thunderborg = thunderborg.ThunderBorg()
        self.thunderborg.Init()
        # Check that a ThunderBorg chip can be found
        self._find_chips()
        # Set the motors and LEDs off
        self.thunderborg.MotorsOff()
        self.thunderborg.SetLedShowBattery(False)
        self.thunderborg.SetLeds(0,0,1)

    def drive(self, left, right):
        """ Moves the MikeyMonster """
        self.thunderborg.SetMotor1(right * self.power.max_power)
        self.thunderborg.SetMotor2(left  * self.power.max_power)

    def set_leds(self, led1, led2, led3):
        """ Sets the LEDs """
        self.thunderborg.SetLeds(led1, led2, led3)

    def get_battery_details(self):
        """ Returns the state of the battery """
        battery = {}
        battery["minimum"], battery["maximum"] = self.thunderborg.GetBatteryMonitoringLimits()
        battery["current"] = self.thunderborg.GetBatteryReading()
        return battery

    def enable_failsafe(self):
        """ Enables the failsafe """
        failsafe = False
        # Makes five attempts at enabling the failsafe
        for index in range(5):
            # This is just to stop Pylint complaining about an unused variable
            index = index
            # Set the failsafe
            self.thunderborg.SetCommsFailsafe(True)
            failsafe = self.thunderborg.GetCommsFailsafe()
        # Set the class's failsafe to match the function failsafe
        self.failsafe = failsafe

    def disable_failsafe(self):
        """ Enables the failsafe """
        failsafe = False
        # Makes five attempts at disabling the failsafe
        for index in range(5):
            # This is just to stop Pylint complaining about an unused variable
            index = index
            # Set the failsafe
            self.thunderborg.SetCommsFailsafe(False)
            failsafe = self.thunderborg.GetCommsFailsafe()
        # Set the class's failsafe to match the function failsafe
        self.failsafe = failsafe

    def led_show_battery(self, show = True):
        """ Changes whether the LEDs show the battery status or not """
        self.thunderborg.SetLedShowBattery(show)

    def turn_off(self):
        """ Switches off """
        self.thunderborg.MotorsOff()
        self.disable_failsafe()
        self.led_show_battery(False)
        self.set_leds(0, 0, 0)

    def _find_chips(self):
        """ Scans for ThunderBorgs """
        if not self.thunderborg.foundChip:
            boards = thunderborg.ScanForThunderBorg()
            # If no board was found, state so
            if not boards:
                raise MikeyMonsterException("No ThunderBorg boards found")
            else:
                error = "No ThunderBorg at address " + self.thunderborg.i2cAddress +", but at: "
                error = error + ", ".join(boards)
                raise MikeyMonsterException(error)
