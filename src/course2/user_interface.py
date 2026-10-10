from pathlib import Path

from src.course2.aeroplane import Aeroplane
from src.course2.api import APIAdapter
from src.course2.storage import JSONStorage


def user_interaction() -> None:
    """
    Главная функция для взаимодействия с пользователем через консоль.
    Реализует меню с возможностями:
    1. Получить самолеты по стране
    2. Топ N самолетов по высоте
    3. Фильтр по стране регистрации
    4. Фильтр по диапазону высот
    5. Сохранить данные в файл
    6. Загрузить данные из файла
    0. Выйти
    """

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    api = APIAdapter()
    storage = JSONStorage(str(data_dir / "aeroplanes.json"))

    current_aeroplanes: list[Aeroplane] = []

    print("=" * 60)
    print("🛩️  Добро пожаловать в систему мониторинга самолетов!")
    print("=" * 60)

    while True:
        print("\n📋 Главное меню:")
        print("1. Получить самолеты по стране (из API)")
        print("2. Топ N самолетов по высоте полета")
        print("3. Фильтр по стране регистрации")
        print("4. Фильтр по диапазону высот")
        print("5. Сохранить текущие данные в файл")
        print("6. Загрузить данные из файла")
        print("7. Показать все текущие самолеты")
        print("0. Выйти")

        choice = input("\nВыберите пункт меню (0-7): ").strip()

        if choice == "1":
            current_aeroplanes = _get_aeroplanes_by_country(api)
        elif choice == "2":
            _get_top_by_altitude(current_aeroplanes)
        elif choice == "3":
            _filter_by_country(current_aeroplanes)
        elif choice == "4":
            _filter_by_altitude_range(current_aeroplanes)
        elif choice == "5":
            _save_to_file(storage, current_aeroplanes)
        elif choice == "6":
            current_aeroplanes = _load_from_file(storage)
        elif choice == "7":
            _show_all_aeroplanes(current_aeroplanes)
        elif choice == "0":
            print("\n👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор. Попробуйте снова.")


def _get_aeroplanes_by_country(api: APIAdapter) -> list[Aeroplane]:
    """
    Получение самолетов по названию страны из API.
    Возвращает список объектов Aeroplane.
    """
    country = input("Введите название страны (например, Canada): ").strip()

    if not country:
        print(" Название страны не может быть пустым")
        return []

    print(f"\n Запрашиваем данные о самолетах над {country}...")

    # Получаем "сырые" данные из API
    raw_data = api.get_aeroplanes(country)

    if raw_data is None:
        print(f"❌ Не удалось получить данные для страны '{country}'")
        return []

    # Преобразуем сырые данные в объекты Aeroplane
    aeroplanes = _cast_to_object_list(raw_data)

    if not aeroplanes:
        print("✈️  Самолеты не найдены")
    else:
        print(f"✅ Найдено {len(aeroplanes)} самолетов")
        _show_all_aeroplanes(aeroplanes)

    return aeroplanes


def _cast_to_object_list(raw_data: dict) -> list[Aeroplane]:
    """
    Преобразует "сырой" словарь от OpenSky API в список объектов Aeroplane.
    Обрабатывает ошибки валидации для каждого самолета.
    """
    aeroplanes = []
    states = raw_data.get("states", [])

    for state in states:
        try:
            callsign = state[1] if len(state) > 1 else ""
            country = state[2] if len(state) > 2 else ""
            velocity = state[9] if len(state) > 9 else None
            altitude = state[13] if len(state) > 13 else None

            plane = Aeroplane(
                callsign=callsign,
                country=country,
                velocity=velocity,
                altitude=altitude,
            )
            aeroplanes.append(plane)
        except (ValueError, TypeError, IndexError):
            continue

    return aeroplanes


