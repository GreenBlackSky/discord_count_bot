Countdown Discord Bot

Discord bot, that reacts to direct messages or being tagged in any guild chat. Command it to `count to n` where n is an integer. It will count to given countdown, one message per second. `n` must be positive and no more than 9999, let's be reasonable)

I had to use `discord.Client` to catch all messages in all chats, not only bot commands. In any other situation `discord.ext.commands.Bot` would be more preferable.

To start, add `config.env` file to the root. It must contain folowing parameters:
* DISCORD_TOKEN
* POSTGRES_DB
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_HOST
* POSTGRES_PORT

Than, simply run `docker-compose -f "docker-compose.yaml" up -d --build` to build docker containers and run bot.