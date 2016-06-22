import requests
import json
import discord
from discord.ext import commands
from random import randint
from random import choice as randchoice
import datetime
import time
import aiohttp
import asyncio

class ServerLeague(object):
    def __init__(self, json_response):
        self.parse_json(json_response)

    def parse_json(self, response):
        self.name = response['name']
        self.region = response['region']
        self.size = response['teamsize']
        self.arenas = response['arenas']
        if response['voteingame'] == "1":
            self.vote = True
        else:
            self.vote = False
            self.maxscore = response['maxscore']
            self.maxspeed = response['maxspeed']
            self.ballmaxspeed = response['ballmaxspeed']
            self.balltype = response['balltype']
            self.ballsize = response['ballsize']
            self.ballbounciness = response['ballbounciness']
            self.boostamount = response['boostamount']
            self.booststrength = response['booststregth']
            self.gravity = response['gravity']
            self.demolish = response['demolish']
            self.respawntime = response['respawntime']
        self.platform = response['platform']
        self.starttime = response['starttime']
        self.endtime = response['endtime']
        if response['snrl'] == 1:
            self.snrl = True
        else:
            self.snrl = False


def get_servers(url):
    servers_list = []
    r = requests.get(url)
    response = json.loads(r.text)
    for server in response:
        server_settings = ServerLeague(server)
        servers_list.append(server_settings)
    return servers_list


def count_servers(servers_list):
    return len(servers_list)


def filter_by_region(servers, region):
    filtered_list = []
    for server in servers:
        if server.region == region:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


def filter_by_platform(servers, platform):
    filtered_list = []
    for server in servers:
        if server.platform == platform:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


def filter_by_vote(servers, vote):
    filtered_list = []
    for server in servers:
        if server.vote:
            filtered_list.append(server)
    return filtered_list, len(filtered_list)


class General:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(hidden=True)
    async def hello(self):
        """hello world."""
        await self.bot.say("hithere!")


    @commands.command(hidden=True)
    async def servers(self):
        """servers command returns list of serverleague hosted servers."""
        servers = get_servers(url='http://dev.serverleague.com/api/v1/list')
        await self.bot.say("There are currently **" + str(count_servers(servers))+"** online")
        await self.bot.say("Pong.")


def setup(bot):
    bot.add_cog(ServerLeague(bot))

# servers = get_servers('http://dev.serverleague.com/api/v1/list')
# filtered_servers = filter_by_region(servers, "Oceania")
# for servers in filtered_servers[0]:
#     print servers.region
# print filtered_servers
