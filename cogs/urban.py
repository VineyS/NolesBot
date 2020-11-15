import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure, MissingPermissions, MissingRequiredArgument
import asyncio
import datetime
import time
import urbandict
class UrbanCog(commands.Cog, name="Urban Dictionary"):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def urban(self, ctx, *,word_search):
        '''Urban Dictionary'''
        embed = discord.Embed(
        colour = ctx.author.colour
        )
        common_words=[]
        definition=[]
        examples=[]
        category=[]
        a= ""
        c= ""
        try:
            for i in urbandict.define(word_search):
                if i['word']:
                    common_words.append(i['word'])
                if i['def']:
                    definition.append(i['def'])
                if i['example']:
                    examples.append(i['example'])
                if i['category']:
                    category.append(i['category'])
            for j in common_words:
                a+=j+", "
            kall = [k for k in definition]
            dall = [d for d in examples]
            embed.set_author(name = f"Urban Dictionary - {word_search}")
            embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar_url)
            embed.add_field(name="Possible Words Related", value= f"`{a}`",inline=False)
            embed.add_field(name="Possible Meanings", value= f"`{' '.join([k for k in kall])}`",inline=False)
            embed.add_field(name="Examples For The Word", value= f"`{' '.join([d for d in dall])}`",inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Hmm, the word you are looking for is not found!")
    @urban.error
    async def urbanerror(self,ctx,error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Invalid Command! You didnt enter the word to be searched!")
            await ctx.send(f"`{ctx.prefix}urban <word> ??? Word Argument is Missing`)")




def setup(bot):
    bot.add_cog(UrbanCog(bot))
    print("Loaded Urban Dictionary Successfully")