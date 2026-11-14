
"""Страница авторизации YouGile."""

from playwright.sync_api import Page, expect

from config.settings import settings
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object страницы входа."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.email_input = page.locator("input[type='email']")
        self.password_input = page.locator("input[type='password']")
        self.submit_button = page.get_by_role(
            "button",
            name="Войти",
            exact=True,
        )
        self.error_message = page.locator(
            ".alert-danger, .error, [class*='error'], [class*='invalid']"
        )
        self.root = page.locator("#root")

    def open_login(self) -> None:
        """Открывает страницу входа и инициализирует приложение."""
        self.open(f"{settings.ui_base_url}/team/")

        # Сначала проверяем обычную загрузку формы.
        try:
            expect(self.email_input).to_be_visible(timeout=3000)
            expect(self.password_input).to_be_visible(timeout=3000)
            return
        except AssertionError:
            pass

        # Если форма не появилась, пробуем вызвать инициализацию приложения.
        on_load_type = self.page.evaluate(
            "() => typeof window.onLoad"
        )

        if on_load_type == "function":
            self.page.evaluate("() => window.onLoad()")

        # Проверяем, что форма действительно появилась.
        expect(self.email_input).to_be_visible(timeout=20000)
        expect(self.password_input).to_be_visible(timeout=20000)

    def login(self, email: str, password: str) -> None:
        """Заполняет форму и отправляет её."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def expect_error_visible(self) -> None:
        """Проверяет отображение ошибки авторизации."""
        expect(self.error_message.first).to_be_visible()

    def expect_login_form_visible(self) -> None:
        """Проверяет отображение формы авторизации."""
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()
