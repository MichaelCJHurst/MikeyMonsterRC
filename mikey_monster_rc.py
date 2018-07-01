#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable """
import time
import os
import sys
import pygame
from   Classes.MikeyMonster import JoystickSettings, MikeyMonster, PowerSettings

def user_abort(mikey_monster = False):
    """ Safely exits the program when the user aborts """
    print("User aborted :'(")
    if mikey_monster:
        mikey_monster.disable_failsafe()
        mikey_monster.set_leds(0, 0, 0)
    sys.exit()

def show_exception(exception, mikey_monster = False):
    """ Outputs an exception """
    print(str(exception))
    if mikey_monster:
        mikey_monster.set_leds(0, 0, 1)
        pygame.joystick.quit()


def connect_to_joystick(mikey_monster):
    """ Attempts to connect to the joystick """
    pygame.joystick.init()
    # Attempt to setup the joystick
    if pygame.joystick.get_count() < 1:
        # No joystick, set LEDs to blue
        mikey_monster.set_leds(0, 0, 1)
        pygame.joystick.quit()
        time.sleep(0.1)
        return False
    # There is a joystick, attempt to initialise
    return pygame.joystick.Joystick(0)

def connect_joystick(mikey_monster):
    """ Connects to a joystick """
    while True:
        try:
            joystick = connect_to_joystick(mikey_monster)
            if joystick:
                return joystick
        except KeyboardInterrupt:
            # Cancelled searching
            user_abort(mikey_monster)
        except Exception as ex: # pylint: disable=W0703
            show_exception(ex, mikey_monster)
            time.sleep(0.1)
    return False

def get_vertical_axis(joystick, joystick_settings):
    """ Returns the vertical axis """
    if joystick_settings.invert_left_axis:
        return -joystick.get_axis(joystick_settings.left_axis)
    return joystick.get_axis(joystick_settings.left_axis)

def get_horizontal_axis(joystick, joystick_settings):
    """ Returns the horizontal axis """
    if joystick_settings.invert_right_axis:
        return -joystick.get_axis(joystick_settings.right_axis)
    return joystick.get_axis(joystick_settings.right_axis)

def get_joystick_inputs(joystick, joystick_settings):
    """ Returns both the horizontal and vertical axis """
    return get_horizontal_axis(joystick, joystick_settings), get_vertical_axis(joystick, joystick_settings) # pylint: disable=C0301

def had_event(event):
    """ Check that there has been a valid event """
    running    = True
    temp_event = False
    # print(event)
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.JOYBUTTONDOWN:
        temp_event = True
    elif event.type == pygame.JOYAXISMOTION:
        temp_event = True
    return temp_event, running


def manage_event(power_settings, joystick, joystick_settings):
    """ Deal with any inputted event """
    drive_left  = 0.0
    drive_right = 0.0
    # Read axis positions (-1 to +1)
    horizontal, vertical = get_joystick_inputs(joystick, joystick_settings)
    # Determine the drive POWAAHHH
    drive_left = drive_right = -vertical
    # Deal with turning left
    if horizontal < -0.05:
        # If not moving, move
        if vertical > -0.05 and vertical < 0.05:
            drive_left  = horizontal * power_settings.max_power
            drive_right = -horizontal    * power_settings.max_power
        # If moving, take the deduction
        else:
            drive_left *= 1.0 + (2.0 * horizontal)
    # Turning right
    elif horizontal > 0.05:
        # If not moving, move
        if vertical > -0.05 and vertical < 0.05:
            drive_left    = horizontal * power_settings.max_power
            drive_right = -horizontal    * power_settings.max_power
        # If moving, take the deduction
        else:
            drive_right *= 1.0 - (2.0 * horizontal)
    # Check for button presses
    if joystick.get_button(joystick_settings.slow_button):
        drive_left    *= joystick_settings.slow_factor
        drive_right *= joystick_settings.slow_factor
    # returns the drive values
    return drive_left, drive_right

def perform_move(mikey_monster, drive_left, drive_right):
    """ Performs the actual movement """
    mikey_monster.drive(drive_left, drive_right)

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
        running     = True
        was_event   = False
        # Loop indefinitely
        while running:
            # Get the latest events from the system
            was_event = False
            events = pygame.event.get()
            # Handle each event
            for event in events:
                running, was_event = had_event(event)
                if was_event:
                    drive_left, drive_right = manage_event(power_settings, joystick, joystick_settings) # pylint: disable=C0301
                    perform_move(mikey_monster, drive_left, drive_right)
    except KeyboardInterrupt:
        # CTRL+C exit, so quit gracefully
        mikey_monster.turn_off()

def output_battery(battery):
    """ Outputs the status of the battery """
    print("Battery monitoring settings:")
    print("  Minimum  (red)       %02.2f V" % (battery["minimum"]))
    print("  Half-way (yellow)    %02.2f V" % ((battery["minimum"] + battery["maximum"]) / 2))
    print("  Maximum  (green)     %02.2f V" % (battery["maximum"]))
    print("")
    print("  Current voltage      %02.2f V" % (battery["current"]))
    print("")

if __name__ == "__main__":
    main()
