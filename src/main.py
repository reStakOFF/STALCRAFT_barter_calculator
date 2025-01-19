import tkinter as tk
from PIL import Image, ImageTk
import requests
import csv
import os

# Стоимость ресурсов в обменных монетах.
resource_prices = {
    "Болотный камень": 2,
    "Зеленая плесень": 1,
    
    "Корень-вонючка": 3,
    "Срачник": 4,
    "Остатки медной проволоки": 4,
    
    "Росток чернобыльской ромашки": 4,
    "Остатки радиопередатчика": 4,
    "Рассольник": 6,
    "Фрагмент данных Альфа": 21,
    
    "Фрагмент данных «Бета»": 40,
    "Дурман-камень": 8,
    "Северный мох": 5,
    "Остатки аккумуляторов": 7,
    
    "Фрагмент данных «Гамма»": 66,
    "Вещество 07270": 8,
    "Рыжий папоротник": 10,
    "Остатки пси-маячка": 7,
    
    "Квантовая батарея": 42,
    "Лимб": 15,
    "Горьколистник": 12,
    "Фрагмент данных «Лямбда»": 86,
    "Лимбоплазма": 200,
    "Аномальная батарея": 240,
    "Аномальная сыворотка": 0
}

# Функция для загрузки рецепта из файла CSV
def load_recipe_from_csv(file_path):
    recipe = {}
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            ingredient, quantity = row[0], int(row[1])
            recipe[ingredient] = quantity
    return recipe

# Функция для расчета стоимости бартера
def calculate_barter_cost(recipe):
    total_cost = 0
    for resource, quantity in recipe.items():
        if resource not in resource_prices:
            return None  # Если цена ресурса отсутствует
        total_cost += resource_prices[resource] * quantity
    return total_cost

# Функция для обработки кнопки расчета
def calculate_cost(file_name):
    item_name = os.path.splitext(file_name)[0]  # Название предмета из имени файла
    file_path = os.path.join("recipes", file_name)  # Путь к файлу
    recipe = load_recipe_from_csv(file_path)  # Загрузка рецепта
    cost = calculate_barter_cost(recipe)  # Расчет стоимости
    if cost is not None:
        result_label.config(text=f"Стоимость '{item_name}': {cost} обменок.")
    else:
        result_label.config(text=f"Рецепт для '{item_name}' содержит неизвестные ресурсы.")

# Создание графического интерфейса
root = tk.Tk()
root.title("Калькулятор стоимости бартера в обменках")
root.geometry("1200x1200")
root.resizable(False, False)

# Загрузка изображений.
def load_image(path, size=(100, 100)):
    img = Image.open(requests.get(path, stream=True).raw)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

# Папка с файлами рецептов
recipe_folder = "recipes"

# Изображения для предметов.
images = {
    "АКС-74": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2F1rd56.png&w=1920&q=75"),
    "M4A1_CQC": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2F3gr6z.png&w=1920&q=75"),
    "ОЦ-14_«Гроза»": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2F5ld1g.png&w=1920&q=75"),
    "FN_F2000": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2Fp6r26.png&w=1920&q=75"),
    "АШ-12": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2Flyl3j.png&w=1920&q=75"),
    "АМБ-17": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2F7lry3.png&w=1920&q=75"),
    "M16A3": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2Fj5lk7.png&w=1920&q=75"),
    "АК-74М": load_image("https://stalcraft.wiki/_next/image?url=https%3A%2F%2Fstalcraftwiki-prod.b-cdn.net%2F%2Fru%2Fimages%2Fweapon%2Fvjr1n.png&w=1920&q=75"),
    
}

# Создание кнопок для выбора предметов
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Сканируем папку "recipes" и создаем кнопки для каждого файла
for file_name in os.listdir(recipe_folder):
    if file_name.endswith(".csv"):
        item_name = os.path.splitext(file_name)[0]  # Название предмета из имени файла
        img = images.get(item_name, None)  # Пытаемся найти изображение
        button = tk.Button(
            frame_buttons,
            text=item_name,
            image=img if img else None,  # Если изображение отсутствует, используем только текст
            compound="top",
            command=lambda name=file_name: calculate_cost(name)
        )
        button.pack(side="left", padx=10)

# Метка для отображения результата
result_label = tk.Label(root, text="", font=("Arial", 14), wraplength=450, justify="center")
result_label.pack(pady=20)

# Запуск главного цикла приложения
root.mainloop()