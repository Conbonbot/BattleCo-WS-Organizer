import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import requests

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
                        title = 'BattleCo WS Organizer',
                        description = (f'The current roster for WS Roster #{message}'),
                        colour = discord.Colour.teal()
                    )
                    roster_embed.set_footer(text='Best of luck on this WS!')
                    number = 1
                    for person in people:
                        roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                        number += 1
                    await ctx.send(embed=roster_embed)
                    await ctx.send(f"You have been added to WS Roster #{message}")
            else:
                await ctx.send("You are already in a WS Roster, type !out to leave your current WS Roster")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send("Invalid roster selection, it can either be a 1 or 2")

        
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
            await ctx.send("You are not in any WS Rosters")
        else:
            sql = "DELETE FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("You have been removed from the WS Roster")
        
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
                    title = 'BattleCo WS Organizer',
                    description = (f'The current roster for WS Roster #{message}'),
                    colour = discord.Colour.teal()
                )
                roster_embed.set_footer(text='Best of luck on this WS!')
                number = 1
                for person in people:
                    roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                    number += 1
                await ctx.send(embed=roster_embed)
            else:
                await ctx.send(f"Nobody is in WS Roster #{message}, type !in {message} to join the roster")
        else:
            await ctx.send("Invalid roster, it can either be 1 or 2")






def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')