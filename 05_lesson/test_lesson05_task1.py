from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online")


    # Находим ссылку по точному тексту и кликаем
    html_form_link = driver.find_element(By.LINK_TEXT, "HTML Form")
    html_form_link.click()

    # Проверяем, что URL содержит /forms/post
    assert "/forms/post" in driver.current_url

    # Возвращаемся на предыдущую страницу
    driver.back()

    # Проверяем, что вернулись на стартовый URL
    assert driver.current_url == "https://httpbin.qa-territory.online/"

    driver.quit()
