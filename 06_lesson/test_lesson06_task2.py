from selenium import webdriver



USER1_COOKIES = [
    {"name": "session_id", "value": "NDI2Mzk2NDItNTk5NC00Mjg3LWFmMjMtODBkNTY3YmU2NWQ1"},

]
USER1_PROFILE_URL = "https://gitflic.ru/user/gigngng"

USER2_COOKIES = [
    {"name": "session_id", "value": "ZDk2YzJkYzYtZDZkMC00NTk0LWFhOTAtODE5MjA0ODRmYzI1"},
]
USER2_PROFILE_URL = "https://gitflic.ru/user/newuser123"


def test_session_storage_auth():
    driver = webdriver.Chrome()

    # 1. Откройть страницу
    driver.get("https://gitflic.ru/")

    # 2. Установить cookie пользователя 1
    for cookie in USER1_COOKIES:
        driver.add_cookie(cookie)

    # 3. Обновить страницу (cookie применятся)
    driver.refresh()

    # 4. Перейти на страницу профиля пользователя 1
    driver.get(USER1_PROFILE_URL)

    # 5. Сохранить текущий URL
    user1_url = driver.current_url

    # 6. Разлогиниться — очистить все cookie
    driver.delete_all_cookies()

    # 7. Установить cookie пользователя 2
    for cookie in USER2_COOKIES:
        driver.add_cookie(cookie)

    # 8. Обновить страницу (cookie применятся)
    driver.refresh()

    # 9. Перейти на страницу профиля пользователя 2
    driver.get(USER2_PROFILE_URL)

    # 10. Сохранить текущий URL
    user2_url = driver.current_url

    # 11. Проверить, что URL профилей различаются
    assert user1_url != user2_url, (
        f"URL профилей совпадают: user1={user1_url}, user2={user2_url}"
    )

    driver.quit()