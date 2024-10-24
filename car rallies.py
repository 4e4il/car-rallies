from tkinter import *
from random import randint, choice

tk = Tk()  # Створення головного вікна програми
canvas = Canvas(tk, width=650, height=800)  # Зміна висоти вікна на 800 пікселів
canvas.pack()  # Відображення полотна на екрані

# Завантажуємо зображення автомобілів для попутного та зустрічного напрямку
car_down_images = [
    PhotoImage(file="car_down1.png"),
    PhotoImage(file="car_down2.png"),
    PhotoImage(file="car_down3.png")
]

car_up_images = [
    PhotoImage(file="car_up1.png"),
    PhotoImage(file="car_up2.png"),
]

# Завантажуємо зображення автомобіля гравця
player_car_image = PhotoImage(file="player_car.png")

# Центруємо дорогу, встановлюємо її ширину на 480 пікселів (по 240 пікселів на смугу)
road1 = canvas.create_rectangle(80, 0, 560, 800, fill="gray")  # Довжина дороги збільшена до 800
road2 = canvas.create_rectangle(80, -800, 560, 0, fill="gray")  # Збільшено для плавної анімації

# Створюємо штрихову лінію по центру дороги
center_line1 = canvas.create_line(320, 0, 320, 800, fill="white", dash=(15, 23))  # Збільшено до 800 пікселів
center_line2 = canvas.create_line(320, -800, 320, 0, fill="white", dash=(15, 23))


# Клас для управління автомобілем користувача
class PlayerCar:
    def __init__(self, canvas, x, y, image):
        self.canvas = canvas
        self.image = image
        self.body = canvas.create_image(x, y, anchor=NW, image=self.image)
        self.x_speed = 0
        self.y_speed = 3
        self.max_speed = 10
        self.min_speed = 1

    def move(self):
        # Переміщуємо по горизонталі
        self.canvas.move(self.body, self.x_speed, 0)
        pos = self.canvas.coords(self.body)

        # Обмежуємо рух по вужчій дорозі (нові межі дороги)
        if pos[0] < 80:  # Ліва межа
            self.canvas.move(self.body, 80 - pos[0], 0)
        elif pos[0] + self.image.width() > 560:  # Права межа
            self.canvas.move(self.body, 560 - (pos[0] + self.image.width()), 0)

    def accelerate(self):
        if self.y_speed < self.max_speed:
            self.y_speed += 1

    def brake(self):
        if self.y_speed > self.min_speed:
            self.y_speed -= 1


# Клас для інших автомобілів
class OtherCar:
    def __init__(self, canvas, x, y, image, direction, other_cars):
        self.canvas = canvas
        self.image = image
        self.body = canvas.create_image(x, y, anchor=NW, image=self.image)
        self.direction = direction
        self.speed = randint(2, 5)
        self.other_cars = other_cars  # Список інших автомобілів для перевірки колізій

    def check_collision(self, pos):
        for other in self.other_cars:
            if other != self:
                other_pos = self.canvas.coords(other.body)
                # Перевіряємо, чи автомобілі знаходяться на близьких координатах по осі Y
                if abs(pos[1] - other_pos[1]) < 50 and abs(pos[0] - other_pos[0]) < 50:
                    return True
        return False

    def move(self):
        pos = self.canvas.coords(self.body)

        # Якщо є колізія з іншим автомобілем, тимчасово знижуємо швидкість
        if not self.check_collision(pos):
            if self.direction == "down":
                self.canvas.move(self.body, 0, self.speed)
            else:
                self.canvas.move(self.body, 0, -self.speed)

        pos = self.canvas.coords(self.body)
        if self.direction == "down" and pos[1] > 800:  # Змінено межу на 800
            self.canvas.move(self.body, 0, -900)
        elif self.direction == "up" and pos[1] < -80:
            self.canvas.move(self.body, 0, 900)  # Змінено для плавної анімації


# Функція для перевірки колізій по осі X
def check_x_collision(x, other_cars, min_distance):
    for other in other_cars:
        other_pos = canvas.coords(other.body)
        if abs(x - other_pos[0]) < min_distance:
            return True
    return False


