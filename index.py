import discord
import json
import time
import urllib.request
import shutil
import os
import asyncio
import requests
import datetime
import re
import sys
import traceback
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import sqlite3
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("!")(bot,message)

    with open(r'prefixes.json','r') as f:
        prefixes = json.load(f)
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("!")(bot,message)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot,message)
    return prefixes[str(message.guild.id)]
    #a = str(message.guild.id)
    #extras = await prefixes[(a)]
    
    #return commands.when_mentioned_or(*extras)(bot,message)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix = get_prefix, intents = intents)
@bot.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MAIN(
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT
        )
        ''')
    db1 = sqlite3.connect('main1.sqlite')
    cursor = db1.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MAIN1(
        guild_id TEXT,
        msg TEXT,
        channel_id TEXT
        )
        ''')
    db2 = sqlite3.connect('autorole.sqlite')
    cursor = db2.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AUTOROLE(
        guild_id TEXT,
        channel_id TEXT,
        role_id TEXT
        )
        ''')
    db3 = sqlite3.connect('levelll.sqlite')
    cursor = db3.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS levels(
        guild_id TEXT,
        user_id TEXT,
        exp TEXT,
        level TEXT
        )
        ''')
    db4 = sqlite3.connect('main.sqlite')
    cursor = db4.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userconfiguration(
        user_id TEXT,
        api_token TEXT
        )
        ''')
    print(f'Logged In As {bot.user}')
    print("---------------------------")
    print("Started Tracking All guilds")
    print("_________________________________________________________________________")
    change_status.start()
initial_extension = ['cogs.moderation',
                     'cogs.channel',
                     'cogs.serverprefix',
                     'cogs.info',
                     'cogs.tickettrial',
                     'cogs.admin',
                     'cogs.gtrans',
                     'cogs.welcome',
                     'cogs.leave',
                     'cogs.urban',
                     'cogs.pterylink',
                     'cogs.announce']
if __name__ == '__main__':
    for extension in initial_extension:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed To Load {extension}",file=sys.stderr)
            traceback.print_exc()
bot.load_extension('jishaku')            	

@bot.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    a = f"{message.channel}: {message.author}: {message.author.name}: {message.content}"
    f = open(r'log.txt','a',encoding='utf-8')
    f.write(f"{a}\n")
    #f.write(f"\n")
    f.close()
    await bot.process_commands(message)
        
@tasks.loop()
async def change_status():
    await bot.change_presence(activity=discord.Game(name="NolesNetwork"))

#bot.run("NzU1Mzc2NDg0NDc4MjIyMzg2.X2CZLA.QUuCps0AMm7_JDNY-INyzx8nEFk")
bot.run("NzUxMDU2MDcwNjA4Mjg5ODc0.X1DheQ.f3FAL4LRiyZ0NbLRkzk5WPcaQow")