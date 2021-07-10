# Modules
import datetime
import discord
import shelve
import os
import asyncio
import os 
import discord 
from discord import client  
import asyncpg 
import os
import json
import sys
import os.path
import random
import colorama
import math
import modules
import config
start_time = datetime.datetime.utcnow()
from discord.ext import commands
from colorama import Fore, Style
from colorama import Fore as C
import shelve
import asyncio
import colorama
import os.path
import aiohttp
import requests
from bs4 import BeautifulSoup as bs4
import io
import math
import re
import arg
from discord.ext import commands
import discord
import json
import random
import os
from colorama import Fore
from colorama import Fore as C
import shelve 

# cog(s)
from cogs.Prefix import Prefix
from cogs.giveaway import Giveaway
from cogs.moderation import Moderation
from cogs.snipe import Snipe
from cogs.fun import Fun
from cogs.music import Music
from cogs.welcome import Welcome

#databases
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord_webhook import DiscordWebhook, DiscordEmbed
# Checks

def is_allowed(ctx):
    return ctx.message.author.id == 760649628533784586
    
def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 760649628533784586

intents = discord.Intents.default()
intents.members = True
intents.guilds = True


async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(database="database", user="username", password="password")

client = commands.Bot(command_prefix =commands.when_mentioned_or('?'), intents = intents, help_command = None )

# cog(s)
client.add_cog(Giveaway(client))
client.add_cog(Moderation(client))
client.add_cog(Snipe(client))
client.add_cog(Fun(client))
client.add_cog(Music(client))
client.add_cog(Welcome(client))
client.add_cog(Prefix(client))

async def keep_db_open():
	while True:
		await asyncio.sleep(0.1)
		global db
		db = shelve.open(filename='whitelisted')

@client.listen("on_guild_join")
async def update_db(guild):
	"""
	This coroutine updates the database when the bot
	is added to a new server
	"""
	if str(guild.id) not in db:
		db[str(guild.id)] = []


@client.command(aliases=["clearwld", "clearwl"])
@commands.check(is_server_owner)
async def clearwhitelist(ctx):
	if db[str(ctx.guild.id)] == []:
		clearwl = discord.Embed(
		    description=
		    "there are no whitelisted users!")
		await ctx.send(embed=clearwl)
	else:
		copy = db[str(ctx.guild.id)]
		copy.clear()
		db[str(ctx.guild.id)] = copy
		db.close()
		clrd = discord.Embed(
		    description=
		    f"no more whitelisted users!"
		)
		await ctx.send(embed=clrd)

@client.command(aliases=['wld'], hidden=True)
async def whitelisted(ctx):
	if str(ctx.author.id) in db[str(ctx.guild.id)]:
		try:
			embed = discord.Embed(title="Whitelisted:")
			embed.description = "\n".join(
			    str(client.get_user(id=int(user_id)))
			    for user_id in db[str(ctx.guild.id)])
			embed.set_footer(text=ctx.guild.name)
			embed.set_thumbnail(url=ctx.guild.icon_url)
			await ctx.send(embed=embed)
		except KeyError:
			wld = discord.Embed(
			    description=
			    "there are no whitelisted users!")
			await ctx.send(embed=wld)
	else:
		wldonly = discord.Embed(
		    description=
		    "you have to be whitelisted to see whitelisted users!"
		)
		await ctx.send(embed=wldonly)

@client.command(aliases=['wl'], hidden=True)
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.Member = None):
	if user is None:
		embed = discord.Embed(
		    description=
		    "mention a user to whitelist!"
		)
		await ctx.send(embed=embed)
		return
	if str(ctx.guild.id) not in db:
		db[str(ctx.guild.id)] = []
	if str(user.id) not in db[str(ctx.guild.id)]:
		copy = db[str(ctx.guild.id)]
		copy.append(str(user.id))
		db[str(ctx.guild.id)] = copy
		db.close()
	else:
		wlwl = discord.Embed(
		    description=
		    "the user you mentioned is already whitelisted!"
		)
		await ctx.send(embed=wlwl)
		return
	wl = discord.Embed(
	    description=
	    f"{user} is now whitelisted!")
	await ctx.send(embed=wl)

