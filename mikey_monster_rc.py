#!/usr/bin/env python3
# coding: Latin-1
""" Makes the MonsterBorg remote controllable """
import time
import os
import sys
import pygame
from   Classes.input_handler import InputHandlerClass

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

def had_event(event):
    """ Check that there has been a valid event """
    running    = True
    temp_event = False
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.JOYBUTTONDOWN:
        temp_event = True
    elif event.type == pygame.JOYAXISMOTION:
        temp_event = True
    return running, temp_event

def main():
    """ Run when the program starts """
    # Redirect the output to standard error, to ignore some pygame errors
    sys.stdout = sys.stderr
    input_handler = InputHandlerClass()
    # Output the battery details
    output_battery(input_handler.get_battery_details())
    # Remove the need for a GUI window
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    # Init pygame and wait for a joystick
    pygame.init()
    # Connect to a joystick, if there is one, and then initiate it
    print("Waiting for joystick, press CTRL+C to abort")
    joystick = connect_joystick(input_handler.mikey_monster)
    joystick.init()
    print("Found a joystick")
    input_handler.setup_arm()
    # Use the LEDs like normal
    input_handler.mikey_monster.led_show_battery(True)
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
                    #print(event)
                    input_handler.execute_move(joystick)
    except KeyboardInterrupt:
        # CTRL+C exit, so quit gracefully
        input_handler.stop()

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
