import pyautogui
import pyperclip
import time
import socket

pyautogui.moveTo(100, 100, 1)
"koj3pee+weov2Ee"

data = pyperclip.paste()
print(data)
pyautogui.doubleClick(259,136)
print(pyautogui.size())
print(pyautogui.position())
currentMouseX, currentMouseY = pyautogui.position()

PRefresh = (85, 51)
PCheck = (308, 290)
PClear = (44, 493)
PConsoleUrl = (34, 629)
PMenuCpy = (120, 433)
PMenuCpySel = (301, 433)
PMenuCpySelBash = (334, 740)


def click_at(x, y, duration=0.1, slp=0.1):
    pyautogui.moveTo(x / 2, y / 2, duration)
    pyautogui.click()
    if slp > 0:
        pyautogui.sleep(slp)


def blur_click():
    click_at(170, 194, slp=5)

    click_at(555, 676, duration=0.2, slp=2)
    click_at(623, 891, duration=0.2, slp=1)
    click_at(789, 622, duration=0.2, slp=2)

    click_at(622 * 2, 670 * 2, duration=0.2, slp=1)
    click_at(622, 670, duration=0.6, slp=5)
    click_at(170, 194)


def move_to(x, y, slp=0.1):
    pyautogui.moveTo(x / 2, y / 2)
    if slp > 0:
        pyautogui.sleep(slp)


def right_click_at(x, y, duration=0.1, slp=0.1):
    pyautogui.moveTo(x / 2, y / 2, duration)
    pyautogui.rightClick()
    if slp > 0:
        pyautogui.sleep(slp)


def get_curl():
    click_at(88, 1024, slp=0.5)  # clear all request
    click_at(170, 196, slp=2)  # refresh url

    right_click_at(80, 1338, slp=0.5)  # right click
    move_to(134, 1574, slp=0.5)  # move to
    move_to(598, 1574, slp=0.5)  # move to
    click_at(656, 1880, slp=0.5)  # move to

    data = pyperclip.paste()
    print(data)


time.sleep(5)
blur_click()
get_curl()
