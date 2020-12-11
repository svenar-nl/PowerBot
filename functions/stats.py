import discord
from discord.ext import commands
import time
import config

startTime = time.time()

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def stats(self, ctx, detailed_information: bool=False):
        ping_t1 = time.perf_counter()
        await ctx.trigger_typing()
        ping_t2 = time.perf_counter()

        guilds = self.bot.guilds
        members_online = 0
        members_offline = 0
        for guild in guilds:
            for member in guild.members:
                if (str(member.status).lower() != "offline"):
                    members_online += 1
                else:
                    members_offline += 1
        
        user_data = ""
        user_data += "**Total users:** " + str(members_online + members_offline) + "\n"
        user_data += "**Online users:** " + str(members_online ) + "\n"
        user_data += "**Offline users:** " + str(members_offline) + "\n"

        info_board = discord.Embed(
            title="PowerBot stats",
            colour=discord.Colour.blue()
        )

        info_board.add_field(name="Uptime", value=str(getUptime()), inline=False)
        info_board.add_field(name="Processed messages", value=str(config.total_messages_count), inline=False)
        info_board.add_field(name="Discord member stats", value=user_data, inline=False)
        info_board.add_field(name="Response time", value=f"{round((ping_t2-ping_t1)*1000)}ms", inline=False)
        
        await ctx.send(embed=info_board)

def setup(bot):
    bot.add_cog(stats(bot))

def getUptime():
    """
    Return HH:MM:SS since start
    """
    total_seconds = int(time.time() - startTime)

    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24
 
    days    = str(int(total_seconds / DAY))
    hours   = int((total_seconds % DAY) / HOUR)
    minutes = int((total_seconds % HOUR) / MINUTE)
    seconds = int(total_seconds % MINUTE)

    if hours < 10:
        hours = "0" + str(hours)
    else:
        hours = str(hours)
    
    if minutes < 10:
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    
    if seconds < 10:
        seconds = "0" + str(seconds)
    else:
        seconds = str(seconds)

    return days + " days " + hours + ":" + minutes + ":" + seconds