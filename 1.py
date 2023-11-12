# Код 1
import trio
from datetime import datetime
from telegram import Bot
import textwrap
import warnings
import random

warnings.filterwarnings("ignore", category=RuntimeWarning, module="trio")

# Read chat IDs from the file
with open("/storage/sdcard0/qpython/projects3/oper/chat_ids.txt", "r") as file:
    bot_chat_ids = [int(line.strip()) for line in file if line.strip()]

# Read the rate from usdt.txt file
try:
    with open("/storage/sdcard0/qpython/projects3/oper/usdt.txt", "r") as rate_file:
        rate = float(rate_file.readline().strip())
except FileNotFoundError:
    rate = 25.87  # Set a default rate if the file is not found

bot_token = "6067244950:AAGbAHcyAPWjtsJHMOmvY1Uf6wfaW4KJo5w"

rateamd = 411.0  # Set the value of rateamd here

# Read transaction_no from the file
try:
    with open("/storage/sdcard0/qpython/projects3/oper/transaction_no.txt", "r") as file:
        transaction_no = int(file.read().strip())
except FileNotFoundError:
        transaction_no = 263842  # Set the initial value of transaction_no here
async def get_transaction_data():
    with open("/storage/sdcard0/qpython/projects3/oper/transaction_values.txt", "r") as values_file:
        lines = values_file.readlines()
        if len(lines) >= 4:
            dash_address = lines[0].strip()
            transaction_id = lines[1].strip()
            date_time_str = lines[2].strip()
            amount = float(lines[3].strip())
            return dash_address, transaction_id, date_time_str, amount
    return None

def calculate_amounts(rate, amount):
    usd_amount = round(rate * amount, 2)
    amd_amount = round(amount * rate * rateamd / 100) * 100
    bot_amount = amd_amount + 1500
    return usd_amount, amd_amount, bot_amount

def format_output(template, dash_address, amount, usd_amount, amd_amount, date_time, transaction_id, transaction_counter):
    return template.format(
        dash_address=dash_address,
        amount=amount,
        usd_amount=usd_amount,
        amd_amount=amd_amount,
        date=date_time.strftime('%Y-%m-%d'),
        time=date_time.strftime('%H:%M:%S'),
        transaction_id=transaction_id,
        transaction_no=transaction_counter
    )

async def retry_with_delay(func, delay=60):
    while True:
        try:
            await func()
            return
        except Exception as e:
            print("Error occurred during transaction generation:", e)
            await trio.sleep(delay)

previous_transaction_ids = set()  # To store previous transaction IDs

async def generate_transaction(template):
    while True:
        current_rate = rate  # Use the rate variable here
        if current_rate is None:
            await trio.sleep(120)  # Retry after 60 seconds if rate fetching fails
            continue
        transaction_data = await get_transaction_data()
        if transaction_data is None:
            await trio.sleep(120)  # Retry after 60 seconds if transaction data is not available
            continue
        dash_address, transaction_id, date_time_str, amount = transaction_data

        # Check if the transaction ID has been generated before
        if transaction_id not in previous_transaction_ids:
            previous_transaction_ids.add(transaction_id)  # Add the current transaction ID
            date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            usd_amount, amd_amount, bot_amount = calculate_amounts(current_rate, amount)
            transaction_counter = random.randint(100000, 999999)
            output = format_output(template, dash_address, amount, usd_amount, amd_amount, date_time, transaction_id, transaction_counter)
            print(output)

            bot = Bot(token=bot_token)
            for chat_id in bot_chat_ids:
                await bot.send_message(chat_id=chat_id, text=output)
        await trio.sleep(2)  # Wait for 60 seconds before generating the next transaction


async def run_trio_loop():
    print("Generating transactions using the provided values...")
    print("Template 1:")
    template1 = textwrap.dedent("""
        Գործարքի համար: {transaction_no}
        Գործարքի տեսակ: Գնում 
        Գումարի չափ: {amd_amount} AMD
        Կարգավիճակ։ հաջորդ 
        Ձեզ փորձապարկվել է: {amount} DASH 
        Հաշիվ: {dash_address} 
        Ամսաթիվ: {date} {time} 
        Փորձապարկում: {transaction_id}
        Transaction Link: https://blockchair.com/dash/transaction/{transaction_id}
        """)



    async with trio.open_nursery() as nursery:
        nursery.start_soon(generate_transaction, template1)

if __name__ == "__main__":
    trio.run(run_trio_loop)


# Код 2
import telebot
from telebot import types

# Create a bot instance and set the API token
bot = telebot.TeleBot('6067244950:AAGbAHcyAPWjtsJHMOmvY1Uf6wfaW4KJo5w')

# Dictionary to store user choices (buy or sell) for each user
user_choices = {}

# Dictionary to store the user's currency choice along with the amount they want to buy or sell
user_currency_amount = {}

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_start_message(message):
    # Create inline keyboard markup with two buttons in each row
    markup = types.InlineKeyboardMarkup()

    # Add the first row of buttons
    row1_buttons = [
        types.InlineKeyboardButton('Գնել BTC', callback_data='buy_btc'),
        types.InlineKeyboardButton('Վաճառել BTC', callback_data='sell_btc')
    ]
    markup.row(*row1_buttons)

    # Add the second row of buttons
    row2_buttons = [
        types.InlineKeyboardButton('Գնել DASH', callback_data='buy_dash'),
        types.InlineKeyboardButton('Վաճառել DASH', callback_data='sell_dash')
    ]
    markup.row(*row2_buttons)

    # Add the third row of buttons
    row3_buttons = [
        types.InlineKeyboardButton('Գնել LTC', callback_data='buy_ltc'),
        types.InlineKeyboardButton('Վաճառել LTC', callback_data='sell_ltc')
    ]
    markup.row(*row3_buttons)

    # Add the fourth row of buttons
    row4_buttons = [
        types.InlineKeyboardButton('Գնել USD-TRC20', callback_data='buy_usd'),
        types.InlineKeyboardButton('Վաճառել USDT', callback_data='sell_usd')
    ]
    markup.row(*row4_buttons)

    # Send the inline keyboard markup
    bot.send_message(message.chat.id, '👨‍🚀 Ես ձեզ կօգնեմ գնել կամ վաճառել Bitcoin և Dash 💵', reply_markup=markup)

