import pytest

from src.course2.aeroplane import Aeroplane


def test_aeroplane_creation_valid():
    """Тест успешного создания самолета с корректными данными."""
    plane = Aeroplane("BA123", "United Kingdom", 250.5, 10000.0)
    assert plane.callsign == "BA123"
    assert plane.country == "United Kingdom"
    assert plane.velocity == 250.5
    assert plane.altitude == 10000.0


def test_aeroplane_creation_with_none():
    """Тест создания самолета, когда API вернул None для чисел."""
    plane = Aeroplane("AF456", "France", None, None)
    assert plane.velocity == 0.0  # Должно замениться на 0.0
    assert plane.altitude == 0.0


def test_aeroplane_validation_negative_altitude():
    """Тест валидации: отрицательная высота должна вызывать ошибку."""
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Aeroplane("DL789", "USA", 200.0, -500.0)


def test_aeroplane_validation_invalid_type():
    """Тест валидации: передача строки вместо числа."""
    with pytest.raises(TypeError, match="Скорость должна быть числом"):
        Aeroplane("LH111", "Germany", "быстро", 5000.0)


def test_aeroplane_comparison():
    """Тест магических методов сравнения."""
    plane1 = Aeroplane("P1", "Country", 200.0, 5000.0)
    plane2 = Aeroplane("P2", "Country", 300.0, 10000.0)
    plane3 = Aeroplane("P1", "Country", 200.0, 5000.0)  # Копия plane1

    assert plane1 < plane2  # 5000 < 10000 (True)
    assert plane2 > plane1  # 10000 > 5000 (True)
    assert plane1 == plane3  # Одинаковый callsign (True)
    assert plane1 != plane2  # Разный callsign (True)


def test_aeroplane_is_faster_than():
    """Тест явного метода сравнения по скорости."""
    plane1 = Aeroplane("P1", "Country", 200.0, 5000.0)
    plane2 = Aeroplane("P2", "Country", 300.0, 10000.0)

    assert plane2.is_faster_than(plane1) is True
    assert plane1.is_faster_than(plane2) is False
