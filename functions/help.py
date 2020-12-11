import  discord
import random
from discord.ext import commands
import settings
import json

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def avatar(self, ctx):
        await ctx.send(ctx.author.avatar_url)

    @commands.command(pass_context=True)
    async def help(self, ctx, help_selector="default"):
        info_board = discord.Embed(
            title="PowerBot",
            colour=discord.Colour.blue()
        )
        info_board.set_author(name="PowerBot Commands")

        if "default" in help_selector.lower():
            info_board.add_field(name=settings.discord_bot_prefix + "help [default/general/fun/moderator]", value="Shows a list of available commands.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "ping", value="Check the bot response time.", inline=False)
        
        if "fun" in help_selector.lower():
            info_board.add_field(name=settings.discord_bot_prefix + "level", value="[FUN] Show your level in this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "leaderboard", value="[FUN] Show the top 10 active users.", inline=False)

        if "mod" in help_selector.lower():
            info_board.add_field(name=settings.discord_bot_prefix + "stats", value="[DEV] View bot stats", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "learn \"question\" \"answer\"", value="[MOD] Learn the bot a new auto Q&A item.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "poll <message>", value="[MOD] Create a yes/no poll.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "clear <0-100>", value="[MOD] Clear 0-100 messages in a channel.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "userinfo [member]", value="[MOD] Show information about a specific user.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "serverinfo", value="[MOD] Show information about this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "(un)mute <member>", value="[MOD] (Un)mute a member on the server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "warn <member> [weight] [reason]", value="[MOD] Warn a member in this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "warns [member]", value="[MOD] Show all warnings from a member in the server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "kick <member> [reason]", value="[MOD] Kick a member from this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "(un)ban <member> [reason]", value="[MOD] Ban/Unban a member in this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "serverinfo", value="[MOD] Show information about this server.", inline=False)
            info_board.add_field(name=settings.discord_bot_prefix + "reactionrole <messageID> <emoji> <role>", value="[DEV] Add a reaction role to a message.", inline=False)

        if "default" in help_selector.lower() or "general" in help_selector.lower():
            simple_commands = {}
            try:
                simple_commands = json.load(open("commands.json"))
                cmd_list = ""
                for cmd in simple_commands:
                    cmd_list += settings.discord_bot_prefix + cmd + "\n"
                info_board.add_field(name="General", value=cmd_list, inline=False)
            except FileNotFoundError:
                json.dump(simple_commands, open("commands.json", "w"))
        
        info_board.add_field(name = "Developed by", value = "https://svenar.nl", inline = False)
        info_board.add_field(name = "Support me", value = "https://ko-fi.com/svenar", inline = False)

        await ctx.send(embed=info_board)

def setup(bot):
    bot.add_cog(info(bot))
