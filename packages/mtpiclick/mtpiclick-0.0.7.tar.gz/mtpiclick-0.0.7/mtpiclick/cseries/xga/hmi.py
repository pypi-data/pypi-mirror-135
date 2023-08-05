import time
from pyautogui import (
    moveTo, keyDown, keyUp, press
)
from mtpiclick.click import moveClick
from mtpiclick.point import point

class hmi:
    """ """
    home = "ButtonHome"
    start = "ButtonStart"
    menu  = "ButtonList"
    changeover = "packageName"
    lock = "buttonUser"
    weight = "labelWeight"
    
    def __init__(self):
        self.description = "interface to the main controls"

    def RecordStart(self):
        moveClick(capture)
        time.sleep(2.5)
        moveClick(frame)
        self.Home()
        keyDown('shift')
        press('f9')
        keyUp('shift')
        time.sleep(5)

    def RecordStop(self):
        self.Home()
        time.sleep(2)
        keyDown('shift')
        press('f9')
        keyUp('shift')

    def Record(self, navigation):
        self.RecordStart()
        navigation()
        self.RecordStop()