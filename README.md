# Course2

## 1. Описание проекта

Проект представляет собой консольное приложение для мониторинга воздушного движения над определённой страной. Оно использует данные OpenSky и Nominatim API, преобразует их в объекты самолётов и позволяет работать с полученной информацией через удобный интерфейс.

Основная логика приложения разделена на несколько компонентов:

- `Aeroplane` — модель самолёта с полями `callsign`, `country`, `velocity` и `altitude`.
- `APIAdapter` — адаптер для работы с внешними API:
  - получение `boundingbox` страны через Nominatim;
  - получение списка самолётов по координатам через OpenSky.
- `JSONStorage` — хранилище, которое сохраняет и загружает данные в JSON-файл.
- `user_interaction()` — консольное меню для работы с пользователем.

### Основные возможности

Приложение позволяет:

- получать список самолётов по названию страны;
- сортировать самолёты по высоте и выводить топ-N объектов;
- фильтровать самолёты по стране регистрации;
- фильтровать самолёты по диапазону высот;
- сохранять текущие данные в JSON-файл;
- загружать данные из файла на следующий запуск;
- выводить список всех текущих самолётов в читаемом формате.

Также в проекте предусмотрена валидация данных:

- позывной и страна должны быть непустыми строками;
- скорость и высота должны быть числами и не могут быть отрицательными;
- при отсутствии значения API передаёт `None`, и код автоматически заменяет его на `0.0`.

---

## 2. Технологии и стек

Проект реализован на языке Python 3.12.

### Используемые технологии и библиотеки

- Python 3.12
- `requests` — для выполнения HTTP-запросов к внешним API
- `pytest` — для автоматического тестирования
- `pytest-cov` — для оценки покрытия кода тестами
- `ruff`, `flake8`, `mypy` — для анализа и проверки качества кода
- JSON — для хранения данных в локальном файле

### Структура проекта

```text
Course2/
├── main.py
├── pyproject.toml
├── README.md
├── src/
│   └── course2/
│       ├── __init__.py
│       ├── aeroplane.py
│       ├── api.py
│       ├── storage.py
│       └── user_interface.py
├── tests/
│   ├── test_aeroplane.py
│   ├── test_api.py
│   ├── test_storage.py
│   └── __init__.py
└── data/
```

---

## 3. Инструкция по установке

### 1. Клонировать репозиторий

```bash
git clone <ссылка-на-репозиторий>
cd Course2
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
```

На Windows:

```bash
.venv\Scripts\activate
```

На macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Установить зависимости

Через Poetry:

```bash
poetry install
```

Или через `pip`:

```bash
pip install requests
pip install pytest pytest-cov ruff flake8 mypy
```

> В проекте также есть конфигурация `pyproject.toml`, в которой указаны зависимости и параметры Python.

---

## 4. Как запустить проект

Главная точка входа — файл `main.py`.

### Запуск приложения

```bash
python main.py
```

После запуска откроется интерактивное меню с возможностями:

1. Получить самолёты по стране
2. Топ N самолётов по высоте
3. Фильтр по стране регистрации
4. Фильтр по диапазону высот
5. Сохранить данные в файл
6. Загрузить данные из файла
7. Показать все текущие самолёты
0. Выйти

### Запуск тестов

```bash
pytest -q
```

Для отчёта по покрытию:

```bash
pytest --cov=src --cov-report=term-missing -q
```

---

## 5. Примеры использования

### Пример 1. Создание объекта самолёта

```python
from src.course2.aeroplane import Aeroplane

plane = Aeroplane("BA123", "United Kingdom", 250.5, 10000.0)
print(plane)
```

Результат:

```text
✈️ BA123 (United Kingdom) | Высота: 10000.0 м | Скорость: 250.5 м/с
```

### Пример 2. Получение данных по стране через API

```python
from src.course2.api import APIAdapter

api = APIAdapter()
response = api.get_aeroplanes("Canada")

if response is not None:
    print(response.get("states", []))
```

### Пример 3. Сохранение и загрузка данных

```python
from src.course2.storage import JSONStorage
from src.course2.aeroplane import Aeroplane

storage = JSONStorage("data/aeroplanes.json")
plane = Aeroplane("TEST1", "France", 180.0, 7000.0)

storage.add_aeroplane(plane)
storage.save()

loaded = storage.get_aeroplanes()
print(len(loaded))
```

### Пример 4. Сравнение самолётов по высоте

```python
from src.course2.aeroplane import Aeroplane

plane1 = Aeroplane("P1", "Country", 200.0, 5000.0)
plane2 = Aeroplane("P2", "Country", 300.0, 10000.0)

print(plane1 < plane2)  # True
print(plane2 > plane1)  # True
print(plane2.is_faster_than(plane1))  # True
```

### Пример 5. Фильтрация по диапазону высот

```python
planes = [
    Aeroplane("A1", "Canada", 200.0, 5000.0),
    Aeroplane("A2", "Canada", 250.0, 8000.0),
]

filtered = [p for p in planes if 4000 <= p.altitude <= 9000]
print(filtered)
```

---

## Краткое резюме

Проект является учебной реализацией системы, которая позволяет получать, хранить и анализировать данные о самолётах с использованием внешних API и локального JSON-хранилища. Основная цель — показать работу с API, обработку данных, валидацию моделей и построение простого пользовательского интерфейса в консоли.