@whitelist.error
async def whitelist_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		embed = discord.Embed(
		    descriptio=
		    "only server owner can whitelist!"
		)
		await ctx.send(embed=embed)

@client.command(aliases=['dwl','bl'], hidden=True)
@commands.check(is_server_owner)
async def blacklist(ctx, user: discord.User = None):
	if user is None:
		embed = discord.Embed(
		    description=
		    "you need to mention a user to blacklist!"
		)
		await ctx.send(embed=embed)
		return
	if str(user.id) not in db[str(ctx.guild.id)]:
		dwl = discord.Embed(
		    description=
		    f"{user} was never whitelisted!"
		)
		await ctx.send(embed=dwl)
	else:
		copy = db[str(ctx.guild.id)]
		copy.remove(str(user.id))
		db[str(ctx.guild.id)] = copy
		db.close()
		uwl = discord.Embed(
		    description=
		    f"{user} is now off whitelist"
		)
		await ctx.send(embed=uwl)

@blacklist.error
async def blacklist_error(ctx, error):
	if isinstance(error, commands.CheckFailure):
		embed = discord.Embed(
		    description=
		    "only server only can blacklist!"
		)
		await ctx.send(embed=embed)

# Help command
@client.command(aliases=['h','Help'], pass_context=True)
async def help(ctx, category=None):
  if category == None:
    embed = discord.Embed(description="Usage: ```;help category```\n\n*Categorys:*\n> `mod`\n> `utility`\n> `info`\n> `antinuke`\n> `misc`", color=0x36393F)
  # if footer == None:
   # embed = discord.embed(description="japan on top",color=0x36393F)
    await ctx.send(embed=embed)
    return
  elif category == "mod":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="ban - unban", value=f"```;ban/unban\nbans/unbans mentioned member```", inline=False)
    em.add_field(name="kick", value=f"```;kick\nkicks mentioned member```", inline=False)
    em.add_field(name="mute - unmute", value=f"```;mute/unmute\nmutes/unmutes mentioned member```", inline=False)
    em.add_field(name="lock - unlock", value=f"```;lock/unlock\nlocks/unlocks channel commamd used in```", inline=False)
    em.add_field(name="warn", value=f"```;warn\nwarns mentioned member```", inline=False)
    message = await ctx.send(embed=em)
    return
  elif category == "util":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="serverinfo", value=f"```;serverinfo\nshows info about server```", inline=False)
    em.add_field(name="whois", value=f"```;whois\nshows info about user```", inline=False)
    em.add_field(name="avatar", value=f"```;av\nshows users avatar```", inline=False)
    em.add_field(name="nuke", value=f"```;nuke\nnukes channel```", inline=False)
    em.add_field(name="purge", value="```;purge\npurges {amount} of messages```", inline=False)
    em.add_field(name="userinfo", value="```;userinfo\nshows info on mentioned user```")
    em.add_field(name="serverinfo", value=f"```;serverinfo\nshows info on server```", inline=False)
    message = await ctx.send(embed=em)
    return
  elif category == "antinuke":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="whitelist", value=f"```;whitelist\nallows a user to bypass the antinuke module```", inline=False)
    em.add_field(name="dewhitelist", value=f"```;dewhitelist\nremoves a user from the whitelist so they cant bypass antinuke modules```", inline=False)
    em.add_field(name="whitelisted", value=f"```;whitelisted\nshows every user whitelisted in the guild```", inline=False)
    em.add_field(name="clearwl", value=f"```;clearwl\nremoves every user from the whitelist```", inline=False)
    em.add_field(name="setup", value=f"```;setup\nshows more info on the antinuke & the purposes of it```", inline=False)
    em.add_field(name="unbanall", value="```;unbanall\nmass unbans every banned user in the guild```", inline=False)
    message = await ctx.send(embed=em)
    return
  elif category == "server":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="serverinfo", value=f"```>serverinfo\ndisplays server information```", inline=False)
    em.add_field(name="whois", value=f"```>whois\ndisplays info on the mentioned user```", inline=False)
    em.add_field(name="roleinfo", value=f"```>roleinfo\ndisplays info on the mentioned user```", inline=False)
    em.add_field(name="avatar", value=f"```>avatar\nsends the mentioned user avatar inside of an embed```", inline=False)
    em.add_field(name="servericon", value=f"```>servericon\nsends the current guilds icon```", inline=False)
    em.add_field(name="banner", value=f"```>banner\nsends the current guilds server banner```", inline=False)
    message = await ctx.send(embed=em)
    return
  elif category == "misc":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="giveaway", value=f"```&giveaway\ncreates a giveaway with set paramaters```", inline=False)
    em.add_field(name="servers", value=f"```&servers\nshows all the severs wrls is currently in```", inline=False)
    em.add_field(name="mute - unmute", value=f"```&snipe\nshows the last deleted message```", inline=False)
    em.add_field(name="esnipe", value=f"```&esnipe\nshows last edited message```", inline=False)
    em.add_field(name="ping", value=f"```&ping\nshows the current ping of the bot```", inline=False)
    message = await ctx.send(embed=em)
    return
  elif category == "music":
    em = discord.Embed(description="", color=0x36393F, timestamp=ctx.message.created_at)
    em.add_field(name="join", value=f"```&join\njoins authors vc```", inline=False)
    em.add_field(name="play", value=f"```&play\nplays song entered by auhtor```", inline=False)
    em.add_field(name="pause", value=f"```&pause\npauses current song```", inline=False)
    em.add_field(name="resume", value=f"```&resume\nresumes current song```", inline=False)
    em.add_field(name="stop", value=f"```&stop\nstops current song```", inline=False)
    em.add_field(name="skip", value=f"```&skip\nskips current song```", inline=False)
    em.add_field(name="queue", value=f"```&queue\nshows your songs queued```", inline=False)
    em.add_field(name="shuffle", value=f"```&shuffle\nshuffles the queue```", inline=False)
    em.add_field(name="remove", value=f"```&remove\nremove a song from the queue```", inline=False)
    em.add_field(name="syt", value=f"```&syt\nsearchs for it on youtube```", inline=False)
    message = await ctx.send(embed=em)

