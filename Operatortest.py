from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
from telegram import Bot
import asyncio
from decimal import Decimal


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


# Function to convert a value to a safe float
def safe_float(value):
    try:
        return float(value.strip()) if value.strip() else None
    except ValueError:
        return None


# Function to format a USD amount as specified
# Function to format a USD amount as specified
def format_usd_amount(amount):
    formatted_amount = f"${amount:.2f}" if amount % 1 != 0 else f"${int(amount)}"
    formatted_amount = formatted_amount.rstrip("0").rstrip(".")
    return formatted_amount


# Function to generate a transaction template
def generate_transaction_template(data, template_version):
    try:
        dash_address = data['dash_address']
        amount = data['amount']
        rate = data['rate']

        if template_version == 2:
            rate += 0.01
        elif template_version == 3:
            rate -= 0.01

        usd_amount = round(amount * rate, 2)
        amd_amount = data['amd_amount']
        date_time = data['date_time']
        txid = data['txid']

        if txid in processed_txids:
            return None

        processed_txids[txid] = True
        usd_amount_str = format_usd_amount(usd_amount)

        if template_version == 1 or template_version == 2:
            template = f"""  
            -----------------------------------------------
            Transaction Details:
            Dash Address: {dash_address}
            Amount: {amount:.8f} DASH
            USD: {usd_amount_str}
            AMD: {amd_amount:.0f}
            Transaction Time: {date_time}
            DASH Rate: ${rate:.2f} (binance)
            Transaction ID: https://blockchair.com/dash/transaction/{txid}
            -----------------------------------------------
            """
        elif template_version == 3:
            template = f"""  
            *************************************************
            Transaction Info:
            Address: {dash_address}
            DASH: {amount:.8f}
            Equivalent in USD: {usd_amount_str}
            Equivalent in AMD: {amd_amount:.0f}
            Time of Transaction: {date_time}
            Current DASH Rate: ${rate:.2f} (binance)
            Link to Transaction: https://blockchair.com/dash/transaction/{txid}
            *************************************************
            """

        with open('123.txt', 'a') as f:
            f.write(template + "\n")

        return template
    except KeyError as e:
        print(f"Error: Missing key '{e}' in transaction data.")
        exit()


# Custom event handler class
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'event type: {event.event_type}  path: {event.src_path}')
        if event.event_type == 'modified':
            print(f'<{time.ctime()}> Received modified event - {event.src_path}.')
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 6:
                    return

                data = {
                    'dash_address': lines[0].strip(),
                    'amount': Decimal(lines[3].strip()),
                    'txid': lines[1].strip(),
                    'date_time': lines[2].strip(),
                    'rate': Decimal(lines[4].strip()) if len(lines) > 4 else None,
                    'usd_amount': Decimal(lines[5].strip()) if len(lines) > 5 else None,
                    'amd_amount': Decimal(lines[6].strip()) if len(lines) > 6 else None,
                }

                for i in range(1, 4):
                    template = generate_transaction_template(data, i)
                    if template is None:
                        continue

                    asyncio.run(send_message(template))


# Asynchronous function to send a message to Telegram
async def send_message(template):
    bot_token = '6263739899:AAGiO-6W8WMcs-tHY3NZzEG_AyzLPHPXrhM'
    bot = Bot(token=bot_token)
    chat_ids = ['740279851', '6564297273', '6585383486']
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=template)
        except Exception as e:
            print(f"Failed to send the message to chat ID {chat_id}. Error: {e}")


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./transaction_values.txt', recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()