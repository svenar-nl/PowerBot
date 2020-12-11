import discord
from discord.ext import commands
import time

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Ping command."""
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        await ctx.send(f"🏓 Pong!: {round((t2-t1)*1000)}ms")

def setup(bot):
    bot.add_cog(ping(bot))