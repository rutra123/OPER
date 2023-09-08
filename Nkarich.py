from PIL import Image, ImageDraw, ImageFont
from telegram import Bot
import asyncio
from datetime import datetime, timedelta
import requests

# Определение функции для добавления текста к изображению
def add_text_to_image(image, text, coordinates, font_path, font_size, font_color):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    draw.text(coordinates, text, font=font, fill=font_color)

# Определение функции для получения суммы в USD с использованием API CoinGecko
def get_usd_amount_online(dash_amount):
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=dash&vs_currencies=usd')
        response.raise_for_status()
        data = response.json()
        dash_usd_price = data.get('dash', {}).get('usd')
        if dash_usd_price is not None:
            return dash_amount * dash_usd_price
        else:
            raise Exception("Не удалось получить цену DASH в USD из API")
    except requests.exceptions.RequestException as e:
        raise Exception("Ошибка при выполнении сетевого запроса:", e)
    except Exception as e:
        raise Exception("Ошибка при обработке данных API:", e)

# Открытие изображения
img = Image.open('/Users/artur/Desktop/main/QART2.jpg')

# Определение настроек шрифта
font_path = '/Users/artur/Desktop/main/arial.ttf'
font_size = 30
font_color = (19, 18, 23)

# Создание объектов для рисования на изображении
draw = ImageDraw.Draw(img)

# Чтение данных из файла transaction_values.txt
with open("transaction_values.txt", "r") as file:
    lines = file.read().splitlines()

# Получение значения даты и времени из файла и преобразование в объект datetime
date_time_str = lines[2]
month_names = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
]
formatted_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
formatted_datetime = formatted_datetime.replace(month=(formatted_datetime.month + 0) % 12)

# Добавление текста скорректированного конечного времени на изображение
adjusted_end_time = formatted_datetime - timedelta(minutes=2)
formatted_adjusted_end_time = adjusted_end_time.strftime("%-d {} %I:%M").format(
    month_names[adjusted_end_time.month - 1])

# Добавление текста скорректированного конечного времени на изображение
adjusted_end_time_coords = (535, 520)
font_size_adjusted = 28
font_color_adjusted = (19, 18, 23)
add_text_to_image(img, f"{formatted_adjusted_end_time}", adjusted_end_time_coords, font_path, font_size_adjusted,
                   font_color_adjusted)


# Получение значения 'dash' из файла
dash = float(lines[3])  # 3-я строка файла

# Добавление первой части текста на изображение, используя значение 'dash'
text_part1_coords = (80, 60)
text_part1_size = 75
add_text_to_image(img, "{:.7f}".format(dash)[:-5], text_part1_coords, font_path, text_part1_size, font_color)

# Добавление второй части текста на изображение, используя значение 'dash'
text_part2_coords = (230, 70)
text_part2_size = 62
add_text_to_image(img, "{:.7f}".format(dash)[-5:], text_part2_coords, font_path, text_part2_size, font_color)

# Форматирование получателя и добавление текста на изображение
recipient_input = lines[0]  # 1-я строка файла
max_address_length = 32
formatted_recipient = recipient_input[:9] + "..." + recipient_input[-9:]
recipient_coords = (385, 340)
recipient_font_size = 30
add_text_to_image(img, formatted_recipient, recipient_coords, font_path, recipient_font_size, font_color)

# Форматирование отправителя и добавление текста на изображение
sender_input = lines[4]  # 5-я строка файла
formatted_sender = sender_input[:9] + "..." + sender_input[-9:]
sender_coords = (385, 250)
sender_font_size = 30
add_text_to_image(img, formatted_sender, sender_coords, font_path, sender_font_size, font_color)

# Получение комиссии и добавление текста на изображение
fee_input = lines[5]  # 6-я строка файла

# Добавление первой части текста на изображение, используя значение 'fee'
text_part1_coords = (555, 431)
text_part1_size = 29
add_text_to_image(img, "{:.7f}".format(float(fee_input))[:-5], text_part1_coords, font_path, text_part1_size, font_color)

# Добавление второй части текста на изображение, используя значение 'fee'
text_part2_coords = (613, 435)  # Обновленные координаты для второй части текста
text_part2_size = 25
add_text_to_image(img, "{:.8f}".format(float(fee_input))[-6:], text_part2_coords, font_path, text_part2_size, font_color)

# Вычисление и добавление суммы в USD на изображение с использованием функции get_usd_amount_online
usd_amount = get_usd_amount_online(dash)
if usd_amount is not None:
    usd_amount_coords = (75, 140)
    usd_amount_font_size = 30
    usd_amount_font_color = (131, 142, 138)
    add_text_to_image(img, f"{usd_amount:.2f}", usd_amount_coords, font_path, usd_amount_font_size, usd_amount_font_color)

# Сохранение измененного изображения
img.save("car2.png")

# Инициализация бота с вашим токеном
bot_token = "6143029111:AAGsW5KPfBjGBjJ-cnH_pktWBPpbSU-RXX8"
bot = Bot(token=bot_token)


# Определение асинхронной функции для отправки изображения нескольким пользователям
async def send_image_to_users(chat_ids):
    try:
        for chat_id in chat_ids:
            with open("car2.png", "rb") as image_file:
                await bot.send_photo(chat_id=chat_id, photo=image_file)
                print("Изображение отправлено через Telegram в чат с ID:", chat_id)
    except Exception as e:
        print("Ошибка при отправке изображения:", e)

# Запуск цикла событий для отправки изображения
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        # Ваш код для получения chat_ids
        chat_ids = [740279851]  # Замените этот список на ваш реальный список chat_ids
        if chat_ids:
            loop.run_until_complete(send_image_to_users(chat_ids))
        else:
            print("Нет доступных или недействительных chat_ids.")
    finally:
        loop.close()