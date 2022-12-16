import discord # pip install -U discord.py
from discord.ext import tasks, commands # extension library

from piazza_api import Piazza # pip install piazza-api
from piazza_api import network

from credentials import EMAIL, PASSWORD, DISCORD_TOKEN, IDs # Needs to be filled out
from prettify import *

#################################################

# Creates an instance of the Piazza class, and logs in
p = Piazza()
p.user_login(email=EMAIL, password=PASSWORD)

# Connects to Discord bot, test out intent #
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == 'School':
            break
    print(f'{client.user} is connected to {guild.name}')
    
    notifications.start(IDs)

# Function will run every minute
@tasks.loop(minutes = 1)

# notifications() will scan each class's Piazza feed and send updates to specific channels in a Discord server
# List of (Str, Str, Int) -> None
# Ex) notifications( [('Class name', 'Course's network ID on Piazza', 'Channel's ID on Discord')] )
async def notifications(ids):
    for ID in ids:
        network_id = ID[1]
        channel_id = ID[2]
        
        # Instance of Network class, for the Piazza course with (network_id)
        course = p.network(network_id) 

        # Instance of Channel , for Discord channel with (channel_id)
        channel = client.get_channel(channel_id)

        # List of unread Piazza posts
        unread = course.get_filtered_feed(network.UnreadFilter())['feed']
        unread.reverse() # FIFO

        for post in unread:
            # Dictionary
            info = course.get_post(cid=post['id'])
            
            url = f"https://piazza.com/class/{network_id}/post/{info['nr']}"
            
            # Most recent action on that post
            action = info['change_log'][-1]['type']
            
            if action == 'create' or action == 'update':
                # **bold** and __underline__ in Discord
                subject = f"__**{info['history'][0]['subject']}**__" 
                subject = BeautifulSoup(subject, 'html.parser').text
                
                content = info['history'][0]['content']
                content = prettify(content)

                await channel.send(subject + '\n\n' + content + '\n\n' + url)

            elif info['is_bookmarked']:
                if action == 'i_answer' or action == 'i_answer_update':
                    answerer = 'Instructor'
                    for answer in info['children']:
                        if answer['type'] == 'i_answer':
                            reply = answer['history'][0]['content']
                            
                if action == 's_answer' or action == 's_answer_update':
                    answerer = 'Student'
                    for answer in info['children']:
                            if answer['type'] == 's_answer':
                                reply = answer['history'][0]['content']

                reply = prettify(reply)
                
                async for message in channel.history(limit=100):
                    if url in message.content:
                        await message.reply(f"__**{answerer} answer**__\n{reply}")
                    
        
# Runs application
client.run(DISCORD_TOKEN)
