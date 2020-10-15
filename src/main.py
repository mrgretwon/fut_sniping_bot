from src.bot import Bot
from src.config import USER, PLAYER

bot = Bot()
bot.login(USER)
bot.buy_player(PLAYER["name"], PLAYER["cost"])
bot.quit()


