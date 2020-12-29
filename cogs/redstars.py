import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import requests
import asyncio
import numpy as np
from discord.utils import get
from discord import client

def react_check(user, msg, emoji):
    def check(reaction, usr):
        return usr==user and reaction.message.id==msg.id and reaction.emoji==emoji
    return check

class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Use this command to join a rs queue by either typing in !rs to join your current rs level or !rs # to join a specific rs queue")
    async def rs(self, ctx, level=None):
        for role in (ctx.message.author.roles):
            print(role)


    @commands.command(aliases=['q'], help="Use this command to see what queues are currently active and join one!")
    async def queue(self, ctx):
        queue_embed = discord.Embed(
            description = (f'The current Red Star queues or soemething'),
            colour = discord.Colour.red()
        )
        queue_embed.add_field(name="React below to join a Red Star queue", value="Queues: 6, 7, 8, 9, 10")
        message = await ctx.send(embed=queue_embed)
        emojis = ['6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for emoji in emojis:
            await message.add_reaction(emoji)
        
    


def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('Redstars loaded')