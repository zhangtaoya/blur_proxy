import asyncio
import time
import pyautogui
import pyperclip
import tornado.web
from tornado import gen

pyautogui.FAILSAFE = False
'''
#M2
PEnterRefresh = (746, 50)
PRefresh = (85, 52)
PCheck = (308, 290)
PClear = (44, 493)
PConsoleUrl = (33, 628)
PMenuCpy = (128, 429)
PMenuCpySel = (317, 434)
PMenuCpySelBash = (314, 734)  # coy HAR parsed log
'''

# win 1024*768

print(pyautogui.size())
pyautogui.FAILSAFE = False
PEnterRefresh = (647, 52)
PRefresh = (85, 53)
PCheck = (63, 290)
PClear = (46, 318)
dy = 590 - 454
PConsoleUrl = (34, 454 + 136)
PMenuCpy = (86, 259 + 136)
PMenuCpySel = (319, 258 + 136)
PMenuCpySelBash = (320, 559 + 136)  # coy HAR parsed log

MYIP = ""


def time_str(ts=None):
    if not ts:
        ts = time.time()
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


async def move_to(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    if slp > 0:
        await asyncio.sleep(slp)


async def move_to_left_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.click(pose[0], pose[1])
    if slp > 0:
        await asyncio.sleep(slp)


async def move_to_right_click(pose, dur=0.1, slp=0.1):
    pyautogui.moveTo(pose[0], pose[1], duration=dur)
    pyautogui.rightClick(pose[0], pose[1])
    if slp > 0:
        await asyncio.sleep(slp)


async def blur_click():
    await move_to_left_click(PEnterRefresh, slp=1)
    pyautogui.keyDown("enter")
    await asyncio.sleep(0.5)
    pyautogui.keyUp("enter")
    await asyncio.sleep(20)
    # pyautogui.sleep(20)
    await move_to(PClear)
    await move_to_left_click(PCheck, dur=1, slp=10)


async def cpy_curl():
    await move_to_left_click(PClear)
    await move_to_left_click(PRefresh, slp=5)
    await move_to_right_click(PConsoleUrl, slp=1)
    await move_to(PMenuCpy, slp=1)
    await move_to(PMenuCpySel, slp=1)
    await move_to_left_click(PMenuCpySelBash, dur=1, slp=0.5)
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
