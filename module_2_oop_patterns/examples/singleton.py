"""
Паттерн проектирования: Singleton

Singleton гарантирует, что у класса есть только один экземпляр,
и предоставляет глобальную точку доступа к этому экземпляру.
"""


class SingletonMeta(type):
    """
    Метакласс для реализации паттерна Singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    """
    Пример класса Singleton для подключения к базе данных.
    """
    
    def __init__(self):
        self.connection = None
        print("Инициализация соединения с базой данных")
    
    def connect(self, host, port):
        """Установить соединение с базой данных."""
        if self.connection is None:
            self.connection = f"Connected to {host}:{port}"
            print(self.connection)
        else:
            print("Соединение уже установлено")
    
    def get_connection(self):
        """Получить текущее соединение."""
        return self.connection


# Альтернативная реализация с декоратором
def singleton(cls):
    """Декоратор для реализации Singleton паттерна."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Configuration:
    """Пример Singleton для конфигурации приложения."""
    
    def __init__(self):
        self.settings = {}
        print("Инициализация конфигурации")
    
    def set(self, key, value):
        """Установить значение конфигурации."""
        self.settings[key] = value
    
    def get(self, key):
        """Получить значение конфигурации."""
        return self.settings.get(key)


def main():
    print("=" * 60)
    print("Демонстрация паттерна Singleton")
    print("=" * 60)
    
    # Пример 1: DatabaseConnection с метаклассом
    print("\n1. DatabaseConnection (метакласс):")
    db1 = DatabaseConnection()
    db1.connect("localhost", 5432)
    
    db2 = DatabaseConnection()
    db2.connect("remote", 5432)  # Не создаст новое соединение
    
    print(f"db1 is db2: {db1 is db2}")  # True
    print(f"Connection: {db2.get_connection()}")
    
    # Пример 2: Configuration с декоратором
    print("\n2. Configuration (декоратор):")
    config1 = Configuration()
    config1.set("debug", True)
    config1.set("version", "1.0.0")
    
    config2 = Configuration()
    print(f"config1 is config2: {config1 is config2}")  # True
    print(f"Debug mode: {config2.get('debug')}")
    print(f"Version: {config2.get('version')}")


if __name__ == "__main__":
    main()
