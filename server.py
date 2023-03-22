import asyncio
import pyautogui
import pyperclip
import tornado.web

PRefresh = (85, 51)
PCheck = (308, 290)
PClear = (44, 493)
PConsoleUrl = (34, 629)
PMenuCpy = (120, 433)
PMenuCpySel = (301, 433)
PMenuCpySelBash = (334, 740)  # coy HAR parsed log

MYIP = ""


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
    return data


def click_and_report():
    print("now click_and_report")
    blur_click()
    data = cpy_curl()
    print(MYIP, data)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class ClickCaptchaHandler(tornado.web.RequestHandler):
    def get(self):
        click_and_report()
        self.write('{"ret":1}')

    def post(self):
        click_and_report()
        self.write('{"ret":1}')


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/click_captcha/httpapi/click", ClickCaptchaHandler),
    ])


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    import sys

    MYIP = sys.argv[1]
    asyncio.run(main())
