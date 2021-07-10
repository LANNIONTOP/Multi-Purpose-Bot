import discord
from discord import Permissions
from discord.ext import commands
import datetime
import os
import asyncio
import pymongo
import ssl
from pymongo.uri_parser import parse_userinfo
from discord.ext.commands.errors import InvalidEndOfQuotedStringError

def is_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id 

def is_dev(ctx):
    return ctx.message.author.id == 290405378800222208 

def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 290405378800222208 

async def is_whitelisted(ctx):
      return ctx.message.author.id in welcome.find_one({ "guild_id": ctx.guild.id })["users"] or ctx.message.author.id in welcome.find_one({ "guild_id": ctx.guild.id })["commands"] or ctx.message.author.id == 290405378800222208   

MONGODB_URL = os.environ.get('mongodb+srv://pb:Andrew1224@cluster0.fumwv.mongodb.net/botdb?retryWrites=true&w=majority')
MONGODB_CERT_PATH = os.environ.get('MONGODB_CERT_PATH')

if MONGODB_CERT_PATH:
    mclient = pymongo.MongoClient(
    MONGODB_URL,
    ssl=True, 
    ssl_ca_certs=MONGODB_CERT_PATH)
else:
    mclient = pymongo.MongoClient(
    MONGODB_URL)

db = mclient[ "death" ] 
welcome = db[ "welcome" ] 

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.group(aliases=['we', 'welc'])
    async def welcome(self, ctx):
     if ctx.invoked_subcommand is None:
       return 


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @welcome.command(aliases=['msg'])
    async def message(self, ctx, *, args=None):
     if args == None:
        embed10 = discord.Embed(color=0x6c7783, title=f"welcome message", description=f"updates the welcome message to respond to users that join").add_field(name="Aliases", value="N/A", inline=True).add_field(name="Parameters", value="text", inline=True).add_field(name="Permissions", value="<:warning:818576275115081798> Manage Guild", inline=True).add_field(name="Usage", value="```Usage: welcome message <message_here>\nExample: antinuke message welcome to my server```", inline=True).set_footer(text=f"Page 1/1")
        await ctx.send(embed=embed10)
        return
   
     welcome.update_one({ "guild_id": ctx.guild.id }, { "$set": { "message": args }})
    
     embed = discord.Embed(color=0xa3eb7b)
     embed.description = f"<:approve:818583497056714783> {ctx.author.mention}: The welcome message has been set\n**Code:**\n\n```{args}```"
     await ctx.send(embed=embed)  

   

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @welcome.command(aliases=['channel'])
    async def set(self, ctx, channel: discord.TextChannel=None):
     if channel == None:
        embed11 = discord.Embed(color=0x6c7783, title=f"welcome channel", description=f"sets the channel where welcome message are sent").add_field(name="Aliases", value="set", inline=True).add_field(name="Parameters", value="channel", inline=True).add_field(name="Permissions", value="<:warning:818576275115081798> Manage Guild", inline=True).add_field(name="Usage", value="```Usage: welcome channel <channel>\nExample: antinuke channel #joins```", inline=True).set_footer(text=f"Page 1/1")
        await ctx.send(embed=embed11)
        return
   
     welcome.update_one({ "guild_id": ctx.guild.id }, { "$set": { "channel": channel.id }})
    
     embed = discord.Embed(color=0xa3eb7b)
     embed.description = f"<:approve:818583497056714783> {ctx.author.mention}: Updated <#{channel.id}> as the welcome module channel"
     await ctx.send(embed=embed) 


    @commands.guild_only()
    @welcome.command(aliases=['var', 'vars'])
    async def variables(self, ctx):
     if ctx.invoked_subcommand is None:
      embed = discord.Embed(color=0x7289da)
      embed.title=f"{ctx.prefix}welcome variables"
      embed.description=f"documentation for the the welcoming format are shown below"
      embed.add_field(name=f"variables", value="{usermention} - displays the users mention\n{server} - displays the servers name\n{user} - displays the user\n{username} - displays the users username", inline=False)
      await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @welcome.command(aliases=['settings', 'display'])
    async def status(self, ctx):
     welc = welcome.find_one({ "guild_id": ctx.guild.id })['channel']
     msg = welcome.find_one({ "guild_id": ctx.guild.id })['message']
     welcome1 = welcome.find_one({ "guild_id": ctx.guild.id })['toggle']
   
     welcc = ""
     msgg = ""

    
     welcc += f"<#{welc}>\n"
     msgg += f"{msg}"
  


    
     if welc == "None":
       welcc = f"{ctx.prefix}welcome channel #channel"

     if msg == "None":
       msgg = f"{ctx.prefix}welcome message [message]"

     if welcome1 == "Disabled":
        embed = discord.Embed(color=0x7289da)
        embed.title=f"welcome settings"
        embed.add_field(name=f"Welcome", value="Toggled Off", inline=True)
        embed.add_field(name=f"Message", value=f"Toggled Off", inline=True)
        embed.add_field(name=f"Embed", value=f"Toggled Off", inline=True)
        embed.set_footer(text=f"for more info use, '{ctx.prefix}help welcome (subcommand)'") 
        await ctx.send(embed=embed)
        return 

     else:
       embed = discord.Embed(color=0x7289da)
       embed.title=f"welcome settings"
       embed.add_field(name=f"Welcome", value=welcc, inline=True)
       embed.add_field(name=f"Message", value=f"`{msgg}`", inline=True)
       embed.add_field(name=f"Embed", value=f"N/A", inline=True)
       embed.set_footer(text=f"for more info use, '{ctx.prefix}help welcome (subcommand)'") 
       await ctx.send(embed=embed)
       return 


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @welcome.command(aliases=['filter', 'tog'])
    async def toggle(self, ctx, value: bool):
     if value:
       welcome.update_one({ "guild_id": ctx.guild.id }, { "$set": { "toggle": "Enabled" }})
       embed = discord.Embed(color=0xa3eb7b)
       embed.description = f"<:approve:818583497056714783> {ctx.author.mention}: Toggled the welcome module on"
       await ctx.send(embed=embed) 

     else:
       welcome.update_one({ "guild_id": ctx.guild.id }, { "$set": { "toggle": "Disabled" }})
       embed = discord.Embed(color=0xa3eb7b)
       embed.description = f"<:approve:818583497056714783> {ctx.author.mention}: Toggled the welcome module off"
       await ctx.send(embed=embed) 


def setup(bot):
    bot.add_cog(Welcome(bot))        