import discord, shelve, asyncio, datetime, json
from discord.ext import commands

async def keep_db_open():
	"""
	This coroutine keeps the shelf file open,
	so that several new openings do not need to be performed
	"""
	while True:
		await asyncio.sleep(0.1)
		global db
		db = shelve.open('database.db')

class antievents(commands.Cog):
	def __init__(self, client):
		self.client = client
	@commands.Cog.listener()
	async def on_ready(self):
		self.client.loop.create_task(
			keep_db_open()
		)
	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
			if i.user == i.guild.owner:
				return
			if str(i.user.id) in db[str(guild.id)]:
			  return
		await i.user.ban(reason="Anti-Nuke ; Banning Users")
		return
   
    def setup(client):
  client.add_cog(antievents(client))