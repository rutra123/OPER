import asyncio
import re
from datetime import datetime
from telegram import Bot

# Define your Telegram bot token
bot_token = '6327040267:AAHMasLxQFEa7Noimv9Z_yDa82FFilzMFUQ'  # Your bot token
chat_id = '6585383486'  # Your chat ID

# Create a Telegram bot instance
bot = Bot(token=bot_token)

# Read the template from the file
with open('123.txt', 'r') as file:
    template = file.read()

async def send_messages():
    final_file = open('final.txt', 'w')  # Open the file to write the final versions

    # Create a loop to generate and send 60 versions of the template
    for i in range(1, 61):
        # Generate a random transaction time
        transaction_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Replace the transaction time seconds value in the template
        modified_template = re.sub(r'Time: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', f'Time: {transaction_time}', template)

        # Replace the transaction seconds value in the template
        modified_template = re.sub(r'Transaction: .+', f'Transaction: https://blockchair.com/dash/transaction/{i}', modified_template)

        # Send the modified template to your Telegram chat ID as a separate message
        await bot.send_message(chat_id=chat_id, text=modified_template)

        # Write the modified template to the final file
        final_file.write(modified_template + '\n')

        # Wait for 0.2 seconds before sending the next version
        await asyncio.sleep(0.2)

    final_file.close()  # Close the final file after writing all the versions

# Create an event loop and run the async function
loop = asyncio.get_event_loop()
loop.run_until_complete(send_messages())