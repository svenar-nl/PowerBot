import discord
from discord.ext import commands
import time

class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    # @commands.has_role("Moderator")
    async def userinfo(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        else:
            has_permission = False
            for role in ctx.message.author.roles:
                if role.name == config.moderator_role:
                    has_permission = True

            if not has_permission:
                await ctx.send("[ERROR] Role 'Moderator' is required to run this command.")
                return
        
        if user.activity is not None:
            game = user.activity.name
        else:
            game = None
        voice_state = None if not user.voice else user.voice.channel
        embed = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.blue())
        embed_values = {
        	"User ID": user.id,
        	"Nick": user.nick,
        	"Status": user.status,
        	"On Mobile": user.is_on_mobile(),
        	"In Voice": voice_state,
        	"Game": game,
        	"Highest Role": user.top_role.name,
        	"Account Created": user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
        	"Join Date": user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')
        }
        for n, v in embed_values.items():
        	embed.add_field(name=n, value=v, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(userinfo(bot))
