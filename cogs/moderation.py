import os
import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord

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
            title = 'BattleCo WS Organizer',
            description = (f'The current builds for {ctx.author.name}'),
            colour = discord.Colour.blue()
        )
        embed.set_footer(text='Best of luck on this WS!')
        embed.set_author(name=ctx.author)
        embed.add_field(name='Battleship', value=f'{bs_data}', inline=False)
        embed.add_field(name='Miner', value=f'{miner_data}', inline=True)
        embed.add_field(name='Transport', value=f'{ts_data}', inline=True)

        await ctx.send(embed=embed)


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
                title = 'BattleCo WS Organizer',
                description = (f'The current builds for {player}'),
                colour = discord.Colour.blue()
            )
            embed.set_footer(text='Best of luck on this WS!')
            embed.set_author(name=player_name)
            embed.add_field(name='Battleship', value=f'{bs_data}', inline=False)
            embed.add_field(name='Miner', value=f'{miner_data}', inline=True)
            embed.add_field(name='Transport', value=f'{ts_data}', inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Player not found")



    @commands.group(invoke_without_command=True, help="Add, edit, show, and delete ships, type !ws for more details")
    async def ws(self, ctx):
        print(ctx.author.name, " has typed the !ws command")
        ws_embed = discord.Embed(
            title = 'BattleCo WS Organizer',
            description = 'WS Setup Commands',
            colour = discord.Colour.green()
        )
        ws_embed.set_footer(text='Example: !ws add battleship battery10 omega8 teleport7 repair7 emp8 rocket6 \nExample: !ws show miner')
        ws_embed.set_author(name=ctx.author)
        ws_embed.add_field(name='Add Ship', value='!ws add', inline=True)
        ws_embed.add_field(name='Show Ship', value='!ws show', inline=True)
        ws_embed.add_field(name='Delete Ship', value='!ws delete', inline=True)
        ws_embed.add_field(name='Next Steps', value='for adding (use can use the add command to edit your ships) ships, add the mods listed on your ship, but for show and delete, just enter the name of the ship you want to see/delete', inline=False)
        await ctx.send(embed=ws_embed)
        

    @ws.command()
    async def add(self, ctx, tag, *mods):
        #print(tag, mods)
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
        if(tag == 'battleship'):
            sql = "SELECT battleship FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            result = cursor.fetchall()
            if len(result) == 1:
                string_mods = " ".join(mods)
                sql = ("UPDATE main SET battleship = ? WHERE nickname = ?")
                val = (string_mods, user_nickname)
            else:
                await ctx.send("Invalid Options")
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
                await ctx.send("Invalid Options")
            cursor.execute(sql,val)
        # Adding a Transport
        elif(tag == 'transport'):
            sql = "SELECT transport FROM main WHERE nickname=?"
            cursor.execute(sql, [(ctx.author.name)])
            result = cursor.fetchall()
            if len(result) == 1:
                string_mods = " ".join(mods)
                sql = ("UPDATE main SET transport = ? WHERE nickname = ?")
                val = (string_mods, user_nickname)
            else:
                await ctx.send("Invalid Options")
            cursor.execute(sql,val)
        else:
            await ctx.send('Invalid Option')
        db.commit()
        cursor.close()
        db.close()

        # Battleship EMBED
        final_embed = discord.Embed(
            title = 'BattleCo WS Organizer',
            description = f'Current {tag}',
            colour = discord.Colour.dark_gold()
        )
        final_embed.set_footer(text='Best of luck on this WS!')
        final_embed.set_author(name=ctx.author)
        final_embed.add_field(name=f'The current {tag} of {ctx.author.name}', value=f'{" ".join(mods)}')
        await ctx.send(embed=final_embed)

    @ws.command(help="Shows a player their bs/miner/ts")
    async def show(self, ctx, tag):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        if (tag == 'battleship'):
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
                title = 'BattleCo WS Organizer',
                description = (f'The current battleship of {ctx.author.name}'),
                colour = discord.Colour.blue()
            )
            embed.set_footer(text='Best of luck on this WS!')
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Battleship', value=f'{bs_data}', inline=False)

            await ctx.send(embed=embed)

        elif(tag == 'miner'):
            miner_sql = "SELECT miner FROM main WHERE nickname=?"
            cursor.execute(miner_sql, [(ctx.author.name)])
            miner_data_raw = cursor.fetchall()
            miner_data = str(miner_data_raw).strip('[]')
            miner_data = str(miner_data).strip('()')
            if (miner_data != 'None,'):
                miner_data = miner_data[1:]
                miner_data = miner_data[:len(bs_data)-2]
            else:
                miner_data = miner_data[:len(miner_data)-1]
            

            embed = discord.Embed(
                title = 'BattleCo WS Organizer',
                description = (f'The current miner of {ctx.author.name}'),
                colour = discord.Colour.blue()
            )
            embed.set_footer(text='Best of luck on this WS!')
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Miner', value=f'{miner_data}', inline=False)

            await ctx.send(embed=embed)
        elif(tag == 'transport'):
            ts_sql = "SELECT transport FROM main WHERE nickname=?"
            cursor.execute(ts_sql, [(ctx.author.name)])
            ts_data_raw = cursor.fetchall()
            ts_data = str(ts_data_raw).strip('[]')
            ts_data = str(ts_data).strip('()')
            if (ts_data != 'None,'):
                ts_data = ts_data[1:]
                ts_data = ts_data[:len(bs_data)-2]
            else:
                ts_data = ts_data[:len(bs_data)-1]
            


            embed = discord.Embed(
                title = 'BattleCo WS Organizer',
                description = (f'The current transport of {ctx.author.name}'),
                colour = discord.Colour.blue()
            )
            embed.set_footer(text='Best of luck on this WS!')
            embed.set_author(name=ctx.author.name)
            embed.add_field(name='Transport', value=f'{ts_data}', inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid Options")

        db.commit()
        cursor.close()
        db.close()

    @ws.command(help="deletes a players bs/miner/ts")
    async def delete(self, ctx, tag):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        if (tag == 'battleship'):
            bs_sql = "SELECT battleship FROM main WHERE nickname=?"
            cursor.execute(bs_sql, [(ctx.author.name)])
            sql = "UPDATE main SET battleship = ? WHERE nickname = ?"
            val = (None, ctx.author.name)
            cursor.execute(sql, val)
            await ctx.send("Battleship deleted")
        db.commit()
        cursor.close()
        db.close()

    @commands.command(help="a command for you to ask questions/give feedback")
    async def question(self, ctx, *message):
        db = sqlite3.connect('questions.sqlite')
        cursor = db.cursor()
        sql = "SELECT nickname FROM main WHERE nickname=?"
        cursor.execute(sql, [(ctx.author.name)])
        result = cursor.fetchall()
        user_nickname = ctx.author.name
        string_message = " ".join(message)
        sql = ("INSERT INTO main(nickname, questions) VALUES(?,?)")
        val = (user_nickname, string_message)
        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        await ctx.send("Question is stored to database")

def setup(bot):
    bot.add_cog(BattleCoCogs(bot))
    print('BattleCo is loaded')

