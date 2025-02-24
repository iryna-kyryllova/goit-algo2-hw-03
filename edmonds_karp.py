import networkx as nx
from collections import deque
import matplotlib.pyplot as plt
import pandas as pd

# Створюємо орієнтований граф
G = nx.DiGraph()

# Додаємо ребра з пропускною здатністю
edges = [
    ("Термінал 1", "Склад 1", 25),
    ("Термінал 1", "Склад 2", 20),
    ("Термінал 1", "Склад 3", 15),
    ("Термінал 2", "Склад 3", 15),
    ("Термінал 2", "Склад 4", 30),
    ("Термінал 2", "Склад 2", 10),
    ("Склад 1", "Магазин 1", 15),
    ("Склад 1", "Магазин 2", 10),
    ("Склад 1", "Магазин 3", 20),
    ("Склад 2", "Магазин 4", 15),
    ("Склад 2", "Магазин 5", 10),
    ("Склад 2", "Магазин 6", 25),
    ("Склад 3", "Магазин 7", 20),
    ("Склад 3", "Магазин 8", 15),
    ("Склад 3", "Магазин 9", 10),
    ("Склад 4", "Магазин 10", 20),
    ("Склад 4", "Магазин 11", 10),
    ("Склад 4", "Магазин 12", 15),
    ("Склад 4", "Магазин 13", 5),
    ("Склад 4", "Магазин 14", 10),
]

# Додаємо всі ребра до графа
G.add_weighted_edges_from(edges)

# Позиції для малювання графа
pos = {
    "Термінал 1": (1, 2),
    "Термінал 2": (5, 2),
    "Склад 1": (2, 3),
    "Склад 2": (4, 3),
    "Склад 3": (2, 1),
    "Склад 4": (4, 1),
    "Магазин 1": (0, 4),
    "Магазин 2": (1, 4),
    "Магазин 3": (2, 4),
    "Магазин 4": (3, 4),
    "Магазин 5": (4, 4),
    "Магазин 6": (5, 4),
    "Магазин 7": (0, 0),
    "Магазин 8": (1, 0),
    "Магазин 9": (2, 0),
    "Магазин 10": (3, 0),
    "Магазин 11": (4, 0),
    "Магазин 12": (5, 0),
    "Магазин 13": (6, 0),
    "Магазин 14": (7, 0),
}

# Малюємо граф
plt.figure(figsize=(12, 8))
nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=2000,
    node_color="skyblue",
    font_size=8,
    font_weight="bold",
    arrows=True,
)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=9)

# Відображаємо граф
plt.title("Логістична мережа")
plt.show()


# Функція для пошуку збільшуючого шляху (BFS)
def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            # Перевірка, чи є залишкова пропускна здатність у каналі
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


# Основна функція для обчислення максимального потоку
def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow

    return max_flow, flow_matrix


# Створюємо матрицю пропускної здатності
num_nodes = 22  # 20 вузлів + SuperSource (20) + SuperSink (21)
capacity_matrix = [[0] * num_nodes for _ in range(num_nodes)]

# Додаємо з'єднання терміналів зі складами
connections = [
    (20, 0, 60),
    (20, 1, 55),  # SuperSource => Термінали
    (0, 2, 25),
    (0, 3, 20),
    (0, 4, 15),
    (1, 4, 15),
    (1, 5, 30),
    (1, 3, 10),
    (2, 6, 15),
    (2, 7, 10),
    (2, 8, 20),
    (3, 9, 15),
    (3, 10, 10),
    (3, 11, 25),
    (4, 12, 20),
    (4, 13, 15),
    (4, 14, 10),
    (5, 15, 20),
    (5, 16, 10),
    (5, 17, 15),
    (5, 18, 5),
    (5, 19, 10),  # Склади => магазини
    (6, 21, 100),
    (7, 21, 100),
    (8, 21, 100),
    (9, 21, 100),
    (10, 21, 100),
    (11, 21, 100),
    (12, 21, 100),
    (13, 21, 100),
    (14, 21, 100),
    (15, 21, 100),
    (16, 21, 100),
    (17, 21, 100),
    (18, 21, 100),
    (19, 21, 100),  # Магазини => SuperSink
]

# Заповнюємо матрицю пропускної здатності
for u, v, capacity in connections:
    capacity_matrix[u][v] = capacity

# Визначаємо джерело та стік
source = 20  # SuperSource
sink = 21  # SuperSink

# Запускаємо алгоритм
max_flow, flow_matrix = edmonds_karp(capacity_matrix, source, sink)

print(f"Максимальний потік: {max_flow}")

# Формуємо таблицю фактичних потоків між терміналами та магазинами
flow_data = []

for terminal in [0, 1]:  # Термінал 1 (0) і Термінал 2 (1)
    for store in range(6, 20):  # Магазини (індекси 6-19)
        actual_flow = sum(
            flow_matrix[warehouse][store]
            for warehouse in range(2, 6)
            if flow_matrix[warehouse][store] > 0
        )
        flow_data.append(
            [f"Термінал {terminal + 1}", f"Магазин {store - 5}", actual_flow]
        )

df_flows = pd.DataFrame(
    flow_data, columns=["Термінал", "Магазин", "Фактичний Потік (одиниць)"]
)

print(f"Фактичний Потік:\n{df_flows}")
