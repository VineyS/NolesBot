import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import datetime
import time
import sqlite3
import requests
class WelcomeCog(commands.Cog, name="Welcome"):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor=db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result=cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            userno = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            userid=member.id
            channel = self.bot.get_channel(id=int(result[0]))
            await channel.send(f"{str(result1[0]).format(userno=userno, mention=mention, user=user, userid=userid)}")
    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        '''For Welcome Messages'''
        await ctx.send(f'Setup Commands are: \n{ctx.prefix}welcome channel <#channel>\n{ctx.prefix}welcome text <message>]\n{ctx.prefix}welcome cancel (For disabling Automated Welcome Messages)')
        await ctx.send('NOTE: For welcome text you can use the following for message:\n{userno} - returns the member position number in the guild. Ex: 11th user\n{mention} - mentions the user Ex - @Test has joined us\n{user} - returns name of user without mentioning it Ex - Test has joined us\n{userid} - returns the id of the member Ex - 12345232323234213 has joined us')
    @welcome.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Welcome Message Channel Has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    @channel.error
    async def channelerror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"You must mention a text channel where welcome messages are to be sent")
            await ctx.send(f"`welcome channel <TextChannel> ??? TextChannel is missing`")
        elif isinstance(error, MissingPermissions):
            await ctx.send(f"You need the following permissions for that command to work: `Manage Sever`")
#        elif isinstance(error, MissingAccess):
#            await ctx.send(f"I dont have permissions to send on that channel")

    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Welcome Message Has been set to {text}")
            elif result is not None:
                sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Welcome Message has been updated to {text}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    @text.error
    async def texterror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Text to be sent when member joins is missing")
            await ctx.send(f"`welcome text <Text> ??? Text is missing`")
        elif isinstance(error, MissingPermissions):
            await ctx.send(f"You need the following permissions for that command to work: `Manage Server`")
    @welcome.command(pass_context=True)
    async def cancel(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            print(result)
            if result is None:
                await ctx.send(f"Hmm, You did not setup any welcome channel or the text.")
            elif result is not None:
                sql = ("DELETE from main WHERE guild_id = ?")
                val = (ctx.guild.id,)
                await ctx.send("Automated Welcome for this server has been disabled")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    @cancel.error
    async def wecancel(self, ctx,error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"You need the following permissions for that command to work: `Manage Sever`")
            

#        elif isinstance(error, MissingAccess):
#            await ctx.send(f"I dont have permissions to send on that channel")
def setup(bot):
    bot.add_cog(WelcomeCog(bot))
    print("Loaded Welcome Successfully")