import discord
from discord.ext import commands
from discord.utils import get
import time
import json
import config

reaction_role_cache = []

class reaction_role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id
        member = payload.member
        emoji = payload.emoji

        if member.bot:
            return

        target_role = None

        for cached_reaction_role in reaction_role_cache:
            if str(cached_reaction_role["message"]) == str(message_id):
                if (emoji.id == None and cached_reaction_role["emoji"] == emoji.name) or (str(cached_reaction_role["emoji"]) == str(emoji)):
                    target_role = int(cached_reaction_role["role"])
                    break
        
        if target_role is not None:
            role = get(member.guild.roles, id=target_role)
            await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        message_id = payload.message_id
        emoji = payload.emoji

        try:
            guild = self.bot.get_guild(payload.guild_id)
            member = get(guild.members, id=payload.user_id)

            if member.bot:
                return

            target_role = None

            for cached_reaction_role in reaction_role_cache:
                if str(cached_reaction_role["message"]) == str(message_id):
                    if (emoji.id == None and cached_reaction_role["emoji"] == emoji.name) or (str(cached_reaction_role["emoji"]) == str(emoji)):
                        target_role = int(cached_reaction_role["role"])
                        break
            
            if target_role is not None:
                role = get(member.guild.roles, id=target_role)
                await member.remove_roles(role)
        except:
            pass


    @commands.command(pass_context=True)
    @commands.has_role(config.moderator_role)
    async def reactionrole(self, ctx, message_id, emoji, role: discord.Role = None):
        channel = ctx.channel

        index = 0
        match_found = False
        for cached_reaction_role in reaction_role_cache:
            if cached_reaction_role["message"] == str(message_id) and cached_reaction_role["emoji"] == str(emoji):
                match_found = True
                break
            index += 1
        
        if role is not None:
            if not match_found:
                reaction_role_cache.append({"message": str(message_id), "channel": str(channel), "emoji": str(emoji), "role": str(role.id)})
                await ctx.send("Reaction role added!")
            else:
                del reaction_role_cache[index]
                await ctx.send("Reaction role removed!")
        else:
            if not match_found:
                await ctx.send("Reaction role not found!")
            else:
                del reaction_role_cache[index]
                await ctx.send("Reaction role removed!")
        saveData()

        target_message = await ctx.fetch_message(message_id)
        await target_message.add_reaction(emoji)

def setup(bot):
    bot.add_cog(reaction_role(bot))
    loadData()

def saveData():
    global reaction_role_cache

    json.dump(reaction_role_cache, open("reaction_role_data.json", "w"))

def loadData():
    global reaction_role_cache
    try:
        reaction_role_cache = json.load(open("reaction_role_data.json"))
    except FileNotFoundError:
        json.dump(reaction_role_cache, open("reaction_role_data.json", "w"))

def get_role_from_id(guild, role_id):
    output_role = None
    for role in guild.roles:
        if str(role.id) == str(role_id):
            output_role = role
            break
    
    return output_role