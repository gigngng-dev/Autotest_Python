
"""Страница проектов YouGile."""

from playwright.sync_api import Page, expect

from tests.ui.pages.base_page import BasePage


class ProjectsPage(BasePage):
    """Page Object страницы проектов."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.add_project_button = page.get_by_test_id(
            "add-project-button"
        )
        self.default_project_menu_item = page.get_by_test_id(
            "menu-item-add-default-project"
        )
        self.project_name_input = page.locator(
            'input[placeholder="Введите название проекта…"]'
        )
        self.confirm_create_button = page.get_by_role(
            "button",
            name="Добавить проект с задачами",
            exact=True,
        )
        self.project_cards = page.get_by_test_id("project-card")

    def create_project(self, title: str) -> None:
        """Создаёт обычный проект с задачами."""
        if self.add_project_button.get_attribute("aria-expanded") != "true":
            self.add_project_button.click()

        self.default_project_menu_item.click()

        expect(self.project_name_input).to_be_visible(timeout=10000)
        self.project_name_input.fill(title)

        expect(self.confirm_create_button).to_be_visible(timeout=10000)
        self.confirm_create_button.click()
    
    
    def expect_project_visible(self, title: str) -> None:
     """Проверяет, что созданный проект отображается в интерфейсе."""
     project_title = self.page.get_by_text(
        title,
        exact=False,
    ).first

     expect(project_title).to_be_visible(timeout=15000)
    
    
    def delete_project(self, title: str) -> None:
        """Удаляет созданный тестом проект и проверяет результат."""

        # Переходим к списку проектов компании.
        self.page.get_by_test_id("my-company-item").click()

        project_card = self.page.get_by_test_id("project-card").filter(
            has_text=title
        )

        # Убеждаемся, что найден ровно один нужный проект.
        expect(project_card).to_have_count(1, timeout=15000)

        # Открываем меню именно этого проекта.
        project_card.get_by_test_id(
            "project-card-menu-button"
        ).click()

        # Выбираем удаление.
        self.page.get_by_test_id("menu-item-remove").click()

        # Проверяем, что появилось подтверждение удаления.
        expect(
            self.page.get_by_text("Удалить проект?", exact=True)
        ).to_be_visible(timeout=10000)

        # Подтверждаем удаление.
        delete_button = self.page.get_by_text(
            "Удалить",
            exact=True,
        ).last

        expect(delete_button).to_be_visible(timeout=10000)
        delete_button.click()

        # Проверяем, что проект исчез из списка.
        expect(project_card).to_have_count(0, timeout=15000)





