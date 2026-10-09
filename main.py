from src.course2.aeroplane import Aeroplane

# 1. Успешное создание
plane1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
plane2 = Aeroplane("AFR456", "France", 300.5, 11500.0)
plane3 = Aeroplane("BAW123", "UK", None, None) # Проверка обработки None

print("--- Тест 1: Вывод объектов ---")
print(plane1)  # Вызовет __str__
print(plane3)  # Высота и скорость будут 0.0

print("\n--- Тест 2: Сравнение по высоте (магические методы) ---")
print(f"plane2 выше plane1? {plane2 > plane1}")  # True (11500 > 10203)
print(f"plane1 ниже plane2? {plane1 < plane2}")  # True

print("\n--- Тест 3: Сравнение по скорости (явный метод) ---")
print(f"plane2 быстрее plane1? {plane2.is_faster_than(plane1)}") # True

print("\n--- Тест 4: Валидация (должна вызвать ошибку) ---")
try:
    bad_plane = Aeroplane("BAD", "Nowhere", -50, 1000)
except ValueError as e:
    print(f"✅ Успешно поймали ошибку: {e}")