# Handle the callback data from inline buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.message:
        if call.data.startswith(('buy_', 'sell_')):
            # Save the user's choice (buy or sell) for later use
            user_choices[call.message.chat.id] = call.data

            # Create a new inline keyboard markup for currency selection
            markup = types.InlineKeyboardMarkup()

            # Add the currency selection buttons
            currency_buttons = [
                types.InlineKeyboardButton('🇦🇲 AMD', callback_data='amd'),
                types.InlineKeyboardButton('🇺🇸 USD', callback_data='usd'),
                types.InlineKeyboardButton('💰 BTC', callback_data='btc')
            ]
            markup.row(*currency_buttons)

            # Send the currency selection inline keyboard markup
            bot.send_message(call.message.chat.id, 'Ի՞նչ արժույթով եք ցանկանում նշել DASH-ի քանակը', reply_markup=markup)

        elif call.data in ('amd', 'usd', 'btc'):
            # Get the user's previous choice (buy or sell) from the stored dictionary
            user_choice = user_choices.get(call.message.chat.id)

            if user_choice:
                # Save the user's currency choice
                user_currency_amount[call.message.chat.id] = {'currency': call.data}

                # Create a new inline keyboard markup for amount input
                markup = types.InlineKeyboardMarkup()

                # Add the number keypad buttons
                number_buttons = [
                    types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 10)
                ]
                # Move the '⬅️' button to the first row
                markup.row(types.InlineKeyboardButton('C', callback_data='clear'), types.InlineKeyboardButton('⬅️', callback_data='del'))
                markup.row(*number_buttons[0:3])  # Second row: 1, 2, 3
                markup.row(*number_buttons[3:6])  # Third row: 4, 5, 6
                markup.row(*number_buttons[6:9])  # Fourth row: 7, 8, 9
                markup.row(types.InlineKeyboardButton('.', callback_data='.'), types.InlineKeyboardButton('0', callback_data='0'), types.InlineKeyboardButton('✅', callback_data='done'))   # Fifth row: Decimal point

                # Send the amount input inline keyboard markup
                bot.send_message(call.message.chat.id, 'Որքա՞ն AMD-ի համարժեք DASH եք ցանկանում գնելը՝', reply_markup=markup)

        elif call.data.isdigit():
            # Get the user's previous choice (buy or sell) from the stored dictionary
            user_choice = user_choices.get(call.message.chat.id)

            if user_choice and call.message.chat.id in user_currency_amount:
                if call.data == '0' and 'amount' not in user_currency_amount[call.message.chat.id]:
                    # Ignore leading zeros
                    return

                if call.data == 'clear':
                    # Clear the amount input
                    user_currency_amount[call.message.chat.id].pop('amount', None)
                elif call.data == 'del':
                    # Delete the last character in the amount input
                    if 'amount' in user_currency_amount[call.message.chat.id]:
                        user_currency_amount[call.message.chat.id]['amount'] = user_currency_amount[call.message.chat.id]['amount'][:-1]
                elif call.data == 'done':
                    # User has finished entering the amount
                    if 'amount' in user_currency_amount[call.message.chat.id]:
                        action = 'Buy' if user_choice.startswith('buy_') else 'Sell'
                        currency = user_currency_amount[call.message.chat.id]['currency'].upper()
                        amount = int(user_currency_amount[call.message.chat.id]['amount'])

                        bot.send_message(call.message.chat.id, f'{action} {amount} {currency}')
                        # Clear user's choices after processing
                        del user_choices[call.message.chat.id]
                        del user_currency_amount[call.message.chat.id]
                        return
                else:
                    # Update the amount input
                    if 'amount' not in user_currency_amount[call.message.chat.id]:
                        user_currency_amount[call.message.chat.id]['amount'] = call.data
                    else:
                        user_currency_amount[call.message.chat.id]['amount'] += call.data

                # Create a new inline keyboard markup for amount input
                markup = types.InlineKeyboardMarkup()

                # Add the number keypad buttons
                number_buttons = [
                    types.InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1, 10)
                ]
                 # Move the '⬅️' button to the first row
                markup.row(types.InlineKeyboardButton('C', callback_data='clear'), types.InlineKeyboardButton('⬅️', callback_data='del'))
                markup.row(*number_buttons[0:3])  # Second row: 1, 2, 3
                markup.row(*number_buttons[3:6])  # Third row: 4, 5, 6
                markup.row(*number_buttons[6:9])  # Fourth row: 7, 8, 9
                markup.row(types.InlineKeyboardButton('.', callback_data='.'), types.InlineKeyboardButton('0', callback_data='0'), types.InlineKeyboardButton('✅', callback_data='done'))   # Fifth row: Decimal point

                # Send the updated amount input inline keyboard markup
                bot.edit_message_text(
                    f'Որքա՞ն AMD-ի համարժեք DASH եք ցանկանում գնելը՝\nԳումար: {user_currency_amount[call.message.chat.id].get("amount", "0")}',
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup
                )
            else:
                bot.send_message(call.message.chat.id, 'Invalid selection. Please start again.')

# Start the bot
bot.polling()
```
