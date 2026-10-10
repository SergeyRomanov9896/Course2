from unittest.mock import MagicMock, patch

from src.course2.api import APIAdapter

# Создаем фиктивный ответ, который вернет наша заглушка
MOCK_NOMINATIM_RESPONSE = [{"boundingbox": ["41.6", "83.1", "-141.0", "-52.6"]}]
MOCK_OPENSKY_RESPONSE = {
    "states": [
        # Индексы: 1=callsign, 2=country, 9=velocity, 13=altitude
        ["ign", "CAN123", "Canada", "ign", "ign", "ign", "ign", "ign", "ign", 250.0, "ign", "ign", "ign", 10000.0]
    ]
}


@patch("src.course2.api.requests.get")
def test_get_country_bbox_success(mock_get):
    """Тест успешного получения boundingbox."""
    # Настраиваем поведение заглушки
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_NOMINATIM_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = APIAdapter()
    result = adapter.get_country_bbox("Canada")

    assert result == ["41.6", "83.1", "-141.0", "-52.6"]
    mock_get.assert_called_once()  # Проверяем, что запрос был сделан ровно 1 раз


@patch("src.course2.api.requests.get")
def test_get_country_bbox_not_found(mock_get):
    """Тест ситуации, когда страна не найдена (пустой ответ)."""
    mock_response = MagicMock()
    mock_response.json.return_value = []  # Пустой список
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = APIAdapter()
    result = adapter.get_country_bbox("НесуществующаяСтрана")

    assert result is None


@patch("src.course2.api.requests.get")
def test_get_aeroplanes_by_bbox_success(mock_get):
    """Тест получения самолетов по координатам."""
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_OPENSKY_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    adapter = APIAdapter()
    bbox = ["41.6", "83.1", "-141.0", "-52.6"]
    result = adapter.get_aeroplanes_by_bbox(bbox)

    assert result is not None
    assert "states" in result
    assert len(result["states"]) == 1
