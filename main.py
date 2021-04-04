import time

from main.wrapper.client_wrapper import FTXClientWrapper
from settings import telegram_token, chat_ids, api_key, api_secret


if __name__ == "__main__":

    ''' The bot sends telegram messages on fills as long as the websocket is active. '''

    bot = FTXClientWrapper(telegram_token, chat_ids, api_key, api_secret)

    print("Running main loop forever.")

    while True:
        time.sleep(60)