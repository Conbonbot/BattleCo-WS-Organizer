import random
from dotenv import load_dotenv
import sqlite3
import datetime
from discord.ext import commands
import discord
import requests
import asyncio
import numpy as np

class BattleCoWSCogs(commands.Cog, name='BattleCo'):


    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Show the current polls with their poll number")
    async def polls(self, ctx):
        msg = []
        print(ctx.author.name, " has typed the !polls command")
        db = sqlite3.connect('polls.sqlite')
        cursor = db.cursor()
        question_sql = "SELECT question FROM main"
        cursor.execute(question_sql)
        questions = cursor.fetchall()
        
        number_sql = "SELECT number FROM main"
        cursor.execute(number_sql)
        numbers = cursor.fetchall()
        
        yes_sql = "SELECT yes FROM main"
        cursor.execute(yes_sql)
        yes = cursor.fetchall()

        no_sql = "SELECT no FROM main"
        cursor.execute(no_sql)
        no = cursor.fetchall()

        full = np.array([questions, numbers, yes, no]) # 0 is questions, 1 is numbers, 2 is yes, 3 is no
        for i in range(len(full)-1):
            question_ = str(full[0][i])
            question_ = question_[2:-2]
            
            poll_number_ = str(full[1][i])
            poll_number_ = poll_number_[1:-1]

            yes_ = str(full[2][i])
            yes_ = yes_[1:-1]

            no_ = str(full[3][i])
            no_ = no_[1:-1]

            final = f"**Poll #{poll_number_}: **" + question_ + "\n **Y - **" + yes_ + "\n **N - **" + no_
            msg.append(await ctx.send(final))
        await asyncio.sleep(50)
        await ctx.message.delete()
        for ms in msg:
            await ms.delete()


            


    # TODO check yes/no_person tuple lists for duplicate users, and prevent voting from them
    @commands.command(help="Vote on a poll, just type the poll number and either Y or N")
    async def vote(self, ctx, number, vote):
        if(vote == "Y" or vote == "N"):
            print(ctx.author.name, " has typed the !polls command")
            db = sqlite3.connect('polls.sqlite')
            cursor = db.cursor()
            number_sql = "SELECT question FROM main WHERE number=?"
            cursor.execute(number_sql, [(number)])
            question = cursor.fetchall()
            print(question)
            if(vote == "Y"):
                check_sql = "SELECT yes FROM main WHERE number=?"
                cursor.execute(check_sql, [(number)])
                yes = cursor.fetchone()
                yes = str(yes)
                yes = yes[1:-2]
                if(yes == "None"):
                    sql = "UPDATE main SET yes = ? WHERE number = ?"
                    val = (1, number)
                    cursor.execute(sql, val)
                else:
                    num = int(yes)
                    num += 1
                    sql = "UPDATE main SET yes = ? WHERE number = ?"
                    val = (num, number)
                    cursor.execute(sql,val)
            if(vote == "N"):
                check_sql = "SELECT no FROM main WHERE number=?"
                cursor.execute(check_sql, [(number)])
                no = cursor.fetchone()
                no = str(no)
                no = no[1:-2]
                if(no == "None"):
                    sql = "UPDATE main SET no = ? WHERE number = ?"
                    val = (1, number)
                    cursor.execute(sql, val)
                else:
                    num = int(no)
                    num += 1
                    sql = "UPDATE main SET no = ? WHERE number = ?"
                    val = (num, number)
                    cursor.execute(sql,val)
            


            db.commit()
            cursor.close()
            db.close()
        else:
            msg = await ctx.send("Invaild voting option, it can either be Y or N")
        await asyncio.sleep(20)
        await ctx.message.delete()
        await msg.delete()




    @commands.group(invoke_without_command=True, help="Shows poll commands")
    async def poll(self, ctx):
        print(ctx.author.name, " has typed the !poll command")
        poll_embed = discord.Embed(
            description = 'Poll Commands',
            colour = discord.Colour.dark_blue()
        )
        poll_embed.set_author(name=ctx.author)
        poll_embed.add_field(name='Start Poll', value="!poll start question ", inline=True)
        poll_embed.add_field(name='See Polls', value='!polls', inline=True)
        poll_embed.add_field(name='See Specific Poll', value='!poll show PollNumber')
        poll_embed.add_field(name='Vote on a Poll', value='!vote PollNumber Y/N', inline=False)
        poll_embed.add_field(name='Remove your vote', value='!poll remove PollNumber', inline=True)
        poll_embed.add_field(name='Delete Poll', value='!poll delete PollNumber', inline=True)
        msg = await ctx.send(embed=poll_embed)
        await asyncio.sleep(80)
        await ctx.message.delete()
        await msg.delete()

    @poll.command(help="Starts a poll with a question")
    async def start(self, ctx, *message):
        #print(message)
        actual_message = ' '.join(message)
        print(actual_message)
        db = sqlite3.connect('polls.sqlite')
        cursor = db.cursor()
        check_sql = "SELECT number FROM main"
        cursor.execute(check_sql)
        results = cursor.fetchall() # Returns a list of tuples
        print(results)
        if(len(results) == 0):
            num = 1
        else:
            print("Here")
            num = 0
            for result in results:
                result = str(result)
                result = result[1:-2]
                print(result)
                num = int(result)
                num += 1
                
        sql = "INSERT INTO main(question, number) VALUES(?,?)"
        val = (actual_message, num)
        cursor.execute(sql, val)
        # sweet okay this works (:
        db.commit()
        cursor.close()
        db.close()

        msg = await ctx.send(f"The poll is now active, with poll number #{num}")
        await asyncio.sleep(15)
        await ctx.message.delete()
        await msg.delete()

    @poll.command(help="Shows a poll based of the poll number")
    async def show(self, ctx, number):
        print(ctx.author.name, " has typed the !poll show command")
        db = sqlite3.connect('polls.sqlite')
        cursor = db.cursor()

        checking_sql = "SELECT question FROM main WHERE number = ?"
        cursor.execute(checking_sql, number)
        results = cursor.fetchall()
        if len(results) != 0:
            question_sql = "SELECT question FROM main WHERE number = ?"
            cursor.execute(question_sql, number)
            question = cursor.fetchone()
            question = str(question)
            question = question[2:-3]

            yes_sql = "SELECT yes FROM main WHERE number = ?"
            cursor.execute(yes_sql, number)
            yes = cursor.fetchone()
            yes = str(yes)
            yes = yes[1:-2]

            no_sql = "SELECT no FROM main WHERE number = ?"
            cursor.execute(no_sql, number)
            no = cursor.fetchone()
            no = str(no)
            no = no[1:-2]
            
            msg = await ctx.send(f"**Poll #{number}: **" + question + "\n **Y - **" + yes + "\n **N - **" + no)
        else:
            msg = await ctx.send(f"There is no Poll #{number}")
        await asyncio.sleep(50)
        await ctx.message.delete()
        await msg.delete()


        






def setup(bot):
    bot.add_cog(BattleCoWSCogs(bot))
    print('BattleCo is loaded')