'''
Created on 29Jan.,2017

@author = Alex Palmer
'''
import permissions
from discord.ext import commands
class Reload:
    """Blitzcrank's reloading module,"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    @permissions.is_owner()
    async def reload(self, *, module: str):
        """Reloads the specified module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say("There was an error reloading module {}:".format(module))
            await self.bot.say("```fix\n{}: {}\n```".format(type(e).__name__, e))
        else:
            await self.bot.say("{} successfully reloaded.".format(module))

def setup(bot):
    bot.add_cog(Reload(bot))
