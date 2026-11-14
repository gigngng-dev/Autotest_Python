"""Базовый класс страниц (Page Object)."""
from playwright.sync_api import Page

from config.settings import settings


class BasePage:
    """Общие действия для всех страниц."""

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.page.set_default_timeout(settings.default_timeout)

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")
