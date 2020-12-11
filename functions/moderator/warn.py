import  discord
import random
from discord.ext import commands
import settings
import config
import json

class warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(config.moderator_role)
    async def warn(self, ctx, member: discord.Member=None, weight: int=None, *, reason=None):
        if member is None or weight is None:
            await ctx.send(settings.discord_bot_prefix + "warn <member> [weight] [reason]")
            return
        
        add_warning(member, weight, reason)

        await ctx.message.add_reaction("✅")
    
    @commands.command()
    # @commands.has_role(config.moderator_role)
    async def warns(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.message.author
        else:
            if not config.moderator_role in ctx.message.author.roles:
                await ctx.send("[ERROR] Role 'Moderator' is required to run this command.")
                return
        
        member_id = str(member.id)

        if not member_id in config.warning_cache:
            await ctx.send(f"Member {member.name} has no warnings!")
            return
        
        embed = discord.Embed(
            title=member.name + "'s warnings",
            colour=discord.Colour.blue()
        )
        
        warnings_weight = 0
        for warning in config.warning_cache[member_id]:
            warnings_weight += int(warning["weight"])

        embed.add_field(name="Warnings: ", value=str(len(config.warning_cache[member_id])), inline=True)
        embed.add_field(name="Weight: ", value=str(warnings_weight), inline=True)

        index = 0
        for warning in config.warning_cache[member_id]:
            index += 1
            embed.add_field(name=f"#{index}: ", value="(" + str(warning["weight"]) + ") " + warning["reason"], inline=False)

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(warn(bot))
    loadData()

def add_warning(member: discord.Member, weight: int, reason):
    member_id = str(member.id)

    if not member_id in config.warning_cache:
        config.warning_cache[member_id] = []
    
    warn_item = {"reason": reason, "weight": weight}
    config.warning_cache[member_id].append(warn_item)

    saveData()

def saveData():
    json.dump(config.warning_cache, open("warnings.json", "w"))

def loadData():
    try:
        config.warning_cache = json.load(open("warnings.json"))
    except FileNotFoundError:
        json.dump(config.warning_cache, open("warnings.json", "w"))
