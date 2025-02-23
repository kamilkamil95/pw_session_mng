import time
from playwright.sync_api import Page


def test_logged(page_logged: Page):
    page_logged.goto("http://127.0.0.1:8000")
    time.sleep(5)
    assert "Logged in" in page_logged.content()


def test_not_logged(page_not_logged: Page):
    page_not_logged.goto("http://127.0.0.1:8000")
    time.sleep(5)
    assert "Not logged in" in page_not_logged.content()
