import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions
import asyncio
import datetime
import time
class TC(commands.Cog,name='Channels'):
    def __init__(self,bot):
        self.bot=bot
        
    @commands.command()
    @commands.has_role("Owner")
    async def lockdown(self, ctx):
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(ctx.guild.default_role, connect=False)
        await ctx.send("LockDown Mode Initiated")
        
    @commands.command()
    @commands.has_role("Owner")
    async def unlockmode(self, ctx):
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(ctx.guild.default_role, connect=None)
        await ctx.send("LockDown Mode Ended")    
    
    @commands.command()
    async def lock(self,ctx):
        if ctx.author.guild_permissions.manage_guild:
            ch = ctx.channel
            embed= discord.Embed(
                color = discord.Colour.red()
            )
            await ch.set_permissions(ctx.guild.default_role, send_messages=False)
            embed.description = f':red_square: Channel Locked'
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"You dont have permissions! You need to following permissions `Manage Server`")
    @lock.error
    async def lockerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"I can't lock this channel. I need the following permissions to do so: `Manage Server` and `Manage Channels`")
    @commands.command()
    async def unlock(self,ctx):
        if ctx.author.guild_permissions.manage_guild:
            ch = ctx.channel
            embed= discord.Embed(
                color = discord.Colour.green()
            )
            await ch.set_permissions(ctx.guild.default_role, send_messages=True)
            embed.description = f':green_square: Channel Unlocked'
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"You dont have permissions! You need to following permissions `Manage Server`")
    @unlock.error
    async def unlockerror(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send(f"I can't unlock this channel. I need the following permissions to do so: `Manage Server` and `Manage Channels`")




def setup(bot):
    bot.add_cog(TC(bot))
    print("Loaded Channel Moderation Successfully")