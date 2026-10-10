import time
from abc import ABC, abstractmethod

import requests


class BaseAPIAdapter(ABC):
    @abstractmethod
    def get_country_bbox(self, country: str) -> list[str] | None:
        """Получает boundingbox страны. Возвращает список из 4 чисел или None."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> dict | None:
        """Получает данные о самолетах над страной. Возвращает список словарей."""
        pass


class APIAdapter(BaseAPIAdapter):
    def __init__(
        self,
        nominatim_url: str = "https://nominatim.openstreetmap.org/search",
        opensky_url: str = "https://opensky-network.org/api/states/all?",
    ) -> None:
        self.nominatim_url = nominatim_url
        self.opensky_url = opensky_url

    def get_country_bbox(self, country: str) -> list[str] | None:
        """
        Получает координаты (bounding box) страны.
        Возвращает список из 4 чисел или None, если страна не найдена.
        """
        if not country or not country.strip():
            return None

        headers = {"User-Agent": "my-test-app/1.0"}
        params = {"q": country, "format": "json", "limit": 1}

        response = requests.get(url=self.nominatim_url, params=params, headers=headers)
        response.raise_for_status()
        time.sleep(1)
        data = response.json()

        if len(data) == 0:
            return None

        return data[0].get("boundingbox")

    def get_aeroplanes_by_bbox(self, bbox: list[str]) -> dict | None:
        """
        Получает данные о самолетах в заданном прямоугольнике координат.
        Возвращает словарь (JSON ответ от OpenSky).
        """
        if not bbox or len(bbox) != 4:
            return None

        lamin, lamax, lomin, lomax = bbox

        params = {
            "lamin": lamin,
            "lamax": lamax,
            "lomin": lomin,
            "lomax": lomax,
        }

        try:
            response = requests.get(url=self.opensky_url, params=params)
            response.raise_for_status()
            time.sleep(1)
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к OpenSky: {e}")
            return None

        if data is None or "states" not in data:
            return None

        return data

    def get_aeroplanes(self, country: str) -> dict | None:
        """
        Получает самолеты по названию страны.
        Использует два метода выше.
        """

        bbox = self.get_country_bbox(country)

        if bbox is None:
            print(f"Страна '{country}' не найдена!")
            return None

        return self.get_aeroplanes_by_bbox(bbox)
