"""Web API: концепция, запросы к open-meteo.com, обработка JSON.

Используем open-meteo.com — полностью бесплатный API погоды,
не требует регистрации и API-ключа.

Документация: https://open-meteo.com/en/docs

Запуск:
    python seminars/seminar_15_beautifulsoup_apis/examples/03_web_apis.py
"""

import time
from datetime import date, timedelta

import requests
from requests.exceptions import RequestException

# ============================================================
# Раздел 1: Что такое Web API
# ============================================================

# Web API (Application Programming Interface) — это интерфейс,
# который позволяет программам общаться друг с другом через HTTP.
#
# Клиент (наш скрипт)  →  HTTP-запрос  →  Сервер API
# Клиент               ←  JSON-ответ   ←  Сервер API
#
# Отличие от веб-скрапинга:
#   Скрапинг: парсим HTML, предназначенный для людей
#   API:      получаем структурированные данные (JSON/XML), предназначенные для программ


# ============================================================
# Раздел 2: Базовый запрос к API погоды
# ============================================================

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Коды погодных условий WMO (Weather Interpretation Codes)
WMO_CODES: dict[int, str] = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Лёгкая морось",
    61: "Небольшой дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    71: "Небольшой снег",
    73: "Умеренный снег",
    75: "Сильный снег",
    80: "Ливень",
    95: "Гроза",
}


def get_current_weather(latitude: float, longitude: float) -> dict | None:
    """Получает текущую погоду для заданных координат.

    Args:
        latitude: широта
        longitude: долгота

    Returns:
        Словарь с данными о погоде или None при ошибке
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        # Текущие данные: температура, влажность, скорость ветра, код погоды
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "Europe/Moscow",
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Ошибка запроса к API: {e}")
        return None


def print_current_weather(city_name: str, lat: float, lon: float) -> None:
    """Выводит текущую погоду для города.

    Args:
        city_name: название города (для отображения)
        lat: широта
        lon: долгота
    """
    data = get_current_weather(lat, lon)
    if data is None:
        print(f"  {city_name}: данные недоступны")
        return

    # Структура ответа:
    # {
    #   "latitude": 55.75,
    #   "longitude": 37.62,
    #   "current": {
    #     "time": "2026-05-11T12:00",
    #     "temperature_2m": 18.5,
    #     "relative_humidity_2m": 65,
    #     "wind_speed_10m": 12.3,
    #     "weather_code": 2
    #   },
    #   "current_units": {"temperature_2m": "°C", ...}
    # }
    current = data.get("current", {})
    units = data.get("current_units", {})

    temp = current.get("temperature_2m", "?")
    humidity = current.get("relative_humidity_2m", "?")
    wind = current.get("wind_speed_10m", "?")
    code = current.get("weather_code", -1)
    condition = WMO_CODES.get(code, f"Код {code}")

    temp_unit = units.get("temperature_2m", "°C")
    wind_unit = units.get("wind_speed_10m", "км/ч")

    print(
        f"  {city_name}: {condition}, {temp}{temp_unit}, "
        f"влажность {humidity}%, ветер {wind} {wind_unit}"
    )


# ============================================================
# Раздел 3: Прогноз на несколько дней
# ============================================================


def get_weekly_forecast(
    latitude: float, longitude: float
) -> list[dict[str, str | float | int]]:
    """Получает прогноз погоды на 7 дней.

    Args:
        latitude: широта
        longitude: долгота

    Returns:
        Список словарей с дневными данными
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
        "timezone": "Europe/Moscow",
        "forecast_days": 7,
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except RequestException as e:
        print(f"Ошибка: {e}")
        return []

    daily = data.get("daily", {})
    dates = daily.get("time", [])
    max_temps = daily.get("temperature_2m_max", [])
    min_temps = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    codes = daily.get("weather_code", [])

    # Собираем список словарей — по одному на каждый день
    forecast = []
    for i, day_date in enumerate(dates):
        forecast.append(
            {
                "date": day_date,
                "max_temp": max_temps[i] if i < len(max_temps) else None,
                "min_temp": min_temps[i] if i < len(min_temps) else None,
                "precipitation": precip[i] if i < len(precip) else None,
                "condition": WMO_CODES.get(
                    codes[i] if i < len(codes) else -1, "Неизвестно"
                ),
            }
        )

    return forecast


