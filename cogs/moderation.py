import discord 
import asyncio
from discord.ext import commands 



class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to add role to has a higher role than you, so you can't add this role to them.")
            return

        await member.add_roles(role)
        embed = discord.Embed(title = "Role Added", description = f"Successfully added {role.mention} role to {member.mention}.", color = 0x00FF0C)
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to remove role from has a higher role than you, so you can't remove this role from them.")
            return

        await member.remove_roles(role)
        embed = discord.Embed(title = "Role Removed", description = f"Successfully removed {role.mention} role from {member.mention}.", color = 0xFF0000)
        await ctx.send(embed = embed)
   
    @commands.cooldown(1, 5,
    commands.BucketType.user)
    @commands.command(aliases=["shards"])
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

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['deletechannel', 'delete-channel', 'nukechannel'])
    @commands.has_permissions(manage_channels = True)
    async def delete_channel(self, ctx, channel: discord.TextChannel = None):

        if channel == None:
            channel = ctx.channel

        msg = await ctx.send(f"Deleting `{channel}`... <a:EpicLoading1:762919634336088074>")
        await channel.delete()
        await msg.edit(content = f"Deleted `{channel}` <a:check:783529955803529247>")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['createchannel', 'create-channel'])
    @commands.has_permissions(manage_channels = True)
    async def create_channel(self, ctx, channelName = None):

        if channelName == None:
            await ctx.message.reply(f"You didn't mention what name you want the channel to have, please try again.")
            return

        msg = await ctx.send(f"Creating `{channelName}`... <a:EpicLoading1:762919634336088074>")
        await ctx.guild.create_text_channel(name = channelName)
        await msg.edit(content = f"Created `{channelName}` :white_check_mark: ")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['changenick', 'nickname'])
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member = None, *,nickname):

        old_nick = member.nick
        await member.edit(nick = f"{nickname}")
        new_nick = member.nick
        await ctx.send(f"{member.mention}'s nickname changed from `{old_nick}` to `{new_nick}` :white_check_mark: ")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} was unbanned.')
                return

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @create_channel.error
    async def create_channel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @delete_channel.error
    async def delete_channel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")


    @add_role.error
    async def add_role_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @remove_role.error
    async def remove_role_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @commands.command(aliases=["massunban", "purgebans"])
    @commands.has_permissions(ban_members=True)
    async def unbanall(self, ctx):
        guild = ctx.guild
        banlist = await guild.bans()
        await ctx.send('Unbanning `{}` members!'.format(len(banlist)))
        for users in banlist:
                await ctx.guild.unban(user=users.user, reason=f"Responsible User: {ctx.author}")

def setup(client):
    client.add_cog(Moderation(client))