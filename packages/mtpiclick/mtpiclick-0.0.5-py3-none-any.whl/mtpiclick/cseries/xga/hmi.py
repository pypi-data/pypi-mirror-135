import time
import pyautogui as gui
from .coordinates import home, login, login_password, key_3, key_ok, login_ok, menu, capture, frame
from mtpiclick.click import moveClick

def MoveHome():
    gui.moveTo(home.x, home.y, 1)

def Home():
    moveClick(home)

def Login():
    moveClick(login)

def Login_Password():
    moveClick(login_password)

def Keyboard_3():
    moveClick(key_3)

def Keyboard_OK():
    moveClick(key_ok)

def Login_OK():
    moveClick(login_ok)

def Menu():
    moveClick(menu)

def RecordStart():
    moveClick(capture)
    time.sleep(2.5)
    moveClick(frame)
    Home()
    gui.keyDown('shift')
    gui.press('f9')
    gui.keyUp('shift')
    time.sleep(5)

def RecordStop():
    Home()
    time.sleep(2)
    gui.keyDown('shift')
    gui.press('f9')
    gui.keyUp('shift')

def Record(navigation):
    RecordStart()
    navigation()
    RecordStop()