import pyautogui
import pyperclip

PRefresh = (85, 51)
PCheck = (308, 290)
PClear = (44, 493)
PConsoleUrl = (34, 629)
PMenuCpy = (120, 433)
PMenuCpySel = (301, 433)
PMenuCpySelBash = (334, 740)  # coy HAR parsed log


def move_to(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    if slp > 0:
        pyautogui.sleep(slp)


def move_to_left_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.click()
    if slp > 0:
        pyautogui.sleep(slp)


def move_to_right_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.rightClick()
    if slp > 0:
        pyautogui.sleep(slp)


def blur_click():
    move_to_left_click(PRefresh, slp=10)
    move_to(PClear)
    move_to_left_click(PCheck, dur=1, slp=10)


def cpy_curl():
    move_to_left_click(PClear)
    move_to_left_click(PRefresh, slp=5)
    move_to_right_click(PConsoleUrl, slp=1)
    move_to(PMenuCpy, slp=1)
    move_to(PMenuCpySel, slp=1)
    move_to_left_click(PMenuCpySelBash)
    data = pyperclip.paste()
    print(data)
    return data


blur_click()
cpy_curl()
