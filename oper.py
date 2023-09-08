import asyncio
import time
from telegram import Bot
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Define your Telegram bot token here
TELEGRAM_BOT_TOKEN = '6263739899:AAGiO-6W8WMcs-tHY3NZzEG_AyzLPHPXrhM'

# List of Telegram chat IDs to which you want to send the templates
chat_ids = ['740279851', '6564297273','6585383486 ']  # Replace with your actual chat IDs

# Dictionary to store processed txids
processed_txids = {}

# Function to read transaction values from the file
def read_transaction_values(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print("Error: 'transaction_values.txt' file not found.")
        exit()

# Function to read the rate value from usdt.txt
def read_usdt_rate(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 7:
                rate = safe_float(lines[6])  # Read rate from the 7th line (index 6)
                return rate
            else:
                print("Error: 'usdt.txt' file does not have enough lines.")
                exit()
    except FileNotFoundError:
        print("Error: 'usdt.txt' file not found.")
        exit()

# Function to convert a value to a safe float
def safe_float(value):
    try:
        return float(value.strip()) if value.strip() else None
    except ValueError:
        return None

# Function to format a USD amount as specified
def format_usd_amount(amount):
    formatted_amount = f"${amount:.2f}" if amount % 1 != 0 else f"${int(amount)}"

    # Remove ".0" or ".00" from the end
    formatted_amount = formatted_amount.rstrip("0").rstrip(".")

    return formatted_amount


# Function to process transaction data from the file
def process_transaction_data(lines):
    try:
        dash_address = lines[0].strip()
        amount = safe_float(lines[3])
        txid = lines[1].strip()  # Transaction ID (txid)
        rate = None  # Initialize rate to None

        if len(lines) >= 7:
            rate = read_usdt_rate('usdt.txt')  # Read rate from usdt.txt

        if None in (amount, rate):
            raise ValueError("'amount' or 'rate' is not a valid float in the file.")

        usd_amount = amount * rate
        amd_amount = 391 * amount * rate
        date_time = lines[2].strip()

        return {
            'dash_address': dash_address,
            'amount': amount,
            'usd_amount': usd_amount,
            'amd_amount': amd_amount,
            'date_time': date_time,
            'rate': rate,  # Include rate in the returned data
            'txid': txid  # Include txid in the returned data
        }
    except ValueError as e:
        print(f"Error: {e}")
        exit()


# Ваша функция для генерации шаблона
def generate_transaction_template(data):
    try:
        dash_address = data['dash_address']
        amount = data['amount']
        usd_amount = round(data['usd_amount'], 2)  # Round to one decimal place
        amd_amount = data['amd_amount']
        date_time = data['date_time']
        rate = data['rate']
        txid = data['txid']  # Transaction ID (txid)

        # Check if this txid has been processed before
        if txid in processed_txids:
            return None  # Skip generating the template

        # Add this txid to the processed_txids dictionary
        processed_txids[txid] = True

        # Format the USD amount as specified
        usd_amount_str = format_usd_amount(usd_amount)

        template = f""" 
-----------------------------------------------
To: {dash_address}
Amount: {amount:.8f} DASH ({usd_amount_str} / {amd_amount:.0f} AMD) 
Time: {date_time}
DASH rate: ${rate:.2f} (binance)
Sent by @BitcoinOperator
-----------------------------------------------
Transaction: https://blockchair.com/dash/transaction/{txid}
        """


        return template
    except KeyError as e:
        print(f"Error: Missing key '{e}' in transaction data.")
        exit()

def safe_float(value):
    try:
        return float(value.strip()) if value.strip() else None
    except ValueError:
        return None

# Function to format a USD amount as specified
def format_usd_amount(amount):
    formatted_amount = f"${amount:.2f}" if amount % 1 != 0 else f"${int(amount)}"

    # Remove ".0" or ".00" from the end
    formatted_amount = formatted_amount.rstrip("0").rstrip(".")

    return formatted_amount


# Function to process transaction data from the file
def process_transaction_data(lines):
    try:
        dash_address = lines[0].strip()
        amount = safe_float(lines[3])
        txid = lines[1].strip()  # Transaction ID (txid)
        rate = None  # Initialize rate to None

        if len(lines) >= 7:
            rate = read_usdt_rate('usdt.txt')  # Read rate from usdt.txt

        if None in (amount, rate):
            raise ValueError("'amount' or 'rate' is not a valid float in the file.")

        usd_amount = amount * rate
        amd_amount = 391 * amount * rate
        date_time = lines[2].strip()

        return {
            'dash_address': dash_address,
            'amount': amount,
            'usd_amount': usd_amount,
            'amd_amount': amd_amount,
            'date_time': date_time,
            'rate': rate,  # Include rate in the returned data
            'txid': txid  # Include txid in the returned data
        }
    except ValueError as e:
        print(f"Error: {e}")
        exit()


# Ваша функция для генерации шаблона
def generate_transaction_template(data):
    try:
        dash_address = data['dash_address']
        amount = data['amount']
        usd_amount = round(data['usd_amount'], 2)  # Round to one decimal place
        amd_amount = data['amd_amount']
        date_time = data['date_time']
        rate = data['rate']
        txid = data['txid']  # Transaction ID (txid)

        # Check if this txid has been processed before
        if txid in processed_txids:
            return None  # Skip generating the template

        # Add this txid to the processed_txids dictionary
        processed_txids[txid] = True

        # Format the USD amount as specified
        usd_amount_str = format_usd_amount(usd_amount)

        template = f""" 
-----------------------------------------------
To: {dash_address}
Amount: {amount:.8f} DASH ({usd_amount_str} / {amd_amount:.0f} AMD) 
Time: {date_time}
DASH rate: ${rate + 0.01:.2f} (binance)
Sent by @BitcoinOperator
-----------------------------------------------
Transaction: https://blockchair.com/dash/transaction/{txid}
        """


        return template
    except KeyError as e:
        print(f"Error: Missing key '{e}' in transaction data.")
        exit()

def safe_float(value):
    try:
        return float(value.strip()) if value.strip() else None
    except ValueError:
        return None

# Function to format a USD amount as specified
def format_usd_amount(amount):
    formatted_amount = f"${amount:.2f}" if amount % 1 != 0 else f"${int(amount)}"

    # Remove ".0" or ".00" from the end
    formatted_amount = formatted_amount.rstrip("0").rstrip(".")

    return formatted_amount


# Function to process transaction data from the file
def process_transaction_data(lines):
    try:
        dash_address = lines[0].strip()
        amount = safe_float(lines[3])
        txid = lines[1].strip()  # Transaction ID (txid)
        rate = None  # Initialize rate to None

        if len(lines) >= 7:
            rate = read_usdt_rate('usdt.txt')  # Read rate from usdt.txt

        if None in (amount, rate):
            raise ValueError("'amount' or 'rate' is not a valid float in the file.")

        usd_amount = amount * rate
        amd_amount = 391 * amount * rate
        date_time = lines[2].strip()

        return {
            'dash_address': dash_address,
            'amount': amount,
            'usd_amount': usd_amount,
            'amd_amount': amd_amount,
            'date_time': date_time,
            'rate': rate,  # Include rate in the returned data
            'txid': txid  # Include txid in the returned data
        }
    except ValueError as e:
        print(f"Error: {e}")
        exit()


# Ваша функция для генерации шаблона
def generate_transaction_template(data):
    try:
        dash_address = data['dash_address']
        amount = data['amount']
        usd_amount = round(data['usd_amount'], 2)  # Round to one decimal place
        amd_amount = data['amd_amount']
        date_time = data['date_time']
        rate = data['rate']
        txid = data['txid']  # Transaction ID (txid)

        # Check if this txid has been processed before
        if txid in processed_txids:
            return None  # Skip generating the template

        # Add this txid to the processed_txids dictionary
        processed_txids[txid] = True

        # Format the USD amount as specified
        usd_amount_str = format_usd_amount(usd_amount)

        template = f""" 
-----------------------------------------------
To: {dash_address}
Amount: {amount:.8f} DASH ({usd_amount_str} / {amd_amount:.0f} AMD) 
Time: {date_time}
DASH rate: ${rate - 0.01:.2f} (binance)
Sent by @BitcoinOperator
-----------------------------------------------
Transaction: https://blockchair.com/dash/transaction/{txid}
        """


        return template
    except KeyError as e:
        print(f"Error: Missing key '{e}' in transaction data.")
        exit()

# Asynchronous function to send a message to Telegram
async def send_telegram_message(message, chat_id):
    if message:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=chat_id, text=message)


# Custom event handler class
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print("Waiting...")
        updated_template = generate_transaction_template(process_transaction_data(read_transaction_values('transaction_values.txt')))
        if updated_template:
            print(updated_template)



# Create an observer and set the custom event handler
observer = Observer()
observer.schedule(MyHandler(), path='.')
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
