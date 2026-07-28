import threading

from playwright.sync_api import sync_playwright


class Browser:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def open(self, url, timeout=60000):
        self.page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

    def img(self):
        return self.page.screenshot()


    def click(self, url, timeout=60000):
        self.page.locator(url).click(timeout=timeout)

    def close(self):
        self.page.close()
        self.browser.close()
        self.p.stop()

_local = threading.local()


def get_browser() -> Browser:
    if not hasattr(_local, "browser"):
        _local.browser = Browser()
    return _local.browser