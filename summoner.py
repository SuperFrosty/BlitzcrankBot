'''
Created on 19Feb.,2017

@author = Alex Palmer
'''
import discord
from discord.ext import commands
from cassiopeia import riotapi

class Summoner:
    """Commands relating to individual summoners."""
    riotapi.set_api_key('RGAPI-8d8a8efd-d6da-4025-895f-905ccdb38a21')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, ignore_extra=False)
    async def champmastery(self, ctx, sumName:str, champName:str, region:str):
        """'Summoner Name' 'Champion' 'Region'"""
        if "'" in sumName:
            await self.bot.send_message(ctx.message.channel, "Please use double quotes to enclose names.")
            return
        if "'" + champName + "'" in champName:
            await self.bot.send_message(ctx.message.channel, "Please use double quotes to enclose names.")
            return 
        await self.bot.send_typing(ctx.message.channel)
        chest = None
        riotapi.set_region(region)
        champion = riotapi.get_champion_by_name(champName)
        summoner = riotapi.get_summoner_by_name(sumName)
        mastery = riotapi.get_champion_mastery(summoner, champion)
        if " " in mastery.champion.name:
            urlChampName = mastery.champion.name.replace(" ", "")
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(urlChampName)
        elif "Vel'Koz" in mastery.champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Velkoz.png'
        elif "Kha'Zix" in mastery.champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Khazix.png'
        elif "Rek'Sai" in mastery.champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/RekSai.png'
        elif "Cho'Gath" in mastery.champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/Chogath.png'
        elif "Kog'Maw" in mastery.champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/KogMaw.png'
        else:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(mastery.champion.name)
        if mastery.chest_granted == True:
            chest = "Yes"
        elif mastery.chest_granted == False:
            chest = "No"

        em = discord.Embed(title="Champion Mastery", colour=0x1affa7)
        em.set_thumbnail(url=url)
        em.add_field(name='Summoner:', value='{}'.format(sumName), inline=True)
        em.add_field(name='Champion:', value="{}".format(champName),
                        inline=True)
        em.add_field(name='Champion level:', value='{}'.format(mastery.level),
                        inline=True)
        em.add_field(name='Champion points:', value='{}'.format(mastery.points),
                        inline=True)
        em.add_field(name='Points to next level:',
                        value='{}'.format(mastery.points_until_next_level),
                        inline=True)
        em.add_field(name='Chest granted:', value='{}'.format(
                        chest), inline=True)

        await self.bot.send_message(ctx.message.channel, '', embed=em)

    @commands.command(pass_context=True, no_pm=True, ignore_extra=False)
    async def lookup(self, ctx, sumName:str, region:str):
        """'Summoner Name' 'Region'"""
        if "'" in sumName:
            await self.bot.send_message(ctx.message.channel, "Please use double quotes to enclose names.")
            return
        await self.bot.send_typing(ctx.message.channel)
        title = "Summoner Lookup - {0} ({1})".format(sumName, region)
        em = discord.Embed(title=title, colour=0x1affa7)
        loop = 0
        overallWins = 0
        overallLosses = 0
        riotapi.set_region(region)
        summoner = riotapi.get_summoner_by_name(sumName)
        leagues = riotapi.get_league_entries_by_summoner(summoner)
        topChamp = riotapi.get_top_champion_masteries(summoner, max_entries=3)
        topChamps = "{0}, {1} and {2}".format(topChamp[0].champion.name,
                    topChamp[1].champion.name, topChamp[2].champion.name)
        em.add_field(name="Top Champions", value=topChamps, inline=False)
        if " " in topChamp[0].champion.name:
            urlChampName = topChamp[0].champion.name.replace(" ", "")
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(urlChampName)
        elif "Vel'Koz" in topChamp[0].champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Velkoz.png'
        elif "Kha'Zix" in topChamp[0].champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/Khazix.png'
        elif "Rek'Sai" in topChamp[0].champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/RekSai.png'
        elif "Cho'Gath" in topChamp[0].champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/Chogath.png'
        elif "Kog'Maw" in topChamp[0].champion.name:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.8.1/img/champion/KogMaw.png'
        else:
            url = 'http://ddragon.leagueoflegends.com/cdn/7.3.3/img/champion/{}.png'.format(topChamp[0].champion.name)
        em.set_thumbnail(url=url)
        for league in leagues:
            loop += 1
            queue = league.queue.value
            tier = league.tier.value
            for entries in league.entries:
                division = entries.division.value
                lp = str(entries.league_points) + ' LP'
                wins = entries.wins
                overallWins += wins
                losses = entries.losses
                overallLosses += losses
            if queue == 'RANKED_SOLO_5x5':
                ratio = (wins / (wins + losses) * 100)
                value = "{0} {1} {2} ({3}W/{4}L {5:.2f}%)".format(tier,
                            division, lp, wins, losses, ratio)
                em.add_field(name="Ranked Solo", value=value, inline=False)
            elif queue == 'RANKED_FLEX_SR':
                ratio = (wins / (wins + losses) * 100)
                value = "{0} {1} {2} ({3}W/{4}L {5:.2f}%)".format(tier,
                            division, lp, wins, losses, ratio)
                em.add_field(name="Ranked Flex", value=value, inline=False)
            elif queue == 'RANKED_FLEX_TT':
                ratio = (wins / (wins + losses) * 100)
                value = "{0} {1} {2} ({3}W/{4}L {5:.2f}%)".format(tier,
                            division, lp, wins, losses, ratio)
                em.add_field(name="Ranked TT", value=value, inline=False)
            overallRatio = (overallWins / (overallWins + overallLosses) * 100)
        value1 = "{0}W/{1}L ({2:.2f})%".format(overallWins, overallLosses,
                    overallRatio)

        em.add_field(name="Overall", value=value1, inline=False)
        await self.bot.send_message(ctx.message.channel, "", embed=em)


def setup(bot):
    bot.add_cog(Summoner(bot))
