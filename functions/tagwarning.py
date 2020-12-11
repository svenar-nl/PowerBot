import discord
from discord.ext import commands

class taglistener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user or message.author.bot):
            return
        
        for user in message.mentions:
            if user is not message.author:
                for role in user.roles:
                    if "support" in role.name.lower():
                        await message.channel.send("Whoa {}. Do not tag support directly!".format(message.author.mention))
                        return

def setup(bot):
    bot.add_cog(taglistener(bot))