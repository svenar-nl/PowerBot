import discord
from discord.ext import commands
from datetime import datetime
import config

class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def poll(self, ctx, *, args):
        """Creates a poll. Takes the polltext as an argument."""
        await ctx.message.delete()
        embed=discord.Embed(title="Poll:", description=args, color=discord.Colour.blue())
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        # embed.set_thumbnail(url=random_line('pollimages'))
        # await ctx.send(embed=embed)
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        # await message.add_reaction('🤷')

def setup(bot):
    bot.add_cog(poll(bot))