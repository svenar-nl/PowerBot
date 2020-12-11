import discord
from discord.ext import commands
import config
import settings
import json

simple_commands = {}

class simplecommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user or message.author.bot):
            return
        
        if not message.content.lower().startswith(settings.discord_bot_prefix):
            config.messages_count += 1
            config.total_messages_count += 1
            return
        
        commands = message.content.split(' ')

        for simple_command in simple_commands:
            if simple_command.lower() in " ".join(commands).lower():
                command_found = True
                await message.channel.send(config.chat_prefix + simple_commands[simple_command])

def setup(bot):
    bot.add_cog(simplecommands(bot))
    loadCommandData()

def loadCommandData():
    global simple_commands
    try:
        simple_commands = json.load(open("commands.json"))
    except FileNotFoundError:
        json.dump(simple_commands, open("commands.json", "w"))