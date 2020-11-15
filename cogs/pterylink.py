from os import error, kill
from types import resolve_bases
from discord import colour
from discord.enums import Status
from discord.errors import HTTPException
from discord.ext import commands
import discord
from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.core import check, command, cooldown
from discord.ext.commands.errors import CommandInvokeError, CommandOnCooldown, MissingRequiredArgument, PrivateMessageOnly
from pydactyl import PterodactylClient
import asyncio
import sqlite3
from pydactyl import client
from pydactyl import responses
from requests.models import HTTPError

class PteroLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def addapi(self, ctx, api_token_user : str=None):
        if api_token_user is not None:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM USERCONFIGURATION WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None:
                #cursor.execute(f"SELECT api_token from userconfiguration WHERE user_id = '{ctx.author.id}'")
                sql = ("INSERT INTO userconfiguration(user_id, api_token) VALUES(?,?)")
                val = (str(ctx.author.id),str(api_token_user))
                cursor.execute(sql, val)
                db.commit()
                em = discord.Embed(colour = discord.Colour.dark_green())
                em.add_field(name= "<a:anim_check:760126713409175573> Added <a:anim_check:760126713409175573>", value= "**Token Added Successfully!!!**")
                await ctx.author.send(embed = em)
            elif result is not None and result[1] != api_token_user:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name= "<a:anim_cross:757875533030883379 Error <a:anim_cross:760126684069363712>", value= f"Hmm, Seems like there is already a token updated in the database! Either remove the existing token by typing the command `{ctx.prefix}removeapitoken` or Change the existing token by typing the command `{ctx.prefix}changeapitoken <new_api_token>`")
                await ctx.author.send(embed=em)
            elif result is not None and result[1] == api_token_user:
                em = discord.Embed(colour = discord.Colour.dark_green())
                em.add_field(name= "<a:anim_check:760126713409175573> Token Already Registered <a:anim_check:760126713409175573>", value= f"The entered token is already registered in the database! If you feel this is an error change your api with command `{ctx.prefix}changeapitoken <new_api_token>`")
            #elif result is not None and result[1] is not None:
            #    em1.add_field(name="<a:anim_check:760126713409175573> API TOKEN REGISTRATION <a:anim_check:760126713409175573> ", value = f"Type The Command {ctx.prefix}addapi <api_token> where  <api_token> is the API Token! Create your API Token in https://panel.danbot.host/account/api. If you need help on creating API, type the command {ctx.prefix}getstartedapi")
                #await ctx.author.send(embed=em1)
             #   await ctx.author.send(embed = em)
        elif api_token_user is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"**No Token Was Entered!!** Please  again by using the command `{ctx.prefix}addapi <api_token>` Create your API Token in https://panel.danbot.host/account/api. If you need help on creating API, type the command {ctx.prefix}getstartedapi", inline=False)
            await ctx.send(embed = em)
    @addapi.error
    async def addapierror(self, ctx, error):
        await ctx.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report this error: Ex00e110! ")
        await ctx.send(error)
    @commands.command()
    async def getstartedapi(self, ctx):
        em = discord.Embed(colour = discord.Colour.green())
        em.set_author(name= "Get Started Docs")
        em.add_field(name="Basic Information", value= "Hi, I am PlethoBot! With The Help of me , you can control your servers from me rather than visiting https://panel.danbot.host/ everytime!, This is the get started docs. I will help you to setup!", inline = False)
        em.add_field(name= "**__STEP 1__**", value="First Head Over to [Panel Security Settings By Click This Blue Text](https://panel.danbot.host/account/api)", inline=False)
        em.add_field(name='**__STEP 2__**', value="Select `Create New`", inline=False)
        em.add_field(name='**__STEP 3__**', value="In description field Enter Anything you want for better understanding and In Allowed IPs is optional( But Recommended) This just allows only those IP's entered in the Field To Use Your API Token", inline=False)
        em.add_field(name='**__STEP 4__**', value="Click `Create` button", inline=False)
        em.add_field(name='**__STEP 5__**', value=" Success Shows Your API Token has been created! Now click the `Key` as shown to reveal your token", inline=False)
        em.add_field(name="**__STEP 5**__", value="Copy the API token", inline= False )
        em.add_field(name="**__STEP 6**__", value="After Copying The Token, Head over to the DMs of NolesNetwork and run the command {}addapi <api_token> where <app_token> is replaced by the Token you just copied.".format(ctx.prefix), inline= False)
        em.add_field(name="**__STEP 7**__", value="Your API has been set up successfully, Type `{}myservers` to display the list of your servers".format(ctx.prefix),inline= False)

