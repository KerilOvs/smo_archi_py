# -*- coding: windows-1251 -*-
import matplotlib.pyplot as plt


def parse_file(file_path):
    """
    Функция для чтения и парсинга данных из файла.
    Возвращает списки clients и t_stay.
    """
    clients = []
    t_stay = []

    try:
        with open(file_path, 'r', encoding='windows-1251') as file:
            lines = file.readlines()
            table_started = False

            for line in lines:
                # Ищем начало таблицы
                if "=== Table 1: Source characteristics ===" in line:
                    table_started = True
                    continue
                # Если нашли конец таблицы, прекращаем парсинг
                if table_started and "===" in line:
                    break
                # Парсим строки таблицы
                if table_started and line.strip():
                    parts = line.split()
                    # Проверяем, что строка начинается с номера клиента
                    if parts[0].isdigit():
                        clients.append(int(parts[0]))
                        t_stay.append(float(parts[3]))  # T_stay находится на 4-й позиции
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")

    return clients, t_stay


def plot_graph(clients, t_stay):
    """
    Функция для построения графика.
    """
    plt.figure(figsize=(10, 6))  # Размер графика
    plt.plot(clients, t_stay, marker='o', linestyle='-', color='b', label='T_stay')  # Линия с маркерами
    plt.title('Зависимость T_stay от № Client')  # Заголовок
    plt.xlabel('№ Client')  # Ось X
    plt.ylabel('T_stay')  # Ось Y
    plt.grid(True)  # Сетка
    plt.legend()  # Легенда
    plt.show()  # Показать график


# Укажите путь к файлу
file_path = 'statistics.txt'  # Замените на актуальный путь к файлу

# Чтение и парсинг данных
clients, t_stay = parse_file(file_path)

# Построение графика
if clients and t_stay:  # Проверяем, что данные были успешно прочитаны
    plot_graph(clients, t_stay)
else:
    print("Данные для построения графика отсутствуют.")