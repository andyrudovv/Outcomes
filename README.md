
# Outcomes Bot

-----

## About

The **Outcomes Bot** is a simple yet effective Telegram bot designed to help you easily track and manage your personal expenses. It allows you to quickly log expenditures with predefined categories and provides basic functionalities to view and manage your financial records. Built with `aiogram` and `sqlite3`, it offers a straightforward way to keep tabs on your spending directly within Telegram.

-----

## Features

  * **Expense Tracking:** Easily add new expenses with a specified amount and select from a set of predefined categories.
  * **Category Selection:** Choose from common expense categories like "Продукты" (Groceries), "Транспорт" (Transport), "Развлечения" (Entertainment), "Здоровье" (Health), "Одежда" (Clothes), "Коммунальные услуги" (Utilities), "Образование" (Education), and "Прочее" (Other).
  * **Persistent Storage:** All expense data is stored locally in an SQLite database (`botdata.db`).
  * **Last Month's Expenses:** View all expenses recorded within the last 30 days.
  * **Delete Last Expense:** Remove the most recently added expense from the last 30 days.
  * **Clear All Expenses:** Option to completely clear all recorded expenses from the database.
  * **User-Friendly Interface:** Interacts with users through intuitive commands and keyboard buttons in Telegram.

-----

## Getting Started

To get your Outcomes Bot up and running, you'll need Python and a Telegram Bot Token.

### Prerequisites

  * **Python 3.x** (preferably 3.9+)
  * **pip** (Python package installer)
  * A **Telegram Bot Token** (Obtain one by talking to [@BotFather](https://t.me/BotFather) on Telegram and creating a new bot.)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/andyrudovv/Outcomes.git
    cd Outcomes
    ```

2.  **Install dependencies:**
    The project uses `aiogram` for the bot framework and `pydantic-settings` for configuration.

    ```bash
    pip install -r requirements.txt
    ```


3.  **Configure your bot token:**
    Create a file named `.env` in the root directory of your project (same level as `main.py`) and add your Telegram Bot Token to it:

    ```env
    # .env
    BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN_HERE>
    ```

    *Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` with the actual token you received from BotFather.*

### Database Setup

The bot uses SQLite to store expense data. A database file named `botdata.db` will be automatically created in the project directory when the bot runs for the first time. The `create_table.py` script is mainly for testing database connectivity but `main.py` handles table creation if `botdata.db` doesn't exist.

-----

## Running the Bot

After completing the installation and configuration steps, you can start your bot:

```bash
python main.py
```

The bot will then start polling for updates from Telegram. You should see `INFO` messages in your console.

-----

## Usage

Once the bot is running, open Telegram and find your bot by its username.

Here are the commands you can use to interact with the bot:

  * **`/start`**: Greets you and initializes the bot.
  * **`/help`**: Shows a list of all available commands and their descriptions.
  * **`/add_expense`** (or "добавить расход", "добавить", "/add"): Starts the process of adding a new expense. The bot will prompt you to select a category using keyboard buttons, then ask for the amount.
  * **`/last_month_expenses`**: Displays all expenses recorded within the last 30 days.
  * **`/delete_last`** (or "удалить последний месяцовый расход", "delete", "Удалить"): Deletes the most recent expense entry from the database that falls within the last month.
  * **`/clear_whole_expenses`** (or "удалить всё", "удалить все", "удалить", "/delete\_all"): **CAUTION\!** This command will permanently delete *all* expense records from your database.

-----

## Project Structure

  * `main.py`: The core bot logic, handling commands, messages, and state management using `aiogram`. It also manages database interactions for expenses.
  * `config_reader.py`: Handles loading environment variables (specifically the bot token) using `pydantic-settings` for secure configuration.
  * `create_table.py`: A utility script to demonstrate SQLite database connection, although `main.py` handles table creation on startup.
  * `.env`: (Not committed to Git) Stores your sensitive environment variables like the `BOT_TOKEN`.
  * `botdata.db`: (Generated) The SQLite database file where all your expense data is stored.
