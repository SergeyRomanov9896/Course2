from src.course2.api import APIAdapter

if __name__ == "__main__":
    # Создание экземпляра класса для работы с API сайтов с самолетами
    api = APIAdapter()

    # Получение информации о самолетах с opensky-network.org
    result = api.get_aeroplanes("Canada")
    if result:
        print(f"Найдено самолетов: {len(result.get('states', []))}")
