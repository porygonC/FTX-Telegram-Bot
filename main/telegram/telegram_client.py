import telegram


''' Sends messages to a specified user via telegram. '''
class TelegramClient:

    def __init__(self, token, chat_ids):
        self.chat_ids = chat_ids
        self.bot = telegram.Bot(token=token)

    def send_message(self, msg):
        for chat_id in self.chat_ids:
            self.bot.sendMessage(chat_id=chat_id, text=msg)