import discord
import json
import requests
from discord import Game
from discord.ext import commands
import random
import asyncio
import datetime, time

with open('config.json') as f:
    data = json.load(f)

TOKEN = data["token"]
BOT_PREFIX = data["prefix"]

bot = commands.Bot(command_prefix=BOT_PREFIX)
start_time = time.time()

#---------------------------------------------#
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    bot.loop.create_task(status_task())

#----------------------------------------------#
# Task sets the bots "Playing" status to a random string from a list stored
# in the config.json file.
async def status_task():

    status_messages = data["status_messages"]

    while True:
        status_num = random.randint(0, len(status_messages) - 1)
        new_status = status_messages[status_num]
        await bot.change_presence(game=Game(name=new_status))
        await asyncio.sleep(180)

#----------------------------------------------#
# Kill command for the bot.
@bot.command(name='stop',
            pass_context=True)
async def stop(context):

    m = context.message.author
    if m.server_permissions.administrator or "Officer" in m.roles:
        await bot.close()
    else:
        return
#---------------------------------------------#
# Roll dice command, follows common dice formatting.
@bot.command(name='roll',
            description='Rolls given die/dice in the format nDN with the valid die as d2,3,4,6,8,10,12,20,100,1000',
            brief='Rolls a given die/dice',
            aliases=['Roll', 'ROLL'],
            pass_context=True)
async def roll(context):

    if context.message.channel.name != "tabletop_games":
        return

    entered_message = context.message.content.split(' ', 1)[1]
    num_dice = int(entered_message.split('d')[0]);
    die = int(entered_message.split('d')[1]);

    legal_dice = [2, 3, 4, 6, 8, 10, 12, 20, 100, 1000]

    if num_dice < 1:
        await bot.say('Please specify an integer number of die(ce) greater than 0.')
        return

    if die not in legal_dice:
        await bot.say('Please specify a valid die, the valid dice are: d2, 3, 4, 6, 8, 10, 12, 20, 100, 1000.')
        return

    rolled = 0
    for i in range(1, num_dice + 1):
        rolled += random.randint(1, die)

    if num_dice == 1 and die == 20:
        if rolled == 1:
            await bot.say("Uh oh, your **1d20** rolled a **nat 1**.")
            return
        elif rolled == 20:
            await bot.say("Wow, your **1d20** rolled a **nat 20**.")
            return

    await bot.say("Your **{0}** rolled a(n) **{1}**.".format(entered_message, rolled))

#-------------------------------------------------------------#
# Pulls a random dog pic from the Dog CEO api.
@bot.command(name='puppy',
            description='',
            brief='',
            aliases=['Puppy', 'PUPPY'])
async def puppy():

    url = 'https://dog.ceo/api/breeds/image/random'

    response = requests.get(url)
    image = response.json()["message"]
    await bot.say(image)

#--------------------------------------------------------------#

@bot.command(name='kitty',
            description='',
            brief='',
            aliases=['Kitty', 'KITTY'])
async def kitty():

    url = 'https://api.thecatapi.com/v1/images/search'

    response = requests.get(url)
    image = response.json()[0]["url"]
    await bot.say(image)

#--------------------------------------------------------------#

@bot.command(name="ud",
            description='Defines a given term using Urban Dictionary',
            brief='Urban definition',
            aliases=['urban', 'UD'])
async def ud(message):

    url = 'http://api.urbandictionary.com/v0/define?term='
    url += "{" + message + "}"
    response = requests.get(url)
    data = response.json()
    await bot.say(data["list"][0]["definition"])

#-------------------------------------------------------------#

@bot.command(name='uptime',
            description='Gives the current uptime of the bot as Hour/Min/Sec',
            brief='Curent uptime of BOTch',
            aliases=['up', 'Uptime', 'Up'])
async def uptime():
    current_time = time.time()
    uptime = int(round(current_time - start_time))
    await bot.say("uptime: {}".format(str(datetime.timedelta(seconds=uptime))))

#-------------------------------------------------------------#

bot.run(TOKEN)