def _get_top_by_altitude(aeroplanes: list[Aeroplane]) -> None:
    """
    Получение топ N самолетов по высоте полета.
    Использует метод __lt__ из класса Aeroplane для сортировки.
    """
    if not aeroplanes:
        print("❌ Список самолетов пуст. Сначала загрузите данные (пункт 1 или 6)")
        return

    try:
        n = int(input("Введите количество самолетов для топ-N: ").strip())
        if n <= 0:
            raise ValueError
    except ValueError:
        print("❌ Введите положительное целое число")
        return

    sorted_aeroplanes = sorted(aeroplanes, reverse=True)

    top_n = sorted_aeroplanes[:n]

    print(f"\n Топ-{n} самолетов по высоте:")
    for i, plane in enumerate(top_n, 1):
        print(f"{i}. {plane}")


def _filter_by_country(aeroplanes: list[Aeroplane]) -> None:
    """
    Фильтрация самолетов по стране регистрации.
    """
    if not aeroplanes:
        print("❌ Список самолетов пуст. Сначала загрузите данные (пункт 1 или 6)")
        return

    country = input("Введите страну для фильтрации (например, United States): ").strip()

    if not country:
        print("❌ Название страны не может быть пустым")
        return

    # Фильтруем (нечувствительно к регистру)
    filtered = [p for p in aeroplanes if p.country.lower() == country.lower()]

    if not filtered:
        print(f"️  Самолеты из '{country}' не найдены")
    else:
        print(f"\n✈️  Найдено {len(filtered)} самолетов из {country}:")
        for plane in filtered:
            print(plane)


def _filter_by_altitude_range(aeroplanes: list[Aeroplane]) -> None:
    """
    Фильтрация по диапазону высот (дополнительная возможность).
    """
    if not aeroplanes:
        print("❌ Список самолетов пуст. Сначала загрузите данные (пункт 1 или 6)")
        return

    try:
        min_alt = float(input("Введите минимальную высоту (метров): ").strip())
        max_alt = float(input("Введите максимальную высоту (метров): ").strip())

        if min_alt < 0 or max_alt < 0:
            raise ValueError
        if min_alt > max_alt:
            print("❌ Минимальная высота не может быть больше максимальной")
            return
    except ValueError:
        print("❌ Введите корректные числа")
        return

    # Фильтруем по диапазону
    filtered = [p for p in aeroplanes if min_alt <= p.altitude <= max_alt]

    if not filtered:
        print(f"✈️  Самолеты в диапазоне {min_alt}-{max_alt}м не найдены")
    else:
        print(f"\n✈️  Найдено {len(filtered)} самолетов в диапазоне {min_alt}-{max_alt}м:")
        for plane in filtered:
            print(plane)


def _save_to_file(storage: JSONStorage, aeroplanes: list[Aeroplane]) -> None:
    """
    Сохранение текущих данных в JSON-файл.
    """
    if not aeroplanes:
        print("❌ Нечего сохранять. Список самолетов пуст")
        return

    # Добавляем все самолеты в хранилище
    for plane in aeroplanes:
        storage.add_aeroplane(plane)

    # Сохраняем на диск
    storage.save()
    print(f"✅ Сохранено {len(aeroplanes)} самолетов в файл")


def _load_from_file(storage: JSONStorage) -> list[Aeroplane]:
    """
    Загрузка данных из JSON-файла.
    Возвращает список объектов Aeroplane.
    """
    storage.load()
    aeroplanes = storage.get_aeroplanes()

    if not aeroplanes:
        print("❌ Файл пуст или не найден")
    else:
        print(f"✅ Загружено {len(aeroplanes)} самолетов из файла")
        _show_all_aeroplanes(aeroplanes)

    return aeroplanes


def _show_all_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """
    Показать все текущие самолеты.
    """
    if not aeroplanes:
        print(" Список самолетов пуст")
        return

    print(f"\n📊 Всего самолетов: {len(aeroplanes)}")
    print("-" * 60)
    for plane in aeroplanes:
        print(plane)
    print("-" * 60)
