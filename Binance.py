import time
import requests


def get_dashusdt_price():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=DASHUSDT')
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data['price']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_formatted_time():
    current_time = time.strftime('%H:%M:%S', time.localtime())
    return current_time


def save_last_10_prices(price, filename='usdt.txt', max_lines=10):
    try:
        formatted_time = get_formatted_time()
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Add the new line to the end of the list
        lines.append(f"{price}\n")

        # Trim the list to max_lines
        lines = lines[-max_lines:]

        # Print the rotated lines to the console
        for line in lines:
            print(line, end="")

        # Rewrite the file with the updated lines
        with open(filename, 'w') as file:
            file.writelines(lines)
    except IOError as e:
        print(f"Error writing to the file: {e}")


if __name__ == "__main__":
    while True:
        price = get_dashusdt_price()
        if price is not None:
            save_last_10_prices(price)
        time.sleep(1)
