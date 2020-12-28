from src.bot import Bot
from src.config import USER, PLAYER, LOGIN_MANUALLY, USE_CHROME_PROFILE

bot = Bot()
if LOGIN_MANUALLY and not USE_CHROME_PROFILE:
    bot.login_manually()
elif not USE_CHROME_PROFILE:
    bot.login(USER)
else:
    bot.wait_for_login()

bot.buy_player(PLAYER["name"], PLAYER["cost"])
