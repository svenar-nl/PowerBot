import discord
from discord.ext import commands

class errorhandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        ignored = (commands.CommandNotFound, )

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        await ctx.send("[ERROR] " + str(error))
        return

def setup(bot):
    bot.add_cog(errorhandler(bot))