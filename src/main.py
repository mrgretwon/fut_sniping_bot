from src.bot import Bot
from src.config import USER, PLAYER, LOGIN_MANUALLY, USE_CHROME_PROFILE, MAX_PLAYER

bot = Bot()
if LOGIN_MANUALLY and not USE_CHROME_PROFILE:
    bot.login_manually()
elif not USE_CHROME_PROFILE:
    bot.login(USER)
else:
    bot.wait_for_login()

bot.buy_players(PLAYER["name"], PLAYER["cost"], MAX_PLAYER)
