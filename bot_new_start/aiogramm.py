import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

#        меню в низу
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Курс")],
        [KeyboardButton(text="🔄 Конвертер")],
        [KeyboardButton(text="ℹ️ Допомога")],
    ],
    resize_keyboard=True,
)

# ---------- Стани ----------
class Convertor(StatesGroup):
    waiting_amount = State()

def get_rates():
    data = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()
    usd = eur = None
    for item in data:
        if item["cc"] == "USD":
            usd = item["rate"]
        if item["cc"] == "EUR":
            eur = item["rate"]
    return usd, eur, data[0]["exchangedate"]


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()              #після команди скидаємо стан
    await message.answer("Привіт! Обери дію 👇", reply_markup=menu)

@dp.message(F.text == "💵 Курс")
async def get_exchange_rate(message: Message):
    usd, eur, date = get_rates()
    await message.answer(f"💵 Курс валют на {date}:\n\n"
                         f"USD: {usd:.2f}\n"
                         f"EUR: {eur:.2f}")

@dp.message(F.text == "🔄 Конвертер")
async def start_converter(message: Message, state: FSMContext): 
    await state.set_state(Convertor.waiting_amount)
    await message.answer("Введіть суму в гривнях:")

@dp.message(Convertor.waiting_amount)
async def convert_currency(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(',', '.'))
        usd, eur, _ = get_rates()
    except ValueError:
        await message.answer("Будь ласка, введіть коректну числову суму.")
    else:
        converted_usd = amount / usd
        converted_eur = amount / eur
        await message.answer(f"Сума в доларах: {converted_usd:.2f}\n"
                             f"Сума в євро: {converted_eur:.2f}")
        await state.clear()

@dp.message(F.text == "ℹ️ Допомога")
async def help_command(message: Message):
    await message.answer("крутий бот!")

@dp.message(F.text)
async def handle_message(message: Message):
    await message.answer("Ви надіслали повідомлення: " + message.text)


async def main():
    await dp.start_polling(bot)
asyncio.run(main())