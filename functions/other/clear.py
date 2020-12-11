import discord
from discord.ext import commands
import time
import config

class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def clear(self, ctx, count: int):
        """Deletes a specified amount of messages. (Max 100)"""
        count += 1
        if count > 100:
            count = 100
        await ctx.message.channel.purge(limit=count, bulk=True)
        

def setup(bot):
    bot.add_cog(clear(bot))