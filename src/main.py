from src.bot import Bot
from src.config import USER

bot = Bot()
bot.login(USER)
bot.buy_player("Rooney", 600)


