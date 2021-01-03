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

def print_people(level):
    db = sqlite3.connect('rsqueue.sqlite')
    cursor = db.cursor()
    sql = "SELECT name FROM main WHERE level=?"
    cursor.execute(sql, [(level)])
    people = cursor.fetchall()
    str_people = ""
    for person in people:
        str_people += person + " "
        str_people += " "
    return str_people


@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji

    if str(user) != "Oxyg3n's WS Organizer#7677" and str(reaction.message.author) == "Oxyg3n's WS Organizer#7677":
        rs_pings = {
            "RS6" : "<@&710466154149314572>",
            "RS7" : "<@&712351336766636182>",
            "RS8" : "<@&712351461224218664>",
            "RS9" : "<@&719383035602272306>",
            "RS10" : "<@&795056815091089409>",
        }   
        if(emoji == "6️⃣"):
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            if(rs_level >= 6 and add(6, user)):
                if(queue_status(6) < 4): # MAKE SURE TO CHANGE TO BE ACTUAL RS PINGS
                    await reaction.message.channel.send(f'{rs_pings["RS6"]} ({queue_status(6)}/4) {user.mention} joined.')
                else:
                    await reaction.message.channel.send(f"RS9 Ready! {print_people(6)}")
                    sql = "DELETE FROM main WHERE level=?"
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    cursor.execute(sql, [(6)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= 6):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS6 queue 😡")
        elif(emoji == "7️⃣"):
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            if(rs_level >= 7 and add(7, user)):
                if(queue_status(7) < 4):
                    await reaction.message.channel.send(f'{rs_pings["RS7"]} ({queue_status(6)}/4) {user.mention} joined.')
                else:
                    await reaction.message.channel.send(f"RS9 Ready! {print_people(7)}")
                    sql = "DELETE FROM main WHERE level=?"
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    cursor.execute(sql, [(6)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= 7):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS7 queue 😡")
        elif(emoji == "8️⃣"):
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            if(rs_level >= 8 and add(8, user)):
                if(queue_status(8) < 4):
                    await reaction.message.channel.send(f'{rs_pings["RS8"]} ({queue_status(6)}/4) {user.mention} joined.')
                else:
                    await reaction.message.channel.send(f"RS9 Ready! {print_people(8)}")
                    sql = "DELETE FROM main WHERE level=?"
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    cursor.execute(sql, [(6)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= 8):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS8 queue 😡")
        elif(emoji == "9️⃣"):
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            if(rs_level >= 9 and add(9, user)):
                if(queue_status(9) < 4):
                    await reaction.message.channel.send(f'{rs_pings["RS9"]} ({queue_status(6)}/4) {user.mention} joined.')
                else:
                    await reaction.message.channel.send(f"RS9 Ready! {print_people(9)}")
                    sql = "DELETE FROM main WHERE level=?"
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    cursor.execute(sql, [(6)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= 9):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS9 queue 😡")
        elif(emoji == "🔟"):
            load_dotenv()
            api_request_str = os.getenv('API_KEY_REQUEST') + str(user.id)
            api_request = requests.get(api_request_str)
            total_info = api_request.json()
            rs_level = total_info["map"]["rs"]["level"]
            if(rs_level >= 10 and add(10, user)):
                if(queue_status(10) < 4):
                    await reaction.message.channel.send(f'{rs_pings["RS10"]} ({queue_status(6)}/4) {user.mention} joined.')
                else:
                    await reaction.message.channel.send(f"RS9 Ready! {print_people(10)}")
                    sql = "DELETE FROM main WHERE level=?"
                    db = sqlite3.connect('rsqueue.sqlite')
                    cursor = db.cursor()
                    cursor.execute(sql, [(6)])
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                if(rs_level >= 10):
                    await reaction.message.channel.send(f"{user.mention} you are already in a RS Queue, use !rs o to leave the queue")
                else:
                    await reaction.message.channel.send(f"{user.mention} your current RS level is {rs_level}, you can't join a RS10 queue 😡")



intital_extensions = ['cogs.moderation', 'cogs.ws_planning', 'cogs.poll', 'cogs.medals', 'cogs.results', 'cogs.redstars']

if __name__ == '__main__':
    for extension in intital_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)






bot.run(TOKEN)