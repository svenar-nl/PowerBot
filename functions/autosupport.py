import discord
from discord.ext import commands
import json
import config
import numpy as np

qa_data_cache = {}

class autosupport(commands.Cog):
    global qa_data_cache
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user):
            return
        
        auto_support_msg = ""
        last_auto_support_percent = 0

        for auto_support_key in qa_data_cache.keys():
            auto_support_val = qa_data_cache[auto_support_key]
            if message is not None and message.content is not None and auto_support_key is not None and len(message.content) > 0 and len(auto_support_key) > 0:
                level = int(levenshtein_ratio_and_distance(message.content.lower(), auto_support_key.lower()) * 100)
                if level > 75:
                    if level > last_auto_support_percent:
                        last_auto_support_percent = level
                        auto_support_msg = auto_support_val
        
        if len(auto_support_msg) > 0:
            await message.channel.send(config.chat_prefix + config.formatMessageData(auto_support_msg))
            await message.channel.send("*This message was sent automatically and was recognized with an accuracy of " + str(last_auto_support_percent) + "%*")

def setup(bot):
    loadQAData()

    bot.add_cog(autosupport(bot))

def addQAData(question, answer):
    global qa_data_cache
    qa_data_cache[question] = answer

    json.dump(qa_data_cache, open("qa_data.json", "w"))

def loadQAData():
    global qa_data_cache
    try:
        qa_data_cache = json.load(open("qa_data.json"))
    except FileNotFoundError:
        json.dump(qa_data_cache, open("qa_data.json", "w"))

def levenshtein_ratio_and_distance(s, t):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        The function computes the levenshtein distance ratio
        of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0 # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                cost = 2
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    try:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    except:
        pass