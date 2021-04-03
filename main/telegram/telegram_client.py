import telegram


''' Sends messages to a specified user via telegram. '''
class TelegramClient:

    def __init__(self, token, chat_id):
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=token)

    def send_message(self, msg):
        self.bot.sendMessage(chat_id=self.chat_id, text=msg)