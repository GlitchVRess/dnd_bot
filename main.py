#!/home/kazasu/programming/python/dnd_bot/cognitive_modules/bin/python3.6
import asyncio
import configparser
import gambling_subprocessor as gambler
import discord
import os
import setproctitle

# Sets current working directory to the script's home directory.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# config class creation, checks if able to import from config.txt
config = configparser.ConfigParser()
try:
    config.read("config.txt")
except IOError:
    with open("error_log.txt", "a") as file:
        file.write(datetime.now() + ":    " +
                   traceback.format_exc())
    raise SystemExit(0)

# Setting the title of the process.
setproctitle.setproctitle(config.get("discord_config", "name"))

# Setting discord secret token.
token = config.get("discord_config", "token")

client = discord.Client()


# Printing bot information on initial login.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


# Watches messages in channel for specific content. Typically used for
# returning messages when certain actions are requested.
@client.event
async def on_message(message):
    # Roll dice, example: !roll 1d20 or !roll 1d20+3.
    if message.content.startswith('!roll'):
        await client.send_message(
            message.channel,
            "{0}: {1}".format(message.author, gambler.roll(message.content)))
    # Stereotypical help message. Needs work.
    elif message.content.startswith('!help'):
        await client.send_message(
            message.channel,
            '{0}: Please use !roll 1d20 to roll.'.format(message.author))
    # Uses json file to perform specific rolls based on the string following
    # !cast
    elif message.content.startswith('!cast'):
        await client.send_message(
            message.channel,
            "{0}: {1}".format(message.author, gambler.cast(message.content)))

client.run(token)
