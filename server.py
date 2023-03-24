import asyncio
import time
import pyautogui
import pyperclip
import tornado.web
from tornado import gen

pyautogui.FAILSAFE = False
PEnterRefresh = (619, 49)
PRefresh = (85, 51)
PCheck = (308, 290)
PClear = (44, 451)
PConsoleUrl = (33, 586)
PMenuCpy = (106, 396)
PMenuCpySel = (351, 392)
PMenuCpySelBash = (313, 689)  # coy HAR parsed log

MYIP = ""


def time_str(ts=None):
    if not ts:
        ts = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def move_to(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    if slp > 0:
        pyautogui.sleep(slp)


async def move_to_left_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.click()
    if slp > 0:
        await asyncio.sleep(slp)


async def move_to_right_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.rightClick()
    if slp > 0:
        await asyncio.sleep(slp)


async def blur_click():
    move_to(PEnterRefresh, slp=1)
    pyautogui.keyDown("enter")
    await asyncio.sleep(0.5)
    pyautogui.keyUp("enter")
    await asyncio.sleep(20)
    # pyautogui.sleep(20)
    move_to(PClear)
    await move_to_left_click(PCheck, dur=1, slp=10)


async def cpy_curl():
    await move_to_left_click(PClear)
    await move_to_left_click(PRefresh, slp=5)
    await move_to_right_click(PConsoleUrl, slp=1)
    move_to(PMenuCpy, slp=1)
    move_to(PMenuCpySel, slp=1)
    await move_to_left_click(PMenuCpySelBash)
    data = pyperclip.paste()
    return data


ON_CLICK = False


async def click_and_report():
    global ON_CLICK
    if ON_CLICK:
        print(time_str(), "now click doing, bypass")
        return ""
    ON_CLICK = True
    print(time_str(), "now click_and_report")

    await blur_click()
    data = await cpy_curl()
    ON_CLICK = False

    # print(MYIP, data)
    print(time_str(), "click_and_report done")
    return data


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ClickCaptchaHandler(tornado.web.RequestHandler):
    async def get(self):
        data = await click_and_report()
        self.write(data)

    async def post(self):
        data = await click_and_report()
        self.write(data)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/click_captcha/httpapi/click", ClickCaptchaHandler),
    ])


async def main():
    app = make_app()
    port = 8888
    print("now listen on port", port)
    app.listen(port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    import sys

    MYIP = sys.argv[1]
    asyncio.run(main())