# Створюємо автомобіль користувача
player_car = PlayerCar(canvas, 500, 170, player_car_image)  # Корекція позиції по Y

# Створюємо інші автомобілі
other_cars = []
min_distance_x = 60  # Мінімальна відстань між автомобілями по осі X

# Автомобілі на зустрічній смузі (зменшуємо кількість машин і збільшуємо відстань між ними)
for _ in range(2):  # Було 3, тепер 2 для меншої щільності
    image = choice(car_down_images)  # Випадкове зображення для попутної смуги
    x_position = randint(100, 240)
    while check_x_collision(x_position, other_cars, min_distance_x):  # Перевіряємо колізії по X
        x_position = randint(100, 240)  # Якщо є, вибираємо нову позицію
    new_car = OtherCar(canvas, x_position, randint(-800, -100), image, "down", other_cars)  # Збільшено відстань
    other_cars.append(new_car)

# Автомобілі на попутній смузі (зменшуємо кількість машин і збільшуємо відстань між ними)
for _ in range(2):  # Було 3, тепер 2 для меншої щільності
    image = choice(car_up_images)  # Випадкове зображення для зустрічної смуги
    x_position = randint(360, 480)
    while check_x_collision(x_position, other_cars, min_distance_x):  # Перевіряємо колізії по X
        x_position = randint(360, 480)  # Якщо є, вибираємо нову позицію
    new_car = OtherCar(canvas, x_position, randint(900, 1500), image, "up", other_cars)  # Збільшено відстань
    other_cars.append(new_car)


# Функція для перевірки колізій між автомобілем гравця та іншими автомобілями
def check_collision():
    player_pos = canvas.coords(player_car.body)
    for car in other_cars:
        car_pos = canvas.coords(car.body)
        if abs(player_pos[0] - car_pos[0]) < 50 and abs(player_pos[1] - car_pos[1]) < 50:
            return True
    return False


# Функція для анімації дороги та автомобілів
def animate():
    if check_collision():  # Перевіряємо зіткнення
        canvas.create_text(325, 400, text="Аварія! Виклик поліції!", font=("Arial", 30), fill="red")
        return  # Зупиняємо гру при зіткненні

    # Рух дороги вниз
    canvas.move(road1, 0, player_car.y_speed)
    canvas.move(road2, 0, player_car.y_speed)
    canvas.move(center_line1, 0, player_car.y_speed)
    canvas.move(center_line2, 0, player_car.y_speed)

    # Якщо одна частина дороги виходить за межі екрану, переміщаємо її назад
    road1_pos = canvas.coords(road1)
    road2_pos = canvas.coords(road2)
    if road1_pos[1] >= 800:  # Новий поріг для довшої дороги
        canvas.move(road1, 0, -1600)  # Змінено для довжини 800 пікселів
        canvas.move(center_line1, 0, -1600)
    if road2_pos[1] >= 800:  # Новий поріг для довшої дороги
        canvas.move(road2, 0, -1600)  # Змінено для довжини 800 пікселів
        canvas.move(center_line2, 0, -1600)

        # Рух автомобілів
    player_car.move()
    for car in other_cars:
        car.move()

    tk.after(20, animate)  # Повторний виклик функції через 20 мілісекунд

    # Функція для обробки натискань клавіш


def key_pressed(event):
    if event.keysym == "Left":  # Вліво
        player_car.x_speed = -5
    elif event.keysym == "Right":  # Вправо
        player_car.x_speed = 5
    elif event.keysym == "Up":  # Прискорення
        player_car.accelerate()
    elif event.keysym == "Down":  # Гальмування
        player_car.brake()


def key_released(event):
    if event.keysym in ("Left", "Right"):  # Припиняємо рух ліворуч/праворуч
        player_car.x_speed = 0

    # Прив'язка натискання клавіш до функцій


tk.bind("<KeyPress>", key_pressed)
tk.bind("<KeyRelease>", key_released)

animate()  # Запуск анімації
tk.mainloop()
