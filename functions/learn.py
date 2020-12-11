import discord
from discord.ext import commands
import functions.autosupport as autosupport
import config

class learn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def learn(self, ctx, question, answer):
        # print(question)
        # print(answer)
        await ctx.send("Learning question:\n:regional_indicator_q: " + question + "\n:regional_indicator_a: " + answer)
        #autosupport.data[question] = answer
        autosupport.addQAData(question, answer)

def setup(bot):
    bot.add_cog(learn(bot))