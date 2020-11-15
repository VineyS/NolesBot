import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
default = 'en'
from googletrans import Translator
from typing import Optional
class GoogleTranslateCog(commands.Cog, name= 'Google Translate'):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    async def translate(self, ctx , destin, *,text_conv):
        try:
            embed = discord.Embed(
            colour = ctx.author.colour
            )
            translator =  Translator()
            source  = translator.translate(text_conv).src
            conv = translator.translate(text_conv, dest=destin).text
            embed.set_author(name= "Google Translate")
            embed.description = f"Translated from {source} to {destin}: {conv}"
            embed.set_footer(text=f"Requested By: {ctx.author}")
            await ctx.send(embed=embed)
        except:
            embed2 = discord.Embed(
            colour = ctx.author.colour
            )
            await ctx.send("Improper language format Code, Please check the below example and the link out")
            embed2.set_author(name="Help")
            embed2.add_field(name="Command", value=f"Command Usage: {ctx.prefix}translate <language_code> <text to be translated>", inline= False)
            embed2.add_field(name="Example",value =f"`Ex: {ctx.prefix}translate en Bonjour`----> here en = english, which tells the bot to translate the text `Bonjour` to english",inline=False)
            embed2.add_field(name="Result", value = f"`Result: Translated from fr to en: Hello` ----> fr is french as the bot detect the language inputted",inline=False)
            embed2.add_field(name="Language Codes", value =f"https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code")
            await ctx.send(embed=embed2)
    @translate.error
    async def transerror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            embed1 = discord.Embed(
            colour = ctx.author.colour
            )

            await ctx.send(f"Seems like improper command usage!")
            embed1.set_author(name="Command Usage")
            embed1.add_field(name="Command", value=f"Command Usage: {ctx.prefix}translate <language_code> <text to be translated>", inline= False)
            embed1.add_field(name="Example",value =f"`Ex: {ctx.prefix}translate en Bonjour`----> here en = english, which tells the bot to translate the text `Bonjour` to english",inline=False)
            embed1.add_field(name="Result", value = f"`Result: Translated from fr to en: Hello` ----> fr is french as the bot detect the language inputted",inline=False)
            embed1.add_field(name="Language Codes", value =f"https://meta.wikimedia.org/wiki/Template:List_of_language_names_ordered_by_code")
            await ctx.send(embed=embed1)
        elif isinstance(error, MissingPermissions):
            await ctx.send(f"I need the following permissions to run this command: `Embed Links`")
        #elif isinstance(error, ValueError):




def setup(bot):
    bot.add_cog(GoogleTranslateCog(bot))
    print("Loaded Google Translate Successfully")
