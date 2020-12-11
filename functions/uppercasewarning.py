import discord
from discord.ext import commands
import config
import settings
import json
import functions.moderator.warn as warn

class uppercasewarning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user or message.author.bot):
            return
        
        if message.content.lower().startswith(settings.discord_bot_prefix):
            return
        
        if len(message.content) > 4:
        
            alph = list(filter(str.isalpha, message.content))
            if len(alph) > 0:
                uppercase_percent = int(sum(map(str.isupper, alph)) / len(alph) * 100)

                if uppercase_percent > config.max_uppercase_percent:
                    await message.channel.send("Whoa {}. Your message contains {}% uppercase letters. Watch it!".format(message.author.mention, str(uppercase_percent)))
                    warn.add_warning(message.author, 1, "{}% caps".format(str(uppercase_percent)))

def setup(bot):
    bot.add_cog(uppercasewarning(bot))