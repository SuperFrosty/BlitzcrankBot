'''
Created on 19Feb.,2017

@author: Alex Palmer
'''
import asyncio
import logging
import traceback

import aiohttp
import websockets
import discord
from discord.ext import commands

import backoff
import permissions

description = ("Made by SuperFrosty#5263 for various Riot API related "
               "commands. Every command should be prefix'd with bl! "
               "(for example, bl!lookup).")
bot = commands.Bot(command_prefix=commands.when_mentioned_or('bl!'),
                   description=description)
startup_extensions = ['utilities', 'summoner', 'info', 'reload']
ownerID = '66141201631285248'

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='blitzcrank.log', encoding='utf-8',
                                   mode='w')
formatter = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
log = logging.getLogger()
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log.addHandler(ch)
file_handler.setFormatter(logging.Formatter(formatter))
discord_logger.addHandler(file_handler)

@bot.event
async def on_ready():
    """Sets game presence and indicates when ready."""
    game = 'bl!help | Fleshling Compatibility Service'
    await bot.change_presence(game=discord.Game(name=game))
    print('Logged in as:\n{0} (ID: {0.id})'.format(bot.user))
    print('--------------------------------')

@bot.event
async def on_message(message):
    """Functions that are not part of ext for various reasons."""
    #eval command here because idk how to get it to work in cogs
    if message.content.startswith('bl!eval') and permissions.is_owner():
        parameters = ' '.join(message.content.strip().split(' ')[1:])
        output = None
        try:
            originalmessage = await bot.send_message(message.channel,
                    'Executing: ' + message.content + ' one moment, please...')
            output = eval(parameters)
        except Exception:
            error = "```fix\n" + str(traceback.format_exc()) + "\n```"
            await bot.edit_message(originalmessage, error)
            traceback.print_exc()
        if asyncio.iscoroutine(output):
            output = await output
        if output:
            success = "```fix\n" + str(output) + "\n```"
            await bot.edit_message(originalmessage, success)
    await bot.process_commands(message)

@bot.event
async def on_command_error(error, ctx):
    """Error handling."""
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, error)
    elif isinstance(error, commands.CommandInvokeError):
        if str(error).startswith('Command raised an exception: APIError: Server'
                                 ' returned error '
                                 '404 on call'):
            error_msg = ('Server returned 404. This mostly likly means you have '
                         'no ranked stats this season. Alternativly, '
                         'you spelt your summoner name wrong.')
            await bot.send_message(ctx.message.channel, error_msg)
            print(ctx.message.content)
            print(error)
        elif str(error).startswith("Command raised an exception: AttributeError"
                                   ": NoneType object has no attribute 'id'"):
            error_msg = ("Please use capitals for champion names (i.e. 'Teemo'"
                         "not 'teemo').")
            await bot.send_message(ctx.message.channel, error_msg)
        if str(error).startswith('Command raised an exception: APIError: Server'
                                 ' returned error 400 on call'):
            error_msg = ("Server returned empty values, this usually mean no "
                         "mastery points found for given champion.")
            await bot.send_message(ctx.message.channel, error_msg)
            print(ctx.message.content)
            print(error)
        if str(error).startswith('Command raised an exception: APIError: Server'
                                 ' returned error 403 on call'):
            error_msg = ("Riot's servers denied your attempt escaping a URL :( (Don't use "
                         "'/'s in your name)")
            await bot.send_message(ctx.message.channel, error_msg)
            print(ctx.message.content)
            print(error)
        else:
            await bot.send_message(ctx.message.channel, "Something went wrong, sorry :I")
            print(ctx.message.content)
            print(error)
            traceback.print_exc()
        await bot.send_message(ctx.message.channel, "If you feel like this shouldn't be happening, feel free to join my support server with bl!support")
@bot.event
async def on_server_join(server):
    l = list(filter(lambda m: m.bot, server.members))
    members = len(server.members)
    if len(l) / len(server.members) >= .60:
        bots = "{0}% bots".format(100 * (len(l) / len(server.members)))
        await bot.leave_server(server)
        embed = discord.Embed(title="Left Server", colour=0x1affa7)
        embed.add_field(name="Server:", value=server.name, inline=True)
        embed.add_field(name="Reason:", value="Bot collection server", inline=True)
        embed.add_field(name="Users:", value=members, inline=True)
        embed.add_field(name="Justification:", value=bots, inline=True)
        await bot.send_message(discord.Object(id='295831639219634177'), "", embed=embed)
    else:
        embed = discord.Embed(title="Joined Server", colour=0x1affa7)
        embed.add_field(name="Server:", value=server.name, inline=True)
        embed.add_field(name="Users:", value=members, inline=True)
        embed.add_field(name="Total:", value=len(bot.servers), inline=True)
        await bot.send_message(discord.Object(id='295831639219634177'), "", embed=embed)

async def keep_running():
    """Retries connect on loss for any reason other than 4004."""
    retry = backoff.ExponentialBackoff()

    while True:
        try:
            await bot.login(TOKEN)

        except (discord.HTTPException, aiohttp.ClientError):
            logging.exception("Attempting to login")
            await asyncio.sleep(retry.delay())

        else:
            break

    while bot.is_logged_in:
        if bot.is_closed:
            bot._closed.clear()
            bot.http.recreate()

        try:
            await bot.connect()

        except (discord.HTTPException, aiohttp.ClientError,
                discord.GatewayNotFound, discord.ConnectionClosed,
                websockets.InvalidHandshake,
                websockets.WebSocketProtocolError) as e:
            if isinstance(e, discord.ConnectionClosed) and e.code == 4004:
                raise # Do not reconnect on authentication failure
            logging.exception("Attempting to login")
            await asyncio.sleep(retry.delay())
TOKEN = 'MjgyNzY1MjQzODYyNjE0MDE2.C7phSg.mCQp7oLEqdZeWTmxpt5QQqVNrqQ'

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    asyncio.get_event_loop().run_until_complete(keep_running())
