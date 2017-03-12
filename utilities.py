'''
Created on 10Feb.,2017
@author = Alex Palmer
'''
import time
import logging
import permissions
from discord.ext import commands
from datetime import timedelta
log = logging.getLogger()
startTime = time.localtime()
ownerID = '66141201631285248'
class Utilities:
    """ Commands relating to the Blitzcrank Bot's operations."""
    def __init__(self, bot):
        self.bot = bot

    async def on_command(self, command, ctx):
        message = ctx.message
        destination = None
        if message.channel.is_private:
            destination = 'Private message'
        else:
            destination = '#{0.channel.name}: {0.server.name})'.format(message)

        log.info('{0.timestamp}: {0.author} in {1}: {0.content}'.format(message, destination))

    @commands.command(pass_context=True, no_pm=True)
    async def ping(self, ctx):
        """Tests response time."""
        pingStart = time.time()
        msg = await self.bot.say('Pong!')
        pingEnd = time.time()
        pingDiff = pingEnd - pingStart
        response = 'Pong! completed in {}s.'.format(pingDiff)
        await self.bot.edit_message(msg, response)

    @commands.command(pass_context=True, no_pm=True)
    async def uptime(self, ctx):
        """Return's Blitzcrank Bot's uptime."""
        compareTime = time.localtime()
        elapsedTime = time.mktime(compareTime) - time.mktime(startTime)
        response = "Running for {}".format(timedelta(seconds=elapsedTime))
        await self.bot.say(response)

    @commands.command(pass_context=True, no_pm=True)
    @permissions.is_owner()
    async def shutdown(self, ctx):
        await self.bot.logout()

    @commands.command(pass_context=True, no_pm=True)
    async def info(self, ctx):
        info = ("A simple bot in it's first iteration for League of Legends "
                "summoner look ups. Written using discord.py by "
                "SuperFrosty#5263.")
        await self.bot.send_message(ctx.message.channel, info)
def setup(bot):
    bot.add_cog(Utilities(bot))
