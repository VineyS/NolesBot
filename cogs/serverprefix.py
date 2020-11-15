import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
import datetime
import time
import json
import sqlite3
class PrefixCog(commands.Cog, name="Prefix"):
    def __init__(self, bot):
        self.bot=bot
    @commands.command(aliases=[('cp')])
    async def changeprefix(self, ctx, *, pre):
        '''Change Prefix Of The Bot'''
        with open(r"prefixes.json", "r") as f:
            prefixes = json.load(f)
        if ctx.message.author.guild_permissions.administrator:
            try:
                prefixes[str(ctx.guild.id)] = pre
                await ctx.send(f"Bot prefix on this server has been changed to `{pre}`")
                with open(r"prefixes.json","w") as f:
                    json.dump(prefixes, f, indent=4)
            except:
                await ctx.send("An error arised due to which bot couldn't change its server prefix! Please contact the support server if this issue persists furthur.")
        else:
            await ctx.send("You don't have administrative priviledges!!")
    @changeprefix.error
    async def cp_error(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Bruh! You didn't mention the new prefix that I should change to")
            await ctx.send(f"`{ctx.prefix}changeprefix <new prefix> ??? New prefix is a required argument`")
    @commands.command(aliases=[('what is my prefix','p')])
    async def myprefix(self, ctx):
        '''Displays Bot Prefix'''
        await ctx.send(f'Bot prefix for this server is `{ctx.prefix}`')
def setup(bot):
    bot.add_cog(PrefixCog(bot))
    print("Loaded Server Prefixes Successfully")