#        :
        await ctx.send(embed=em)
        
#            await ctx.author.send(embed=em)
        #:
        '''await ctx.send("**__First Picture__**")
        await ctx.send("https://imgur.com/a/uWDCeZn")
        await ctx.send("**__Second Picture__**")
        await ctx.send("https://imgur.com/a/hvPYbmc")
        await ctx.send("**__Third Picture__**")
        await ctx.send("https://imgur.com/a/eNMfsEd")
        await ctx.send("**__Fourth Picture__**")
        await ctx.send("https://imgur.com/a/uiboxZZ")
        await ctx.send("**__Fifth Picture__**")
        await ctx.send("https://imgur.com/a/i5Ywdt3")
        await ctx.send("**__Sixth Picture__**")
        await ctx.send("https://imgur.com/a/EgBGaIo")
        await ctx.send("https://imgur.com/a/tzYN1yh")
        '''
        
        #    await ctx.author.send("**__First Picture__**")
        #    await ctx.author.send("https://imgur.com/a/uWDCeZn")
        #    await ctx.author.send("**__Second Picture__**")
        #    await ctx.author.send("https://imgur.com/a/hvPYbmc")
        ##    await ctx.author.send("**__Third Picture__**")
         #   await ctx.author.send("https://imgur.com/a/eNMfsEd")
         ##   await ctx.author.send("**__Fourth Picture__**")
          #  await ctx.author.send("https://imgur.com/a/uiboxZZ")
          ##  await ctx.author.send("**__Fifth Picture__**")
         ##   await ctx.author.send("https://imgur.com/a/i5Ywdt3")
           # await ctx.author.send("**__Sixth Picture__**")
           # await ctx.author.send("https://imgur.com/a/EgBGaIo")
            #await ctx.author.send("https://imgur.com/a/tzYN1yh")
    

    @commands.command()
    async def reset(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM USERCONFIGURATION WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"Hey, Seems like you are new because No API Token was found in the database under your name and I can't reset your account if there is no account associated with the database only. Please add one by typing `{ctx.prefix}addapi <api_token_user>`")
            await ctx.author.send(embed=em)
        elif result is not None:
            em = discord.Embed(colour = discord.Colour.dark_gold())
            em.add_field(name= ":warning: Account Reset :warning:", value= f"Warning, You Have requested for the deletion of your API from the Bot Database! This action is irreversible! Proceed with Caution. Type `yes` to confirm the removal of your token from the Bot database! You just have 60 seconds to answer this! ")
            em.set_footer(text= "NOTE: Removal/Deletion Just Removes your API from The Bot Database! This doesnt delete the API token in Plethonode Panel Area!")
            await ctx.send(embed=em)
            def check(message):
                    return message.author == ctx.author and message.content.lower() == "yes"
            msg = await self.bot.wait_for('message', check=check, timeout=60)
            if (msg):
                sql = "DELETE FROM userconfiguration WHERE user_id = ?"
                val = (str(ctx.author.id),)
                cursor.execute(sql, val)
                db.commit()
                em = discord.Embed(colour = discord.Colour.dark_green())
                em.add_field(name="<a:anim_check:760126713409175573> ACCOUNT DELETED FROM BOT <a:anim_check:760126713409175573>", value = " Your account has been deleted successfully from Bot")
                await ctx.send(embed=em)
            else:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"You didnt type `yes` You may have mispelled the word!")
                await ctx.send(embed=em)
        else:
            await ctx.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report this error: Ex00e111! ")
            await ctx.send(error)
    @reset.error
    async def reseterror(self, ctx,error):
