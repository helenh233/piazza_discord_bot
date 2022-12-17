import discord # (pip install -U discord.py)
from discord.ext import tasks, commands # extension library

from piazza_api import Piazza # (pip install piazza-api)
from piazza_api import network

from credentials import EMAIL, PASSWORD, DISCORD_TOKEN, IDs # Needs to be filled out
from prettify import *

###################################################################################

# Creates an instance of the class Piazza, and logs in
p = Piazza()
p.user_login(email=EMAIL, password=PASSWORD)

# Connects to Discord bot,                                                        test out intent #
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} is connected to {guild.name}') # to console
    notifications.start(IDs)

# Bot will scan for messages every minute
@tasks.loop(minutes = 1)

# notifications will scan each Piazza course in (ids) and send unread notifications to their corresponding Discord channel
# List of (Str, Int) -> None
async def notifications(ids):
    for ID in ids:
        network_id = ID[0]
        channel_id = ID[1]
        
        # Instance of Network class, for the Piazza course corresponding to (network_id)
        course = p.network(network_id) 

        # Instance of Channel class, for Discord channel corresponding to (channel_id)
        channel = client.get_channel(channel_id)

        # List of unread Piazza posts
        unread = course.get_filtered_feed(network.UnreadFilter())['feed']
        # Put in chronological order
        unread.reverse()

        for post in unread:
            '''
            network.get_post(cid) returns all the information stored about the post corresponding to (cid)
            Str -> Dict
            '''
            info = course.get_post(cid=post['id'])
            
            # Link to the Piazza post
            url = f"https://piazza.com/class/{network_id}/post/{info['nr']}"
            
            # Most recent action on that post
            action = info['change_log'][-1]['type']
            
            # A question is created/updated:
            if action == 'create' or action == 'update':
                # Print post's subject as **bold** and __underline__ in Discord
                subject = f"__**{info['history'][0]['subject']}**__"
                # Translate HTML entities to Unicode characters
                subject = BeautifulSoup(subject, 'html.parser').text
                
                content = info['history'][0]['content']
                content = prettify(content)
                # Send summary of the post as a message to the Discord channel
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
