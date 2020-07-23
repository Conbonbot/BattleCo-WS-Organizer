import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import requests
import asyncio

class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['in'], help="Type !in (yes I know it says !_in but !in works) followed by either a 1 or a 2 to join a roster")
    async def _in(self, ctx, message):
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT nickname FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            result = cursor.fetchall()
            user_name = ctx.author.mention
            user_nickname = ctx.author.name
            if len(result) == 0:
                sql = ("INSERT INTO main(name, nickname, roster) VALUES(?,?,?)")
                val = (user_name, user_nickname, message)
                cursor.execute(sql,val)
                sql = "SELECT nickname FROM main WHERE roster = ?"
                cursor.execute(sql, message)
                results = cursor.fetchall()
                if len(results) != 0:
                    people = []
                    for result in results:
                        result = str(result)
                        result = result[2:]
                        result = result[:len(result)-3]
                        people.append(result)
                    roster_embed = discord.Embed(
                        description = (f'The current roster for WS Roster #{message}'),
                        colour = discord.Colour.teal()
                    )
                    roster_embed.set_footer(text='Best of luck on this WS!')
                    number = 1
                    for person in people:
                        roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                        number += 1
                    embed_msg = await ctx.send(embed=roster_embed)
                    msg = await ctx.send(f"You have been added to WS Roster #{message}")
            else:
                msg = await ctx.send("You are already in a WS Roster, type !out to leave your current WS Roster")
            db.commit()
            cursor.close()
            db.close()
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
            await embed_msg.delete()
        else:
            msg = await ctx.send("Invalid roster selection, it can either be a 1 or 2")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
        
    @commands.command(help="Used to add people to the WS Roster (ping the user, then type their name)")
    async def manualadd(self, ctx, message, mention, name):
        print("HEllo")
        print(self, ctx, message, mention, name)
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT nickname FROM main WHERE nickname=?"
            cursor.execute(sql, [(name)])
            result = cursor.fetchall()
            user_name = mention
            user_nickname = name
            if len(result) == 0:
                sql = ("INSERT INTO main(name, nickname, roster) VALUES(?,?,?)")
                val = (user_name, user_nickname, message)
                cursor.execute(sql,val)
                sql = "SELECT nickname FROM main WHERE roster = ?"
                cursor.execute(sql, message)
                results = cursor.fetchall()
                if len(results) != 0:
                    people = []
                    for result in results:
                        result = str(result)
                        result = result[2:]
                        result = result[:len(result)-3]
                        people.append(result)
                    roster_embed = discord.Embed(
                        description = (f'The current roster for WS Roster #{message}'),
                        colour = discord.Colour.teal()
                    )
                    roster_embed.set_footer(text='Best of luck on this WS!')
                    number = 1
                    for person in people:
                        roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                        number += 1
                    embed_msg = await ctx.send(embed=roster_embed)
                    msg = await ctx.send(f"{user_nickname} has been added to WS Roster #{message}")
                else:
                    msg = await ctx.send("You are already in a WS Roster, type !out to leave your current WS Roster")
            else:
                msg = await ctx.send(f"{name} already exists in a WS Roster")
            db.commit()
            cursor.close()
            db.close()
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
            await embed_msg.delete()
        else:
            msg = await ctx.send("Invalid option, it can either be a 1 or a 2")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()

    

    

        
    @commands.command(help="Use this command (!out) to leave a roster")
    async def out(self, ctx):
        db = sqlite3.connect('roster.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(ctx.author.name)])
        result = cursor.fetchall()
        user_name = ctx.author.mention
        user_nickname = ctx.author.name
        if len(result) == 0:
            msg = await ctx.send("You are not in any WS Rosters")
        else:
            sql = "DELETE FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            db.commit()
            cursor.close()
            db.close()
            msg = await ctx.send("You have been removed from the WS Roster")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

    @commands.command(help="Use this command (!out) to leave a roster")
    async def manualout(self, ctx, mention, name):
        db = sqlite3.connect('roster.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(name)])
        result = cursor.fetchall()
        user_name = ctx.author.mention
        user_nickname = ctx.author.name
        if len(result) == 0:
            msg = await ctx.send(f"{name} is not in any WS Rosters")
        else:
            sql = "DELETE FROM main WHERE nickname=?"
            cursor.execute(sql, [(name)])
            db.commit()
            cursor.close()
            db.close()
            msg = await ctx.send(f"{name} has been removed from the WS Roster")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()
        
    @commands.command(help="Use this command (!roster) followed by either a 1 or a 2 to see who is in that WS Roster")
    async def roster(self, ctx, message):
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT nickname FROM main WHERE roster = ?"
            cursor.execute(sql, message)
            results = cursor.fetchall()
            if len(results) != 0:
                people = []
                for result in results:
                    result = str(result)
                    result = result[2:]
                    result = result[:len(result)-3]
                    people.append(result)
                roster_embed = discord.Embed(
                    description = (f'The current roster for WS Roster #{message}'),
                    colour = discord.Colour.teal()
                )
                roster_embed.set_footer(text='Best of luck on this WS!')
                number = 1
                for person in people:
                    roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                    number += 1
                msg = await ctx.send(embed=roster_embed)
            else:
                msg = await ctx.send(f"Nobody is in WS Roster #{message}, type !in {message} to join the roster")
        else:
            msg = await ctx.send("Invalid roster, it can either be 1 or 2")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

    @commands.command(help="Use this command to clear the WS Queue, to start the WS")
    async def start(self, ctx, message):
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT roster FROM main WHERE roster=?"
            cursor.execute(sql, message)
            results = cursor.fetchall()
            if (len(results) != 0):
                if(len(results) % 5 == 0) and (len(results) < 15):
                    sql = "DELETE FROM main WHERE roster=?"
                    cursor.execute(sql, message)
                    db.commit()
                    cursor.close()
                    db.close()
                    msg = await ctx.send(f"The WS roster #{message} has been cleared, best of luck!")
                else:
                    msg = await ctx.send("The roster doesn't have 5, 10, or 15 people in it")
            else:
                msg = await ctx.send(f"There is nobody in WS Roster #{message}")
        else:
            msg = await ctx.send("There are only two rosters, so use !start 1 or !start 2")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()
        # okay
        
                    





 
def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')