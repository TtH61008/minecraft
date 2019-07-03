# discordのbotです
# サーバで動かす場合、gcloud関連とdiscord関連でそれぞれセットアップをする必要があります
# https://qiita.com/thinceller/items/6bc7d28a04a8da75e818
# https://mattyan1053.hatenablog.com/entry/2019/02/18/205020

import asyncio
import os
from time import sleep

from googleapiclient import discovery
import discord

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Instance information
# PROJECT = 'minecraft-server'
PROJECT = 'confident-slice-243412'
ZONE = 'asia-northeast1-b'
INSTANCE = 'mc-server'

# Build and nitialize google api
compute = discovery.build('compute', 'v1')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content =="/cat":
        await message.channel.send('にゃーん')
    if message.content.startswith('/minecraft'):
        # ex.) message.content: '/minecraft start' => command: 'start'
        command = message.content.split(' ')[1]

        if command == 'start':
            m = await message.channel.send('Server starting up...')
            start_server(PROJECT, ZONE, INSTANCE)
            await m.edit(content='Success! Server started up.')
            # sleep(10)
            # await m.delete()
        elif command == 'stop':
            m = await message.channel.send( 'Server stopping...')
            stop_server(PROJECT, ZONE, INSTANCE)
            await m.edit(content='Success! Server stopped.')
            # sleep(10)
            # await m.delete()
        elif command == 'status':
            status = get_server_status(PROJECT, ZONE, INSTANCE)

            if status == 'RUNNING':
                m = await message.channel.send('Server is running! Please enjoy Minecraft!')
                # sleep(10)
                # await m.delete()
            elif status in {'STOPPING', 'STOPPED'}:
                m = await message.channel.send(
                                'Server is stopped. If you play Minecraft, please chat in this channel, `/minecraft start`.')
                # sleep(10)
                # await m.delete()
            else:
                m = await message.channel.send(
                                'Server is not running. Please wait for a while, and chat in this channel, `/minecraft start`.')
                # sleep(10)
                # await m.delete()
        elif command == 'help':
            m = '''
            ```Usage: /minecraft [start][stop][status]
    start   Start up minecraft server
    stop    Stop minecraft server
    status  Show minecraft server status(running or stopped)```
            '''.strip()
            await message.channel.send(m)

def start_server(project, zone, instance):
    compute.instances().start(project=project, zone=zone, instance=instance).execute()

def stop_server(project, zone, instance):
    compute.instances().stop(project=project, zone=zone, instance=instance).execute()

def get_server_status(project, zone, instance):
    res = compute.instances().get(project=project, zone=zone, instance=instance).execute()
    return res['status']

client.run(BOT_TOKEN)