#        if isinstance(error, PrivateMessageOnly):
#            em = discord.Embed(colour = discord.Colour.dark_green())
#            em.add_field(name="<a:anim_check:760126713409175573> API REMOVAL REQUEST <a:anim_check:760126713409175573>", value = "You have requested for the removal for the API Token in the bot! Furthur Information Have Been Sent To Your DMs")
            #await ctx.send(embed=em)
            #em1 = discord.Embed(colour = discord.Colour.dark_gold())
            #em1.add_field(name= ":warning: Account Reset :warning:", value= f"Warning, You Have requested for the deletion of your API from the Bot Database! Type `{ctx.prefix}reset` again in here to reset your account")
            #em1.set_footer(text= "NOTe: Removal/Deletion Just Removes your API from The Bot Database! This doesnt delete the API token in Plethonode Panel Area!")
            #await ctx.send(embed=em1)
        await ctx.author.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report this error: Ex00e110-1! ")
        await ctx.author.send(error)

            
    @commands.command()
    async def changeapitoken(self, ctx, new_api_token: str=None):
        if new_api_token is not None:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM USERCONFIGURATION WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None and result[1] is None:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"Hey, Seems like you are new because No API Token was added only and I cant change API token if there is no token only. Please add one by typing `{ctx.prefix}addapi <api_token_user>`")
                await ctx.author.send(embed=em)
            elif result is not None:
                sql1 = ("UPDATE userconfiguration SET api_token = ? WHERE user_id = ?")
                val1 = (str(new_api_token), str(ctx.author.id))
                cursor.execute(sql1, val1)
                db.commit()
                em = discord.Embed(colour = discord.Colour.dark_green())
                em.add_field(name= "<a:anim_check:760126713409175573> Added <a:anim_check:760126713409175573>", value= "**Token Changed Successfully!**")
                await ctx.author.send(embed = em)
        else:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"You didnt enter the token!!! {ctx.prefix}changeapitoken <new_api_token> ??? new_api_token is a missing required argument")
            await ctx.author.send(embed=em)
    @changeapitoken.error
    async def changeapitokenerror(self, ctx, error):
        await ctx.author.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report this error: Ex00e111! ")
        await ctx.author.send(error)
    '''            
    @commands.command(pass_context=True)
    async def show(self, ctx):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM USERCONFIGURATION WHERE user_id = '{ctx.author.id}'")
        result = cursor.fetchone()
        token = result[1]
        if result is None:
            await ctx.send("No server")
        elif result is not None:
            client = PterodactylClient('https://gp.falixnodes.net', token)
            myservers = client.client.list_servers()
            print(myservers)
            #myservers1 = client.client.get_server('07be21d9', detail=True)
            #em = discord.Embed(colour = ctx.author.colour)
            #em.description = f"{myservers}"
            #await ctx.send(embed=em)
            #await ctx.send(result)
            #print(myservers)
            a = 0
            for i in myservers[a]['identifier']:
                :
                    await ctx.send(myservers[a]['name'])
                    await ctx.send(myservers[a]['identifier'])
                    await ctx.send(myservers[a]['limits']['memory'])
                    await ctx.send(myservers[a]['limits']['swap'])
                    await ctx.send(myservers[a]['limits']['disk'])
                    await ctx.send(myservers[a]['limits']['io'])
                    await ctx.send(myservers[a]['limits']['cpu'])
                    await ctx.send(myservers[a]['feature_limits']['databases'])
                    a+=1
                
                    pass
            #await ctx.send(result)
            #print(result)
    '''
    @commands.command(aliases = ['myservers', 'serverlist','servers'])
    @commands.cooldown(rate=1, per=120, type=BucketType.user)
    async def show(self,ctx):
        try:
            em = discord.Embed(colour = discord.Colour.green())
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM USERCONFIGURATION WHERE user_id = '{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"You aren't registered in the database! Please run the command {ctx.prefix}addapi")
                await ctx.send(embed=em)
            elif result is not None and result[1] is None:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name= "<a:anim_cross:760126684069363712> Error <a:anim_cross:760126684069363712>", value= f"You aren't registered in the database! Please run the command {ctx.prefix}addapi")
                await ctx.send(embed=em)
                
                #    await ctx.author.send(embed=em)
            elif result is not None:
                token = str(result[1])
                client = PterodactylClient('https://panel.danbot.host', token)
                myservers = client.client.list_servers()
                #myservers1 = client.servers.get_server_info(server_id='ce98995a')
                #myservers1 = client.client.get_server('1ccc3f0b', detail=True)
                #await ctx.send(myservers1)
                a = 0
                a1 = 0
                allo_id = 1
                em.set_author(name = myservers[a1]['name'])
                em.description = f"ID: {allo_id}"
                em.add_field(name = "Server UUID: ", value = myservers[a1]['identifier'])
                em.add_field(name = "Memory: ", value = myservers[a1]['limits']['memory'])
                em.add_field(name = "Swap: ", value = myservers[a1]['limits']['swap'])
                em.add_field(name = "Disk: ", value = myservers[a1]['limits']['disk'])
                em.add_field(name = "IO : ", value = myservers[a1]['limits']['io'])
                em.add_field(name = "Cpu: ", value = myservers[a1]['limits']['cpu'])
                em.add_field(name = "Databases: ", value = myservers[a1]['feature_limits']['databases'])
                current = 1
                pages2 = len(myservers)
                message = await ctx.send(f"Page {current}/{pages2}:")
                message1 = await ctx.send(embed=em)
                await message1.add_reaction("◀️")    
                await message1.add_reaction("▶️")
                def check1(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
    
                while True:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check1)
                    if str(reaction.emoji) ==  "▶️" and current != pages2:
                        current+=1
                        a1 +=1
                        allo_id +=1
                        em1 = discord.Embed(colour= discord.Colour.green())
                        em1.set_author(name = myservers[a1]['name'])
                        em1.description = f"ID: {allo_id}"
                        em1.add_field(name = "Server UUID: ", value = myservers[a1]['identifier'])
                        em1.add_field(name = "Memory: ", value = myservers[a1]['limits']['memory'])
                        em1.add_field(name = "Swap: ", value = myservers[a1]['limits']['swap'])
                        em1.add_field(name = "Disk: ", value = myservers[a1]['limits']['disk'])
                        em1.add_field(name = "IO : ", value = myservers[a1]['limits']['io'])
                        em1.add_field(name = "Cpu: ", value = myservers[a1]['limits']['cpu'])
                        em1.add_field(name = "Databases: ", value = myservers[a1]['feature_limits']['databases'])
                        await message.edit(content = f"Page {current}/{pages2}:")
                        await message1.edit(embed=em1)
                        await message1.remove_reaction(reaction, user)
    
                    elif str(reaction.emoji) == "◀️" and current > 1:
                        current-=1
                        a1-=1
                        allo_id-=1
                        em2 = discord.Embed(colour= discord.Colour.green())
                        em2.description = f"ID: {allo_id}"
                        em2.set_author(name = myservers[a1]['name'])
                        em2.add_field(name = "Server UUID: ", value = myservers[a1]['identifier'])
                        em2.add_field(name = "Memory: ", value = myservers[a1]['limits']['memory'])
                        em2.add_field(name = "Swap: ", value = myservers[a1]['limits']['swap'])
                        em2.add_field(name = "Disk: ", value = myservers[a1]['limits']['disk'])
                        em2.add_field(name = "IO : ", value = myservers[a1]['limits']['io'])
                        em2.add_field(name = "Cpu: ", value = myservers[a1]['limits']['cpu'])
                        em2.add_field(name = "Databases: ", value = myservers[a1]['feature_limits']['databases'])
    
                        await message.edit(content=f"Page {current}/{pages2}:")
                        await message1.edit(embed=em2)
                        await message1.remove_reaction(reaction, user)                    
                    else:
                        await message1.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            pass
    @show.error
    async def pageserror(self, ctx, error):
        if isinstance(error, TimeoutError):
            print("Command Timeout")
        elif isinstance(error, CommandOnCooldown):
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> Command On Cooldown <a:anim_cross:760126684069363712>", value = f"This command is curently on cooldown. Please re this command after `{round(float(error.retry_after),2)}s`. Now why is the command on cooldown: This is because, we want to reduce traffic on the bot and not make it crash!")
            await ctx.send(embed=em)
            
            #    await ctx.author.send(embed=em)
        else:
            #:
            await ctx.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report the below error")
            await ctx.send(error)
            #
            #    await ctx.author.send("A fatal error occured! Please contact the NolesNetwork Staff Team by making a ticket and report the below error")
            #    await ctx.author.send(error)
    @commands.command()
    async def start(self, ctx, serverid: int):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM userconfiguration WHERE user_id ='{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None: #FFuW4JxjmxfZrBYeC24m3PVkrDQp6U58PeTJnLYSnQLUJ65q
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstartedapi` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
            #    await ctx.author.send(embed=em)
            # await ctx.send("You didnt set any api, serverid or name. Please add one")
        elif result is not None and result[1] is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstartedapi` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
        #        await ctx.author.send(embed=em)
        elif result is not None:
            client = PterodactylClient('https://panel.danbot.host', result[1])
            id1 = client.client.list_servers()
            client.client.send_power_action(id1[serverid-1]['identifier'], 'start')
            em = discord.Embed(colour = discord.Colour.greyple())
            em.description = f"<a:anim_idle:757647720025423973> **Initializing Server Boot**"
         #   :
            mess = await ctx.send(embed=em)

            await asyncio.sleep(5)
            em1 = discord.Embed(colour = discord.Colour.green())
            em1.description = f"<a:anim_online:757647692246548510> **Server Started!**"
          #  :
            await mess.edit(embed=em1)
            
           #     await mess1.edit(embed=em1)
        else:
            #:
            await ctx.send("Invalid Name")
            
            #    await ctx.author.send("Invalid Name")
   
    @start.error
    async def starterror(self, ctx, error):
        if isinstance(error, IndexError): 
            #:
            await ctx.send("Invalid Server ID")
            
            #    await ctx.author.send("Invalid Server ID")
        elif isinstance(error, HTTPError):
           # :
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            #    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            #    await ctx.author.send(error)
        elif isinstance(error, MissingRequiredArgument):
            #:
            await ctx.send("serverid is a missing required argument")
            await ctx.send("{}start <serverid> ??? serverid is missing! Dont know how to start a server? No worries, type `{}getstarted start` to learn how to start a server!".format(ctx.prefix, ctx.prefix))
            
            #    await ctx.author.send("serverid is a missing required argument")
             #   await ctx.author.send("{}start <serverid> ??? serverid is missing! Dont know how to start a server? No worries, type `{}getstarted start` to learn how to start a server!".format(ctx.prefix, ctx.prefix))

        else:
            #:
            await ctx.send(error)
            
            #    await ctx.author.send(error)
    @commands.command()
    async def stop(self, ctx, serverid: int):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM userconfiguration WHERE user_id ='{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None: #FFuW4JxjmxfZrBYeC24m3PVkrDQp6U58PeTJnLYSnQLUJ65q
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
         #       await ctx.author.send(embed=em)
            # await ctx.send("You didnt set any api, serverid or name. Please add one")
        elif result is not None and result[1] is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
          #  :
            await ctx.send(embed=em)
            
           #     await ctx.author.send(embed=em)
        elif result is not None:
            client = PterodactylClient('https://panel.danbot.host', result[1])
            id1 = client.client.list_servers()
            client.client.send_power_action(id1[serverid-1]['identifier'], 'stop')
            em = discord.Embed(colour = discord.Colour.greyple())
            em1 = discord.Embed(colour = discord.Colour.dark_red())
            em1.description = f"<a:anim_dnd:757646711941496903> **Server Stopped**"
            #:
            await ctx.send(embed=em1)
            
            #    await ctx.author.send(embed=em1)
        else:
            #:
            await ctx.send("Invalid Name")
            
            #    await ctx.author.send("Invalid Name")
   
    @stop.error
    async def starterror(self, ctx, error):
        if isinstance(error, IndexError): 
            #:
            await ctx.send("Invalid Server ID")
            
            #    await ctx.author.send("Invalid Server ID")
        elif isinstance(error, HTTPError):
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")   
            await ctx.send(error)
            
            #    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")   
            #    await ctx.author.send(error)
        elif isinstance(error, MissingRequiredArgument):
            #:
            await ctx.send("serverid is a missing required argument")
            await ctx.send("{}start <serverid> ??? serverid is missing! Dont know how to stop a server? No worries, type `{}getstarted power` to learn how to stop a server!".format(ctx.prefix, ctx.prefix))
            
            #    await ctx.author.send("serverid is a missing required argument")
            #    await ctx.author.send("{}start <serverid> ??? serverid is missing! Dont know how to stop a server? No worries, type `{}getstarted power` to learn how to stop a server!".format(ctx.prefix, ctx.prefix))
        else:
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            #    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            #    await ctx.author.send(error)
    @commands.command()
    async def kill(self, ctx, serverid: int):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM userconfiguration WHERE user_id ='{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None: #FFuW4JxjmxfZrBYeC24m3PVkrDQp6U58PeTJnLYSnQLUJ65q
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
            #    await ctx.author.send(embed=em)
            # await ctx.send("You didnt set any api, serverid or name. Please add one")
        elif result is not None and result[1] is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
        #:
            await ctx.send(embed=em)
            
         #       await ctx.author.send(embed=em)
        elif result is not None:
            client = PterodactylClient('https://panel.danbot.host', result[1])
            id1 = client.client.list_servers()
            client.client.send_power_action(id1[serverid-1]['identifier'], 'kill')
            em = discord.Embed(colour = discord.Colour.greyple())
            em1 = discord.Embed(colour = discord.Colour.dark_red())
            em1.description = f"<a:anim_dnd:757646711941496903> **Server Killed**"
          #  :
            await ctx.send(embed=em1)
            
           #     await ctx.author.send(embed=em1)
        else:
            #:
            await ctx.send("Invalid ID")
            
            #    await ctx.author.send("Invalid ID")
   
    @kill.error
    async def starterror(self, ctx, error):
        if isinstance(error, IndexError): 
            #:
            await ctx.send("Invalid Server ID")
            
            #    await ctx.author.send("Invalid Server ID")
        elif isinstance(error, HTTPError):
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            ##    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
             #   await ctx.author.send(error)
        elif isinstance(error, MissingRequiredArgument):
            #:
            await ctx.send("serverid is a missing required argument")
            await ctx.send("{}start <serverid> ??? serverid is missing! Dont know how to kill a server? No worries, type `{}getstarted power` to learn how to kill a server!".format(ctx.prefix, ctx.prefix))
            
            #    await ctx.author.send("serverid is a missing required argument")
            #    await ctx.author.send("{}start <serverid> ??? serverid is missing! Dont know how to kill a server? No worries, type `{}getstarted power` to learn how to kill a server!".format(ctx.prefix, ctx.prefix))
        else:
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
           #     await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
           #     await ctx.author.send(error)

    @commands.command()
    async def restart(self, ctx, serverid: int):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM userconfiguration WHERE user_id ='{ctx.author.id}'")
        result = cursor.fetchone()
        if result is None: #FFuW4JxjmxfZrBYeC24m3PVkrDQp6U58PeTJnLYSnQLUJ65q
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
           #     await ctx.author.send(embed=em)
            # await ctx.send("You didnt set any api, serverid or name. Please add one")
        elif result is not None and result[1] is None:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
            #:
            await ctx.send(embed=em)
            
            #    await ctx.author.send(embed=em)#await ctx.send(embed=em)
        elif result is not None:
            client = PterodactylClient('https://panel.danbot.host', result[1])
            id1 = client.client.list_servers()
            client.client.send_power_action(id1[serverid-1]['identifier'], 'restart')
            em = discord.Embed(colour = discord.Colour.greyple())
            em1 = discord.Embed(colour = discord.Colour.green())
            em1.description = f"<a:anim_check:760126713409175573> **Server Restart Command Sent**"
            #:
            await ctx.send(embed=em1)
            
            #    await ctx.author.send(embed=em1)
        else:
            #:
            await ctx.send("Invalid ID")
            
            #@#@    await ctx.author.send("Invalid ID")
   
    @restart.error
    async def starterror(self, ctx, error):
        if isinstance(error, IndexError):
            #:
            await ctx.send("Invalid Server ID")
            
            #    await ctx.author.send("Invalid Server ID")
        elif isinstance(error, HTTPError):
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            #    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
           #     await ctx.author.send(error)
        elif isinstance(error, MissingRequiredArgument):
            #:
            await ctx.send("serverid is a missing required argument")
            await ctx.send("{}start <serverid> ??? serverid is missing! Dont know how to restart a server? No worries, type `{}getstarted power` to learn how to restart a server!".format(ctx.prefix, ctx.prefix))
            
           #@     await ctx.author.send("serverid is a missing required argument")
           #     await ctx.author.send("{}start <serverid> ??? serverid is missing! Dont know how to restart a server? No worries, type `{}getstarted power` to learn how to restart a server!".format(ctx.prefix, ctx.prefix))
        else:
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            #    await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            #    await ctx.author.send(error)

    @commands.command()
    async def send(self, ctx, serverid: int, *,console_cmd : str):
        if serverid is not None:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM userconfiguration WHERE user_id ='{ctx.author.id}'")
            result = cursor.fetchone()
            if result is None: #FFuW4JxjmxfZrBYeC24m3PVkrDQp6U58PeTJnLYSnQLUJ65q
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
                #:
                await ctx.send(embed=em)
                
                #    await ctx.author.send(embed=em)
                # await ctx.send("You didnt set any api, serverid or name. Please add one")
            elif result is not None and result[1] is None:
                em = discord.Embed(colour = discord.Colour.dark_red())
                em.add_field(name = f"<a:anim_cross:760126684069363712> No API Error <a:anim_cross:760126684069363712>", value = "You didnt set an API Token Only! Please set one by typing `{}addapi <api_token>` or type `{}getstarted` to learn how to get an API Token".format(ctx.prefix, ctx.prefix))
                #:
                await ctx.send(embed=em)
                
                #@#    await ctx.author.send(embed=em)
            elif result is not None:
                client = PterodactylClient('https://panel.danbot.host', result[1])
                id1 = client.client.list_servers()
                client.client.send_console_command(id1[serverid-1]['identifier'], console_cmd)
                #client.client.send_power_action(id1[serverid-1]['identifier'], 'restart')
                em = discord.Embed(colour = discord.Colour.greyple())
                em1 = discord.Embed(colour = discord.Colour.green())
                em1.description = f"<a:anim_check:760126713409175573> **Server Command Sent!**"
                #:
                await ctx.send(embed=em1)
                
                #    await ctx.author.send(embed=em1)
            else:
                #:
                await ctx.send("Invalid ID")
                
                #    await ctx.author.send("Invalid ID")
        else:
            em = discord.Embed(colour = discord.Colour.dark_red())
            em.add_field(name= "<a:anim_cross:757875533030883379 Command Failed <a:anim_cross:760126684069363712>", value= f"Command Failed, You didnt enter Bot Server Unique Id! Don't Know how to use this command? Well Don't worry! Just type `{ctx.prefix}getstarted send` to learn how to use send command ")
            await ctx.send(embed=em)

    @send.error
    async def starterror(self, ctx, error):
        if isinstance(error, IndexError): 
            #:
            await ctx.send("Invalid Server ID")
            
           #     await ctx.author.send("Invlid Server ID")
        elif isinstance(error, HTTPError):
                #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
           #     await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
           #     await ctx.author.send(error)
        elif isinstance(error, MissingRequiredArgument):
            #:
            await ctx.send("console_command is a missing required argument")
            await ctx.send("{}send <serverid> <console_command ??? console_command is missing! Dont know how to send custom command to your server? No worries, type `{}getstarted send` to learn how to send a custom command to your server!".format(ctx.prefix, ctx.prefix))
            
            ##    await ctx.author.send("console_command is a missing required argument")
             #  await ctx.author.send("{}send <serverid> <console_command ??? console_command is missing! Dont know how to send custom command to your server? No worries, type `{}getstarted send` to learn how to send a custom command to your server!".format(ctx.prefix, ctx.prefix))
        else:
            #:
            await ctx.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            await ctx.send(error)
            
            #   await ctx.author.send("A fatal error occured! Please contact NolesNetwork Staff Team and report the below error:")
            #    await ctx.author.send(error)
def setup(bot):
    bot.add_cog(PteroLink(bot))
    print("Loaded PteroLink Successfully")