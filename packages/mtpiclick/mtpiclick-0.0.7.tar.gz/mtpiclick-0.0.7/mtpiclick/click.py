import time
import pyautogui
from .point import point
from pywinauto import application
from pyautogui import (
    moveTo, keyDown, keyUp, press
)

def moveClick(target):
    """

    Parameters
    ----------
    target :
        

    Returns
    -------

    """
    pyautogui.moveTo(target.x, target.y, 1, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(target.x, target.y, 1)
    time.sleep(0.1)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    time.sleep(1)

class window:
    """ """
    def __init__(self, exe, reference):
        try:
            app = application.Application(backend="uia").connect(path = exe)
            self.dlg = app.window(title_re=reference)
            app.top_window().set_focus()
        except:
            app = application.Application(backend="uia").start(exe)    
            time.sleep(30)
            self.dlg = app.window(title_re=reference)

    @staticmethod
    def center(control):
        rect = control.rectangle()
        left = rect.left
        top = rect.top
        bottom = rect.bottom
        right = rect.right
        x = int(left - (left - right)/2)
        y = int(bottom - (bottom - top)/2)
        return point(x, y)

    def move(self, target):
        control = self.get(target)
        center = window.center(control)
        moveTo(center.x, center.y, 1)
        moveTo(center.x + 1, center.y + 1, 1)

    def click(self, target):
        control = self.get(target)
        center = window.center(control)
        moveClick(center)

    @staticmethod
    def value(control):
        return control.legacy_properties()['Name']

    def click_if(self, target, condition):
        control = self.get(target)

        if (window.value(control) == condition):
            self.click(target)

    def get(self, target):
        return self.dlg.child_window(auto_id = target)

    
