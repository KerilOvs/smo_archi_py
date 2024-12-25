# -*- coding: windows-1251 -*-
import matplotlib.pyplot as plt


def parse_file(file_path):
    """
    ������� ��� ������ � �������� ������ �� �����.
    ���������� ������ clients � t_stay.
    """
    clients = []
    t_stay = []

    try:
        with open(file_path, 'r', encoding='windows-1251') as file:
            lines = file.readlines()
            table_started = False

            for line in lines:
                # ���� ������ �������
                if "=== Table 1: Source characteristics ===" in line:
                    table_started = True
                    continue
                # ���� ����� ����� �������, ���������� �������
                if table_started and "===" in line:
                    break
                # ������ ������ �������
                if table_started and line.strip():
                    parts = line.split()
                    # ���������, ��� ������ ���������� � ������ �������
                    if parts[0].isdigit():
                        clients.append(int(parts[0]))
                        t_stay.append(float(parts[3]))  # T_stay ��������� �� 4-� �������
    except FileNotFoundError:
        print(f"���� {file_path} �� ������.")
    except Exception as e:
        print(f"��������� ������ ��� ������ �����: {e}")

    return clients, t_stay


def plot_graph(clients, t_stay):
    """
    ������� ��� ���������� �������.
    """
    plt.figure(figsize=(10, 6))  # ������ �������
    plt.plot(clients, t_stay, marker='o', linestyle='-', color='b', label='T_stay')  # ����� � ���������
    plt.title('����������� T_stay �� � Client')  # ���������
    plt.xlabel('� Client')  # ��� X
    plt.ylabel('T_stay')  # ��� Y
    plt.grid(True)  # �����
    plt.legend()  # �������
    plt.show()  # �������� ������


# ������� ���� � �����
file_path = 'statistics.txt'  # �������� �� ���������� ���� � �����

# ������ � ������� ������
clients, t_stay = parse_file(file_path)

# ���������� �������
if clients and t_stay:  # ���������, ��� ������ ���� ������� ���������
    plot_graph(clients, t_stay)
else:
    print("������ ��� ���������� ������� �����������.")