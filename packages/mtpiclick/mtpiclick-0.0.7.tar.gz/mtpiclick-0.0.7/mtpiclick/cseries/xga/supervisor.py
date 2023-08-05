""" from mtpiclick.click import moveClick
from mtpiclick.point import point
from .hmi import Login, Login_Password, Keyboard_3, Keyboard_OK, Login_OK, Menu
from .coordinates import left, submenu, subsubmenu

supervisor_information = point(left, 281)
supervisor_setup = point(left, 506)
supervisor_system = point(submenu, 382)
supervisor_motor = point(subsubmenu, 318)

def LoginSupervisor():
    Login()
    Login_Password()
    Keyboard_3()
    Keyboard_OK()
    Login_OK()

def InformationSupervisor():
    Menu()
    moveClick(supervisor_information)

def SetupSupervisor(loginFirst=False):
    if (loginFirst):
        LoginSupervisor()
    Menu()
    moveClick(supervisor_setup)

def SystemSupervisor(loginFirst=False):
    SetupSupervisor(loginFirst=loginFirst)
    moveClick(supervisor_system)

def MotorSupervisor(loginFirst=False):
    SystemSupervisor(loginFirst=loginFirst)
    moveClick(supervisor_motor) """