from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram import executor
import requests

token = ...
API = "90b6405885f6b0bf5035ae84aa42cabd"
bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет напиши название города!")


@dp.message_handler()
async def get_wether(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API}&units=metric")
        data = r.json()
        city = data["name"]
        cur_weather = data["main"]["temp"]
        wind = data["wind"]["speed"]
        await message.reply(f"Погода в городе: {city}\nСейчас на улицах {cur_weather} градусов.\n\
		Скорость ветра равна {wind} м\с")
    except:
        await message.reply("Проверьте название города")

if __name__ == "__main__":
    executor.start_polling(dp)