# Clear command
@client.command(
aliases = ["purge"]
)
@commands.guild_only()
@commands.bot_has_guild_permissions(manage_messages = True )
@commands.has_guild_permissions(manage_messages = True )
@commands.cooldown(rate = 3, per = 25.0, type = BucketType.channel)
async def clear(ctx, amount = 0):
	await ctx.message.delete()
	if amount == 0:
		await ctx.send(
		"Please provide an amount of messages to delete."
		)
	elif amount == 1:
		deleted = await ctx.channel.purge(limit = amount )
		await ctx.channel.send(content ="{} message has been deleted.".format(len(deleted ) ), delete_after = True )
	else:
		deleted = await ctx.channel.purge(limit = amount )
		await ctx.channel.send(content ="{} messages have been deleted.".format(len(deleted ) ), delete_after = True )

# error handler for clear command
@clear.error
async def clear_command_error(ctx, error):
	if isinstance(
		error,
		commands.CheckFailure
	):
		await ctx.send("You must have Manage Messages permission to execute that command")
	else:
		await ctx.send(error)

# activity status loop
async def status_task():
	while True:
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"To add me use {client.command_prefix}invite"))
		await asyncio.sleep(10)
		await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Online & Protecting Servers!"))
		await asyncio.sleep(10)
		servers = client.guilds
		servers.sort(key=lambda x: x.member_count, reverse=True)
		y = 0
		for x in client.guilds:
			y += x.member_count
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Over {y}+ Users!"))
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Over {len(client.guilds)}+ Servers!",url='https://www.twitch.tv/wtf'))
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Join The Support Server For Any Help!"))
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"For more info use >help"))
			await asyncio.sleep(10)
			await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Add me to your server for protection!"))
			await asyncio.sleep(10)


