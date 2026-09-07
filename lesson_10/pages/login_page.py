"""Page Object для страницы авторизации SauceDemo."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Класс страницы логина (https://www.saucedemo.com)."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы логина.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу авторизации")
    def open(self) -> None:
        """Открываем страницу авторизации SauceDemo."""
        self.driver.get("https://www.saucedemo.com/")

    @allure.step("Ввести имя пользователя: {username}")
    def enter_username(self, username: str) -> None:
        """
        Вводим имя пользователя в поле Username.
        """
        self.wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        ).send_keys(username)

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> None:
        """
        Вводим пароль в поле Password.
        """
        self.driver.find_element(By.ID, "password").send_keys(password)

    @allure.step("Нажать кнопку Login")
    def click_login(self) -> None:
        """Нажимаем кнопку входа в систему."""
        self.driver.find_element(By.ID, "login-button").click()
