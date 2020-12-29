import os
import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import asyncio
import sys
import requests
import numpy as np
from discord.utils import get

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


 
# Ready
@bot.event
async def on_ready():
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
            user BLOB,
            nickname TEXT,
            level INTEGER
        )
    ''')
    #addColumn = "ALTER TABLE main ADD COLUMN relics TEXT"
    #cursor.execute(addColumn)
    print(f'{bot.user.name} has connected to Discord!')
    return await bot.change_presence(activity=discord.Activity(type=1, name="BattleCo"))

@bot.event
async def on_message(ctx):
    if(ctx.content.find('The `roster` command is disabled.') != -1):
        await ctx.delete()
    await bot.process_commands(ctx)


def add(queue, user):
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    sql = "SELECT nickname FROM main WHERE nickname=?"
    cursor.execute(sql, [(user.display_name)])
    result = cursor.fetchall()
    if len(result) == 0: # Person wasn't found in database, add them to the rs queue
        sql = ("INSERT INTO main(user, nickname, level) VALUES(?,?,?)")
        val = (user, user.display_name, queue)
        cursor.execute(sql, val)

@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if str(user) != "Oxyg3n's WS Organizer#7677" and str(reaction.message.author) == "Oxyg3n's WS Organizer#7677":
        if(emoji == "6️⃣"):
            #add(6, user)
            await reaction.message.channel.send("added to rs6 queue")
        elif(emoji == "7️⃣"):
            add(7, user)
        elif(emoji == "8️⃣"):
            add(8, user)
        elif(emoji == "9️⃣"):
            add(9, user)
        elif(emoji == "🔟"):
            add(10, user)



intital_extensions = ['cogs.moderation', 'cogs.ws_planning', 'cogs.poll', 'cogs.medals', 'cogs.results', 'cogs.redstars']

if __name__ == '__main__':
    for extension in intital_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)






bot.run(TOKEN)