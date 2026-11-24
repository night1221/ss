import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
import datetime
import requests

response = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
data = response.json()
for item in data:
    if item['cc'] == 'USD':
        usd = item['rate']
for item in data:
    if item['cc'] == 'EUR':
        eur = item['rate']

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт! Команди: /rate - курс валют, /convert - конвертація, /replay - повторення повідомлення")

@dp.message(Command("rate"))
async def rate(message: Message):
    await message.answer(f"USD: {usd}  in: {datetime.datetime.now()}")
    await message.answer(f"EUR: {eur}  in: {datetime.datetime.now()}")


class Convertor(StatesGroup):
    waiting_amount = State()

async def abc(message:Message, text:str):
    try:
        waiting_amount = float(text.replace(",", "."))
    except ValueError:
        await message.answer("Будь ласка, введіть число.")
        return False
    await message.answer(f"Сума в доларах: {waiting_amount / usd:.2f}")
    await message.answer(f"Сума в євро: {waiting_amount / eur:.2f}")
    return True

@dp.message(Command("convert"))
async def do_convert(message: Message, command: CommandObject, state: FSMContext):
        if command.args:
                await abc(message, command.args)
        else:
            await state.set_state(Convertor.waiting_amount)
            await message.answer("Введіть суму в гривнях: ")

@dp.message(Convertor.waiting_amount)
async def process_amount(message: Message, state: FSMContext):
    if await abc(message, message.text):
        await state.clear()


@dp.message(F.text)
async def replay(message: Message):
    await message.answer(f"Ти написав: {message.text}") 

async def main():
    await dp.start_polling(bot)

asyncio.run(main())