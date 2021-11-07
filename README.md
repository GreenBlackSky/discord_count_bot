# Countdown Discord Bot

Discord bot, that reacts to direct messages or being tagged in any guild chat. Command it to `count to n` where n is an integer. It will count to given countdown, one message per second. `n` must be positive and no more than 9999, let's be reasonable)

Bot can count in several chats simultaneously, but only one countdown per chat.

Tag bot and send message `stop` to stop countdown.

I had to use `discord.Client` to catch all messages in all chats, not only bot commands. In any other situation `discord.ext.commands.Bot` would be more preferable.

## Start up

To start, add `config.env` file to the root. It must contain folowing parameters:
* DISCORD_TOKEN
* POSTGRES_DB
* POSTGRES_USER
* POSTGRES_PASSWORD
* POSTGRES_HOST
* POSTGRES_PORT
* PGADMIN_DEFAULT_EMAIL
* PGADMIN_DEFAULT_PASSWORD

Than, simply run `docker-compose -f "docker-compose.yaml" up -d --build` to build docker containers and run bot.

## Commands
Tag bot in any room and print command, or write it DM.
 * `count to n` where n in a positive integer. Bot will respond by counting from one to given number, one message per second. Bot will not perform two countdowns in one room at one time. But it can count in any number of rooms simultaneously.
 * `stop` will make bot stop counting in given room.

## Logic

## Maintance

There are some ways to monitor bot's activity. 

* Pgadmin allows to look into bot's database. Go to http://localhost:5050/ , use `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` from your `config.env` to log in. Then create server, use standart postgresql port (5432) and host from `docker-compose.yaml` (`db`). Database name, username and password, again, take from `config.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` correspondingly).

## Database structure

Database has three tables:

* `tasks` table keeps all the records about valid commands bot received.
* `command_errors` table stores information about errors, that occured while bot was handling command.
* `general_errors` table keeps information about errors, that was not caused by command.

## Containers

Bot is container-based application. It is consists of following containers:

* bot - python 3.9-slim-buster based container, that contains all application logic. While bot is in development, folder with code is not copied, but mapped as a volume. This way there is no need to rebuild whole container every time we change code. Upon release, though, source code should be copied into container.
* postgres - standart postgresql container. Only interesting bit here is an `init.sql` file, that contains database structure.
* pgadmin - it contains tool to administrate local database.