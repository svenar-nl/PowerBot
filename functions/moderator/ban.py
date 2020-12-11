import  discord
import random
from discord.ext import commands
import settings
import json
import config

class ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.has_permissions(administrator=True)
    @commands.command()
    @commands.has_role(config.moderator_role)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'User {member} has been banned')
        except:
            await ctx.send(f'Could not find user!')
    
    @commands.command()
    @commands.has_role(config.moderator_role)
    async def unban(self, ctx, *, member):
        try:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'Unbanned {user.mention}')
                    return
        except:
            await ctx.send(f'Could not find user!')

def setup(bot):
    bot.add_cog(ban(bot))
