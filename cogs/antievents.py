
import discord
from discord import Permissions
from discord.ext import commands
import datetime
import os
import asyncio
import requests
import discord
import pymongo
import asyncio
from urllib.parse import quote as _uriquote
from discord.ext.commands.errors import InvalidEndOfQuotedStringError

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

db = mclient[ "botdb" ] 
db = db[ "data2" ] 
lastfm = db[ "lastfm" ] 





class AntiEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        whitelistedUsers = db.find_one({ "guild_id": channel.guild.id })["users"]
        anti1 = db.find_one({ "guild_id": channel.guild.id })["antinuke"]
        now = datetime.datetime.now()
        async for i in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id == 809766065865359360:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            
            try:
                await i.user.ban(reason=f"antinuke; channels cannot be removed")
                diamond = channel.position
                newchannel = await channel.clone(reason=f"antinuke; restored deleted channels after being deleted")
                await newchannel.edit(position=diamond, sync_permissions=True)
                embed = discord.Embed(color=0xb699ff)
                embed.title=f"channel restored"
                embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{channel.guild.name}**\n\naction: restored {channel.name} - ({channel.id})\nresponse time: `{time} ms`\n\n__Action Status__\n**Channel Restored:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
                await newchannel.send(embed=embed)
            except:
                await channel.guild.ban(discord.Object(i.user.id), reason=f"antinuke; channels cannot be removed")
                diamond = channel.position
                newchannel = await channel.clone(reason=f"antinuke; restored deleted channels after being deleted")
                embed = discord.Embed(color=0xb699ff)
                embed.title=f"channel restored"
                embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{channel.guild.name}**\n\naction: restored {channel.name} - ({channel.id})\nresponse time: `{time} ms`\n\n__Action Status__\n**Channel Restored:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
                await newchannel.edit(position=diamond, sync_permissions=True)
                await newchannel.send(embed=embed)


            logchannel = db.find_one({ "guild_id": channel.guild.id })["logchannel"] 
            if logchannel == "None":
             pass
            else:
             embed = discord.Embed(color=0xb699ff)
             embed.title=f"antinuke logchannel"
             embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{channel.guild.name}**\n\naction: deleted the channel {channel.name} - ({channel.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Member Banned:** <:check:818148801377468417>\n> **Channel Restored:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
             await self.bot.get_channel(int(logchannel)).send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
     goodbyetoggle = db.find_one({ "guild_id": member.guild.id })["goodbye"]
     goodbyechannel = db.find_one({ "guild_id": member.guild.id })["goodbyechannel"]
     goodbyemsg = db.find_one({ "guild_id": member.guild.id })["goodbyemsg"]
     if goodbyetoggle == 0:
       return


     if goodbyetoggle == 1:
      msg = goodbyemsg.format(usermention=member.mention,server=member.guild.name,username=member.name, user=member)
      await self.bot.get_channel(int(goodbyechannel)).send(f'{msg}')


    @commands.Cog.listener()
    async def on_member_join(self, member):
     welcometoggle = db.find_one({ "guild_id": member.guild.id })["welcome"]
     blacklist = db.find_one({ "guild_id": member.guild.id })["blacklist2"]
     welcomechannel = db.find_one({ "guild_id": member.guild.id })["welcomechannel"]
     welcomemsg = db.find_one({ "guild_id": member.guild.id })["welcomemsg"]
     whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]

     lastfm.insert_one({
                    "color": "None",
                    "embed": "None",
                    "_id": member.id
                })  

     if member.bot:
      async for i in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
 
            await i.user.ban(reason=f'antinuke; bots cannot be granted access to the server')
            await member.ban(reason=f'antinuke; members cannot grant bots access to the server ')
            return  

     if welcometoggle == 0:
      return
    
    
     if blacklist == 0:
       return

     if blacklist == 1:
       if member.id in db.find_one({ "guild_id": member.guild.id })["blacklist"]:
          await member.kick(reason=f'blacklist; member cannot be granted access to the server {member.name}#{member.discriminator}')
          return

     if welcometoggle == 1:
      msg = welcomemsg.format(usermention=member.mention,server=member.guild.name,username=member.name, user=member)
      await self.bot.get_channel(int(welcomechannel)).send(f'{msg}')
      return


  
    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
     try:
        guild = webhook.guild
        now = datetime.datetime.now()
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.webhook_create).flatten()
        logs = logs[0]
        whitelistedUsers = db.find_one({ "guild_id": guild.id })['users']
        anti1 = db.find_one({ "guild_id": guild.id })['antinuke']

        date_format = "%a, %d %b %Y %I:%M %p"
        after = datetime.datetime.now()
        time = after - now
        if anti1 == 0:
                return

        if logs.user.id in whitelistedUsers:
            return
        if logs.user.id == 809766065865359360:
                return
        requests.delete(webhook)
        try:
                await logs.user.ban(reason=f"antinuke; webhooks cannot be created")
        except:
                await guild.ban(discord.Object(logs.user.id), reason=f"antinuke; webhooks cannot be created")
        channel = db.find_one({ "guild_id": guild.id })['logchannel']
        if channel == "None":
            pass
        else:
            embed = discord.Embed(color=0xb699ff)
            embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/xICPsu-ZeMXkHaIYxuM7wFx8MlciSM2_1fsDtZhfl6Q/%3Fwidth%3D389%26height%3D389/https/images-ext-1.discordapp.net/external/L7rZNyP8jITUi5OVTdbPw4qHJVwmIVc0zs_HfkrDBQw/%253Fwidth%253D432%2526height%253D432/https/media.discordapp.net/attachments/808027078209306625/808384680067334243/ga.gif?width=251&height=251")
            embed.description=f"__Action Status__\n> responded in: `{time} ms`\n> Action: created the webhook {webhook.name} - ({webhook.id})\n\n> Whitelisted: \n> User Banned: <:check:818148801377468417>\n> Webhook Deleted: <:check:818148801377468417>\n\n__User Information__\n> Mention: {logs.user.mention}\n > Name: {logs.user.name}\n > Discriminator: #{logs.user.discriminator}\n > ID: {logs.user.id}\n > Joined At: {logs.user.joined_at.strftime(date_format)}" 
            await self.bot.get_channel(int(channel)).send(embed=embed)
     except:
         pass 


    



    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        whitelistedUsers = db.find_one({ "guild_id": channel.guild.id })["users"]
        anti1 = db.find_one({ "guild_id": channel.guild.id })["antinuke"]
        now = datetime.datetime.now()
        async for i in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id == 809766065865359360:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            
            try:
                await i.user.ban(reason=f"antinuke; channels cannot be created")
                await channel.delete()
            except:
                await channel.guild.ban(discord.Object(i.user.id), reason=f"antinuke; channels cannot be created")
                await i.target.delete()

            logchannel = db.find_one({ "guild_id": channel.guild.id })["logchannel"] 
            if logchannel == "None":
             pass
            else:
             embed = discord.Embed(color=0xb699ff)
             embed.title=f"antinuke logchannel"
             embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{channel.guild.name}**\n\naction: created the channel {channel.name} - ({channel.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Member Banned:** <:check:818148801377468417>\n> **Channel Removed:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
             await self.bot.get_channel(int(logchannel)).send(embed=embed)
            

  


    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
     try:
        now = datetime.datetime.now()
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        logs = logs[0]
        reason = "antinuke; members cannot be banned"
        whitelistedUsers = db.find_one({ "guild_id": guild.id })["users"] 
        logchannel = db.find_one({ "guild_id": guild.id })["logchannel"] 
        anti1 = db.find_one({ "guild_id": guild.id })["antinuke"] 
        date_format = "%a, %d %b %Y %I:%M %p"
        after = datetime.datetime.now()
        time = after - now
        if anti1 == 0:
                return
        if logs.user.id in whitelistedUsers:
            return
        if logs.user.id == 809766065865359360:
                return

        try:
                await logs.user.ban(reason=f"{reason}")
                await guild.unban(discord.Object(id=logs.target.id), reason=f"banned by unwhitelisted user")
        except:
                await guild.ban(discord.Object(logs.user.id), reason=f"{reason}")
                await guild.unban(discord.Object(id=logs.target.id), reason=f"banned by unwhitelisted user")
        banlist = await guild.bans()           
        for logs in banlist:
                try:
                 await guild.unban(discord.Object(id=logs.target.id), reason=f"banned by unwhitelisted user")
                except:
                    pass            

        logchannel = db.find_one({ "guild_id": guild.id })["logchannel"] 
        if logchannel == "None":
            pass
        else:
            embed = discord.Embed(color=0xb699ff)
            embed.title=f"antinuke logchannel"
            embed.description=f"action from **{logs.user.name}#{logs.user.discriminator}** in **{guild.name}**\n\naction: banned the member {logs.target.name} - ({logs.target.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Banned:** <:check:818148801377468417>\n> **Member Unbanned:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {logs.user.mention}\n > **Name:** {logs.user.name}\n > **Discriminator:** #{logs.user.discriminator}\n > **ID:** {logs.user.id}\n > **Joined At:** {logs.user.joined_at.strftime(date_format)}" 
            await self.bot.get_channel(int(logchannel)).send(embed=embed)
            
     except:
         pass   

    @commands.Cog.listener()
    async def on_member_remove(self, member):
     try:
        guild = member.guild
        now = datetime.datetime.now()
        logs = await member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
        logs = logs[0]
        whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]
        anti1 = db.find_one({ "guild_id": member.guild.id })["antinuke"]
        date_format = "%a, %d %b %Y %I:%M %p"
        after = datetime.datetime.now()
        time = after - now
        if anti1 == 0:
                return

        if logs.target.id == member.id:
         try:
                await logs.user.ban(reason=f"antinuke; members cannot be kicked")
         except:
                await guild.ban(discord.Object(logs.user.id), reason=f"antinuke; members cannot be kicked")
        channel = db.find_one({ "guild_id": guild.id })['logchannel']
        if channel == "None":
            pass
        else:
            embed = discord.Embed(color=0xb699ff)
            embed.title=f"antinuke logchannel"
            embed.description=f"action from **{logs.user.name}#{logs.user.discriminator}** in **{guild.name}**\n\naction: kicked the member {logs.target.name} - ({logs.target.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Banned:** <:check:818148801377468417>\n> **Member Notified:** <:x_:815962474721181706>\n__User Info__\n> **Mention:** {logs.user.mention}\n > **Name:** {logs.user.name}\n > **Discriminator:** #{logs.user.discriminator}\n > **ID:** {logs.user.id}\n > **Joined At:** {logs.user.joined_at.strftime(date_format)}" 
            await self.bot.get_channel(int(channel)).send(embed=embed)
     except:
        pass  



         


    @commands.Cog.listener()
    async def on_member_prune(self, guild, member):
        whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]  
        anti1 = db.find_one({ "guild_id": member.guild.id })["antinuke"]
        now = datetime.datetime.now()
        async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.member_prune):
           date_format = "%a, %d %b %Y %I:%M %p"
           after = datetime.datetime.now()
           time = after - now
           if anti1 == 0:
                return

           if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
                
           if i.target.id == member.id:
                await member.ban(reason="antinuke; members cannot be pruned")
                return


    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        whitelistedUsers = db.find_one({ "guild_id": guild.id })["users"]
        anti1 = db.find_one({ "guild_id": guild.id })["antinuke"]
        logchannel = db.find_one({ "guild_id": guild.id })["logchannel"]
        now = datetime.datetime.now()
        async for i in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await i.user.ban(reason=f"antinuke; members cannot be unbanned")
            await guild.ban(discord.Object(i.target.id), reason = f"antinuke; unbanned by unwhitelisted user")
            embed = discord.Embed(color=0xb699ff)
            embed.title=f"antinuke logchannel"
            embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{guild.name}**\n\naction: kicked the member {i.target.name} - ({i.target.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Banned:** <:check:818148801377468417>\n> **Member Rebanned:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
            await self.bot.get_channel(int(logchannel)).send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        whitelistedUsers = db.find_one({ "guild_id": role.guild.id })["users"]
        anti1 = db.find_one({ "guild_id": role.guild.id })["antinuke"]
        now = datetime.datetime.now()
        async for i in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id == 809766065865359360:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            
            try:
                await i.user.ban(reason=f"antinuke; roles cannot be created")
                await role.delete()
            except:
                await role.guild.ban(discord.Object(i.user.id), reason=f"antinuke; roles cannot be created")
                await i.target.delete()

            logchannel = db.find_one({ "guild_id": role.guild.id })["logchannel"] 
            if logchannel == "None":
             pass
            else:
             embed = discord.Embed(color=0xb699ff)
             embed.title=f"antinuke logchannel"
             embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{role.guild.name}**\n\naction: created the role {role.name} - ({role.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Member Banned:** <:check:818148801377468417>\n> **Role Removed:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
             await self.bot.get_channel(int(logchannel)).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        whitelistedUsers = db.find_one({ "guild_id": role.guild.id })["users"]
        anti1 = db.find_one({ "guild_id": role.guild.id })["antinuke"]
        now = datetime.datetime.now()
        async for i in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id == 809766065865359360:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            
            try:
                await i.user.ban(reason=f"antinuke; roles cannot be created")
            except:
                await role.guild.ban(discord.Object(i.user.id), reason=f"antinuke; roles cannot be created")

            logchannel = db.find_one({ "guild_id": role.guild.id })["logchannel"] 
            if logchannel == "None":
             pass
            else:
             embed = discord.Embed(color=0xb699ff)
             embed.title=f"antinuke logchannel"
             embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{role.guild.name}**\n\naction: deleted the role {role.name} - ({role.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Member Banned:** <:check:818148801377468417>\n> **Role Saved:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
             await self.bot.get_channel(int(logchannel)).send(embed=embed)         





    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        whitelistedUsers = db.find_one({ "guild_id": after.guild.id })["users"]
        logchannel = db.find_one({ "guild_id": after.guild.id })["logchannel"]
        anti1 = db.find_one({ "guild_id": after.guild.id })["antinuke"]
        perms = discord.Permissions()
        perms.update(kick_members = False)
        now = datetime.datetime.now()
        async for i in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
            date_format = "%a, %d %b %Y %I:%M %p"
            after = datetime.datetime.now()
            time = after - now
            if anti1 == 0:
                return

            if i.user.id == 809766065865359360:
                return    

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            embed = discord.Embed(color=0xb699ff)
            embed.title=f"antinuke logchannel"
            embed.description=f"action from **{i.user.name}#{i.user.discriminator}** in **{before.guild.name}**\n\naction: updated the role with dangerous permissions {before.name} - ({before.id})\nresponse time: `{time} ms`\n\n__Action Status__\n> **Member Banned:** <:check:818148801377468417>\n> **Role Permissions Reverted:** <:check:818148801377468417>\n__User Info__\n> **Mention:** {i.user.mention}\n > **Name:** {i.user.name}\n > **Discriminator:** #{i.user.discriminator}\n > **ID:** {i.user.id}\n > **Joined At:** {i.user.joined_at.strftime(date_format)}" 
            await self.bot.get_channel(int(logchannel)).send(embed=embed) 

            perm = Permissions()
            perm.update(kick_members = True)
            if before.permissions.kick_members and not after.permissions.kick_members:
               await after.guild.ban(i.user, reason=f'antinuke; roles cannot be removed kick members permissions')
               await after.edit(permissions=perm)
               return

            
            if not before.permissions.kick_members and after.permissions.kick_members:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted kick members permissions')
                await after.edit(permissions=perms)
                return

            perm = Permissions()
            perm.update(ban_members = False)
            if not before.permissions.ban_members and after.permissions.ban_members:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted ban members permissions')
                await after.edit(permissions=perm)  
                return

            perms = Permissions()
            perms.update(ban_members = True)
            if before.permissions.ban_members and not after.permissions.ban_members:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be removed ban members permissions')
                await after.edit(permissions=perms)  
                return    


            perm = Permissions()
            perm.update(administrator = False)
            if not before.permissions.administrator and after.permissions.administrator:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted administrator permissions')
                await after.edit(permissions=perm)  
                return

            perms = Permissions()
            perms.update(administrator = True)
            if before.permissions.administrator and not after.permissions.administrator:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be removed administrator permissions')
                await after.edit(permissions=perms)  
                return    

            perm = Permissions()
            perm.update(manage_guild = False)
            if not before.permissions.manage_guild and after.permissions.manage_guild:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted manage guild permissions')
                await after.edit(permissions=perm)  
                return    

            perms = Permissions()
            perms.update(manage_guild = True)
            if before.permissions.manage_guild and not after.permissions.manage_guild:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be removed manage guild permissions')
                await after.edit(permissions=perms)  
                return      

            perm = Permissions()
            perm.update(manage_channels = False)
            if not before.permissions.manage_channels and after.permissions.manage_channels:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted manage channels permissions')
                await after.edit(permissions=perm)  
                return       

            perms = Permissions()
            perms.update(manage_channels = True)
            if before.permissions.manage_channels and after.permissions.manage_channels:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be removed manage channels permissions')
                await after.edit(permissions=perms)  
                return      

            perm = Permissions()
            perm.update(manage_webhooks = False)
            if not before.permissions.manage_webhooks and after.permissions.manage_webhooks:
                await after.guild.ban(i.user, reason=f'antinuke; roles cannot be granted manage webhook permissions')
                await after.edit(permissions=perm)  
                return       


def setup(bot):
    bot.add_cog(AntiEvents(bot)) 
    
           
            
            
 

   