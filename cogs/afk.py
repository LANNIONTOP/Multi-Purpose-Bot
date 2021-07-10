import discord
from discord.ext import commands

afkdict = {}

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('AFK Cog loaded')

    @commands.Cog.listener()
    async def on_message(self, message):
        global afkdict
        
        if "/afk" in message.content.lower():
         return


        for member in message.mentions:
            if member != message.author:
                if member in afkdict:
                    afkmsg = afkdict[member]
                    embed = discord.Embed(color=0x9c84dc)
                    embed.set_author(name=f"{member.author.name} is afk with the message", icon_url=member.author.avatar_url)
                    embed.description=f"> `{afkmsg}`"

                    await message.channel.send(embed=embed)
                    
        if message.author in afkdict:
            afkdict.pop(message.author)
            embed = discord.Embed(color=0x9c84dc)
            embed.set_author(name=f"{message.author.name} is no longer afk", icon_url=message.author.avatar_url)
            embed.description=f"> `removed afk message`"
            await message.channel.send(embed=embed)



    @commands.command()
    async def afk(self, ctx, *, message):
        global afkdict
        
        if ctx.message.author in afkdict:
            afkdict.pop(ctx.message.author)
            embed = discord.Embed(color=0x9c84dc)
            embed.set_author(name=f"{message.author.name} is no longer afk", icon_url=ctx.message.author.avatar_url)
            embed.description=f"> `removed afk message`"
            embed.set_footer(text=f"{ctx.message.author.name}")
            await message.channel.send(embed=embed)

        else:
            afkdict[ctx.message.author] = message
            embed = discord.Embed(color=0x9c84dc)
            embed.set_author(name=f"{ctx.message.author.name} is afk with the message", icon_url=ctx.message.author.avatar_url)
            embed.description=f"> `{message}`"
            await ctx.send(embed=embed)



def setup(client):
    client.add_cog(AFK(client))
