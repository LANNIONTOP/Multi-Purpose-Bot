# modules
import discord
import asyncio
from discord.ext import commands
import datetime
import asqlite # database module

# database
async def database():
	# connection
	global connection # making the database connection variable a global variable, so that I can use it anywhere
	connection = await asqlite.connect("database.db") # the connection to the database
	# cursor
	global cursor # making the database cursor variable a global variable, so that I can use it anywhere
	cursor = await connection.cursor() # the 		database cursor

# class
class AntiRemoval(commands.Cog):
	def __init__(
		self,
		client
	):
		self.client = client
		client.loop.run_until_complete(database())
	# when a channel in a guild gets created
	@commands.Cog.listener()
	async def on_member_remove(
		self,
		member
	):
		await cursor.execute(
			"SELECT user_id FROM whitelisted_users WHERE guild_id = {}".format(member.guild.id)
		)
		async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):
			user_iDs = await cursor.fetchall()
			if i.user.id in [user_iD[0] for user_iD in user_iDs]:
				return
			else:
				await member.guild.ban(i.user, reason="Anti-Nuke ; Banning Members")
				return
	# when a channel in a guild gets deleted
	@commands.Cog.listener()
	async def on_member_remove(
		self,
		guild,
		user
	):
		await cursor.execute(
			"SELECT user_id FROM whitelisted_users WHERE guild_id = {}".format(guild.id)
		)
		async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
			user_iDs = await cursor.fetchall()
			if i.user.id in [user_iD[0] for user_iD in user_iDs]:
				return
			else:
				await guild.ban(i.user, reason="Anti-Nuke ; Kicking Members")
				return
        
@commands.Cog.listener()
async def on_member_join(
		self,
		guild,
		user,
    member
	):
		await cursor.execute(
			"SELECT user_id FROM whitelisted_users WHERE guild_id = {}".format(guild.id)
	
		async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
			user_iDs = await cursor.fetchall()
			if i.user.id in [user_iD[0] for user_iD in user_iDs]:
				return
			else
				await guild.ban(i.user, reason="Anti-Nuke ; Kicking Members")
				return
        
def setup(client):
  client.add_cog(AntiRemoval(client))