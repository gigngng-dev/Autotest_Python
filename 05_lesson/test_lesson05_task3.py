from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By


def test_multiple_elements():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/links/10")


    # Находим все ссылки на странице
    links = driver.find_elements(By.TAG_NAME, "a")

    # Проверяем, что ссылок ровно 9
    assert len(links) == 9

    # Проверяем, что каждая ссылка отображается на странице
    for link in links:
        assert link.is_displayed()

    # Проверяем, что текст первой ссылки содержит "1"
    assert "1" in links[0].text

    driver.quit()
