import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
import datetime
import time
import sqlite3
class LeaveCog(commands.Cog, name="Leave"):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = sqlite3.connect('main1.sqlite')
        cursor=db.cursor()
        cursor.execute(f"SELECT channel_id FROM main1 WHERE guild_id = {member.guild.id}")
        result=cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main1 WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            userno = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            userid=member.id
            channel = self.bot.get_channel(id=int(result[0]))
            await channel.send(f"{str(result1[0]).format(userno=userno, mention=mention, user=user, userid=userid)}")
    @commands.group(invoke_without_command=True)
    async def leave(self, ctx):
        '''For Leave Messages'''
        await ctx.send(f'Setup Commands are: \n{ctx.prefix}leave channel <#channel>\n{ctx.prefix}leave text <message>\n{ctx.prefix}leave cancel (For disabling Automated Leave Messages)')
        await ctx.send('NOTE: For leave text you can use the following for message:\n{userno} - returns the member position number in the guild. Ex: 11th user\n{mention} - mentions the user Ex - @Test has left us\n{user} - returns name of user without mentioning it Ex - Test has left us\n{userid} - returns the id of the member Ex - 12345232323234213 has left us')

    @leave.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main1.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT channel_id FROM main1 WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main1(guild_id, channel_id) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"leave Message Channel Has been set to {channel.mention}")
            elif result is not None:
                sql = ("UPDATE main1 SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f"Channel has been updated to {channel.mention}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    @channel.error
    async def channellerror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"You must mention a text channel where leave messages are to be sent")
            await ctx.send(f"`leave channel <TextChannel> ??? TextChannel is missing`")
        elif isinstance(error, MissingPermissions):
            await ctx.send(f"You need the following permissions for that command to work: `Manage Sever`")

    @leave.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main1.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT msg FROM main1 WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main1(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f"Leave Message Has been set to {text}")
            elif result is not None:
                sql = ("UPDATE main1 SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Leave Message has been updated to {text}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    @text.error
    async def textlerror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Text to be sent when member leaves is missing")
            await ctx.send(f"`leave text <Text> ??? Text is missing`")
        elif isinstance(error, MissingPermissions):
            await ctx.send(f"You need the following permissions for that command to work: `Manage Sever`")
    @leave.command(pass_context=True)
    async def cancel(self, ctx):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main1.sqlite')
            cursor=db.cursor()
            cursor.execute(f"SELECT msg FROM main1 WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            print(result)
            if result is None:
                await ctx.send(f"Hmm, You did not setup any leave channel.")
            elif result is not None:
                sql = ("DELETE from main1 WHERE guild_id = ?")
                val = (ctx.guild.id,)
                await ctx.send("Automated Leave for this server has been disabled")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
    @cancel.error
    async def lecancel(self, ctx,error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"I dont have permissions to send on that channel")

def setup(bot):
    bot.add_cog(LeaveCog(bot))
    print("Loaded Leave Successfully")