import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord

class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True, help="Plan the next WS with a roster")
    async def roster(self, ctx):
        await ctx.send("Test command")




def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')