import discord
import json
from discord import Game
from discord.ext import commands
import random
import asyncio

with open('config.json') as f:
    data = json.load(f)

TOKEN = data["token"]
BOT_PREFIX = data["prefix"]

bot = commands.Bot(command_prefix=BOT_PREFIX)

#---------------------------------------------#
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')
    await bot.change_presence(game=Game(name="Waking Up"))
    bot.loop.create_task(status_task())

#----------------------------------------------#
async def status_task():

    status_messages = data["status_messages"]

    while True:
        await asyncio.sleep(600)
        status_num = random.randint(0, len(status_messages) - 1)
        new_status = status_messages[status_num]
        await bot.change_presence(game=Game(name=new_status))

#----------------------------------------------#

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
    for i in range(1, num + 1):
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

# @bot.command(name='roll',
#             description='Rolls given die/dice in the format nDN with the valid die as d2,3,4,6,8,10,12,20,100,1000',
#             brief='Rolls a given die/dice',
#             aliases=['Roll', 'ROLL'],
#             pass_context=True)
# async def roll(context):

#--------------------------------------------------------------#

bot.run(TOKEN)