@client.event
async def on_ready():
  print(C.LIGHTRED_EX + f'''

██╗    ██╗██████╗ ██╗     ██████╗ 
██║    ██║██╔══██╗██║     ██╔══██╗
██║ █╗ ██║██████╔╝██║     ██║  ██║
██║███╗██║██╔══██╗██║     ██║  ██║
╚███╔███╔╝██║  ██║███████╗██████╔╝
 ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═════╝ 
                                  
                     {Fore.LIGHTRED_EX}[{Fore.WHITE}W{Fore.LIGHTRED_EX}]{Style.RESET_ALL} Japan Anti-Nuke
                     {Fore.LIGHTRED_EX}[{Fore.WHITE}R{Fore.LIGHTRED_EX}]{Style.RESET_ALL}Coded by static#4911
                     {Fore.LIGHTRED_EX}[{Fore.WHITE}L{Fore.LIGHTRED_EX}]{Style.RESET_ALL}{client.user.name}#{client.user.discriminator} Is Connected & Watching!
                     {Fore.LIGHTRED_EX}[{Fore.WHITE}D{Fore.LIGHTRED_EX}]{Style.RESET_ALL}The Prefix Is & 
''')
  client.loop.create_task(
	keep_db_open()

	)
  await client.change_presence(
    status=discord.Status.idle,
    activity=discord.Activity(
      type=discord.ActivityType
      .watching,
      name=f"from japan"))


@client.listen("on_guild_join")
async def static(guild):
	channel = guild.text_channels[0]
	rope = await channel.create_invite(unique=True)
	me = client.get_user(843219488743751690)
	await me.send("I have been added to:")
	await me.send(rope)

