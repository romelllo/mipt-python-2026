"""
Семинар 4: IP-адреса и порты.

Этот модуль демонстрирует:
- Разбор URL на компоненты (хост, порт, путь)
- Получение IP-адреса по имени хоста
- Работу с адресами localhost
- Проверку доступности портов
"""

import socket
from urllib.parse import urlparse

# ============================================================
# 1. Разбор URL на компоненты
# ============================================================


def demonstrate_url_parsing() -> None:
    """Демонстрация разбора URL на компоненты."""
    print("=" * 60)
    print("1. Разбор URL на компоненты")
    print("=" * 60)

    urls = [
        "https://api.example.com:8443/users/123?active=true",
        "http://localhost:8000/api/v1/items",
        "https://google.com/search?q=python",
        "postgresql://user:pass@localhost:5432/mydb",
    ]

    for url in urls:
        parsed = urlparse(url)
        print(f"\nURL: {url}")
        print(f"  Схема (scheme):   {parsed.scheme}")
        print(f"  Хост (hostname):  {parsed.hostname}")
        print(f"  Порт (port):      {parsed.port or 'не указан (по умолчанию)'}")
        print(f"  Путь (path):      {parsed.path or '/'}")
        print(f"  Параметры (query): {parsed.query or 'нет'}")


# ============================================================
# 2. Получение IP-адреса по имени хоста
# ============================================================


def demonstrate_dns_resolution() -> None:
    """Демонстрация разрешения DNS-имён в IP-адреса."""
    print("\n" + "=" * 60)
    print("2. Получение IP-адреса по имени хоста (DNS)")
    print("=" * 60)

    hostnames = [
        "localhost",
        "google.com",
        "github.com",
        "httpbin.org",
    ]

    for hostname in hostnames:
        try:
            ip_address = socket.gethostbyname(hostname)
            print(f"\n  {hostname} -> {ip_address}")
        except socket.gaierror as e:
            print(f"\n  {hostname} -> Ошибка: {e}")

    # Получение всех IP-адресов хоста
    print("\n  Все IP-адреса google.com:")
    try:
        _, _, ip_list = socket.gethostbyname_ex("google.com")
        for ip in ip_list:
            print(f"    - {ip}")
    except socket.gaierror as e:
        print(f"    Ошибка: {e}")


# ============================================================
# 3. Специальные IP-адреса
# ============================================================


def demonstrate_special_addresses() -> None:
    """Демонстрация специальных IP-адресов."""
    print("\n" + "=" * 60)
    print("3. Специальные IP-адреса")
    print("=" * 60)

    special_ips = [
        ("127.0.0.1", "Loopback (localhost) — обращение к себе"),
        ("0.0.0.0", "Все интерфейсы — сервер слушает на всех адресах"),
        ("192.168.0.0/16", "Частная сеть (домашние роутеры)"),
        ("10.0.0.0/8", "Частная сеть (корпоративные сети)"),
        ("172.16.0.0/12", "Частная сеть"),
        ("255.255.255.255", "Broadcast — всем устройствам в сети"),
    ]

    for ip, description in special_ips:
        print(f"\n  {ip:20} — {description}")

    # Проверка localhost
    print("\n  Проверка localhost:")
    print(
        f"    socket.gethostbyname('localhost') = {socket.gethostbyname('localhost')}"
    )
    print(f"    socket.gethostname() = {socket.gethostname()}")


# ============================================================
# 4. Порты по умолчанию
# ============================================================


def demonstrate_default_ports() -> None:
    """Демонстрация стандартных портов для протоколов."""
    print("\n" + "=" * 60)
    print("4. Стандартные порты")
    print("=" * 60)

    # Таблица портов
    ports = [
        (20, 21, "FTP", "Передача файлов"),
        (22, None, "SSH", "Безопасный удалённый доступ"),
        (25, None, "SMTP", "Отправка email"),
        (53, None, "DNS", "Разрешение имён"),
        (80, None, "HTTP", "Веб (незащищённый)"),
        (443, None, "HTTPS", "Веб (защищённый)"),
        (3306, None, "MySQL", "База данных MySQL"),
        (5432, None, "PostgreSQL", "База данных PostgreSQL"),
        (6379, None, "Redis", "Кэш/очереди"),
        (27017, None, "MongoDB", "NoSQL база данных"),
    ]

    print("\n  Порт    Протокол     Описание")
    print("  " + "-" * 50)
    for port1, port2, protocol, description in ports:
        port_str = f"{port1}" if port2 is None else f"{port1}/{port2}"
        print(f"  {port_str:8} {protocol:12} {description}")

    print("\n  Диапазоны портов:")
    print("    0-1023      — Well-known (требуют root)")
    print("    1024-49151  — Registered (зарегистрированные)")
    print("    49152-65535 — Dynamic/Ephemeral (временные)")


# ============================================================
# 5. Проверка доступности порта
# ============================================================


def check_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Проверяет, открыт ли порт на хосте.

    Args:
        host: Имя хоста или IP-адрес
        port: Номер порта
        timeout: Таймаут в секундах

    Returns:
        True если порт открыт, False иначе
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except OSError:
        return False


def demonstrate_port_check() -> None:
    """Демонстрация проверки доступности портов."""
    print("\n" + "=" * 60)
    print("5. Проверка доступности портов")
    print("=" * 60)

    targets = [
        ("google.com", 80),
        ("google.com", 443),
        ("localhost", 8000),  # Скорее всего закрыт
        ("localhost", 22),  # SSH — зависит от системы
    ]

    print("\n  Проверяем доступность портов...")
    for host, port in targets:
        is_open = check_port(host, port)
        status = "ОТКРЫТ" if is_open else "закрыт"
        print(f"  {host}:{port} — {status}")


# ============================================================
# 6. Создание полного адреса (сокета)
# ============================================================


def demonstrate_socket_address() -> None:
    """Демонстрация создания адреса сокета."""
    print("\n" + "=" * 60)
    print("6. Адрес сокета (IP + Port)")
    print("=" * 60)

    examples = [
        ("192.168.1.100", 8080),
        ("127.0.0.1", 5000),
        ("0.0.0.0", 80),
    ]

    print("\n  IP-адрес + Порт = Адрес сокета")
    print("  " + "-" * 40)
    for ip, port in examples:
        socket_addr = f"{ip}:{port}"
        print(f"  {ip:15} + {port:5} = {socket_addr}")

    print("\n  В URL это выглядит так:")
    print("    http://192.168.1.100:8080/api/users")
    print("    https://127.0.0.1:5000/")
    print("    http://0.0.0.0:80/  (сервер слушает на всех интерфейсах)")


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 4: IP-АДРЕСА И ПОРТЫ")
    print("=" * 60)

    demonstrate_url_parsing()
    demonstrate_dns_resolution()
    demonstrate_special_addresses()
    demonstrate_default_ports()
    demonstrate_port_check()
    demonstrate_socket_address()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
