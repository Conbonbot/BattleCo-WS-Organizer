import os
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

class BattleCoCogs(commands.Cog, name='BattleCo'):

    def __init__(self, bot):
        self.bot = bot


    
    
    


    # Ships
    @commands.command(help="Displays your current ships")
    async def ships(self, ctx):
        print(ctx.author.name, " has typed the !ships command")
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        bs_sql = "SELECT battleship FROM main WHERE nickname=?"
        cursor.execute(bs_sql, [(ctx.author.name)])
        bs_data_raw = cursor.fetchall()
        bs_data = str(bs_data_raw).strip('[]')
        bs_data = str(bs_data).strip('()')
        if (bs_data != 'None,'):
            bs_data = bs_data[1:]
            bs_data = bs_data[:len(bs_data)-2]
        else:
            bs_data = bs_data[:len(bs_data)-1]

        miner_sql = "SELECT miner FROM main WHERE nickname=?"
        cursor.execute(miner_sql, [(ctx.author.name)])
        miner_data_raw = cursor.fetchall()
        miner_data = str(miner_data_raw).strip('[]')
        miner_data = str(miner_data).strip('()')
        if (miner_data != 'None,'):
            miner_data = miner_data[1:]
            miner_data = miner_data[:len(miner_data)-2]
        else:
            miner_data = miner_data[:len(bs_data)-1]

        ts_sql = "SELECT transport FROM main WHERE nickname=?"
        cursor.execute(ts_sql, [(ctx.author.name)])
        ts_data_raw = cursor.fetchall()
        ts_data = str(ts_data_raw).strip('[]')
        ts_data = str(ts_data).strip('()')
        if (ts_data != 'None,'):
            ts_data = ts_data[1:]
            ts_data = ts_data[:len(ts_data)-2]
        else:
            ts_data = ts_data[:len(bs_data)-1]
        
        db.commit()
        cursor.close()
        db.close()

        embed = discord.Embed(
            colour = discord.Colour.blue()
        )
        embed.set_author(name=ctx.author.name)
        embed.add_field(name='Battleship', value=f'{bs_data}', inline=True)
        embed.add_field(name='Miner', value=f'{miner_data}', inline=True)
        embed.add_field(name='Transport', value=f'{ts_data}', inline=True)

        msg = await ctx.send(embed=embed)

        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()


    # Finds a players ships
    @commands.command(help="Finds a players ships based off their name (ping the user)")
    async def find_ship(self, ctx, player):
        print(ctx.author.name, " has typed the !find_ship command")
        player = player.replace('!', '')
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        sql = "SELECT name FROM main WHERE name=?"
        cursor.execute(sql, [(player)])
        result = cursor.fetchall()
        if len(result) == 1: # A match has been found
            player_sql = "SELECT nickname FROM main WHERE name=?"
            cursor.execute(player_sql, [(player)])
            player_name_raw = cursor.fetchone()
            player_name = str(player_name_raw)
            player_name = player_name.strip('()')
            player_name = player_name[1:]
            player_name = player_name[:len(player_name)-2]
            bs_sql = "SELECT battleship FROM main WHERE name=?"
            cursor.execute(bs_sql, [(player)])
            bs_data_raw = cursor.fetchall()
            bs_data = str(bs_data_raw).strip('[]')
            bs_data = str(bs_data).strip('()')
            if (bs_data != 'None,'):
                bs_data = bs_data[1:]
                bs_data = bs_data[:len(bs_data)-2]
            else:
                bs_data = bs_data[:len(bs_data)-1]

            miner_sql = "SELECT miner FROM main WHERE name=?"
            cursor.execute(miner_sql, [(player)])
            miner_data_raw = cursor.fetchall()
            miner_data = str(miner_data_raw).strip('[]')
            miner_data = str(miner_data).strip('()')
            if (miner_data != 'None,'):
                miner_data = miner_data[1:]
                miner_data = miner_data[:len(miner_data)-2]
            else:
                miner_data = miner_data[:len(miner_data)-1]

            ts_sql = "SELECT transport FROM main WHERE name=?"
            cursor.execute(ts_sql, [(player)])
            ts_data_raw = cursor.fetchall()
            ts_data = str(ts_data_raw).strip('[]')
            ts_data = str(ts_data).strip('()')
            if (ts_data != 'None,'):
                ts_data = ts_data[1:]
                ts_data = ts_data[:len(ts_data)-2]
            else:
                ts_data = ts_data[:len(ts_data)-1]
            
            db.commit()
            cursor.close()
            db.close()
            # Shows an embed of the data

            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name=player_name)
            embed.add_field(name='Battleship', value=f'{bs_data}', inline=True)
            embed.add_field(name='Miner', value=f'{miner_data}', inline=True)
            embed.add_field(name='Transport', value=f'{ts_data}', inline=True)

            msg = await ctx.send(embed=embed)
        else:
            msg = await ctx.send("Player not found")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

    
    @commands.command(help="Displays the mod list from the API")
    async def modlist(self, ctx):
        print(ctx.author.name, " has typed the !modlist command")
        modlist_embed = discord.Embed(
            descripion = "Mod List",
            colour = discord.Colour.dark_grey()
        )
        modlist_embed.add_field(name="Trade mods", value = "cargobay, computer, rush, tradeburst, shipdrone, offload, beam, entrust, recall, dispatch", inline=True)
        modlist_embed.add_field(name="Mining mods", value = "miningboost, hydrobay, enrich, remote, hydroupload, miningunity, crunch, genesis, minedrone, hydrorocket", inline=True)
        modlist_embed.add_field(name="Weapon mods", value = "battery, laser, mass, dual, barrage, dart", inline=False)
        modlist_embed.add_field(name="Shield mods", value = "alpha, delta, passive, omega, mirror, blast, area", inline=True)
        modlist_embed.add_field(name="Support mods", value = "emp, teleport, rsextender, repair, warp, unity, sanctuary, stealth, fortify, impulse, rocket, salvage, suppress, destiny, barrier, vengeance, deltarocket, leap, bond, alphadrone, omegarocket, suspend, remotebomb", inline=False)
        msg = await ctx.send(embed=modlist_embed)
        full_mods_raw = "cargobay computer rush tradeburst shipdrone offload beam entrust recall dispatch miningboost hydrobay enrich remote hydroupload miningunity crunch genesis minedrone hydrorocket battery laser mass dual barrage dart alpha delta passive omega mirror blast area emp teleport rsextender repair warp unity sanctuary stealth fortify impulse rocket salvage suppress destiny barrier vengeance deltarocket leap bond alphadrone omegarocket suspend remotebomb"
        full_mods_str = full_mods_raw.strip(',')
        full_mods = full_mods_str.split(" ")
        print(full_mods)
        await asyncio.sleep(80)
        await ctx.message.delete()
        await msg.delete()


    @commands.group(invoke_without_command=True, help="Add, edit, show, and delete ships, type !ws for more details")
    async def ws(self, ctx):
        print(ctx.author.name, " has typed the !ws command")
        ws_embed = discord.Embed(
            description = 'WS Setup Commands',
            colour = discord.Colour.green()
        )
        ws_embed.set_footer(text='Example: !ws add bs battery omega teleport repair warp rocket \nExample: !ws show miner')
        ws_embed.set_author(name=ctx.author)
        ws_embed.add_field(name='Add Ship', value='!ws add bs (example)', inline=True)
        ws_embed.add_field(name='Show Ship', value='!ws show miner (example)', inline=True)
        ws_embed.add_field(name='Delete Ship', value='!ws delete ts (example)', inline=True)
        ws_embed.add_field(name='Next Steps', value='for adding (use can use the add command to edit your ships) ships, add the mods (use the !modlist command for a list of mods because the API is weird) listed on your ship (just list the mod, the Hades Star Compendium Bot will fill the level), but for show and delete, just enter the name of the ship you want to see/delete', inline=False)
        msg = await ctx.send(embed=ws_embed)
        await asyncio.sleep(80)
        await ctx.message.delete()
        await msg.delete()
        

    @ws.command(help="Adds/edits a ship to a players WS fleet")
    async def add(self, ctx, tag, *mods):
        msg = []
        user_id_raw = ctx.author.mention
        user_id = str(user_id_raw).strip('<>')
        user_id = user_id[1:]
        user_id = user_id.strip('!')
        api_request_str = 'https://bot.hs-compendium.com/compendium/api/tech?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIzODQ0ODExNTE0NzUxMjIxNzkiLCJndWlsZElkIjoiMzkzMTQ5NjIxNDYwOTI2NDY0IiwiaWF0IjoxNTk0MjYzMDU2LCJleHAiOjE2MjU4MjA2NTYsInN1YiI6ImFwaSJ9.pokmGiqTNIz0VztPrXhvM_xofWzuOYO1DSA2zTwP01s&userid=' + user_id
        #print(api_request_str)
        api_request = requests.get(api_request_str)
        full_text = api_request.text
        correct_mods = True
        if(tag == "bs"):
            bs_level = full_text.find("bs\":{\"level\":")
            bs_mod_level = full_text[bs_level + len("bs\":{\"level\":"): bs_level + len("bs\":{\"level\":") + 1]
            print(bs_mod_level)
            if(len(mods) > int(bs_mod_level)+1):
                msg.append(await ctx.send("You have too many mods for your current bs"))
                msg.append(await ctx.send(f"You can have only {int(bs_mod_level)+1} mods, not {len(mods)}"))
                correct_mods = False
            elif(len(mods) < int(bs_mod_level)+1):
                msg.append(await ctx.send("You have too few mods for your current bs"))
                msg.append(await ctx.send(f"You can have only {int(bs_mod_level)+1} mods, not {len(mods)}"))
                correct_mods = False
        elif(tag == "miner"):
            miner_level = full_text.find("miner\":{\"level\":")
            miner_mod_level = full_text[miner_level + len("miner\":{\"level\":"): miner_level + len("miner\":{\"level\":") + 1]
            if(len(mods) > int(miner_mod_level)):
                msg.append(await ctx.send("You have too many mods for your current miner"))
                msg.append(await ctx.send(f"You can have only {int(miner_mod_level)} mods, not {len(mods)}"))
                correct_mods = False
            elif(len(mods) < int(miner_mod_level)):
                msg.append(await ctx.send("You have too few mods for your current miner"))
                msg.append(await ctx.send(f"You can have only {int(miner_mod_level)} mods, not {len(mods)}"))
                correct_mods = False
        elif(tag == "ts"):
            ts_level = full_text.find("transp\":{\"level\":")
            ts_mod_level = full_text[ts_level + len("bs\":{\"level\":"): ts_level + len("transp\":{\"level\":") + 1]
            if(int(ts_mod_level) >= 3):
                if(len(mods) > int(ts_mod_level)+1):
                    msg.append(await ctx.send("You have too many mods for your current ts"))
                    msg.append(await ctx.send(f"You can have only {int(ts_mod_level)+1} mods, not {len(mods)}"))
                    correct_mods = False
                elif(len(mods) < int(ts_mod_level)+1):
                    msg.append(await ctx.send("You have too few mods for your current ts"))
                    msg.append(await ctx.send(f"You can have only {int(ts_mod_level)+1} mods, not {len(mods)}"))
                    correct_mods = False
            elif(int(ts_mod_level) <= 2):
                if(len(mods) > int(ts_mod_level)):
                    msg.append(await ctx.send("You have too many mods for your current ts"))
                    msg.append(await ctx.send(f"You can have only {int(ts_mod_level)} mods, not {len(mods)}"))
                    correct_mods = False
                elif(len(mods) < int(ts_mod_level)):
                    msg.append(await ctx.send("You have too few mods for your current ts"))
                    msg.append(await ctx.send(f"You can have only {int(ts_mod_level)} mods, not {len(mods)}")) 
                    correct_mods = False     
        # Check if the names are correct, with proper tags for each ship
        #full_mods = "cargobay computer rush tradeburst shipdrone offload beam entrust recall dispatch miningboost hydrobay enrich remote hydroupload miningunity crunch genesis minedrone hydrorocket battery laser mass dual barrage dart alpha delta passive omega mirror blast area emp teleport rsextender repair warp unity sanctuary stealth fortify impulse rocket salvage suppress destiny barrier vengeance deltarocket leap bond alphadrone omegarocket suspend remotebomb"
        trade_mods = "cargobay computer rush tradeburst shipdrone offload beam entrust recall dispatch"
        mining_mods = "miningboost hydrobay enrich remote hydroupload miningunity crunch genesis minedrone hydrorocket"
        weapon_mods = "battery laser mass dual barrage dart"
        shield_mods = "alpha delta passive omega mirror blast area"
        support_mods = "emp teleport rsextender repair warp unity sanctuary stealth fortify impulse rocket salvage suppress destiny barrier vengeance deltarocket leap bond alphadrone omegarocket suspend remotebomb"
        trade, mine, weapon, shield, support = 0, 0, 0, 0, 0
        for mod in mods:
            if(trade_mods.find(mod) != -1):
                trade += 1
            elif(mining_mods.find(mod) != -1):
                mine += 1
            elif(weapon_mods.find(mod) != -1):
                weapon += 1
            elif(shield_mods.find(mod) != -1):
                shield += 1
            elif(support_mods.find(mod) != -1):
                support += 1
            else:
                correct_mods = False
        print("trade:", trade, " mining:", mine, " weapon:", weapon, " shield:", shield, " support:", support)
        if(tag == 'bs'): # 1 weapon, 1 shield, n support
            print("bs")
            if(weapon != 1):
                correct_mods = False
            if(shield != 1):
                correct_mods = False
            if(support != int(bs_mod_level)-1):
                correct_mods = False
        elif(tag == 'miner'): # 1 support (level 3+), n mining
            print("miner")
            if(int(miner_mod_level) < 3):
                if(mine != int(miner_mod_level)):
                    correct_mods = False
            else:
                if(mine != int(miner_mod_level)-1):
                    correct_mods = False
                if(support != 1):
                    correct_mods = False
        elif(tag == 'ts'): # 1 support (level 3+), n trade
            print("ts")
            if(trade != int(ts_mod_level)):
                correct_mods = False
            if(int(ts_mod_level) < 3):
                if(support != 0):
                    correct_mods = False
            else:
                if(support != 1):
                    correct_mods = False
        new_mods = []
        for mod in mods:
            user_id_raw = ctx.author.mention
            user_id = str(user_id_raw).strip('<>')
            user_id = user_id[1:]
            print(user_id)
            api_request_str = os.getenv('API_KEY_REQUEST') + user_id
            api_request = requests.get(api_request_str)
            #print(api_request.text)
            text_api = str(api_request.text)
            print(text_api.find(mod))
            raw_data = None
            if (text_api.find(mod) != -1):
                raw_data = (text_api[text_api.find(mod):][:text_api[text_api.find(mod):].index('}')+1])
            if(raw_data == None):
                correct_mods = False
            else:
                data = raw_data[len(mod) + 11 : ]
                data = data[:data.index(",")]
                mod = mod + data
                new_mods.append(mod)
                print(mod)
        mods = new_mods
        
        if(correct_mods):
            # Here are the current names for the mods:
            # Trade: cargobay, computer, rush, tradeburst, shipdrone, offload, beam, entrust, recall, dispatch
            # Mining: miningboost, hydrobay, enrich, remote, hydroupload, miningunity, crunch, genesis, minedrone, hydrorocket
            # Weapons: battery, laser, mass, dual, barrage, dart
            # Shields: alpha, delta, passive, omega, mirror, blast, area
            # Support: emp, teleport, rsextender, repair, warp, unity, sanctuary, stealth, fortify, impulse, rocket, salvage, suppress, destiny, barrier, vengeance, deltarocket, leap, bond, alphadrone, omegarocket, suspend, remotebomb

            # change mods to have a number after them, representing the mod level
            


            # Tag represents the ship, mods represent what's present on the ship

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            # Get the stored object from database
            sql = "SELECT nickname FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            result = cursor.fetchall()
            user_name = ctx.author.mention
            user_nickname = ctx.author.name
            # Setting/Updating User data
            if len(result) == 0:
                sql = ("INSERT INTO main(name, nickname) VALUES(?,?)")
                val = (user_name, user_nickname)
            else:
                sql = ("UPDATE main SET name = ? WHERE nickname = ?")
                val = (user_name, user_nickname)
            cursor.execute(sql, val)
            # Adding a Battleship
            if(tag == 'bs'):
                sql = "SELECT battleship FROM main WHERE nickname=?"
                cursor.execute(sql, [(ctx.author.name)])
                result = cursor.fetchall()
                if len(result) == 1:
                    string_mods = " ".join(mods)
                    sql = ("UPDATE main SET battleship = ? WHERE nickname = ?")
                    val = (string_mods, user_nickname)
                else:
                    msg.append(await ctx.send("Invalid Options"))
                cursor.execute(sql,val)
            # Adding a Miner
            elif(tag == 'miner'):
                sql = "SELECT miner FROM main WHERE nickname=?"
                cursor.execute(sql, [(ctx.author.name)])
                result = cursor.fetchall()
                if len(result) == 1:
                    string_mods = " ".join(mods)
                    sql = ("UPDATE main SET miner = ? WHERE nickname = ?")
                    val = (string_mods, user_nickname)
                else:
                   msg.append(await ctx.send("Invalid Options"))
                cursor.execute(sql,val)
            # Adding a Transport
            elif(tag == 'ts'):
                sql = "SELECT transport FROM main WHERE nickname=?"
                cursor.execute(sql, [(ctx.author.name)])
                result = cursor.fetchall()
                if len(result) == 1:
                    string_mods = " ".join(mods)
                    sql = ("UPDATE main SET transport = ? WHERE nickname = ?")
                    val = (string_mods, user_nickname)
                else:
                    msg.append(await ctx.send("Invalid Options"))
                cursor.execute(sql,val)
            else:
                msg.append(await ctx.send('Invalid Option'))
            db.commit()
            cursor.close()
            db.close()

            # Battleship EMBED
            final_embed = discord.Embed(
                colour = discord.Colour.dark_gold()
            )
            final_embed.set_author(name=ctx.author.name)
            final_embed.add_field(name=f'The current {tag} of {ctx.author.name}', value=f'{" ".join(mods)}')
            msg.append(await ctx.send(embed=final_embed))
        else:
            msg.append(await ctx.send("The mods listed aren't correct, either you don't have those mods unlocked or you typed them in incorrectly. Use the !modlist command for a list of mods"))
        await asyncio.sleep(20)
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()
    
            

    @ws.command(help="Shows a player their bs/miner/ts")
    async def show(self, ctx, tag):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        if (tag == 'bs'):
            bs_sql = "SELECT battleship FROM main WHERE nickname=?"
            cursor.execute(bs_sql, [(ctx.author.name)])
            bs_data_raw = cursor.fetchall()
            bs_data = str(bs_data_raw).strip('[]')
            bs_data = str(bs_data).strip('()')
            if (bs_data != 'None,'):
                bs_data = bs_data[1:]
                bs_data = bs_data[:len(bs_data)-2]
            else:
                bs_data = bs_data[:len(bs_data)-1]
            

            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Battleship', value=f'{bs_data}', inline=False)

            msg = await ctx.send(embed=embed)

        elif(tag == 'miner'):
            miner_sql = "SELECT miner FROM main WHERE nickname=?"
            cursor.execute(miner_sql, [(ctx.author.name)])
            miner_data_raw = cursor.fetchall()
            miner_data = str(miner_data_raw).strip('[]')
            miner_data = str(miner_data).strip('()')
            if (miner_data != 'None,'):
                miner_data = miner_data[1:]
                miner_data = miner_data[:len(miner_data)-2]
            else:
                miner_data = miner_data[:len(miner_data)-1]
            

            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Miner', value=f'{miner_data}', inline=False)

            msg = await ctx.send(embed=embed)
        elif(tag == 'ts'):
            ts_sql = "SELECT transport FROM main WHERE nickname=?"
            cursor.execute(ts_sql, [(ctx.author.name)])
            ts_data_raw = cursor.fetchall()
            ts_data = str(ts_data_raw).strip('[]')
            ts_data = str(ts_data).strip('()')
            if (ts_data != 'None,'):
                ts_data = ts_data[1:]
                ts_data = ts_data[:len(ts_data)-2]
            else:
                ts_data = ts_data[:len(ts_data)-1]
            


            embed = discord.Embed(
                colour = discord.Colour.blue()
            )
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Transport', value=f'{ts_data}', inline=False)

            msg = await ctx.send(embed=embed)
        else:
            msg = await ctx.send("Invalid Options")

        db.commit()
        cursor.close()
        db.close()
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()

    @ws.command(help="deletes a players bs/miner/ts")
    async def delete(self, ctx, tag):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        if(tag == 'bs' or tag == 'miner' or tag == 'ts'):
            if (tag == 'bs'):
                bs_sql = "SELECT battleship FROM main WHERE nickname=?"
                cursor.execute(bs_sql, [(ctx.author.name)])
                result = cursor.fetchone()
                if(len(result) != 0):
                    sql = "UPDATE main SET battleship = ? WHERE nickname = ?"
                    val = (None, ctx.author.name)
                    cursor.execute(sql, val)
                    msg = await ctx.send("Battleship deleted")
            if (tag == 'miner'):
                miner_sql = "SELECT miner FROM main WHERE nickname=?"
                cursor.execute(miner_sql, [(ctx.author.name)])
                result = cursor.fetchone()
                if(len(result) != 0):
                    sql = "UPDATE main SET miner = ? WHERE nickname = ?"
                    val = (None, ctx.author.name)
                    cursor.execute(sql, val)
                    msg = await ctx.send("Miner deleted")
            if (tag == 'ts'):
                ts_sql = "SELECT transport FROM main WHERE nickname=?"
                cursor.execute(ts_sql, [(ctx.author.name)])
                result = cursor.fetchone()
                if(len(result) != 0):
                    sql = "UPDATE main SET transport = ? WHERE nickname=?"
                    val = (None, ctx.author.name)
                    cursor.execute(sql, val)
                    msg = await ctx.send("Transport deleted")
        else:
            msg = await ctx.send("Invalid option, either bs/miner/ts")
        db.commit()
        cursor.close()
        db.close()
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()


    @commands.command(help="a command for you to ask questions/give feedback")
    async def question(self, ctx, *message):
        db = sqlite3.connect('questions.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(ctx.author.name)])
        #result = cursor.fetchall()
        user_nickname = ctx.author.name
        string_message = " ".join(message)
        sql = ("INSERT INTO main(nickname, questions) VALUES(?,?)")
        val = (user_nickname, string_message)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        msg = await ctx.send("Question has been stored to database")
        
        await asyncio.sleep(50)
        await ctx.message.delete()
        await msg.delete()

    @commands.command()
    async def getlevel(self, ctx, message):
        user_id_raw = ctx.author.mention
        print(user_id_raw)
        user_id = str(user_id_raw).strip('<>')
        print(user_id)
        user_id = user_id[1:]
        print(user_id)
        user_id = user_id.strip('!')
        print(user_id)
        api_request_str = os.getenv('API_KEY_REQUEST') + user_id
        #print(api_request_str)
        api_request = requests.get(api_request_str)
        #print(api_request.text)
        text_api = str(api_request.text)
        print(text_api.find(message))
        if (text_api.find(message) != -1):
            raw_data = (text_api[text_api.find(message):][:text_api[text_api.find(message):].index('}')+1])
            await ctx.send(text_api[text_api.find(message):][:text_api[text_api.find(message):].index('}')+1])
            print(raw_data)
            #cargobay":{"level":8,"ws":625}
            # cut the message + 11
            # cut everything but one
            data = raw_data[len(message) + 11 : ]
            data = data[:data.index(",")]
            print(data)

        else:
            await ctx.send("I do not have information on that module")

    @commands.command()
    async def getapi(self, ctx):
        user_id_raw = ctx.author.mention
        user_id = str(user_id_raw).strip('<>')
        user_id = user_id[1:]
        user_id = user_id.strip('!')
        api_request_str = os.getenv('API_KEY_REQUEST') + user_id
        api_request = requests.get(api_request_str)
        print(api_request.text)



            


        

def setup(bot):
    bot.add_cog(BattleCoCogs(bot))
    print('BattleCo is loaded')

# example api_request.text
#{"tokenExpires":1625820656,"tz_name":"America/Los_Angeles","tz_offset":-420,"map":{"rs":{"level":7,"ws":0},"shipmentrelay":{"level":5,"ws":0},"corplevel":{"level":7,"ws":0},"transp":{"level":5,"ws":2000},"miner":{"level":5,"ws":4000},"bs":{"level":5,"ws":7000},"cargobay":{"level":8,"ws":625},"computer":{"level":4,"ws":0},"rush":{"level":3,"ws":0},"tradeburst":{"level":4,"ws":0},"shipdrone":{"level":1,"ws":0},"miningboost":{"level":4,"ws":62},"hydrobay":{"level":2,"ws":25},"enrich":{"level":3,"ws":75},"remote":{"level":5,"ws":125},"hydroupload":{"level":2,"ws":0},"genesis":{"level":1,"ws":25},"battery":{"level":10,"ws":1000},"laser":{"level":3,"ws":75},"mass":{"level":2,"ws":25},"dual":{"level":7,"ws":500},"barrage":{"level":2,"ws":25},"alpha":{"level":1,"ws":0},"delta":{"level":1,"ws":0},"passive":{"level":2,"ws":25},"omega":{"level":8,"ws":625},"mirror":{"level":5,"ws":250},"blast":{"level":5,"ws":700},"emp":{"level":8,"ws":625},"teleport":{"level":7,"ws":500},"rsextender":{"level":6,"ws":0},"repair":{"level":7,"ws":500},"warp":{"level":7,"ws":500},"sanctuary":{"level":1,"ws":0},"fortify":{"level":3,"ws":37},"rocket":{"level":6,"ws":625},"salvage":{"level":6,"ws":187},"suppress":{"level":2,"ws":12},"barrier":{"level":4,"ws":125}},"array":[{"type":"rs","level":7,"ws":0},{"type":"shipmentrelay","level":5,"ws":0},{"type":"corplevel","level":7,"ws":0},{"type":"transp","level":5,"ws":2000},{"type":"miner","level":5,"ws":4000},{"type":"bs","level":5,"ws":7000},{"type":"cargobay","level":8,"ws":625},{"type":"computer","level":4,"ws":0},{"type":"rush","level":3,"ws":0},{"type":"tradeburst","level":4,"ws":0},{"type":"shipdrone","level":1,"ws":0},{"type":"miningboost","level":4,"ws":62},{"type":"hydrobay","level":2,"ws":25},{"type":"enrich","level":3,"ws":75},{"type":"remote","level":5,"ws":125},{"type":"hydroupload","level":2,"ws":0},{"type":"genesis","level":1,"ws":25},{"type":"battery","level":10,"ws":1000},{"type":"laser","level":3,"ws":75},{"type":"mass","level":2,"ws":25},{"type":"dual","level":7,"ws":500},{"type":"barrage","level":2,"ws":25},{"type":"alpha","level":1,"ws":0},{"type":"delta","level":1,"ws":0},{"type":"passive","level":2,"ws":25},{"type":"omega","level":8,"ws":625},{"type":"mirror","level":5,"ws":250},{"type":"blast","level":5,"ws":700},{"type":"emp","level":8,"ws":625},{"type":"teleport","level":7,"ws":500},{"type":"rsextender","level":6,"ws":0},{"type":"repair","level":7,"ws":500},{"type":"warp","level":7,"ws":500},{"type":"sanctuary","level":1,"ws":0},{"type":"fortify","level":3,"ws":37},{"type":"rocket","level":6,"ws":625},{"type":"salvage","level":6,"ws":187},{"type":"suppress","level":2,"ws":12},{"type":"barrier","level":4,"ws":125}]}