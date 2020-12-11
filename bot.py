import discord
from discord.ext import commands
import settings

intents = discord.Intents.all()
client = commands.Bot(command_prefix=settings.discord_bot_prefix, intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    print("===----------===")
    print("Logged in as: " + client.user.name + " (" + str(client.user.id) + ")")
    print("")
    num_cogs = load_cogs(True)
    print("")
    print(f"Loaded {num_cogs} cogs!")
    print("===----------===")

    activity = discord.Activity(name=settings.discord_bot_status, type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

def load_cogs(debug):
    cogs = [
        "functions.errorhandler",
        "functions.help",
        "functions.autosupport",
        "functions.tagwarning",
        "functions.learn",
        "functions.simplecommands",
        "functions.stats",
        "functions.uppercasewarning",
        "functions.other.poll",
        "functions.other.ping",
        "functions.other.clear",
        "functions.other.reaction_role",
        "functions.other.userinfo",
        "functions.other.serverinfo",
        "functions.other.level",
        "functions.moderator.mute",
        "functions.moderator.warn",
        "functions.moderator.kick",
        "functions.moderator.ban"
    ]

    for i in cogs:
        try:
            client.load_extension(i)
            if debug:
                print("Loaded cog: ", i)
        except:
            if debug:
                print("Failed to load cog: ", i)
    
    return len(cogs)
    
def main():
    client.run(settings.discord_bot_token)

if __name__ == "__main__":
    main()
