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

    @commands.command(pass_context=True, no_pm=True)
    async def invite(self):
        """Add Blitzcrank to your server with this link!"""
        link = "https://discordapp.com/oauth2/authorize?client_id=282765243862614016&scope=bot&permissions=19456"
        await self.bot.say("Invite me to your server with this link!\n" + link)

    @commands.command(pass_context=True, no_pm=True)
    async def support(self):
        """Join the support server to ask for help!"""
        link = "https://discord.gg/J78uAgZ"
        await self.bot.say("Join my support server if you need help with commands!\n " + link)
        
def setup(bot):
    """Adds cog to bot"""
    bot.add_cog(Info(bot))
