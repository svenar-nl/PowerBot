import  discord
import random
from discord.ext import commands
import settings
import json

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'User {member} has been kicked')
        except:
            await ctx.send(f'Could not find user!')

def setup(bot):
    bot.add_cog(kick(bot))