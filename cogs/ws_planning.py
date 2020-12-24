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


class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot

    


    # Test role addition
    @commands.command(pass_context=True)
    async def addrole(self, ctx):
        member = ctx.message.author
        role = get(member.guild.roles, name="Bot Testing Role")
        await member.add_roles(role)

    # Testing stuff
    @commands.command()
    async def check(self, ctx):
        await ctx.send(ctx.author.display_name)
    
    @commands.command(aliases=['in', 'i'], help="Type !in (yes I know it says !_in but !in works) followed by either a 1 or a 2 to join a roster")
    async def _in(self, ctx, message=None):
        print(ctx, message)
        print(ctx.author.display_name)
        if(message == None):
            message = '1'
        if (message == '1') or (message == '2'):
            member = ctx.message.author
            role = get(member.guild.roles, name="WS_Squad_1")
            await member.add_roles(role)
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT nickname FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.display_name)])
            result = cursor.fetchall()
            user_name = ctx.author.mention
            user_nickname = ctx.author.display_name
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


    @commands.command(help="Add a user with this command")
    async def add(self, ctx, name, roster=None):
        if roster == None:
            roster = '1'
        if (roster == '1') or (roster == '2'):
            nicknames = []
            names = []
            for member in ctx.guild.members:
                if(str(member.display_name).lower().find(name) != -1):
                    names.append(member.mention)
                    nicknames.append(member.nick)
            if(len(nicknames) != 1):
                await ctx.send(f"Too many/no people found with {name} in their name")
            else:
                user_nickname = nicknames[0]
                user_name = names[0]
                db = sqlite3.connect('roster.sqlite')
                cursor = db.cursor()
                sql = "SELECT nickname FROM main WHERE nickname=?"
                cursor.execute(sql, [(user_nickname)])
                result = cursor.fetchall()
                if len(result) == 0:
                    sql = ("INSERT INTO main(name, nickname, roster) VALUES(?,?,?)")
                    val = (user_name, user_nickname, roster)
                    cursor.execute(sql,val)
                    sql = "SELECT nickname FROM main WHERE roster = ?"
                    cursor.execute(sql, roster)
                    results = cursor.fetchall()
                    if len(results) != 0:
                        people = []
                        for result in results:
                            result = str(result)
                            result = result[2:]
                            result = result[:len(result)-3]
                            people.append(result)
                        roster_embed = discord.Embed(
                            description = (f'The current roster for WS Roster #{roster}'),
                            colour = discord.Colour.teal()
                        )
                        roster_embed.set_footer(text='Best of luck on this WS!')
                        number = 1
                        for person in people:
                            roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                            number += 1
                        embed_msg = await ctx.send(embed=roster_embed)
                        msg = await ctx.send(f"{user_name} has been added to WS Roster #{roster}")
                else:
                    msg = await ctx.send(f"{user_name} is already in a WS Roster")
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

    @commands.command(help="Removes a person from a roster")
    async def remove(self, ctx, name, roster=None):
        if roster == None:
            roster = '1'
        if (roster == '1') or (roster == '2'):
            nicknames = []
            names = []
            for member in ctx.guild.members:
                if(str(member.display_name).lower().find(name) != -1):
                    names.append(member.mention)
                    nicknames.append(member.display_name)
            if(len(nicknames) != 1):
                await ctx.send(f"Too many/no people found with {name} in their name")
            else:
                user_nickname = nicknames[0]
                user_name = names[0]
                db = sqlite3.connect('roster.sqlite')
                cursor = db.cursor()
                sql = "SELECT nickname FROM main WHERE nickname=?"
                cursor.execute(sql, [(user_nickname)])
                result = cursor.fetchall()
                print(result)
                if(len(result) == 1):
                    sql = "DELETE FROM main WHERE nickname=?"
                    cursor.execute(sql, [(user_nickname)])
                    db.commit()
                    cursor.close()
                    db.close()
                    msg = await ctx.send(f"{user_nickname} has been removed from the WS Roster")
                else:
                    msg = await ctx.send(f"{user_nickname} wasn't found on the roster")
        else:
            msg = await ctx.send("Invalid roster selection, it can either be a 1 or 2")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

    

    

        
    @commands.command(aliases=['o'], help="Use this command (!out) to leave a roster")
    async def out(self, ctx):
        member = ctx.message.author
        role = get(member.guild.roles, name="WS_Squad_1")
        await member.remove_roles(role)
        db = sqlite3.connect('roster.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(ctx.author.display_name)])
        result = cursor.fetchall()
        if len(result) == 0:
            msg = await ctx.send("You are not in any WS Rosters")
        else:
            sql = "DELETE FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.display_name)])
            db.commit()
            cursor.close()
            db.close()
            msg = await ctx.send("You have been removed from the WS Roster")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

  
        
    @commands.command(aliases=['r'], help="Use this command (!roster) followed by either a 1 or a 2 to see who is in that WS Roster")
    async def roster(self, ctx, message=None):
        msg = []
        if(message == None):
            message = '1'
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT nickname FROM main WHERE roster = ?"
            cursor.execute(sql, message)
            results = cursor.fetchall()
            if len(results) != 0:
                people = []
                msg.append(await ctx.send(f'The current roster for WS Roster #{message}'))
                for result in results:
                    result = str(result)
                    result = result[2:]
                    result = result[:len(result)-3]
                    people.append(result)

                #roster_embed = discord.Embed(
                #    description = (f'The current roster for WS Roster #{message}'),
                #    colour = discord.Colour.teal()
                #)
                #roster_embed.set_footer(text='Best of luck on this WS!')
                number = 1
                stuff = ""
                for person in people:
                    #roster_embed.add_field(name=f'Player #{number}', value=f'{person}', inline=False)
                    stuff += (f'{number}. {person}')
                    stuff += "\n"
                    #await ctx.send(f'{number}. {person}')
                    number += 1
                msg.append(await ctx.send(stuff))
                #await ctx.send(embed=roster_embed)
            else:
                msg.append(await ctx.send(f"Nobody is in WS Roster #{message}, type !in {message} to join the roster"))
        else:
            msg.append(await ctx.send("Invalid roster, it can either be 1 or 2"))
        await asyncio.sleep(1800)
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()

    @commands.command(help="Use this command to clear the WS Queue, to start the WS")
    async def start(self, ctx, message, confirm=None):
        msg = []
        if (message == '1') or (message == '2'):
            db = sqlite3.connect('roster.sqlite')
            cursor = db.cursor()
            sql = "SELECT roster FROM main WHERE roster=?"
            cursor.execute(sql, message)
            results = cursor.fetchall()
            print(results)
            if (len(results) != 0):
                if(len(results) % 5 == 0) and (len(results) < 16):
                    sql = "DELETE FROM main WHERE roster=?"
                    cursor.execute(sql, message)
                    db.commit()
                    cursor.close()
                    db.close()
                    msg.append(await ctx.send(f"The WS roster #{message} has been cleared, best of luck!"))
                elif(confirm == 'clear'):
                    sql = "DELETE FROM main WHERE roster=?"
                    cursor.execute(sql, message)
                    db.commit()
                    cursor.close()
                    db.close()
                    msg.append(await ctx.send(f"The WS roster #{message} has been cleared, best of luck!"))
                else:
                    msg.append(await ctx.send(f"The WS Roster #{message} doesn't have 5, 10, or 15, people. However, you can override this by adding clear to this command"))
            else:
                msg.append(await ctx.send(f"There is nobody in WS Roster #{message}"))
        else:
            msg.append(await ctx.send("There are only two rosters, so use !start 1 or !start 2"))
        await asyncio.sleep(20)
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()


    @commands.command(help="Displays a person(s) on this server")
    async def user(self, ctx, name):
        names = []
        msg = []
        for member in ctx.guild.members:
            if(member.name.lower().find(name.lower()) != -1):
                names.append(member.display_name)
        if(len(names) == 0):
            msg.append(await ctx.send(f"No users found with {name} in their name"))
        else:
            msg.append(await ctx.send(f"**Here are the users that have {name} in their name:**"))
            msg.append(await ctx.send(",  ".join(names)))
        await asyncio.sleep(20 + len(names))
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()

    
    @commands.command(invoke_without_command=True, help="Displays everyone in a role")
    async def role(self, ctx, *roles):
        msg = []
        str_role = ""
        for role in roles:
            str_role += role
        print(str_role)
        people = []
        possible_roles = []
        for total_role in ctx.guild.roles:
            #print(total_role)
            if(str(total_role).lower().find(str_role.lower()) != -1):
                possible_roles.append(total_role)
        if(len(possible_roles) != 0):
            final_messages = []
            for ind_role in possible_roles:
                person = []
                for member in ctx.guild.members:
                    if(str(member.roles).find(str(ind_role)) != -1):
                        person.append(member.display_name)
                people = ",  ".join(person)
                message = f"```Here is who has the {ind_role} role: \n"
                final_message = message + people + "```\n"
                final_messages.append(final_message)
            message = "".join(final_messages)
            msg.append(await ctx.send(message))
        else:
            msg.append(await ctx.send(f"Nobody has the {str_role} role"))
        await asyncio.sleep(20 + len(people))
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()
    

                    





 
def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')