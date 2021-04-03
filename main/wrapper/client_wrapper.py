import time

from main.ftx.ws_client import FtxWebsocketClient
from main.ftx.client import FtxClient
from main.telegram.telegram_client import TelegramClient


''' Wraps the websocket client, has extra methods we need to handle fills. '''
class FTXClientWrapper(FtxWebsocketClient):
    
    def __init__(self, token, chat_id, api_key, api_secret):
        super().__init__(api_key, api_secret)

        self.telegram_bot = TelegramClient(token, chat_id)
        self.rest_client = FtxClient(api_key, api_secret)

        # Subscribe
        self.get_fills()
        self.get_orders()

    def get_tp_and_sl_prices(self, symbol):
        tp_sl = self.rest_client.get_open_trigger_orders(symbol)
        sl = next(item for item in tp_sl if item['type'] == 'stop')['triggerPrice']
        tp = next(item for item in tp_sl if item['type'] == 'take_profit')['triggerPrice']
        return (tp, sl)

    def _handle_fills_message(self, message):
        super()._handle_fills_message(message)

        data = message['data']
        symbol = data['market']
        side = data['side'].upper()
        price = data['price']

        tp, sl = self.get_tp_and_sl_prices(symbol)

        if side == 'BUY':
            rr = (tp - price) / sl - price
        else:
            rr = (price - tp) / (price - sl)

        message_text = f'New position opened\n-------------------------------\n{side} {symbol} \
                       \nEntry price: {price}\nSL: {sl} | TP: {tp}\nRisk/reward: {round(rr, 2)}'

        self.telegram_bot.send_message(message_text)