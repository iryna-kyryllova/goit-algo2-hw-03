import pandas as pd
from BTrees.OOBTree import OOBTree
import timeit

# Завантажуємо дані
df = pd.read_csv("generated_items_data.csv")

# Створюємо структури даних
items_oobtree = OOBTree()
items_dict = {}


# Функція для додавання товару в OOBTree
def add_item_to_tree(tree: OOBTree, item_row: pd.Series):
    tree.insert(item_row["ID"], item_row.drop("ID").to_dict())


# Функція для додавання товару в dict
def add_item_to_dict(items: dict, item_row: pd.Series):
    items[item_row["ID"]] = item_row.drop("ID").to_dict()


# Наповнюємо структури даних товарами
for _, row in df.iterrows():
    add_item_to_tree(items_oobtree, row)
    add_item_to_dict(items_dict, row)


# Функція діапазонного запиту для OOBTree
def range_query_tree(tree: OOBTree, min_price: float, max_price: float):
    return [item for _, item in tree.items() if min_price <= item["Price"] <= max_price]


# Функція діапазонного запиту для dict
def range_query_dict(items: dict, min_price: float, max_price: float):
    return [item for item in items.values() if min_price <= item["Price"] <= max_price]


# Параметри запиту
min_price = 100
max_price = 200

# Вимірюємо час виконання для OOBTree
time_tree = timeit.timeit(
    lambda: range_query_tree(items_oobtree, min_price, max_price), number=100
)

# Вимірюємо час виконання для Dict
time_dict = timeit.timeit(
    lambda: range_query_dict(items_dict, min_price, max_price), number=100
)

# Виводимо результати
print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
print(f"Total range_query time for Dict: {time_dict:.6f} seconds")
