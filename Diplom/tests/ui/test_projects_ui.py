
"""UI-тесты проектов, досок и выхода из системы."""

import allure
import pytest
from playwright.sync_api import Page, expect

from data.test_data import unique_title
from tests.ui.pages.projects_page import ProjectsPage
from tests.ui.pages.board_page import BoardPage
from tests.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@allure.feature("UI: Проекты")
class TestProjects:
    @allure.story("Создание проекта")
    @allure.title("UI-04: созданный проект отображается")
    def test_create_project_visible(self, logged_in_page: Page) -> None:
        projects_page = ProjectsPage(logged_in_page)
        title = unique_title("UI Project")
        project_created = False

        try:
            with allure.step("Создать проект с уникальным названием"):
                projects_page.create_project(title)
                project_created = True

            with allure.step("Проверить отображение проекта"):
                projects_page.expect_project_visible(title)

        finally:
            if project_created:
                with allure.step("Удалить созданный тестовый проект"):
                    projects_page.delete_project(title)


@allure.feature("UI: Сессия")
class TestSession:
    @allure.story("Завершение сессии")
    @allure.title("UI: пользователь может выйти из системы")
    
    
    def test_logout(self, logged_in_page: Page) -> None:
     page = logged_in_page

     with allure.step("Открыть меню профиля"):
        page.get_by_test_id("profile-menu-item").click()

     with allure.step("Выбрать выход из аккаунта"):
        logout_item = page.get_by_text(
            "Выход из аккаунта",
            exact=True,
        )
        expect(logout_item).to_be_visible(timeout=10000)
        logout_item.click()

     with allure.step("Проверить отображение формы авторизации"):
        root = page.locator("#root")

        expect(
            root.locator("input[type='email']")
        ).to_be_visible(timeout=15000)

        expect(
            root.locator("input[type='password']")
        ).to_be_visible(timeout=10000)

        expect(
            root.get_by_text("Войти:", exact=True)
        ).to_be_visible(timeout=10000)




@allure.feature("UI: Доски")
class TestBoards:
    @allure.story("Создание колонки")
    @allure.title("UI-05: созданная колонка отображается на доске")
    def test_create_column_visible(self, logged_in_page: Page) -> None:
        projects_page = ProjectsPage(logged_in_page)
        board_page = BoardPage(logged_in_page)

        project_title = unique_title("UI Column Project")
        column_title = unique_title("UI Column")
        project_created = False

        try:
            with allure.step("Создать отдельный тестовый проект"):
                projects_page.create_project(project_title)
                project_created = True
                projects_page.expect_project_visible(project_title)

            with allure.step("Открыть тестовый проект"):
                project = logged_in_page.get_by_test_id(
                    "project-item"
                ).filter(has_text=project_title)

                expect(project).to_be_visible(timeout=10000)
                project.click()

            with allure.step("Проверить доступность создания колонки"):
                expect(
                    board_page.add_column_button
                ).to_be_visible(timeout=15000)

            with allure.step("Создать колонку"):
                board_page.create_column(column_title)

            with allure.step("Проверить отображение колонки"):
                board_page.expect_column_visible(column_title)

        finally:
            if project_created:
                with allure.step("Удалить тестовый проект"):
                    projects_page.delete_project(project_title)

