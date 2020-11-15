import discord
from discord import Member, Embed, Activity, ActivityType, Embed
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
from datetime import datetime, timedelta
from platform import python_version
from time import time
from apscheduler.triggers.cron import CronTrigger
from discord import __version__ as discord_version
from discord.ext.commands import Cog
from discord.ext.commands import command
from psutil import Process, virtual_memory
import psutil
import asyncio
from typing import Optional
class InfoCog(commands.Cog,name='Information'):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["memberinfo", "ui", "mi"])
    async def user_info(self, ctx, target:Optional[Member]):#:Optional[Member]):
        '''Displays User Information'''
        target = target or ctx.author
        embed = Embed(title="User information",
					  colour=target.colour,
					  timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar_url)
        fields = [("Name", str(target), True),
				  ("ID", target.id, True),
				  ("Bot?", target.bot, True),
				  ("Top role", target.top_role.mention, True),
				  ("Status", str(target.status).title(), True),
				  ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boosted", bool(target.premium_since), True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)
    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi",'ss'])
    async def server_info(self, ctx):
        '''Displays Server Information'''
        embed = Embed(title="Server information",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        statuses = [len(list(filter(lambda m: str(m.status) == "online" and not m.bot, ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        fields = [("ID", ctx.guild.id, True),
				  ("Owner", ctx.guild.owner, True),
				  ("Region", str(ctx.guild.region).capitalize(), True),
				  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Members", len(ctx.guild.members), True),
				  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Banned members", len(await ctx.guild.bans()), True),
				  ("Status", f"<a:anim_online:757647692246548510> {statuses[0]} <a:anim_idle:757647720025423973> {statuses[1]} <a:anim_dnd:757646711941496903> {statuses[2]} <a:anim_offline:757647799826514041> {statuses[3]}", True),
				  ("Text channels", len(ctx.guild.text_channels), True),
				  ("Voice channels", len(ctx.guild.voice_channels), True),
				  ("Categories", len(ctx.guild.categories), True),
				  ("Roles", len(ctx.guild.roles), True),
				  ("Invites", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @commands.command(name="stats")
    async def show_bot_stats(self, ctx):
        embed = Embed(title="Bot stats",colour=ctx.author.colour, thumbnail=self.bot.user.avatar_url, timestamp=datetime.utcnow())
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            #cpu_time = psutil.cpu_percent()
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)
            mo=self.bot.guilds
            sum1=0
            for s in mo:
                sum1+=len(s.members)
        fields = [
			("Python version", python_version(), True),
			("discord.py version", discord_version, True),
			("Uptime", uptime, True),
			("CPU time", f"{cpu_time}%", True),
			("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", True),
			("Users", f"{sum1:,}", True),
            ("Servers", f"{len(self.bot.guilds)}",True),
            ("Region", f"`Europe`", True),
            ("Latency", "`{0}`".format(round(self.bot.latency,4)*1000), True)
		]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(InfoCog(bot))
    print("Loaded Information Successfully")