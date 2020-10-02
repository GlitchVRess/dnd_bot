#!/home/kazasu/programming/python/dnd_bot/cognitive_modules/bin/python3.6
import asyncio
import configparser
import gambling_subprocessor as gambler
import discord
import os
import setproctitle
import time

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


@client.event
async def on_ready():
    """Printing bot information on initial login.
    """
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')


@client.event
async def on_message(message):
    """Watches messages in channel for specific content. Typically used for
    returning messages when certain actions are requested.
    """
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
    # !timer (<number>, <number>s, <number>m)
    elif message.content.startswith('!timer'):
        timer = message.content
        timer = timer.replace('!timer ', '')
        #if it is a number only then take it as seconds
        if timer.isnumeric():
            time.sleep(int(timer))
            await client.send_message(message.channel, 'Time is up!'.format(message))
        #if it is just characters, not valid argument
        elif timer.isalpha():
            await client.send_message(message.channel, 'Please enter a valid time.'.format(message))
        #if it is <number>s, take it as seconds
        elif 's' in timer:
            timer = timer.replace('s', '')
            time.sleep(int(timer))
            await client.send_message(message.channel, 'Time is up!'.format(message))
        #if it is <number>m, take it as minutes
        elif 'm' in timer:
            timer = timer.replace('m', '')
            time.sleep(int(timer*60))
            await client.send_message(message.channel, 'Time is up!'.format(message))

client.run(token)
