'''
Created on 20Feb.,2017

@author = Alex Palmer
'''
from discord.ext import commands

class Info:
    """Commands that return helpful information."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def regions(self):
        """Lists valid regions"""
        msg = "BR, EUNE, EUW, JP, KR, LAN, LAS, NA, OCE, PBE, RU, TR"
        await self.bot.say("```fix\n" + msg + "\n```")


def setup(bot):
    bot.add_cog(Info(bot))
