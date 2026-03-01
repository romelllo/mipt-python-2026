"""
Семинар 5: Структура Django-проекта.

Этот модуль демонстрирует:
- Как создаётся Django-проект и приложение
- Структуру файлов Django-проекта
- Назначение каждого файла
- Основные команды manage.py

Примечание: этот файл выводит информацию о структуре проекта.
Для реальной работы с Django используйте команды django-admin
и manage.py (см. комментарии).
"""

import os
import shutil
import subprocess
import sys
import tempfile

# ============================================================
# 1. Создание Django-проекта
# ============================================================


def demonstrate_project_creation() -> None:
    """Демонстрация создания Django-проекта."""
    print("=" * 60)
    print("1. Создание Django-проекта")
    print("=" * 60)

    print("""
  Команды для создания проекта:

    # Создать проект
    django-admin startproject mysite

    # Перейти в папку проекта
    cd mysite

    # Создать приложение
    python manage.py startapp blog
    """)


# ============================================================
# 2. Структура файлов проекта
# ============================================================


def demonstrate_project_structure() -> None:
    """Демонстрация структуры файлов Django-проекта."""
    print("\n" + "=" * 60)
    print("2. Структура файлов проекта")
    print("=" * 60)

    print("""
  mysite/                        # Корень проекта
  ├── manage.py                  # Утилита управления проектом
  ├── mysite/                    # Пакет настроек проекта
  │   ├── __init__.py            # Отмечает директорию как Python-пакет
  │   ├── settings.py            # Настройки проекта (БД, приложения, и т.д.)
  │   ├── urls.py                # Корневая маршрутизация (URL → View)
  │   ├── asgi.py                # Точка входа для ASGI-серверов (async)
  │   └── wsgi.py                # Точка входа для WSGI-серверов (sync)
  └── blog/                      # Приложение "блог"
      ├── __init__.py
      ├── admin.py               # Настройка админ-панели
      ├── apps.py                # Конфигурация приложения
      ├── migrations/            # Миграции БД (автогенерируемые)
      │   └── __init__.py
      ├── models.py              # Модели данных (таблицы БД)
      ├── tests.py               # Тесты
      ├── views.py               # Представления (обработчики запросов)
      └── templates/             # HTML-шаблоны (создаётся вручную)
          └── blog/
              ├── post_list.html
              └── post_detail.html
    """)


# ============================================================
# 3. Назначение ключевых файлов
# ============================================================


def demonstrate_key_files() -> None:
    """Демонстрация назначения ключевых файлов Django."""
    print("\n" + "=" * 60)
    print("3. Назначение ключевых файлов")
    print("=" * 60)

    files = {
        "manage.py": (
            "Утилита командной строки для управления проектом. "
            "Через неё запускается сервер, создаются миграции, "
            "создаётся суперпользователь и т.д."
        ),
        "settings.py": (
            "Все настройки проекта: список приложений, база данных, "
            "язык, часовой пояс, пути к шаблонам и статическим файлам."
        ),
        "urls.py": (
            "Файл маршрутизации — связывает URL-пути с функциями-обработчиками. "
            "Корневой urls.py обычно подключает маршруты из приложений."
        ),
        "models.py": (
            "Описание моделей данных. Каждый класс-модель соответствует "
            "таблице в базе данных. Django ORM создаёт таблицы автоматически."
        ),
        "views.py": (
            "Представления — функции или классы, которые принимают HTTP-запрос "
            "и возвращают HTTP-ответ (HTML, JSON, редирект и т.д.)."
        ),
        "admin.py": (
            "Регистрация моделей в админ-панели Django. "
            "После регистрации модель можно просматривать и редактировать "
            "через веб-интерфейс по адресу /admin/."
        ),
        "migrations/": (
            "Файлы миграций — инструкции по изменению структуры БД. "
            "Генерируются автоматически командой makemigrations."
        ),
    }

    for filename, description in files.items():
        print(f"\n  {filename}:")
        print(f"    {description}")


# ============================================================
# 4. Основные команды manage.py
# ============================================================


def demonstrate_manage_commands() -> None:
    """Демонстрация основных команд manage.py."""
    print("\n" + "=" * 60)
    print("4. Основные команды manage.py")
    print("=" * 60)

    commands = [
        ("python manage.py runserver", "Запуск сервера разработки (порт 8000)"),
        ("python manage.py runserver 8080", "Запуск на другом порту"),
        ("python manage.py startapp имя", "Создание нового приложения"),
        ("python manage.py makemigrations", "Создание миграций из моделей"),
        ("python manage.py migrate", "Применение миграций к БД"),
        ("python manage.py createsuperuser", "Создание администратора"),
        ("python manage.py shell", "Интерактивная консоль Django"),
        ("python manage.py test", "Запуск тестов"),
    ]

    for command, description in commands:
        print(f"\n  {command}")
        print(f"    → {description}")


# ============================================================
# 5. Демонстрация: создание реального проекта (если возможно)
# ============================================================


def demonstrate_real_project() -> None:
    """Создаёт временный Django-проект для демонстрации структуры."""
    print("\n" + "=" * 60)
    print("5. Демонстрация: создание временного проекта")
    print("=" * 60)

    try:
        import django  # noqa: F401
    except ImportError:
        print("\n  Django не установлен. Установите: uv add django")
        return

    # Создаём временную директорию
    tmp_dir = tempfile.mkdtemp(prefix="django_demo_")
    print(f"\n  Создаём проект в: {tmp_dir}")

    try:
        # Создаём проект
        subprocess.run(
            [sys.executable, "-m", "django", "startproject", "demo_project"],
            cwd=tmp_dir,
            check=True,
            capture_output=True,
        )

        project_dir = os.path.join(tmp_dir, "demo_project")

        # Создаём приложение
        subprocess.run(
            [sys.executable, "manage.py", "startapp", "blog"],
            cwd=project_dir,
            check=True,
            capture_output=True,
        )

        # Выводим структуру
        print("\n  Структура созданного проекта:")
        for root, dirs, files in os.walk(project_dir):
            # Пропускаем __pycache__
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            level = root.replace(project_dir, "").count(os.sep)
            indent = "  " * (level + 2)
            folder_name = os.path.basename(root)
            print(f"{indent}{folder_name}/")
            for file in sorted(files):
                print(f"{indent}  {file}")

        print("\n  Проект успешно создан и удалён.")
    except subprocess.CalledProcessError as e:
        print(f"\n  Ошибка при создании проекта: {e}")
    finally:
        # Удаляем временную директорию
        shutil.rmtree(tmp_dir, ignore_errors=True)


# ============================================================
# Главная функция
# ============================================================


def main() -> None:
    """Запуск всех демонстраций."""
    print("\n" + "=" * 60)
    print("СЕМИНАР 5: СТРУКТУРА DJANGO-ПРОЕКТА")
    print("=" * 60)

    demonstrate_project_creation()
    demonstrate_project_structure()
    demonstrate_key_files()
    demonstrate_manage_commands()
    demonstrate_real_project()

    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
