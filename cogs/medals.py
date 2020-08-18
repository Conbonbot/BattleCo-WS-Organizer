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

    @commands.command(help="Awards medals to an entire group of people")
    @commands.has_role(744995362380578817)
    async def award_group(self, ctx, medal, *group):
        correct = False
        if(len(group) > 1):
            group = " ".join(group)
        group = str(group)
        group = group.strip("<>")
        group = group.strip("@")
        group = group.strip("&")
        possible_roles = []
        for total_role in ctx.guild.roles:
            if(str(total_role).lower().find(group) != -1):
                possible_roles.append(total_role)
        if(len(possible_roles) == 1):
            correct = True
            print(possible_roles)
        else:
            if(len(possible_roles) > 1):
                msg = await ctx.send("There are too many roles with that name")
            else:
                msg = await ctx.send("There are no roles with that name")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
        if(correct):
            if(medal == "victor" or medal == "riser" or medal == "destined" or medal == "strategist"):
                members = []
                print(possible_roles[0])
                for member in ctx.guild.members:
                    if(str(member.roles).find(str(possible_roles[0])) != -1):
                        members.append(member.name)
                print(members)
                for player in members:
                    db = sqlite3.connect('medals.sqlite')
                    cursor = db.cursor()
                    sql = "SELECT nickname FROM main WHERE nickname=?"
                    cursor.execute(sql, [(player)])
                    results = cursor.fetchall()
                    print(results)
                    if (len(results) == 0): # This means they don't have any awards
                        if(medal == "victor"):
                            sql = "INSERT INTO main(nickname,victor) VALUES(?,?)"
                        elif(medal == "early"):
                            sql = "INSERT INTO main(nickname,riser) VALUES(?,?)" 
                        elif(medal == "destined"):
                            sql = "INSERT INTO main(nickname,destined) VALUES(?,?)"
                        elif(medal == "strategist"):
                            sql = "INSERT INTO main(nickname,destined) VALUES(?,?)"
                        val = (player, 1)
                        cursor.execute(sql,val)
                        amount = 1
                    else:
                        if(medal == "victor"):
                            sql = "SELECT victor FROM main WHERE nickname=?"
                        elif(medal == "riser"):
                            sql = "SELECT riser from main WHERE nickname=?"
                        elif(medal == "destined"):
                            sql = "SELECT destined from main WHERE nickname=?"
                        elif(medal == "strategist"):
                            sql = "SELECT strategist from main WHERE nickname=?"
                        val = [(player)]
                        cursor.execute(sql,val)
                        amount = cursor.fetchone()
                        amount = str(amount)
                        amount = amount[1:-2]
                        if(amount == 'None'): # They have awards, but not this one
                            if(medal == "victor"):
                                sql = "UPDATE main SET victor=? WHERE nickname=?"
                            elif(medal == "riser"):
                                sql = "UPDATE main SET riser=? WHERE nickname=?"
                            elif(medal == "destined"):
                                sql = "UPDATE main SET destined=? WHERE nickname=?"
                            elif(medal == "strategist"):
                                sql = "UPDATE main SET strategist=? WHERE nickname=?"
                            val = (1, player)
                            amount = 1
                            cursor.execute(sql,val)
                        else: # They have awards, including the one specified by medal
                            if(medal == "victor"):
                                sql = "UPDATE main SET victor=? WHERE nickname=?"
                            elif(medal == "riser"):
                                sql = "UPDATE main SET riser=? WHERE nickname=?"
                            elif(medal == "destined"):
                                sql = "UPDATE main SET destined=? WHERE nickname=?"
                            elif(medal == "strategist"):
                                sql = "UPDATE main SET strategist=? WHERE nickname=?"
                            val = (int(amount)+1, player)
                            cursor.execute(sql,val) 
                            amount = int(amount)+1
                    db.commit()
                    cursor.close()
                    db.close()
                    final_messages = ""
                    final_messages += (f":tada::tada: Congratulations {player}! :tada::tada:\n")
                    if(medal == "victor"):
                        final_messages += (f"You have won the White Star! Here is a trophy for your accomplishments :trophy:\n")
                        if(int(amount) > 10):
                            final_messages += (f"You have {amount} trophies for winning White Stars! That's actually incredible, you are a master of White Stars!")
                        if(int(amount) > 1):
                            final_messages += (f"You have {amount} trophies for winning White Stars! Hope they are in a good spot")
                        else:
                            final_messages += (f"This is your first trophy for winning a White Star! Put it in a good place (:")
                    elif(medal == "riser"):
                        final_messages += (f"SLEEP IS FOR THE WEAK!!!\nHere is your Early Riser medal :military_medal:\n")
                        final_messages += (f"You decided that a White Star is more important than sleep, and because of your actions the White Star was won!\n")
                        if(int(amount) > 10):
                            final_messages += (f"You have {amount} Early Riser medals. That's some SERIOUS dedication to White Stars! You are now an officer of the No Sleep club")
                        if(int(amount) > 1):
                            final_messages += (f"You have {amount} Early Riser medals. You are now a Senior Member in the No Sleep club!")
                        else:
                            final_messages += (f"This is your first Early Riser medal. Welcome to the No Sleep club!")
                    elif(medal == "destined"):
                        final_messages += (f"Sometimes you have to lose something to get something of greater value\n")
                        final_messages += (f"You threw your transport straight into an enemy planet and exploded them with destiny\n")
                        final_messages += (f"Here is your Destined medal :medal:\n")
                        if(int(amount) > 10):
                            final_messages += (f"You have {amount} Destined medals!!! That's some dedication to exploding transports")
                        if(int(amount) > 1):
                            final_messages += (f"You have {amount} Destined medals!!! Certainly a pyromanic!")
                        else:
                            final_messages += (f"This is your first Destined medal! Wear it with honor")
                    elif(medal == "strategist"):
                        final_messages += (f"Whether on or off the the WS, they provided exceptional help and input with a WS match")
                        final_messages += (f"Here is your Strategist medal :military_medal:")
                        if(int(amount) > 1):
                            final_messages += (f"You have {amount} Strategist medals!!! That's some dedication to be one of the brains behind the WS!!")
                        else:
                            final_messages += (f"You have {amount} Strategist medals!!! Wear it with honor Captain.")
                    await ctx.send(final_messages)
                await asyncio.sleep(60)
                await ctx.message.delete()
                    
                





    @commands.command(help="Awards a medal, use the !award <pinged user> medal_name")
    @commands.has_role(744995362380578817)
    async def award(self, ctx, medal, player):
        correct = False
        names = []
        for member in ctx.guild.members:
            if(str(member.name).lower().find(player) != -1):
                names.append(member.name)
        if(len(names) == 1):
            for name in names:
                player = name
            correct = True
        else:
            if(len(names) > 1):
                msg = await ctx.send("There are too many players with that name")
            else:
                msg = await ctx.send("There are no players with that name")
            await asyncio.sleep(20)
            await ctx.message.delete()
            await msg.delete()
        msg = []
        if(correct):
            if(medal == "victor" or medal == "riser" or medal == "destined" or medal == "strategist"):
                db = sqlite3.connect('medals.sqlite')
                cursor = db.cursor()
                sql = "SELECT nickname FROM main WHERE nickname=?"
                cursor.execute(sql, [(player)])
                results = cursor.fetchall()
                print(results)
                if (len(results) == 0): # This means they don't have any awards
                    if(medal == "victor"):
                        sql = "INSERT INTO main(nickname,victor) VALUES(?,?)"
                    elif(medal == "early"):
                        sql = "INSERT INTO main(nickname,riser) VALUES(?,?)" 
                    elif(medal == "destined"):
                        sql = "INSERT INTO main(nickname,destined) VALUES(?,?)"
                    elif(medal == "strategist"):
                        sql = "INSERT INTO main(nickname,destined) VALUES(?,?)"
                    val = (player, 1)
                    cursor.execute(sql,val)
                    amount = 1
                else:
                    if(medal == "victor"):
                        sql = "SELECT victor FROM main WHERE nickname=?"
                    elif(medal == "riser"):
                        sql = "SELECT riser from main WHERE nickname=?"
                    elif(medal == "destined"):
                        sql = "SELECT destined from main WHERE nickname=?"
                    elif(medal == "strategist"):
                        sql = "SELECT strategist from main WHERE nickname=?"
                    val = [(player)]
                    cursor.execute(sql,val)
                    amount = cursor.fetchone()
                    amount = str(amount)
                    amount = amount[1:-2]
                    if(amount == 'None'): # They have awards, but not this one
                        if(medal == "victor"):
                            sql = "UPDATE main SET victor=? WHERE nickname=?"
                        elif(medal == "riser"):
                            sql = "UPDATE main SET riser=? WHERE nickname=?"
                        elif(medal == "destined"):
                            sql = "UPDATE main SET destined=? WHERE nickname=?"
                        elif(medal == "strategist"):
                            sql = "UPDATE main SET strategist=? WHERE nickname=?"
                        val = (1, player)
                        amount = 1
                        cursor.execute(sql,val)
                    else: # They have awards, including the one specified by medal
                        if(medal == "victor"):
                            sql = "UPDATE main SET victor=? WHERE nickname=?"
                        elif(medal == "riser"):
                            sql = "UPDATE main SET riser=? WHERE nickname=?"
                        elif(medal == "destined"):
                            sql = "UPDATE main SET destined=? WHERE nickname=?"
                        elif(medal == "strategist"):
                            sql = "UPDATE main SET strategist=? WHERE nickname=?"
                        val = (int(amount)+1, player)
                        cursor.execute(sql,val) 
                        amount = int(amount)+1
                db.commit()
                cursor.close()
                db.close()
                final_messages = ""
                final_messages += (f":tada::tada: Congratulations {player}! :tada::tada:\n")
                if(medal == "victor"):
                    final_messages += (f"You have won the White Star! Here is a trophy for your accomplishments :trophy:\n")
                    if(int(amount) > 10):
                        final_messages += (f"You have {amount} trophies for winning White Stars! That's actually incredible, you are a master of White Stars!")
                    if(int(amount) > 1):
                        final_messages += (f"You have {amount} trophies for winning White Stars! Hope they are in a good spot")
                    else:
                        final_messages += (f"This is your first trophy for winning a White Star! Put it in a good place (:")
                elif(medal == "riser"):
                    final_messages += (f"SLEEP IS FOR THE WEAK!!!\nHere is your Early Riser medal :military_medal:\n")
                    final_messages += (f"You decided that a White Star is more important than sleep, and because of your actions the White Star was won!\n")
                    if(int(amount) > 10):
                        final_messages += (f"You have {amount} Early Riser medals. That's some SERIOUS dedication to White Stars! You are now an officer of the No Sleep club")
                    if(int(amount) > 1):
                        final_messages += (f"You have {amount} Early Riser medals. You are now a Senior Member in the No Sleep club!")
                    else:
                        final_messages += (f"This is your first Early Riser medal. Welcome to the No Sleep club!")
                elif(medal == "destined"):
                    final_messages += (f"Sometimes you have to lose something to get something of greater value\n")
                    final_messages += (f"You threw your transport straight into an enemy planet and exploded them with destiny\n")
                    final_messages += (f"Here is your Destined medal :medal:\n")
                    if(int(amount) > 10):
                        final_messages += (f"You have {amount} Destined medals!!! That's some dedication to exploding transports")
                    if(int(amount) > 1):
                        final_messages += (f"You have {amount} Destined medals!!! Certainly a pyromanic!")
                    else:
                        final_messages += (f"This is your first Destined medal! Wear it with honor")
                await ctx.send(final_messages)
            else:
                msg = await ctx.send("Incorrect Medal")
                await asyncio.sleep(20)
                await ctx.message.delete()
                await msg.delete()
        


    @commands.command(help="Displays a person(s) on this server")
    async def user_find(self, ctx, name):
        names = []
        msg = []
        for member in ctx.guild.members:
            if(str(member.name).find(name) != -1):
                names.append(member.name)
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
    async def role_find(self, ctx, *role):
        msg = []
        if(len(role) == 1):
            role = str(role)
            role = role[2:-3]
        else:
            role = " ".join(role)
        people = []
        role = role.strip("<>")
        role = role.strip("@")
        role = role.strip("&")
        possible_roles = []
        for total_role in ctx.guild.roles:
            #print(total_role)
            if(str(total_role).lower().find(role) != -1):
                possible_roles.append(total_role)
        if(len(possible_roles) != 0):
            final_messages = []
            for ind_role in possible_roles:
                person = []
                for member in ctx.guild.members:
                    if(str(member.roles).find(str(ind_role)) != -1):
                        person.append(member.name)
                people = ",  ".join(person)
                message = f"```Here is who has the {ind_role} role: \n"
                final_message = message + people + "```\n"
                final_messages.append(final_message)
            message = "".join(final_messages)
            msg.append(await ctx.send(message))
        else:
            msg.append(await ctx.send(f"Nobody has the {role} role"))
        await asyncio.sleep(20 + len(people))
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()
    




        

        




def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')