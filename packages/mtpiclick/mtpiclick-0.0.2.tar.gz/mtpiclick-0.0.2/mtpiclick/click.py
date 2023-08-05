import time
import pyautogui

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