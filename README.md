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
* GF_SECURITY_ADMIN_USER
* GF_SECURITY_ADMIN_PASSWORD

Than, simply run `docker-compose -f "docker-compose.yaml" up -d --build` to build docker containers and run bot.

## Commands

Tag bot in any room and print command, or write it DM.
 * `count to n` where n in a positive integer. Bot will respond by counting from one to given number, one message per second. Bot will not perform two countdowns in one room at one time. But it can count in any number of rooms simultaneously.
 * `stop` will make bot stop counting in given room.

## Logic

Bot monitors every message in the guild and DM. First it does check the message is adressed to it. If it does, bot checks if it is a command. If it is a command to start countdown, bot writes it's new task to database. Then it starts counting coroutine.

Upon starting, bot checks if there is any tasks in database, that should be done now. If threre are any, it start's performing them.

If an error occures, bot logs it into database as well.

If you look closely, you may notice that interval between messages can sometimes be a little more than a second. Unfortunately, I haven't manged to solve this problem in time. Using dynamic interval leads to an unstability in interval changes. I decided to allow machine do things when it sees suitable. For now.

## Maintenance

There are some ways to monitor bot's activity. 

* Pgadmin allows to look into bot's database. Go to http://localhost:5050/ (pgadmin takes a minute or two to start, don't rush it) , use `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` from your `config.env` to log in. Then create server, use standart postgresql port (5432) and host from `docker-compose.yaml` (`db`). Database name, username and password, again, take from `config.env` (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` correspondingly).

* Prometheus is used to monitor number bot. You can go to http://localhost:9090/ and watch it yourself, it monitors the  folowing metrics:
  * number of given commands
  * number of given invalid commands
  * number of canceled requests
  * number of wrong commands (like when someone asks bot to spot, while it is not counting)
  * distribution of count values

* Grafana is a way to visualize data from prometheus. Go to http://localhost:3000/ , log in useing creds from `GF_SECURITY_ADMIN_USER` and `GF_SECURITY_ADMIN_PASSWORD`, proceed to bot_dashboard and enjoy the view.

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
* prometheus - monitoring tool, scraps metrics from bot.
* grafana - visualisation tool for prometheus metrics.