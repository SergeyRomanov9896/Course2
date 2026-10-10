import json
from abc import ABC, abstractmethod
from pathlib import Path

from src.course2.aeroplane import Aeroplane


class BaseDataStorage(ABC):
    """
    Абстрактный класс для работы с хранилищем данных о самолетах.
    Определяет контракт для всех конкретных реализаций (JSON, CSV, БД).
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(self, filters: dict | None = None) -> list[Aeroplane]:
        """
        Получает список самолетов из хранилища.
        filters - словарь с критериями фильтрации, например:
        {'country': 'Canada', 'min_altitude': 10000}
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, criteria: dict) -> None:
        """
        Удаляет самолет по критериям.
        criteria - словарь с критериями, например: {'callsign': 'UAL1621'}
        """
        pass

    @abstractmethod
    def save(self) -> None:
        """Сохраняет данные из памяти на диск (или в БД)."""
        pass

    @abstractmethod
    def load(self) -> None:
        """Загружает данные с диска (или из БД) в память."""
        pass


class JSONStorage(BaseDataStorage):
    """
    Конкретная реализация хранилища в формате JSON.
    Хранит данные в списке в памяти и синхронизирует с JSON-файлом.
    """

    def __init__(self, filepath: str = "aeroplanes.json") -> None:
        self.filepath = Path(filepath)
        self._aeroplanes: list[Aeroplane] = []  # Внутреннее хранилище в памяти
        self.load()  # При создании сразу загружаем данные из файла, если он есть

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавляет самолет в список в памяти."""
        # Проверка на дубликаты по позывному
        if aeroplane in self._aeroplanes:  # Использует __eq__ из Aeroplane
            print(f"Самолет {aeroplane.callsign} уже есть в хранилище")
            return
        self._aeroplanes.append(aeroplane)
        print(f"Добавлен самолет: {aeroplane.callsign}")

    # ==========================================
    # 2. ПОЛУЧЕНИЕ С ФИЛЬТРАЦИЕЙ
    # ==========================================

    def get_aeroplanes(self, filters: dict | None = None) -> list[Aeroplane]:
        """
        Возвращает список самолетов, применяя фильтры.
        Пример filters: {'country': 'Canada', 'min_altitude': 10000}
        """
        if filters is None:
            return self._aeroplanes.copy()  # Возвращаем копию, чтобы не мутировать оригинал

        result = self._aeroplanes.copy()

        # Фильтр по стране
        if "country" in filters:
            country = filters["country"].lower()
            result = [p for p in result if p.country.lower() == country]

        # Фильтр по минимальной высоте
        if "min_altitude" in filters:
            min_alt = filters["min_altitude"]
            result = [p for p in result if p.altitude >= min_alt]

        # Фильтр по максимальной высоте
        if "max_altitude" in filters:
            max_alt = filters["max_altitude"]
            result = [p for p in result if p.altitude <= max_alt]

        # Фильтр по позывному
        if "callsign" in filters:
            callsign = filters["callsign"].upper()
            result = [p for p in result if p.callsign.upper() == callsign]

        return result

    def delete_aeroplane(self, criteria: dict) -> None:
        """
        Удаляет самолет по критериям.
        Пример criteria: {'callsign': 'UAL1621'}
        """
        if not criteria:
            print("Критерии удаления не указаны")
            return

        initial_count = len(self._aeroplanes)

        self._aeroplanes = [p for p in self._aeroplanes if not self._matches_criteria(p, criteria)]

        deleted_count = initial_count - len(self._aeroplanes)
        if deleted_count > 0:
            print(f"Удалено самолетов: {deleted_count}")
        else:
            print("Самолеты по указанным критериям не найдены")

    def _matches_criteria(self, aeroplane: Aeroplane, criteria: dict) -> bool:
        """
        Вспомогательный метод: проверяет, соответствует ли самолет критериям.
        Все критерии должны выполняться одновременно (логическое И).
        """
        for key, value in criteria.items():
            if hasattr(aeroplane, key):
                attr_value = getattr(aeroplane, key)
                if isinstance(attr_value, str) and isinstance(value, str):
                    # Нечувствительное сравнение строк
                    if attr_value.lower() != value.lower():
                        return False
                else:
                    if attr_value != value:
                        return False
            else:
                return False  # Если атрибута нет, критерий не выполнен
        return True

    def save(self) -> None:
        """Сохраняет список самолетов в JSON-файл."""
        # Преобразуем объекты Aeroplane в словари для JSON
        data = [
            {
                "callsign": p.callsign,
                "country": p.country,
                "velocity": p.velocity,
                "altitude": p.altitude,
            }
            for p in self._aeroplanes
        ]

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Данные сохранены в {self.filepath}")

    def load(self) -> None:
        """Загружает данные из JSON-файла в память."""
        if not self.filepath.exists():
            print(f"Файл {self.filepath} не найден, начинаем с пустым хранилищем")
            return

        with open(self.filepath, encoding="utf-8") as f:
            data = json.load(f)

        self._aeroplanes = []
        for item in data:
            try:
                plane = Aeroplane(
                    callsign=item.get("callsign", ""),
                    country=item.get("country", ""),
                    velocity=item.get("velocity"),
                    altitude=item.get("altitude"),
                )
                self._aeroplanes.append(plane)
            except (ValueError, TypeError) as e:
                print(f"Ошибка при загрузке самолета {item}: {e}")

        print(f"Загружено {len(self._aeroplanes)} самолетов из {self.filepath}")
