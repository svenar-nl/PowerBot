import discord
from discord.ext import commands
import time
import config

class serverinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def serverinfo(self, ctx):
        role_count = len(ctx.guild.roles)
        emoji_count = len(ctx.guild.emojis)
        channel_count = len([x for x in ctx.guild.channels if isinstance(x, discord.channel.TextChannel)])
        embed = discord.Embed(color=discord.Colour.blue(), timestamp=ctx.message.created_at)
        embed_values = {
        	"Name (ID)": (f"{ctx.guild.name} ({ctx.guild.id})", False),
        	"Owner": (ctx.guild.owner, False),
        	"Member Count": (ctx.guild.member_count, True),
        	"Text Channels": (str(channel_count), True),
        	"Region": (ctx.guild.region, True),
        	"Verification Level": (str(ctx.guild.verification_level), True),
        	"Highest Role": (ctx.guild.roles[-1], True),
        	"Number of Roles": (str(role_count), True),
        	"Number of Emotes": (str(emoji_count), True),
        	"Created On": (ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), True)
        }
        for n, v in embed_values.items():
        	embed.add_field(name=n, value=v[0], inline=v[1])
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(serverinfo(bot))