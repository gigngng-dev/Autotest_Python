
"""Страница доски YouGile."""

from playwright.sync_api import Page, expect

from tests.ui.pages.base_page import BasePage


class BoardPage(BasePage):
    """Page Object для работы с колонками доски."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.add_column_button = page.get_by_role(
            "button",
            name="Создать колонку",
            exact=True,
        )

        self.column_title_input = page.get_by_role(
            "textbox",
            name="Введите имя колонки…",
            exact=True,
        )
    
    def create_column(self, title: str) -> None:
        """Создаёт колонку и проверяет её отображение."""

        self.add_column_button.click()

        expect(self.column_title_input).to_be_visible(timeout=10000)
        self.column_title_input.fill(title)
        self.column_title_input.press("Enter")

        # Название колонки может отображаться вместе с числом задач.
        column = self.page.get_by_text(
            title,
            exact=False,
        ).filter(visible=True)

        expect(column.first).to_be_visible(timeout=15000)

    def expect_column_visible(self, title: str) -> None:
        """Проверяет отображение созданной колонки."""

        column = self.page.get_by_text(
            title,
            exact=False,
        ).filter(visible=True)

        expect(column.first).to_be_visible(timeout=15000)

