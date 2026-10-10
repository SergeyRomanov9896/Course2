import pytest

from src.course2.aeroplane import Aeroplane
from src.course2.storage import JSONStorage


@pytest.fixture
def temp_storage(tmp_path):
    """Фикстура: создает хранилище во временной папке для каждого теста."""
    file_path = tmp_path / "test_data.json"
    return JSONStorage(filepath=file_path)


def test_add_and_get_aeroplane(temp_storage):
    """Тест добавления и получения самолета."""
    plane = Aeroplane("TEST1", "Testland", 100.0, 5000.0)
    temp_storage.add_aeroplane(plane)

    result = temp_storage.get_aeroplanes()
    assert len(result) == 1
    assert result[0].callsign == "TEST1"


def test_save_and_load(temp_storage, tmp_path):
    """Тест сохранения в файл и загрузки из него."""
    plane = Aeroplane("SAVE1", "Saveland", 200.0, 8000.0)
    temp_storage.add_aeroplane(plane)
    temp_storage.save()  # Сохраняем в tmp_path

    # Создаем НОВОЕ хранилище, указывая тот же файл, чтобы проверить загрузку
    new_storage = JSONStorage(filepath=tmp_path / "test_data.json")
    result = new_storage.get_aeroplanes()

    assert len(result) == 1
    assert result[0].callsign == "SAVE1"


def test_filter_by_country(temp_storage):
    """Тест фильтрации по стране."""
    p1 = Aeroplane("P1", "Canada", 100.0, 5000.0)
    p2 = Aeroplane("P2", "France", 200.0, 6000.0)
    temp_storage.add_aeroplane(p1)
    temp_storage.add_aeroplane(p2)

    result = temp_storage.get_aeroplanes(filters={"country": "Canada"})
    assert len(result) == 1
    assert result[0].callsign == "P1"


def test_delete_aeroplane(temp_storage):
    """Тест удаления самолета по критериям."""
    p1 = Aeroplane("DEL1", "Country", 100.0, 5000.0)
    p2 = Aeroplane("KEEP1", "Country", 200.0, 6000.0)
    temp_storage.add_aeroplane(p1)
    temp_storage.add_aeroplane(p2)

    temp_storage.delete_aeroplane(criteria={"callsign": "DEL1"})

    result = temp_storage.get_aeroplanes()
    assert len(result) == 1
    assert result[0].callsign == "KEEP1"
