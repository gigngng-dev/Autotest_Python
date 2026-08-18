from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


def test_form_submission():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/forms/post")

    # Находим поле по атрибуту name и вводим текст
    name_field = driver.find_element(By.NAME, "custname")
    name_field.send_keys("Test User")

    # Находим кнопку по частичному тексту
    submit_button = driver.find_element(
        By.XPATH, "//button[contains(text(), 'Submit')]"
    )
    submit_button.click()

    # Проверяем, что URL изменился (форма отправилась)
    assert driver.current_url != "https://httpbin.qa-territory.online/forms/post"

    driver.quit()
