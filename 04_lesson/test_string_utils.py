import pytest
from string_utils import StringUtils


string_utils = StringUtils()


# Написание

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("skypro", "Skypro"),               # базовый случай из документации
    ("hello world", "Hello world"),     # строка с пробелом
    ("python", "Python"),               # обычное слово
    ("Тест", "Тест"),                   # кириллица
    ("123", "123"),                     # цифры как строка
    ("04 апреля 2023", "04 апреля 2023"),  # строка с пробелами и цифрами
])
def test_capitalize_positive(input_str, expected):
    """Позитивные тесты: корректно делает первую букву заглавной."""
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),                           # пустая строка
    (" ", " "),                         # строка из одного пробела
    ("   ", "   "),                     # строка из нескольких пробелов
    ("123abc", "123abc"),               # начинается с цифры
])
def test_capitalize_negative(input_str, expected):
    """Негативные тесты: корректно обрабатывает строки."""
    assert string_utils.capitalize(input_str) == expected


@pytest.mark.negative
def test_capitalize_none():
    """Негативный тест: при None выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.capitalize(None)


@pytest.mark.negative
def test_capitalize_empty_list():
    """Негативный тест: при пустом списке [] выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.capitalize([])


@pytest.mark.negative
def test_capitalize_defect_lowercase_rest():
    """
    ДЕФЕКТ: capitalize() делает ВСЕ остальные буквы строчными,
    а не только первую — заглавной.
    Пример: "hello WORLD" -> "Hello world" (W стала w).
    """
    result = string_utils.capitalize("hello WORLD")
    # Ожидалось бы "Hello WORLD", но фактически:
    assert result == "Hello world"


# Обрезка символов (trim)

@pytest.mark.positive
@pytest.mark.parametrize("input_str, expected", [
    ("   skypro", "skypro"),            # пробелы в начале — удаляем
    ("skypro", "skypro"),               # без пробелов — без изменений
    ("   skypro   ", "skypro   "),      # пробелы только в начале удаляются
    ("Тест", "Тест"),                   # кириллица
    ("123", "123"),                     # цифры
    ("04 апреля 2023", "04 апреля 2023"),  # строка с пробелами внутри
])
def test_trim_positive(input_str, expected):
    """Позитивные тесты: trim удаляет пробелы только в начале строки."""
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
@pytest.mark.parametrize("input_str, expected", [
    ("", ""),                           # пустая строка
    (" ", ""),                          # один пробел -> пустая
    ("     ", ""),                      # несколько пробелов -> пустая
])
def test_trim_negative(input_str, expected):
    """Негативные тесты: trim корректно обрабатывает пустые/пробельные строки."""
    assert string_utils.trim(input_str) == expected


@pytest.mark.negative
def test_trim_none():
    """Негативный тест: trim при None выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.trim(None)


@pytest.mark.negative
def test_trim_empty_list():
    """Негативный тест: trim при пустом списке [] выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.trim([])


# Содержит ли строка символ/подстроку (contains)

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "S", True),              # символ в начале
    ("SkyPro", "k", True),              # символ в середине
    ("SkyPro", "o", True),              # символ в конце
    ("SkyPro", "Pro", True),            # подстрока
    ("04 апреля 2023", " ", True),      # пробел как символ
    ("Тест", "Т", True),                # кириллица
    ("123", "2", True),                 # цифры
    ("SkyPro", "U", False),             # символ отсутствует
    ("SkyPro", "X", False),             # символ отсутствует
])
def test_contains_positive(string, symbol, expected):
    """Позитивные тесты: contains корректно определяет наличие символа/подстроки."""
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("", "a", False),                   # пустая строка
])
def test_contains_negative(string, symbol, expected):
    """Негативные тесты: contains корректно обрабатывает пустые строки."""
    assert string_utils.contains(string, symbol) == expected


@pytest.mark.negative
def test_contains_none_string():
    """Негативный тест: contains при None в string выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.contains(None, "a")


@pytest.mark.negative
def test_contains_none_symbol():
    """Негативный тест: contains при None в symbol выбрасывает TypeError."""
    with pytest.raises(TypeError):
        string_utils.contains("abc", None)


@pytest.mark.negative
def test_contains_empty_list_string():
    """Негативный тест: contains при [] в string возвращает False (не падает)."""
    result = string_utils.contains([], "a")
    assert result is False


@pytest.mark.negative
def test_contains_empty_list_symbol():
    """Негативный тест: contains при [] в symbol выбрасывает TypeError."""
    with pytest.raises(TypeError):
        string_utils.contains("abc", [])


@pytest.mark.negative
def test_contains_empty_symbol():
    """
    ДЕФЕКТ: contains("abc", "") возвращает True.
    Ожидаемый результат: False (пустой символ не может содержаться в строке).
    Фактический результат: True.
    """
    result = string_utils.contains("abc", "")
    assert result is True  # текущее поведение; правильно было бы False


# Удаление символа/подстроки (delete_symbol)

@pytest.mark.positive
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "k", "SyPro"),           # удаление одного символа
    ("SkyPro", "Pro", "Sky"),           # удаление подстроки
    ("04 апреля 2023", " ", "04апреля2023"),  # удаление пробелов
    ("123123", "1", "2323"),            # удаление цифры
    ("Тест", "с", "Тет"),               # кириллица
    ("aaa", "a", ""),                   # удаление всех символов
])
def test_delete_symbol_positive(string, symbol, expected):
    """Позитивные тесты: delete_symbol корректно удаляет символ/подстроку."""
    assert string_utils.delete_symbol(string, symbol) == expected


@pytest.mark.negative
@pytest.mark.parametrize("string, symbol, expected", [
    ("SkyPro", "Z", "SkyPro"),          # символа нет — строка не меняется
    ("", "a", ""),                      # пустая строка
])
def test_delete_symbol_negative(string, symbol, expected):
    """Негативные тесты: delete_symbol корректно обрабатывает."""
    assert string_utils.delete_symbol(string, symbol) == expected


@pytest.mark.negative
def test_delete_symbol_none_string():
    """Негативный тест: delete_symbol при None в строке выбрасывает AttributeError."""
    with pytest.raises(AttributeError):
        string_utils.delete_symbol(None, "a")


@pytest.mark.negative
def test_delete_symbol_none_symbol():
    """Негативный тест: delete_symbol при None в symbol выбрасывает TypeError."""
    with pytest.raises(TypeError):
        string_utils.delete_symbol("abc", None)


@pytest.mark.negative
def test_delete_symbol_empty_list_string():
    """Негативный тест: delete_symbol при [] в string возвращает [] (не падает)."""
    result = string_utils.delete_symbol([], "a")
    assert result == []


@pytest.mark.negative
def test_delete_symbol_empty_list_symbol():
    """Негативный тест: delete_symbol при [] в symbol выбрасывает TypeError."""
    with pytest.raises(TypeError):
        string_utils.delete_symbol("abc", [])