# ============================================================
# Раздел 4: Rate limiting — ограничение частоты запросов
# ============================================================


def demo_rate_limiting() -> None:
    """Демонстрация вежливого обхода rate limiting."""
    print("\n" + "=" * 60)
    print("4. Rate Limiting — ограничение частоты запросов")
    print("=" * 60)

    # Координаты нескольких городов
    cities = [
        ("Москва", 55.7558, 37.6173),
        ("Санкт-Петербург", 59.9343, 30.3351),
        ("Новосибирск", 54.9885, 82.9207),
    ]

    print("Запрашиваем погоду для нескольких городов...")
    print("(пауза 0.5 сек между запросами — хороший тон)\n")

    for city_name, lat, lon in cities:
        print_current_weather(city_name, lat, lon)
        time.sleep(0.5)  # пауза между запросами


# ============================================================
# Раздел 5: Обработка ошибок API
# ============================================================


def safe_api_request(url: str, params: dict) -> dict | None:
    """Универсальная функция для запроса к API с обработкой ошибок.

    Args:
        url: URL эндпоинта
        params: параметры запроса

    Returns:
        Распарсенный JSON или None
    """
    try:
        response = requests.get(url, params=params, timeout=10)

        # Проверяем HTTP-статус
        response.raise_for_status()

        # Проверяем, что ответ — JSON
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type:
            print(f"Неожиданный Content-Type: {content_type}")
            return None

        return response.json()

    except requests.exceptions.Timeout:
        print("Превышен таймаут запроса")
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения — проверьте интернет")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "?"
        print(f"HTTP ошибка {status}: {e}")
    except ValueError:
        print("Ошибка парсинга JSON")

    return None


def main() -> None:
    """Демонстрация работы с Web API."""
    print("=" * 60)
    print("Web API: погода через open-meteo.com")
    print("=" * 60)

    # 1. Текущая погода
    print("\n--- Текущая погода ---")
    print_current_weather("Москва", 55.7558, 37.6173)

    # 2. Прогноз на неделю
    print("\n--- Прогноз на 7 дней (Москва) ---")
    forecast = get_weekly_forecast(55.7558, 37.6173)
    for day in forecast:
        print(
            f"  {day['date']}: {day['condition']}, "
            f"{day['min_temp']}…{day['max_temp']}°C, "
            f"осадки {day['precipitation']} мм"
        )

    # 3. Rate limiting
    demo_rate_limiting()

    # 4. Демонстрация обработки ошибок
    print("\n--- Обработка ошибок ---")
    print("Запрос с неверными параметрами:")
    result = safe_api_request(
        WEATHER_API_URL,
        {"latitude": 999, "longitude": 999},  # невалидные координаты
    )
    if result is None:
        print("  Запрос завершился с ошибкой (ожидаемо)")

    # Проверяем диапазон дат для исторических данных
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    week_ago = (date.today() - timedelta(days=7)).isoformat()
    print(f"\nИсторические данные ({week_ago} — {yesterday}):")
    historical = safe_api_request(
        "https://archive-api.open-meteo.com/v1/archive",
        {
            "latitude": 55.7558,
            "longitude": 37.6173,
            "start_date": week_ago,
            "end_date": yesterday,
            "daily": "temperature_2m_max,temperature_2m_min",
            "timezone": "Europe/Moscow",
        },
    )
    if historical:
        daily = historical.get("daily", {})
        dates = daily.get("time", [])
        max_t = daily.get("temperature_2m_max", [])
        print(f"  Получено дней: {len(dates)}")
        if dates and max_t:
            print(f"  Последний день: {dates[-1]}, макс. {max_t[-1]}°C")

    print("\n" + "=" * 60)
    print("Готово!")
    print("=" * 60)


if __name__ == "__main__":
    main()
