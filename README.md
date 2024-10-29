# RGB Lightning Node Telegram Bot

Telegram bot to test RGB payments on the Lightning Network.

It requires a running instance of [rgb-lightning-node (RLN)].

## Build and run

First, clone the project:
```sh
git clone https://github.com/RGB-Tools/rln-telegram-bot
```

Then obtain an API token that is necessary to create the Telegram bot.
The token can be obtained by contacting `@BotFather` on Telegram, issuing
the `/newbot` command and following the steps.

Once you obtained the token you can copy the sample config file (`cp
config.ini.sample config.ini`) and set the `API_TOKEN` key to its value.

Then, issue an asset on your RGB LN node and set the `ASSET_ID` key of the
config file to its ID.

Finally, provided you have [poetry] installed, you can install and run the bot
executing:
```sh
poetry install
poetry run bot
```

## Develop

When developing, you can run the following utilities:
```sh
# lint code
poetry run pylint rgb_ln_telegram_bot

# format code
poetry run black rgb_ln_telegram_bot

# check code quality
poetry run pylama rgb_ln_telegram_bot

# sort imports
poetry run isort --profile black rgb_ln_telegram_bot

# find unused code
poetry run vulture rgb_ln_telegram_bot

# check compliance with docstring conventions
poetry run pydocstyle rgb_ln_telegram_bot
```


[poetry]: https://python-poetry.org/docs/
[rgb-lightning-node (RLN)]: https://github.com/RGB-Tools/rgb-lightning-node
