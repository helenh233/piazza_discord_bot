import discord # (pip install -U discord.py)
from discord.ext import tasks, commands # extension library

from piazza_api import Piazza # (pip install piazza-api)
from piazza_api import network                                                           #merge with above?

from credentials import EMAIL, PASSWORD, DISCORD_TOKEN, IDs # Needs to be filled out
from prettify import *

###################################################################################

# Creates an instance of the class Piazza, and logs in
p = Piazza()
p.user_login(email=EMAIL, password=PASSWORD)

# Connects to Discord bot                                                        test out intent #
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} is connected to {guild.name}') # to console
    notifications.start(IDs)

# Bot will scan for unread posts every minute
@tasks.loop(minutes = 1)

# notifications will scan each Piazza course in (ids) and send notifications to its corresponding Discord channel
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
            link = f"https://piazza.com/class/{network_id}/post/{info['nr']}"
            
            # Most recent action on that post
            action = info['change_log'][-1]['type']
            
            # A question is created/updated:
            if action == 'create' or action == 'update':
                subject = info['history'][0]['subject']
                subject = prettify(subject, 'subject')
                # Make **bolded** and __underlined__ in Discord
                subject = f'__**{subject}**__'
                
                content = info['history'][0]['content']
                content = prettify(content, 'content')
                
                # Send summary of the post as a message into the Discord channel
                await channel.send(subject + '\n' + content + '\n\n' + link)

            # An answer has been created/updated for a question followed by the user
            elif info['is_bookmarked']:
                if action == 'i_answer' or action == 'i_answer_update':
                    answerer = 'Instructor'
                    # Retrieve contents of instructor answer
                    for answer in info['children']:
                        if answer['type'] == 'i_answer':
                            reply = answer['history'][0]['content']
                            
                if action == 's_answer' or action == 's_answer_update':
                    answerer = 'Student'
                    # Retrieve contents of student answer
                    for answer in info['children']:
                        if answer['type'] == 's_answer':
                            reply = answer['history'][0]['content']

                reply = prettify(reply)
                
                # Search through previous 100 messages in Discord channel for original question (identifiable by unique URL)
                async for message in channel.history(limit=100):
                    if link in message.content:
                        await message.reply(f"__**{answerer} answer**__\n{reply}")
                    
        
# Runs application
client.run(DISCORD_TOKEN)
