import  discord
import random
from discord.ext import commands
from discord.utils import get
import settings
import config
import json

class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(config.moderator_role)
    async def mute(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send(settings.discord_bot_prefix + "mute <member>")
            return
        
        # role = get(member.guild.roles, name=config.mute_role)
        # await member.add_roles(role)
        muted_role = get(ctx.guild.roles, name=config.mute_role)
        if not muted_role:
            muted_role = await ctx.guild.create_role(name=config.mute_role, reason="To use for muting")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, read_message_history=False, read_messages=False)
        
        await member.add_roles(muted_role)

        await ctx.message.add_reaction("✅")

    @commands.command()
    @commands.has_role("Moderator")
    async def unmute(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send(settings.discord_bot_prefix + "mute <member>")
            return
        
        role = get(member.guild.roles, name=config.mute_role)
        await member.remove_roles(role)

        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(mute(bot))
