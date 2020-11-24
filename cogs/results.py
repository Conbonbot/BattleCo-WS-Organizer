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


class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Input a WS results, of the form enemy type(15v15) relic-count")
    async def result(self, ctx, enemy, ws_type, relics):
        if(ws_type == "15v15" or ws_type == "10v10" or ws_type == "5v5"):
            relic_count = relics.split("-")
            print(relic_count[0], relic_count[1])
            db = sqlite3.connect('results.sqlite')
            cursor = db.cursor()
            result = "Win" if (relic_count[0] > relic_count[1]) else "Tie" if (relic_count[0] == relic_count[1]) else "Loss"
            sql = ("INSERT INTO main(enemy, type, result, relics) VALUES(?,?,?,?)")
            val = (enemy, ws_type, result, relics)
            cursor.execute(sql,val)
            db.commit()
            cursor.close()
            db.close()
            if result == "Win":
                result_embed = discord.Embed(
                    description = (f'BattleCo vs. {enemy}'),
                    colour = discord.Colour.green()
                )
            elif result == "Tie":
                result_embed = discord.Embed(
                    description = (f'BattleCo vs. {enemy}'),
                    colour = discord.Colour.blue()
                )
            else:
                result_embed = discord.Embed(
                    description = (f'BattleCo vs. {enemy}'),
                    colour = discord.Colour.red()
                )
            result_embed.add_field(name='Enemy: ', value=enemy)
            result_embed.add_field(name='WS Type: ', value=ws_type)
            result_embed.add_field(name='Result: ', value=result)
            result_embed.add_field(name='Relic Count: ', value=relics)  
            await ctx.send(embed=result_embed)
            await asyncio.sleep(20)
            await ctx.message.delete()
        else:
            msg = await ctx.send("Invalid options, the format is !result enemy ws_type relic-count")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()

    @commands.command(help="Shows the past n WS and their outcomes")
    async def results(self, ctx, amount=10):
        msg = []
        db = sqlite3.connect('results.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM main")
        results = cursor.fetchall()
        if(len(results) < amount):
            amount = len(results)
        results = results[::-1]
        results = results[:int(amount)]
        msg.append(await ctx.send(f"Here are the past {amount} WS and their outcomes:"))
        total_text = ""
        for result in results:
            for text in result:
                total_text += text + " "
            total_text += '\n'
        msg = await ctx.send(total_text)
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()
        

            

        






 
def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')
