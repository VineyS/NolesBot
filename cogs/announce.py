import asyncio
import discord
import platform
from yaml import load, dump
import yaml
with open("channels.yaml", encoding='utf-8') as file: #load all channels
    data = load(file)
    channels = data["channels"]
from discord.ext import commands
class Announce(commands.Cog, name='Leave'):
    def __init__(self, bot):
        self.bot=bot

    
    @commands.command(brief='ann [message]')
    async def announce(self, ctx, *,message : str): #announcement command
            print(str(message))
            if ctx.message.author.guild_permissions.administrator: #compare usernames
                await ctx.send('User Authenticated. The User Running this command has permissions: `Administrator`')
                try:
                    for chan in channels:
                        try:
                            channel = self.bot.get_channel(chan)
                            info = discord.Embed(title='Announcement!', description=str(message), colour=discord.Colour.blue())
                            info.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                            info.set_footer(text="play.noles-network.cf", icon_url=ctx.guild.icon_url)
                            await channel.send(embed=info)
                            await ctx.send("Announced Successfully")
                        except Exception as e:
                                await ctx.send(e)
                                await ctx.send("Error: " + str(chan))
                except Exception as e:
                        await ctx.send(e)

    @commands.command(brief='Add to update list')
    async def addtolist(self, ctx):
            if ctx.message.author.guild_permissions.administrator: #does user have admin rights?
                    ad_ch = ctx.message.channel.id #get channel id

                    with open("channels.yaml", encoding='utf-8') as file: #load all channels in list
                            datachan = load(file)
                    if ad_ch in datachan["channels"]: #channel already in update list
                            await ctx.send('Already in update list')
                    else: #channel not in update list
                        datachan["channels"].append(ad_ch) #add channel
                        channels.append(ad_ch)

                        with open('channels.yaml', 'w') as writer: #save new file
                            yaml.dump(datachan, writer)

                        await ctx.send('Added channel')
            else:
                await ctx.send('You are not allowed to use this command')

    @commands.command(brief='Remove from update list')
    async def removefromlist(self, ctx):
            if ctx.message.author.guild_permissions.administrator: #does user have admin rights?

                    re_ch = ctx.message.channel.id #get channel id

                    with open("channels.yaml", encoding='utf-8') as file: #load other channels
                            datachan = load(file)
                    try:
                        datachan["channels"].remove(re_ch) #remove channel
                        channels.remove(re_ch)

                        with open('channels.yaml', 'w') as writer: #save new file
                            yaml.dump(datachan, writer)

                        await ctx.send('Removed channel')
                    except:
                        await ctx.send('An error occured :|')
            else:
                await ctx.send('You are not allowed to use this command')


def setup(bot):
    bot.add_cog(Announce(bot))
    print("Loaded Announce Successfully")