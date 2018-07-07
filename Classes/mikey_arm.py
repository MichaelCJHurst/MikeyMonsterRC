#!/usr/bin/env python3
# coding: Latin-1
""" Makes the Maplin Arm remote controllable, using the usb_arm library """
import usb.core
import usb.util
# import Classes.usb_arm as usb_arm

# [0,1,0] #Rotate base anti-clockwise
# 1,[0,2,0] #Rotate base clockwise
# 1,[64,0,0] #Shoulder up
# 1,[128,0,0] #Shoulder down
# 1,[16,0,0] #Elbow up
# 1,[32,0,0] #Elbow down
# 1,[4,0,0] #Wrist up
# 1,[8,0,0] # Wrist down
# 1,[2,0,0] #Grip open
# 1,[1,0,0] #Grip close
# 1,[0,0,1] #Light on
# 1,[0,0,0] #Light off

class MikeyArmClass():
    """ Controls the Maplin Arm """
    def __init__(self):
        """ Initialises the Maplin Arm """
        #  If this doesn't work, chances are that the arm isn't connected
        self.arm      = usb.core.find(idVendor=0x1267, idProduct=0x000)
        self.light_on = False

        if self.arm is None:
            print("Arm not found")
            return
        self.arm.reset()
        self.toggle_light()

    def toggle_light(self):
        """ Toggles the light """
        if self.light_on:
            self.light_on = False
            self.send_control([0,0,0])
        else:
            self.light_on = True
            self.send_control([0,0,1])

    def open_grip(self):
        """ Opens the grip """
        self.send_control([2,0,0])

    def close_grip(self):
        """ Closes the grip """
        self.send_control([1,0,0])

    def send_control(self, command):
        """ Moves the arm """
        try:
            self.arm.ctrl_transfer(0x40, 6, 0x100, 0, command)
        except:
            print("oh noes")
            self.emergency_stop()

    def stop_arm(self):
        """ Stops the arm from moving """
        self.send_control([0,0,0])
        if self.light_on:
            self.send_control([0,0,1])

    def emergency_stop(self):
        """ Stops the arm from moving, without checking the led after """
        self.arm.reset()
