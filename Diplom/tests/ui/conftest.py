
"""Фикстуры UI-тестов: браузер, страница, авторизованная страница."""

from collections.abc import Iterator

import pytest
from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    expect,
    sync_playwright,
)

from tests.api.conftest import LOGIN, PASSWORD
from tests.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    """Браузер на весь прогон."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Iterator[Page]:
    """Новый изолированный контекст для каждого теста."""
    context: BrowserContext = browser.new_context()
    page = context.new_page()

    try:
        yield page
    finally:
        context.close()


@pytest.fixture()
def logged_in_page(page: Page) -> Iterator[Page]:
    """Авторизованная страница с проверкой загрузки рабочего пространства."""
    login_page = LoginPage(page)

    # Открываем страницу входа и авторизуемся.
    login_page.open_login()
    login_page.login(LOGIN, PASSWORD)

    # Даём приложению обработать авторизацию.
    page.wait_for_timeout(2000)

    root = page.locator("#root")

    # Если рабочее пространство не отобразилось,
    # перезагружаем страницу и повторяем инициализацию приложения.
    if not root.inner_text().strip():
        page.reload(wait_until="domcontentloaded")

        if page.locator("script[src*='/js/app.js']").count() == 0:
            page.evaluate(
                """() => {
                    if (typeof window.onLoad === "function") {
                        window.onLoad();
                    } else {
                        throw new Error(
                            "Не найдена функция инициализации приложения"
                        );
                    }
                }"""
            )

    # Проверяем, что рабочее пространство загрузилось.
    expect(root).to_contain_text("Мои задачи", timeout=20000)

    yield page
