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

        self.last_received_fills = {}

        # Subscribe
        self.get_fills()
        self.get_orders()

    def get_tp_and_sl_prices(self, symbol):
        tp_sl = self.rest_client.get_open_trigger_orders(symbol)
        try:
            sl = next(item for item in tp_sl if item['type'] == 'stop')
            tp = next(item for item in tp_sl if item['type'] == 'take_profit')
        except Exception as e:
            return (0, 0)
        return (tp['triggerPrice'], sl['triggerPrice'])

    def _handle_fills_message(self, message):
        super()._handle_fills_message(message)

        data = message['data']
        symbol = data['market']
        side = data['side'].upper()
        price = data['price']
        size = data['size']

        if symbol in self.last_received_fills and time.time() - self.last_received_fills[symbol] < 5:
            print("Received double message, ignoring.")
            return
        self.last_received_fills[symbol] = time.time()
        print("Received message.")

        tp, sl = self.get_tp_and_sl_prices(symbol)

        if 'PERP' in symbol:
            position = self.rest_client.get_position(symbol, True)
            print(position)

        if not tp or not sl:
            rr = 'none'
        else:
            if side == 'BUY':
                rr = round( (tp - price) / (price - sl), 2 )
            else:
                rr = round( (price - tp) / (sl - price), 2 )

        message_text = f'New order filled:\n----------------------------\n{side} {symbol} \
                       \nSize: {size}\nEntry price: {price}\nSL: {sl} | TP: {tp}\nRisk/reward: {rr}'

        print("Sending message:\n\n" + message_text + "\n")

        self.telegram_bot.send_message(message_text)