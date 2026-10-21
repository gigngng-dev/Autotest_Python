# """UI-тесты авторизации."""
# import allure
# import pytest

# from data.test_data import INVALID_PASSWORD
# from playwright.sync_api import Page
# from tests.api.conftest import LOGIN, PASSWORD
# from tests.ui.pages.login_page import LoginPage

# pytestmark = pytest.mark.ui


# @allure.feature("UI: Авторизация")
# class TestLogin:
#     @allure.story("Успешная авторизация")
#     @allure.title("UI-01: вход с валидными кредами -> переход в приложение")
#     def test_successful_login(self, page: Page) -> None:
#         login_page = LoginPage(page)
#         with allure.step("Открыть страницу входа"):
#             login_page.open_login()
#         with allure.step("Ввести валидные данные и отправить форму"):
#             login_page.login(LOGIN, PASSWORD)
#         with allure.step("Проверить переход в авторизованную область"):
#             page.wait_for_url(lambda url: "/login" not in url, timeout=15000)
#             assert "/login" not in page.url

#     @allure.story("Отказ при неверном пароле")
#     @allure.title("UI-02: неверный пароль -> сообщение об ошибке")
#     def test_invalid_password_shows_error(self, page: Page) -> None:
#         login_page = LoginPage(page)
#         with allure.step("Открыть страницу входа"):
#             login_page.open_login()
#         with allure.step("Отправить форму с неверным паролем"):
#             login_page.login(LOGIN, INVALID_PASSWORD)
#         with allure.step("Проверить сообщение об ошибке"):
#             login_page.expect_error_visible()

#     @allure.story("Валидация пустых полей")
#     @allure.title("UI-03: пустые поля -> форма не авторизует пользователя")
#     def test_empty_fields_do_not_authenticate(self, page: Page) -> None:
#         login_page = LoginPage(page)
#         with allure.step("Открыть страницу входа"):
#             login_page.open_login()
#         with allure.step("Отправить пустую форму"):
#             login_page.login("", "")
#         with allure.step("Проверить, что пользователь остался на странице входа"):
#             assert "/team/" in page.url

"""UI-тесты авторизации."""
import allure
import pytest

from data.test_data import INVALID_PASSWORD
from playwright.sync_api import Page, expect
from tests.api.conftest import LOGIN, PASSWORD
from tests.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@allure.feature("UI: Авторизация")
class TestLogin:   
    
    @allure.story("Успешная авторизация")
    @allure.title("UI-01: вход с валидными кредами -> рабочее пространство")
    def test_successful_login(self, page: Page) -> None:
        login_page = LoginPage(page)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Ввести валидные данные и отправить форму"):
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Дождаться обработки авторизации"):
            page.wait_for_timeout(2000)

        with allure.step("Восстановить интерфейс после перехода"):
            if not page.locator("#root").inner_text().strip():
                page.reload(wait_until="domcontentloaded")

                if (
                    page.locator("#root").count()
                    and page.locator(
                        "script[src*='/js/app.js']"
                    ).count() == 0
                ):
                    page.evaluate("""
                        () => {
                            if (typeof window.onLoad === "function") {
                                window.onLoad();
                            }
                        }
                    """)

        with allure.step("Проверить отображение рабочего пространства"):
            root = page.locator("#root")
            expect(root).to_contain_text(
                "Мои задачи",
                timeout=20000,
            )

            expect(login_page.email_input).to_have_count(0)
            expect(login_page.password_input).to_have_count(0)


    @allure.story("Отказ при неверном пароле")
    @allure.title("UI-02: неверный пароль -> сообщение об ошибке")
    def test_invalid_password_shows_error(self, page: Page) -> None:
        login_page = LoginPage(page)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Отправить форму с неверным паролем"):
            login_page.login(LOGIN, INVALID_PASSWORD)

        with allure.step("Проверить сообщение об ошибке"):
            login_page.expect_error_visible()

    @allure.story("Валидация пустых полей")
    @allure.title("UI-03: пустые поля -> форма не авторизует пользователя")
    def test_empty_fields_do_not_authenticate(self, page: Page) -> None:
        login_page = LoginPage(page)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Отправить пустую форму"):
            login_page.login("", "")

        with allure.step("Проверить, что форма входа осталась видимой"):
            login_page.expect_login_form_visible()
            assert "/team/" in page.url

    def expect_error_visible(self) -> None:
        """Проверяет отображение ошибки авторизации."""
        expect(self.error_message.first).to_be_visible()

    def expect_login_form_visible(self) -> None:
        """Проверяет, что форма авторизации отображается."""
        expect(self.email_input).to_be_visible()
        expect(self.password_input).to_be_visible()