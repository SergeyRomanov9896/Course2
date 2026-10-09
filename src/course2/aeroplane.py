class Aeroplane:
    def __init__(self, callsign: str, country: str, velocity: float | None, altitude: float | None) -> None:
        # ВАЖНО: Мы присваиваем значения через self.xxx, а не self._xxx.
        # Это специально, чтобы сразу сработали наши сеттеры (@xxx.setter)
        # и данные прошли валидацию ПРЯМО В МОМЕНТ создания объекта.
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    # ==========================================
    # 1. ИНКАПСУЛЯЦИЯ И ВАЛИДАЦИЯ (Properties)
    # ==========================================

    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Позывной должен быть непустой строкой")
        self._callsign = value.strip()

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Страна должна быть непустой строкой")
        self._country = value.strip()

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float | None) -> None:
        # Если API вернул None (датчик не сработал), считаем скорость равной 0
        if value is None:
            self._velocity = 0.0
            return

        if not isinstance(value, (int, float)):
            raise TypeError("Скорость должна быть числом")
        if value < 0:
            raise ValueError("Скорость не может быть отрицательной")

        self._velocity = float(value)

    @property
    def altitude(self) -> float:
        return self._altitude

    @altitude.setter
    def altitude(self, value: float | None) -> None:
        # Аналогично скорости: None превращаем в 0.0
        if value is None:
            self._altitude = 0.0
            return

        if not isinstance(value, (int, float)):
            raise TypeError("Высота должна быть числом")
        if value < 0:
            raise ValueError("Высота не может быть отрицательной")

        self._altitude = float(value)

    # ==========================================
    # 2. МАГИЧЕСКИЕ МЕТОДЫ СРАВНЕНИЯ (Dunder methods)
    # ==========================================

    def __lt__(self, other: "Aeroplane") -> bool:
        """
        Меньше чем (<). Используется функцией sorted() по умолчанию.
        Сравниваем по высоте полета (для задачи "Топ N по высоте").
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented  # Говорим Python: "Я не умею сравнивать себя с этим типом"
        return self.altitude < other.altitude

    def __gt__(self, other: "Aeroplane") -> bool:
        """Больше чем (>)."""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude > other.altitude

    def __eq__(self, other: object) -> bool:
        """
        Равенство (==).
        Логично считать два объекта одинаковыми, если у них одинаковый позывной.
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.callsign == other.callsign

    # ==========================================
    # 3. ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ
    # ==========================================

    def is_faster_than(self, other: "Aeroplane") -> bool:
        """
        Явное сравнение по скорости.
        Нужно, потому что магические методы (<, >) у нас настроены на высоту.
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только с объектом Aeroplane")
        return self.velocity > other.velocity

    def __str__(self) -> str:
        """
        Строковое представление для пользователя (вызывается при print(объект)).
        """
        return (
            f"✈️ {self.callsign} ({self.country}) | Высота: {self.altitude:.1f} м | Скорость: {self.velocity:.1f} м/с"
        )

    def __repr__(self) -> str:
        """
        Строковое представление для разработчика (вызывается в консоли или при отладке).
        """
        return f"Aeroplane(callsign='{self.callsign}', country='{self.country}', velocity={self.velocity}, altitude={self.altitude})"
