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
    db = sqlite3.connect('roster.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main(
            name TEXT,
            nickname TEXT,
            roster TEXT
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




intital_extensions = ['cogs.moderation', 'cogs.ws_planning', 'cogs.poll', 'cogs.medals', 'cogs.results']

if __name__ == '__main__':
    for extension in intital_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)






bot.run(TOKEN)