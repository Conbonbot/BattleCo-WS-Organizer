import os
import random
from discord import user
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands, tasks
import discord
import requests
import asyncio
import numpy as np
from discord.utils import get
from discord import client
import time

class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.check_people.start()


    # This executes an sql command to a database
    def sql_command(self, sql, val, data='rsqueue.sqlite'):
        db = sqlite3.connect(data)
        cursor = db.cursor()
        cursor.execute(sql, val)
        results = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        return results
    
    # This returns how many minutes a person has been in a queue
    def time(self, user_id, level):
        print(f"Running the time command. User ID: {user_id}, level: {level}")
        db = sqlite3.connect("rsqueue.sqlite")
        cursor = db.cursor()
        sql = "SELECT time FROM main WHERE user_id=? AND level=?"
        val = (user_id, level)
        cursor.execute(sql, val)
        person = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        print("Results from the database: ", person)
        for p in person:
            return int((time.time() - int(p))/60)

    # This returns how many people are in a current RS queue
    def amount(self, level):
        people = self.sql_command("SELECT amount FROM main WHERE level=?", [(level)])
        count = 0
        counting = []
        for person in people:
            counting.append(person[0])
            count += int(person[0])
        return count


    def cog_unload(self):
        self.check_people.cancel()

    @tasks.loop(minutes=1.0)
    async def check_people(self):
        print("AHHHH")
        # This command will run every minute, and check if someone has been in a queue for over n minutes
        db = sqlite3.connect('rsqueue.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT time, user_id, level FROM main")
        times = cursor.fetchall()
        print(times)
        for queue_time in times:
            #print(queue_time)
            #print(int(time.time()), queue_time[0], int(time.time())-queue_time[0], int((time.time()-queue_time[0])/60))
            minutes = int((time.time()-queue_time[0])/60)
            print(minutes)
            if(int(minutes) == 60):
                # Ping the user
                user = await self.bot.fetch_user(queue_time[1])
                channel = await self.bot.fetch_channel(542358024669495316)
                await channel.send(f"{user.mention}, still in for a RS{queue_time[2]}? Type !yes {queue_time[2]} to stay in the queue")
                pass
            elif(int(minutes) >= 60+3):
                self.sql_command("DELETE FROM main WHERE user_id=? AND level=?", (queue_time[1], queue_time[2]))
                user = await self.bot.fetch_user(queue_time[1])
                channel = await self.bot.fetch_channel(542358024669495316)
                await channel.send(f"{user.mention} has left RS{queue_time[2]} ({self.amount(queue_time[2])}/4)")
                pass
        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=["yes", "y"])
    async def confirm(self, ctx, level):
        self.sql_command("UPDATE main SET time=? WHERE user_id=? AND level=?", (int(time.time()), ctx.author.id, level))
        await ctx.send(f"{ctx.author.mention}, you are requed for a RS{level}! ({self.amount(level)}/4)")

    @commands.command(help="Use this command to join a rs queue by either typing in !rs to join your current rs level or !rs # to join a specific rs queue, and use !rs out or !rs o to leave a queue")
    async def rs(self, ctx, level=None):
        if(level is None): # Join their RS Scanners level queue
            user_id = ctx.author.id
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user_id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            # add them to the queue (if they aren't on one already)
            db = sqlite3.connect('rsqueue.sqlite')
            cursor = db.cursor()
            sql = "SELECT level FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.display_name)])
            result = cursor.fetchall()
            if len(result) == 0: # Person wasn't found in database, add them to the rs queue
                sql = "INSERT INTO main(time, user_id, nickname, level) VALUES(?,?,?,?)"
                val = (int(time.time()), ctx.author.id, ctx.author.display_name, rs_level)
                cursor.execute(sql, val)
                # print out the RS Queue
                sql = "SELECT user_id FROM main WHERE level=?"
                cursor.execute(sql, [(rs_level)])
                people = cursor.fetchall()
                count = 0
                people_mention = []
                print(people)
                for person in people:
                    people_mention.append(ctx.guild.get_member(int(person[0])))
                    count += 1
                if(count != 4):
                    rs_pings = {
                        "RS6" : "<@&710466154149314572>",
                        "RS7" : "<@&712351336766636182>",
                        "RS8" : "<@&712351461224218664>",
                        "RS9" : "<@&719383035602272306>",
                        "RS10" : "<@&795056815091089409>",
                        "TEST" : "<@&795056080123330610>"
                    }
                    await ctx.send(f'{rs_pings[f"RS{rs_level}"]} ({count}/4) {ctx.author.mention} joined.')
                else:
                    await ctx.send(f"RS{rs_level} Ready! {people_mention[0].mention} {people_mention[1].mention} {people_mention[2].mention} {people_mention[3].mention}")
                    sql = "DELETE FROM main WHERE level=?"
                    cursor.execute(sql, [(rs_level)])
            else:
                await ctx.send(f"You are already in the RS{rs_level} Queue, use !rs o to leave the queue")
            db.commit()
            cursor.close()
            db.close()
        elif(level.isnumeric()): # Join their specified RS queue
            user_id = ctx.author.id
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user_id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            # Making sure their rs queue isn't higher than specified level
            if(int(level) > int(rs_level)):
                await ctx.send(f"You are currently RS{rs_level}, so you can't join a RS{level} queue")
            else:
                db = sqlite3.connect('rsqueue.sqlite')
                cursor = db.cursor()
                sql = "SELECT level FROM main WHERE nickname=?"
                cursor.execute(sql, [(ctx.author.display_name)])
                result = cursor.fetchall()
                if len(result) == 0: # They weren't found on any RS Queues, add them
                    sql = "INSERT INTO main(time, user_id, nickname, level) VALUES(?,?,?,?)"
                    val = (int(time.time()), ctx.author.id, ctx.author.display_name, level)
                    cursor.execute(sql, val)
                    # print out the RS Queue
                    sql = "SELECT user_id FROM main WHERE level=?"
                    cursor.execute(sql, [(level)])  
                    people = cursor.fetchall()
                    count = 0
                    people_mention = []
                    for person in people:
                        people_mention.append(ctx.guild.get_member(int(person[0])))
                        count += 1
                    if(count != 4):
                        rs_pings = {
                            "RS6" : "<@&710466154149314572>",
                            "RS7" : "<@&712351336766636182>",
                            "RS8" : "<@&712351461224218664>",
                            "RS9" : "<@&719383035602272306>",
                            "RS10" : "<@&795056815091089409>",
                            "TEST" : "<@&795056080123330610>"
                        }   
                        await ctx.send(f'{rs_pings[f"RS{level}"]} ({count}/4) {ctx.author.mention} joined.')
                    else:
                        await ctx.send(f"RS{level} Ready! {people_mention[0].mention} {people_mention[1].mention} {people_mention[2].mention} {people_mention[3].mention}")
                        sql = "DELETE FROM main WHERE level=?"
                        cursor.execute(sql, [(level)])
                else:
                    await ctx.send(f"You are already in a RS Queue, use !rs o to leave the queue")
                db.commit()
                cursor.close()
                db.close()
        else: # Leave a queue
            if(level == "o" or level == "out"):
                db = sqlite3.connect('rsqueue.sqlite')
                cursor = db.cursor()
                sql = "SELECT level FROM main WHERE nickname=?"
                cursor.execute(sql, [(ctx.author.display_name)])
                result = cursor.fetchall()
                print(result[0])
                print(result[0][0])
                if len(result) == 0: 
                    await ctx.send("You are not in any rosters, use !rs or !q to join a roster")
                else:
                    sql = "DELETE FROM main WHERE nickname=?"
                    cursor.execute(sql, [(ctx.author.display_name)])
                    sql = "SELECT level FROM main WHERE level=?"
                    cursor.execute(sql, [(result[0][0])])
                    people = cursor.fetchall()
                    try:
                        count = len(people[0])
                    except:
                        count = 0
                    await ctx.send(f"{ctx.author.mention} has left RS{result[0][0]} ({count}/4)")
                db.commit()
                cursor.close()
                db.close()
        
    @commands.command(help="force a queue to start")
    async def ready(self, ctx, level):
        print("hello")
        db = sqlite3.connect('rsqueue.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(ctx.author.display_name)])
        result = cursor.fetchall()
        print(result)
        if(result != []):
            sql = "SELECT user_id FROM main WHERE level=?"
            cursor.execute(sql, [(level)])
            people = cursor.fetchall()
            people_mention = []
            for person in people:
                people_mention.append(ctx.guild.get_member(int(person[0])))
            if(len(people_mention) == 1):
                await ctx.send(f"RS{level} Ready! {people_mention[0].mention}")
            elif(len(people_mention) == 2):
                await ctx.send(f"RS{level} Ready! {people_mention[0].mention} {people_mention[1].mention}")
            elif(len(people_mention) == 3):
                await ctx.send(f"RS{level} Ready! {people_mention[0].mention} {people_mention[1].mention} {people_mention[2].mention}")
            elif(len(people_mention) == 4):
                await ctx.send(f"RS{level} Ready! {people_mention[0].mention} {people_mention[1].mention} {people_mention[2].mention} {people_mention[3].mention}")
            sql = "DELETE FROM main WHERE level=?"
            cursor.execute(sql, [(level)])
        else:
            has_officer = False
            for role in ctx.author.roles:
                if(str(role) == "Officer"):
                    has_officer = True
            if(has_officer):
                sql = "DELETE FROM main WHERE level=?"
                cursor.execute(sql, [(level)])
                await ctx.send("Queue has been cleared")
            else:
                await ctx.send("You can't clear a queue you aren't in")
        db.commit()
        cursor.close()
        db.close()




    @commands.command(aliases=['q'], help="Use this command to see what queues are currently active and join one!")
    async def queue(self, ctx):
        db = sqlite3.connect('rsqueue.sqlite')
        cursor = db.cursor()
        queue_embed = discord.Embed(
            description = (f'The current Red Star queues'),
            colour = discord.Colour.red()
        )
        # Gets RS6-10 Queue data
        for level in range(6,11):
            sql = "SELECT nickname, user_id FROM main WHERE level=?"
            cursor.execute(sql, [(level)])
            people = cursor.fetchall()
            count = 0
            list_people = []
            user_ids = []
            for person in people:
                print(person)
                list_people.append(person[0])
                user_ids.append((await ctx.guild.fetch_member(person[1])).id)
            str_person = ""
            for i in range(len(list_people)):
                str_person += list_people[i] + " 🕒 " + str(self.time(user_ids[i], level)) + "m, "
            str_person = str_person[:-2]
            print(f"RS{level}", str_person, len(list_people))
            if(len(list_people) != 0):
                queue_embed.add_field(name=f"RS{level} Queue ({len(list_people)}/4)", value=str_person, inline=False)
        # Throw everything in an embed and call it a day
        queue_embed.add_field(name="React below to join a Red Star queue (and ❌ to leave a queue)", value="Queues: 6️⃣, 7️⃣, 8️⃣, 9️⃣, 🔟, ❌")
        message = await ctx.send(embed=queue_embed)
        emojis = ['6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '❌']
        for emoji in emojis:
            await message.add_reaction(emoji)
        
    


def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('Redstars loaded')