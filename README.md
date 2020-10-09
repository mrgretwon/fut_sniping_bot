# FUT Sniping BOT

## Install requirements

```
pip install -r requirements.txt
```
Make sure you also have mpg123 package installed.
## Configuration
Provide your credentials in config.py file

```
USER = {
    "email": "your_email@example.com",
    "password": "your_password",
}
```

In main.py file enter the name of the player name and the maximum cost you want to spend for him.
Example:

```
bot.buy_player("Rooney", 600)
```

## Running

```
make run
```

After logging in, you have to provide access code by yourself.


