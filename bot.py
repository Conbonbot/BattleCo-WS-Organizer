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
            user_id TEXT,
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
    if(ctx.content.find('I need the "Manage roles" permission for the `rs` command to work.') != -1):
        await ctx.delete()
    await bot.process_commands(ctx)


def add(queue, user):
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    sql = "SELECT nickname FROM main WHERE nickname=?"
    cursor.execute(sql, [(user.display_name)])
    result = cursor.fetchall()
    if len(result) == 0: # Person wasn't found in database, add them to the rs queue
        sql = "INSERT INTO main(user_id, nickname, level) VALUES(?,?,?)"
        val = (user.id, user.display_name, queue)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return True
    else: # Person was found in another RS queue
        return False


def queue_status(level):
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    sql = "SELECT user_id FROM main WHERE level=?"
    cursor.execute(sql, [(level)])
    people = cursor.fetchall()
    count = 0
    for person in people:
        count += 1
    return count
    

def print_people(level, user):
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    sql = "SELECT user_id FROM main WHERE level=?"
    cursor.execute(sql, [(level)])
    people = cursor.fetchall()
    discord_people = []
    for person in people:
        discord_people.append(user.guild.get_member(int(person[0])))
    return discord_people


@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    if str(user) != "Oxyg3n's WS and RS Organizer#7677" and str(reaction.message.author) == "Oxyg3n's WS and RS Organizer#7677":
        rs_pings = {
            "RS6" : "<@&710466154149314572>",
            "RS7" : "<@&712351336766636182>",
            "RS8" : "<@&712351461224218664>",
            "RS9" : "<@&719383035602272306>",
            "RS10" : "<@&795056815091089409>",
            "TEST" : "<@&795056080123330610>"
        }
        rs_queue = 6 if (emoji == "6️⃣") else 7 if emoji == "7️⃣" else 8 if emoji == "8️⃣" else 9 if emoji == "9️⃣" else 10 if emoji == "🔟" else -1 if emoji == "❌" else 0
        if(rs_queue != 0 and rs_queue != -1): # Add person to respective queue
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            status = queue_status(rs_queue)
            print(rs_level, rs_queue)
            if(rs_level >= rs_queue and add(rs_queue, user)):
                if(queue_status(rs_queue) < 4):
                    await reaction.message.channel.send(f'{rs_pings[f"RS{rs_queue}"]} ({queue_status(rs_queue)}/4) {user.mention} joined.')
                else:
                    people = print_people(rs_queue, user)
                    await reaction.message.channel.send(f"RS{rs_queue} Ready! {people[0].mention}, {people[1].mention}, {people[2].mention}, {people[3].mention}")
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    sql = "DELETE FROM main WHERE level=?"
                    cursor.execute(sql, [(rs_queue)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= rs_queue):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS{rs_queue} queue 😡")
        elif(rs_queue == -1): # Remove them from any queues
            db = sqlite3.connect('rsqueue.sqlite')
            cursor = db.cursor()
            sql = "SELECT level FROM main WHERE nickname=?"
            cursor.execute(sql, [(user.display_name)])
            result = cursor.fetchall()
            if len(result) == 0: 
                await reaction.message.channel.send("You are not in any rosters, use !rs or !q to join a roster")
            else:
                sql = "DELETE FROM main WHERE nickname=?"
                cursor.execute(sql, [(user.display_name)])
                sql = "SELECT level FROM main WHERE level=?"
                cursor.execute(sql, [(result[0][0])])
                people = cursor.fetchall()
                try:
                    count = len(people[0])
                except:
                    count = 0
                await reaction.message.channel.send(f"{user.mention} has left RS{result[0][0]} ({count}/4)")
            db.commit()
            cursor.close()
            db.close()




intital_extensions = ['cogs.ws_planning', 'cogs.poll', 'cogs.medals', 'cogs.results', 'cogs.redstars']

if __name__ == '__main__':
    for extension in intital_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)






bot.run(TOKEN)