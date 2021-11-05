Countdown Discord Bot

Discord bot, that reacts to direct messages or being tagged in any guild chat. Command it to `count to n` where n is an integer. It will count to given countdown, one message per second.

I had to use `discord.Client` to catch all messages in all chats, not only bot commands. In any other situation `discord.ext.commands.Bot` would be more preferable.

