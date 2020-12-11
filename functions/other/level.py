import discord
from discord.ext import commands
import config
import settings
import json
import random

level_cache = {}

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global level_cache

        if (message.author == self.bot.user or message.author.bot):
            return
        
        member_id = str(message.author.id)

        if not member_id in level_cache:
            level_cache[member_id] = {"xp": 0, "level": 0, "target_xp": 0, "messages": 0}
        
        xp = level_cache[member_id]["xp"] + random.randint(config.level_xp_min, config.level_xp_max)
        level = 0

        while True: #I want to cry
            if xp < config.level_xp_base * level * config.level_xp_multiplier + config.level_xp_base:
                break
            level += 1
        
        level_cache[member_id]["xp"] = xp
        level_cache[member_id]["level"] = level
        level_cache[member_id]["target_xp"] = config.level_xp_base * level * config.level_xp_multiplier + config.level_xp_base
        level_cache[member_id]["messages"] = level_cache[member_id]["messages"] + 1

        saveData() # TODO: Do not always save. I/O is precious
    
    @commands.command(aliases=["rank"])
    async def level(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.message.author
        
        member_id = str(member.id)
        if not member_id in level_cache:
            level_cache[member_id] = {"xp": 0, "level": 0, "target_xp": config.level_xp_base, "messages": 0}

        rank = 1
        percent_base_xp = config.level_xp_base * (level_cache[member_id]["level"] - 1) * config.level_xp_multiplier + config.level_xp_base

        if percent_base_xp < 0:
            percent_base_xp = 0
        
        for  _member in level_cache:
            if level_cache[_member]["xp"] > level_cache[member_id]["xp"]:
                rank += 1
        
        current_percent = int((100 / (level_cache[member_id]["target_xp"] - percent_base_xp)) * (level_cache[member_id]["xp"] - percent_base_xp))
        percent_bar = ""
        for i in range(0, 10):
            percent_bar += "▓" if i <= current_percent / 10 else "░"

        embed = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.blue())

        embed.add_field(name="XP", value=str(level_cache[member_id]["xp"]) + "/" + str(int(level_cache[member_id]["target_xp"])), inline=True)
        embed.add_field(name="Messages", value=str(level_cache[member_id]["messages"]), inline=True)
#        embed.add_field(name="Next level XP", value=str(int(level_cache[member_id]["target_xp"])), inline=True)
        embed.add_field(name="Progress", value=percent_bar + " " + str(current_percent) + "%", inline=False)
        embed.add_field(name="Level", value=str(level_cache[member_id]["level"]), inline=True)
        embed.add_field(name="Rank", value="#" + str(rank), inline=True)

        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def leaderboard(self, ctx):
        if not str(ctx.message.author.id) in level_cache:
            level_cache[str(ctx.message.author.id)] = {"xp": 0, "level": 0, "target_xp": config.level_xp_base, "messages": 0}
            
        sorted_leaderboard_items = sorted(level_cache.items(), key=lambda x: x[1]["xp"], reverse=True)

        embed = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.blue())

        top10 = ""
        for i in range(0, 10):
            member_id = sorted_leaderboard_items[i][0]
            member_name = ""
            for m in ctx.message.guild.members:
                if str(m.id) == str(member_id):
                    member_name = m.name
                    break
            member_lvl = sorted_leaderboard_items[i][1]["level"]
            top10 += "#" + str(i + 1) + ": **" + member_name + "**, level: " + str(member_lvl) + "\n"
        
        sender_pos = ""
        index = 0
        for m in sorted_leaderboard_items:
            index += 1
            if str(m[0]) == str(ctx.message.author.id):
                sender_pos = "#" + str(index) + ": **" + ctx.message.author.name + "**, level: " + str(m[1]["level"]) + "\n"
                break

        embed.add_field(name="Top 10", value=top10, inline=False)
        embed.add_field(name="You", value=sender_pos, inline=False)

        # embed.set_thumbnail(url=member.avatar_url)
        # embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(level(bot))
    loadData()

def saveData():
    global level_cache
    json.dump(level_cache, open("levels.json", "w"))

def loadData():
    global level_cache
    try:
        level_cache = json.load(open("levels.json"))
    except FileNotFoundError:
        json.dump(level_cache, open("levels.json", "w"))
