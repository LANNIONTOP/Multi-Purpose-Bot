import discord
from discord.ext import commands
import datetime

date = datetime.datetime.now()

class events(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_guild_channel_delete(self, channel):
    LogsChanl = discord.utils.get(channel.guild.channels, name="faygo-logs")
    if not LogsChanl:
      LogsChanl = await channel.guild.create_text_channel(name="faygo-logs")
      everyoneRole = discord.utils.get(channel.guild.roles, name="@everyone")
      await LogsChanl.set_permissions(everyoneRole, read_message_history=False,view_channel=False,send_messages=False)

    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
      deleter = entry.user
      em = discord.Embed(title=f":warning: Channel Deleted", description=f"Channel Name: [`{channel.name}`]\nChannel Position: [`{channel.position} in {channel.category}`]\nDeleter: [`{deleter}`]\nTime: [`{date:%I}:{date:%M} {date:%p}`]", color=0x2f3136)
      await LogsChanl.send(embed=em)
