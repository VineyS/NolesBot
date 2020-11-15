from operator import ne
import discord
from discord import colour
from discord.member import Member
from num2words import num2words
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
import datetime
import csv
import time
import sqlite3

from discord.ext.commands.errors import BadArgument, MissingRole
class ModCog(commands.Cog,name='Moderation'):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['cls','clear','clearchat'])
    @commands.has_role(758694901214478347)
    async def purge(self,ctx,number:int=None):
        '''This Command Is To Clear Messages'''
        c = 0

        try:
            if number is None:
                await ctx.send(f"You must enter a number!!")
            else:
                deleted = await ctx.channel.purge(limit=number+1)
                await ctx.send(f"`{len(deleted)-1}` messages have been deleted")
                time.sleep(3)
                await ctx.channel.purge(limit=1)
        except:
            await ctx.send("I am not permitted to delete messages. Please give me the role `Manage Messages`")
    @purge.error
    async def purgeerror(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")

    @commands.command(description = "Kicks the user")
    @commands.has_role(758694901214478347)
    async def kick(self,ctx, user: discord.Member, *, reason=None):
        '''Kicks The User'''
        if user.guild_permissions.manage_guild:
            await ctx.send("This user is either a moderator or administrator. I can't kick them")
        else:
            if reason is None:
                await ctx.guild.kick(user=user, reason='None')
                await ctx.send(f'{user} has been kicked')
            else:
                await ctx.guild.kick(user=user, reason=reason)
                await ctx.send(f'{user} has been kicked')
        #else:
        #    await ctx.send(f'{ctx.message.author.mention} You are missing the following permissions: `Kick Members`')
    @kick.error
    async def kickerror(self,ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Bruh! You must mention the member to be kicked")
            await ctx.send(f"`{ctx.prefix}kick <member> ??? Member argument is Missing!`")
        else:
            await ctx.send(f"I must be placed to a higher hierarchy to kick the member out{ctx.message.author.mention}")


    @commands.command()
    @commands.has_role(758694901214478347)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        '''Bans The User'''
        if user.guild_permissions.manage_guild:
            await ctx.send("This user is either a moderator or administrator. I can't ban them")
        else:
            if reason is None:
                await ctx.send(f'`{ctx.prefix}ban <member> <reason> ??? Reason Missing`')
            else:
                await ctx.guild.ban(user=user, reason=reason)
                await ctx.send(f'{user} has been banned for {reason}')
        #else:
        #    await ctx.send(f'{ctx.message.author.mention} You are missing the following permissions: `Ban Members`')
    @ban.error
    async def banerror(self,ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Bruh, You must mention the member to be banned!")
            await ctx.send(f"`{ctx.prefix}ban <member> <reason> ??? Member Argument Missing!`")
        else:
            await ctx.send(f"I must be placed to a higher hierarchy to ban the member{ctx.message.author.mention}")


    
    @commands.command()
    @commands.has_role(758694901214478347)
    async def banid(self, ctx, user: int, *, reason=None):
        '''Bans The User'''
        if reason is None:
            await ctx.send(f'`{ctx.prefix}banid <member> <reason> ??? Reason Missing`')
        else:
            await ctx.guild.ban(discord.Object(id=user), reason=reason)
            await ctx.send(f'**{self.bot.get_user(user)}** has been banned for {reason}')
    @banid.error
    async def baniderror(self,ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Bruh, You must mention the member to be banned!")
            await ctx.send(f"`{ctx.prefix}banid <member> <reason> ??? Member Argument Missing!`")
        else:
            await ctx.send(f"I must be placed to a higher hierarchy to ban the member{ctx.message.author.mention}")

    
    @commands.command()
    @commands.has_role(758694901214478347)
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int=15, *,reason=None):
        '''Mutes The User'''
        if user == ctx.author:
            await ctx.send("You can't mute yourself")
        elif user != ctx.author:
            if reason is None:
                await ctx.send("You didnt mention the reason for mute!")
                await ctx.send(f"`{ctx.prefix}mute <member> <time> <reason> ??? Reason is a missing required argument!`")
            elif reason is not None:
                secs = time * 60 * 60
                get_role = discord.utils.get(ctx.guild.roles, name="Muted")
                await user.add_roles(get_role)
                await ctx.send(f"{user.mention} has been muted for {time}h for {reason}.")
                await asyncio.sleep(secs)
                await user.remove_roles(get_role)
                await ctx.send(f'{user.mention} has been unmuted from the guild.')
    @mute.error
    async def muteeror(self, ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("Member is a missing required argument")
            await ctx.send(f"`{ctx.prefix}mute <member> <time in minutes> <reason> ??? Member is missing!`")
        elif isinstance(error, BadArgument):
            await ctx.send("You forgot to mention the duration of the member to be muted!")
            await ctx.send(f"`{ctx.prefix}mute <member> <time in minutes> <reason> ??? time in minutes is a missing required argument!`")
        else:
             await ctx.send("A fatal error occured that resulted in failure of muting")
             await ctx.send(error)
    @commands.command()
    @commands.has_role(758694901214478347)
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        '''Unmutes The User'''
        if user == ctx.author:
            await ctx.send("You cant unmute yourself")
        elif user != ctx.author:
            get_role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.remove_roles(get_role)
            await ctx.send(f"{user.mention} has been unmuted!")
    @unmute.error
    async def unmuteeror(self, ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("Member is a missing required argument")
            await ctx.send(f"`{ctx.prefix}unmute <member>??? Member is missing!`")
        else:
            await ctx.send("A fatal error occured that resulted in failure of muting")
    @commands.command()
    @commands.has_role(758694901214478347)
    async def warn(self, ctx, member: discord.Member, *, reason):
        '''Warns The User'''
        if ctx.message.author.bot == False:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM warning WHERE guild_id = '{ctx.message.guild.id}' and user_id = '{member.id}'")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO warning(guild_id, user_id, inf, reason) VALUES(?,?,?,?)")
                val = (ctx.author.guild.id, member.id, 1, reason)
                cursor.execute(sql, val)
                db.commit()
                await ctx.send(f"**{member}** has been warned for **{reason}** and is your **first warning!!!**")
            elif result is not None:
                cursor.execute(f"SELECT user_id, inf, reason FROM warning WHERE guild_id = '{ctx.message.guild.id}' AND user_id = '{member.id}'")
                result1 = cursor.fetchone()
                inf = int(result1[1])
                conc = str(result1[2])
                count = inf + 1
                nume3 = num2words(count, to='ordinal')
                sql = ("UPDATE warning SET inf = ? , reason = ? WHERE guild_id = ? AND user_id = ?")
                val  = (inf + 1, (conc + ", " +str(reason)),str(ctx.author.guild.id), str(member.id))
                cursor.execute(sql, val)
                db.commit()
                await ctx.send(f"**{member}** has been warned for **{reason}** and is your **{nume3} warning!!!**")
    @warn.error
    async def warnerror(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        #if isinstance(error, MissingPermissions):
        #    await ctx.send("You cant warn the member! You need the following permissions: `ban member`")
        else:
            await ctx.send("A fatal error occured")

    @commands.command()
    @commands.has_role(758694901214478347)
    async def warns(self, ctx, member: discord.Member = None):
        '''Display Warns Of The User'''
        if member is None or not member.bot:
            if member is not None:
                db = sqlite3.connect("main.sqlite")
                cursor = db.cursor()
                cursor.execute(f"SELECT user_id, inf, reason FROM warning WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{member.id}'")
                result = cursor.fetchone()
                if result is None:
                    await ctx.send("This user has no warnings!")
                else:
                    embed = discord.Embed(
                        colour = ctx.author.colour
                    )
                    new_conc = []
                    await ctx.send(result[2])
                    a = result[2].split(', ')
                    for i in a:
                        new_conc.append(i)
                    user_warn = [j for j in new_conc]
                    embed.set_author(name = f"{member} Warning List")
                    embed.set_thumbnail(url =  member.avatar_url)
                    embed.add_field(name= "Name", value = f"{member}", inline=False)
                    embed.add_field(name="Number of Warnings", value= result[1], inline=False)
                    embed.add_field(name = "Warnings", value = "\n".join([a for a in user_warn]), inline=False)
                    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)
    @warns.error
    async def warnserror(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        #if isinstance(error, MissingPermissions):
        #    await ctx.send("You cant list the warns! You need the following permissions: `ban member`")
        else:
            await ctx.send("A fatal error occured")
    @commands.command()
    @commands.has_role(758694901214478347)
    async def clearwarns(self, ctx, member: discord.Member= None):
        '''Clear Warns The User'''
        if member is None:
            await ctx.send("Please mention a member")
        elif member is not None:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, inf, reason FROM warning WHERE guild_id = '{ctx.author.guild.id}' AND user_id = '{member.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("User has no warnings only to be cleared!")
            elif result is not None:
                cursor.execute(f"SELECT user_id from WARNING WHERE guild_id ='{ctx.author.guild.id}' and user_id = '{member.id}' ")
                sql = "DELETE FROM warning WHERE guild_id = ? AND user_id = ?"
                val = (ctx.author.guild.id, member.id)
                cursor.execute(sql, val)
                db.commit()
                await ctx.send(f"Warns of **{member}** having user id of **{member.id}** who had **{result[1]}** have been cleared successfully by {ctx.message.author}")
    @clearwarns.error
    async def clearwarnserror(self, ctx, error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        #if isinstance(error, MissingPermissions)
        #    await ctx.send("You dont have permission to do this!")
        else:
            await ctx.send("A fatal error occured!")

    @commands.command()
    @commands.has_role(758694901214478347)
    async def unban(self, ctx, user: int, *, reason=None):
        '''Unbans The User'''
        if ctx.message.author.guild_permissions.ban_members:
            try:
                await ctx.guild.unban(discord.Object(id=user))
                await ctx.send(f'**{self.bot.get_user(user)}** has been unbanned')
            except:
                await ctx.send(f'**{self.bot.get_user(user)}** wasnt found!')
        else:
            await ctx.send(f'{ctx.message.author.mention} You are missing the following permissions: `Ban Members`')
    @unban.error
    async def unbanerror(self,ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        #if isinstance(error, MissingPermissions):
        #    await ctx.send(f"You can't unban this member, You need the permissions `ban members`")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Bruh, You must enter the member user id to be unbanned!")
            await ctx.send(f"`{ctx.prefix}banid <member>??? Member Argument Missing!`")
        else:
            await ctx.send(f"I must be placed to a higher hierarchy to ban the member{ctx.message.author.mention}")
        
    @commands.command()
    @commands.has_role(758694901214478347)
    async def tempban(self, ctx, user: discord.Member = None, time: int=1, *, reason=None):
        '''Temp Ban The User'''
        if user is None:
            await ctx.send("You didnt mention the mention for tempban!")
            await ctx.send(f"`{ctx.prefix}tempban <member> <time> <reason> ??? Member is a missing required argument!`")
        elif user is not None:
            if reason is None:
                await ctx.send("You didnt mention the reason for tempban!")
                await ctx.send(f"`{ctx.prefix}tempban <member> <time> <reason> ??? Reason is a missing required argument!`")
            elif reason is not None:
                secs = time * 60 * 60
                await ctx.guild.ban(user=user, reason=reason)                
                await ctx.send(f"{user.mention} has been banned for {time}d for {reason}.")
                await asyncio.sleep(secs)
                await ctx.guild.unban(user=user, reason=reason)
                await ctx.send(f'{user.mention} has been unbanned from the guild.')
    @tempban.error
    async def tempbanerror(self, ctx,error):
        if isinstance(error, MissingRole):
            await ctx.send("You need to have @Staff Role to perform this functions")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("Member is a missing required argument")
            await ctx.send(f"`{ctx.prefix}temp <member> <time in days> <reason> ??? Member is missing!`")
        elif isinstance(error, BadArgument):
            await ctx.send("You forgot to mention the duration of the member to be muted!")
            await ctx.send(f"`{ctx.prefix}tempban <member> <time in days> <reason> ??? time in minutes is a missing required argument!`")
        else:
             await ctx.send("A fatal error occured that resulted in failure of tempban")
             
    @commands.command()
    @commands.is_owner()
    async def setrole(self, ctx):
        get_role = discord.utils.get(ctx.guild.roles, name="Muted")
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(get_role, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(get_role, connect=False)
        
        #await ctx.channel.set_permissions(get_role, send_messages=False)
        await ctx.send("Permission Overwrited")
        
        
def setup(bot):
    bot.add_cog(ModCog(bot))
    print("Loaded Moderation Successfully")