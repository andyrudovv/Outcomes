import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from datetime import datetime, timedelta  # Add timedelta here
from config_reader import config
import sqlite3
import os

# ... rest of your code ...

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


class ExpenseStates(StatesGroup):
    waiting_for_amount = State()

def create_table():
    connection = sqlite3.connect("botdata.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        expense_type TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL
                    )""")
    connection.commit()
    connection.close()

def connect_to_db():
    if not os.path.exists("botdata.db"):
        create_table()
    connection = sqlite3.connect("botdata.db")
    cursor = connection.cursor()
    return connection, cursor

@dp.message(Command("start"))
async def cmd_start(message: types.Message, connection, cursor):

    res = cursor.execute("SELECT * FROM expenses")

    await message.answer(str(res.fetchall()))

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
Это бот для учета расходов. Вы можете использовать следующие команды:

/start - начать использование бота
/help - получить справку
/add_expense - добавить новый расход
/clear_whole_expenses - удалить все расходы
/last_month_expenses - показать расходы за последний месяц
    """
    await message.answer(help_text)

@dp.message(Command("add_expense"))
async def cmd_add_expense(message: types.Message, connection, cursor):
    # Define expense categories
    expense_categories = [
        [KeyboardButton(text="Продукты"), KeyboardButton(text="Транспорт")],
        [KeyboardButton(text="Развлечения"), KeyboardButton(text="Здоровье")],
        [KeyboardButton(text="Одежда"), KeyboardButton(text="Коммунальные услуги")],
        [KeyboardButton(text="Образование"), KeyboardButton(text="Прочее")]
    ]
    
    # Create a keyboard with the expense categories
    keyboard = ReplyKeyboardMarkup(
        keyboard=expense_categories,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(text="Выберите категорию расхода:", reply_markup=keyboard)


@dp.message(lambda message: message.text in \
            ["Продукты", "Транспорт", "Развлечения", "Здоровье", \
             "Одежда", "Коммунальные услуги", "Образование", "Прочее"]
            )
async def handle_expense_category(message: types.Message, state: FSMContext):
    # Save the selected category
    await state.update_data(category=message.text)

    # Ask for the amount
    await message.answer("Введите сумму расхода:")

    # Set the state to waiting for amount
    await state.set_state(ExpenseStates.waiting_for_amount)
    


@dp.message(ExpenseStates.waiting_for_amount)
async def handle_expense_amount(message: types.Message, state: FSMContext, connection, cursor):
    try:
        amount = float(message.text)

        # Get the saved category
        data = await state.get_data()
        category = data.get('category')

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the expense to the database
        cursor.execute("INSERT INTO expenses (expense_type, amount, date) VALUES (?, ?, ?)", 
                       (category, amount, current_datetime))
        connection.commit()

        await message.answer(f"Расход добавлен: {category} - {amount} руб. (Дата: {current_datetime})")

        # Clear the state
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму (число).")
    


@dp.message(Command("clear_whole_expenses"))
async def cmd_clear_expenses(message: types.Message, connection, cursor):
    cursor.execute("DELETE FROM expenses")
    connection.commit()
    await message.answer("Все расходы удалены.")


# show expenses for last month
@dp.message(Command("last_month_expenses"))
async def cmd_last_month_expenses(message: types.Message, connection, cursor):
    last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    res = cursor.execute("SELECT * FROM expenses WHERE date >=?", (last_month,))
    await message.answer(str(res.fetchall()))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    dp["connection"], dp["cursor"] = connect_to_db()
    asyncio.run(main())