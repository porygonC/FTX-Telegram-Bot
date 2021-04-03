import time

from main.wrapper.client_wrapper import FTXClientWrapper
from settings import telegram_token, chat_id, api_key, api_secret


if __name__ == "__main__":

    ''' The bot runs the main loop forever as long as the websocket is active. '''

    bot = FTXClientWrapper(telegram_token, chat_id, api_key, api_secret)

    while True:
        time.sleep(60)