@client.command(pass_contex=True)        
async def userinfo(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = ctx.author if not member else member

    roles = [role for role in member.roles]

    embed = discord.Embed(
        colour=0x2f3136)

    embed.set_author(name=f"User-Info")
    embed.add_field(name="Account Name", value=f"{member}", inline=False)
    embed.add_field(name="Server Nickname", value=member.display_name, inline=False)
    embed.add_field(
        name="Account Creation Date",
        value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(
        name="Member Joined At",
        value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
    embed.add_field(
        name=f"Roles({len(roles)})",
        value=" ".join([role.mention for role in roles]), inline=False)
    embed.set_image(url=member.avatar_url)
    embed.add_field(name="Bot Detection", value=member.bot, inline=False)
    embed.set_footer(text=f"wrld")
    await ctx.send(embed=embed)


@client.command
async def shardinfo(self, ctx):
        """Get information about the current shards."""
        content = discord.Embed(title=f"Running {len(self.bot.shards)} shards")
        for shard in self.bot.shards.values():
            content.add_field(
                name=f"Shard [`{shard.id}`]"
                + (" :point_left:" if ctx.guild.shard_id == shard.id else ""),
                value=f"```Connected: {not shard.is_closed()}\nHeartbeat: {shard.latency * 1000:.2f} ms```",
            )

        await ctx.send(embed=content)

@client.command()
async def ping(ctx):
  await ctx.message.delete()
  embed = discord.Embed(title=f"API Latency is {round(client.latency * 1000)}ms", color=0x2f3136)
  await ctx.send(embed=embed)

@client.command()
async def insult(ctx):
    """Says something mean about you."""
    await ctx.send(ctx.message.author.mention + " " + random.choice(config.insults))  # Mention the user and say the insult


@client.command()
async def uptime(ctx): 
    await ctx.message.delete()
    uptime = datetime.datetime.utcnow() - start_time
    uptime = str(uptime).split('.')[0]
    await ctx.send(f'```'+uptime+'```')

@client.command(pass_contex=True)
async def info(ctx):
    embed = discord.Embed(title="japans info", description="[Invite](https://discord.com/oauth2/authorize?client_id=827109999880568832&permissions=8&scope=bot)  [Support](https://discord.gg/nyc) Or Dm static#4911", color=0x36393F)
   
    embed.add_field(name="**Server & Member count**", value=f"Total Guilds: {len(client.guilds)}\nTotal Users: {len(client.users)}")
    embed.add_field(name="**Prefix**", value=f"Default: &")
    embed.add_field(name="**Library**", value="Discord.py")
    embed.add_field(name="**Developers**", value="<@843219488743751690>")
    embed.add_field(name="**Latency**", value=f"{round(client.latency * 1000)}")
    embed.add_field(name="**Version**", value="0.10")
    embed.add_field(name="**Shard**",
    value=f"Shard 3 | {len(client.users)} Users")
    embed.set_footer(text=f"unwizzable | japan on top")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Command not found! Do &help for a list of commands.")

@client.command()
async def invite(ctx):
  await ctx.message.delete()
  embed = discord.Embed(title="japan",color=0x36393F)
  embed.add_field(name="invite japan", value="[Click Here](https://discord.com/oauth2/authorize?client_id=827109999880568832&permissions=8&scope=bot)", inline=False)
  await ctx.send(embed=embed)

@client.command(aliases = ["so", "removeslowmode", "offslowmode"])
@commands.has_permissions(manage_channels=True)
async def slowmodeoff(ctx):
    await ctx.channel.edit(slowmode_delay=0)

    so = discord.Embed(description="slowmode is now removed", color=0x36393F)
    await ctx.send(embed=so)  

@commands.has_permissions(kick_members=True)
@client.command(pass_contex=True)
async def kick(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send('No User Mentioned')
        else:
            await channel.send("Kicked")
            await member.kick()


@client.command(aliases = ["slowmodeon", "slowmodeset", "onslowmode"])
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
  if seconds > 21600:
    await ctx.send('Number is too large. You can only have a maximum time of `21600` seconds (6 Hours)')
  else:
    await ctx.channel.edit(slowmode_delay=seconds)
    
    so = discord.Embed(description= f"slowmode set {seconds} seconds.", color=0x36393F)

    await ctx.send(embed=so)

@client.command(aliases=['Lock'])
@commands.has_guild_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel=None):
  channel = channel or ctx.channel
  if ctx.guild.default_role not in channel.overwrites:
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
      }
    await channel.edit(overwrites=overwrites)
    embed = discord.Embed(title = f"Sucessfully locked **{channel.name}**")
    await ctx.send(embed=embed)
  elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
      overwrites = channel.overwrites[ctx.guild.default_role]
      overwrites.send_messages = False
      await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
      embed = discord.Embed(description = f"Successfully locked **{channel.name}**", color=0x36393F)
      await ctx.send(embed=embed)

@client.command(aliases=['Unlock'])
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrites = channel.overwrites[ctx.guild.default_role]
    overwrites.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
    embed = discord.Embed(description = f"Successfully unlocked **{channel.name}**", color=0x36393F)
    message = await ctx.send(embed=embed)
    
@commands.has_permissions(ban_members=True)
@client.command(pass_contex=True)
async def ban(ctx, member: discord.Member=None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send('No User Mentioned')
        else:
            await channel.send("Banned")
            await member.ban() 

@client.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
   """This will mute user from messaging"""        
   guild = ctx.guild
   mutedRole = discord.utils.get(guild.roles, name="wrld mute")
   if not mutedRole:
     mutedRole = await guild.create_role(name="wrld mute")

   for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

   await member.edit(roles=[])       
   await member.add_roles(mutedRole, reason=reason)
   message = await ctx.send(f"Successfully Muted **{member.mention}** for **{reason}**")
   await member.send(f"You were muted in **{guild.name}** **{reason}**")

@client.command()
async def setup(ctx):
  await ctx.message.delete()
  embed = discord.Embed(color=0x36393F)
  embed.add_field(name="Get Started With wrld", value="wrlds's anti-nuke is one of the most reliable and safe anti-nukes put on discord. With wrld, you can stop raiders, nukers, and people out to harm your server with its key features you can view by visiting `;anti`. To whitelist a user from Protection's anti-nuke features, you must say `&whitelist [@user]`, but be aware that wrld will take **zero** action towards what they decide to do to and with your server. Logs are automatically set up so there's nothing to worry about.", inline=False) 
  embed.set_footer(text=f"Requested By {ctx.author}")
  await ctx.send(embed=embed)

@client.command()
async def av(ctx, *, member: discord.Member = None):
  member = ctx.author if not member else member
  embed = discord.Embed(
    title=f"{member.name}'s Avatar", color=0x2f3136)
  embed.set_image(url=member.avatar_url)
  embed.set_footer(text=f"Requested By {ctx.author}")
  await ctx.send(embed=embed)

@client.command(aliases=["si"])
async def serverinfo(ctx):
  await ctx.message.delete()
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  roles = str(ctx.guild.roles)

  icon = str(ctx.guild.icon_url)
   
  embed = discord.Embed(
      title=name + " Server Information",
      description=description,
      color=0x2f3136)

  embed.set_thumbnail(url=icon)
  embed.add_field(name="Owner", value=owner, inline=True)
  embed.add_field(name="Server ID", value=id, inline=True)
  embed.add_field(name="Region", value=region, inline=True)
  embed.add_field(name="Member Count", value=memberCount, inline=True)
  
  await ctx.send(embed=embed)

@client.command(aliases=["ctc"])
@commands.has_permissions(manage_channels = True)
async def createtextchannel(ctx,*,reason= "No name"):
    try:
        await ctx.guild.create_text_channel(reason + ' ')
        await ctx.send(f"Your text channel has been created #{reason}")
    except:
          await ctx.send(f"I have no permissions to make {reason}")
 
@client.command(aliases=["cvc"])
@commands.has_permissions(manage_channels = True)
async def create_voice_channel(ctx,*,reason= "No name"):
    try:
        await ctx.guild.create_voice_channel(reason + ' ')
        await ctx.send(f"Your voice has been created #{reason}")
    except:
          await ctx.send(f"I have no permissions to make {reason}")

@client.command(pass_context=True)
async def servers(ctx):
        """View all the servers i'm in"""
        page = 1
        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][0:20])
        s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
        s.set_author(name=":shield: Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
        message = await ctx.send(embed=s)
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        def reactioncheck(reaction, user):
            if user == ctx.author:
                if reaction.message.id == message.id:
                    if reaction.emoji == "▶" or reaction.emoji == "◀":
                        return True
        page2 = True
        while page2:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=30, check=reactioncheck)
                if reaction.emoji == "▶":
                    if page != math.ceil(len(list(set(ctx.bot.guilds))) / 20):
                        page += 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                if reaction.emoji == "◀":
                    if page != 1:
                        page -= 1
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                        await message.edit(embed=s)
                    else:
                        page = math.ceil(len(list(set(ctx.bot.guilds)))/ 20)
                        msg = "\n".join(["`{}` - {} members".format(x.name, x.member_count) for x in sorted(sorted(ctx.bot.guilds, key=lambda x: x.name.lower()), key=lambda x: x.member_count, reverse=True)][page*20-20:page*20])
                        s=discord.Embed(description=msg, colour=3092790, timestamp=__import__('datetime').datetime.utcnow())
                        s.set_author(name="<:shield:827178690059829288> Servers ({})".format(len(ctx.bot.guilds)), icon_url=ctx.bot.user.avatar_url)
                        s.set_footer(text="Page {}/{}".format(page, math.ceil(len(list(set(ctx.bot.guilds))) / 20)))
                        await message.edit(embed=s)
            except asyncio.TimeoutError:
                try:
                    await message.remove_reaction("◀", ctx.me)
                    await message.remove_reaction("▶", ctx.me)
                except:
                    pass
                page2 = False

@client.event
async def on_guild_join(guild):
	for channel in guild.text_channels:
		if channel.permissions_for(guild.me).send_messages:
			embed = discord.Embed()
			embed.description = 'Hi im japan! japan is a multi-use all around discord bot Filled with many commands but mainly an anti-nuke/moderation bot. Use ;help and &setup for more information.\n\n**If you‘d like to invite japan \n\n**[Click Here](https://discord.com/oauth2/authorize?client_id=827109999880568832&permissions=8&scope=bot)\n\n**If you need any support or help please join our support server \n\n**[Click Here](https://discord.gg/420)\n\n**Or Dm otx#1741 with questions\n\n**'
			embed.colour = 0x36393F
			message = await channel.send(embed=embed)
		break
client.run('', bot=True)
