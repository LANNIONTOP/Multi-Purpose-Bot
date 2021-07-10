import discord
from discord import Permissions
from discord.ext import commands
import datetime
import asyncio
import json
from discord.ext.commands.errors import InvalidEndOfQuotedStringError



class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.group()
    async def prefix(self, ctx):
      if ctx.invoked_subcommand is None:
        embed = discord.Embed(color=0x9c84dc)
        embed.description=f"Prefix: `{ctx.prefix}`"
        embed.set_footer(text=f"guardianangel.xyz • 130 commands") 
        await ctx.send(embed=embed)
 

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @prefix.command(aliases=['unsp', 'unprefixchange'])
    async def unset(self, ctx):
     with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

     prefixes[str(ctx.guild.id)] = '/'
     with open('prefixes.json', 'w') as f:

        json.dump(prefixes, f, indent=4)
        await ctx.send(f'Prefix has been unset to / 👍')


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @prefix.command(aliases=['sp', 'setprefix'])
    async def set(self, ctx, prefix):
     with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

     prefixes[str(ctx.guild.id)] = prefix
     with open('prefixes.json', 'w') as f:

        json.dump(prefixes, f, indent=4)
        await ctx.send(f'Prefix has been set to {prefix} 👍')


    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @prefix.command()
    async def settings(self, ctx):
        embed = discord.Embed(color=0x9c84dc)
        embed.description=f"Below is the current prefix settingss for {ctx.guild.name}\n\n> Status: <:check:809419103080677436>\n > Server Owner: {ctx.guild.owner}"
        embed.add_field(name=f"prefix", value=f'`{ctx.prefix}`', inline=True)
        embed.set_footer(text=f"aliases: p, prefix • 3 commands") 
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Prefix(bot))         
