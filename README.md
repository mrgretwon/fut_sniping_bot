# FUT Sniping BOT

## Install requirements

```
pip install -r requirements.txt
```
Make sure you also have mpg123 package installed.
## Configuration
Everything is configured using config.py file.
Provide your credentials

```
USER = {
    "email": "your_email@example.com",
    "password": "your_password",
}
```

Enter the name of the player name and the maximum cost you want to spend for him.
Example:

```
PLAYER = {
    "name": "Sterling",
    "cost": 100000,
}
```

## Running

```
make run
```

After logging in, you have to provide access code by yourself.


