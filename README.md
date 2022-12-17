# piazza_discord_bot
## A Discord bot that will send channel notifications for new posts in specified Piazza classes.

When given a list of Piazza classes, this bot will scan each class for unread questions every minute, then send a message into the class's coressponding Discord channel to notify the user.
It will preserve text formatting, automatically link images, and render LaTex.
If a student/instructor answer is created/updated for a Piazza post that the user follows, the bot will reply to the original Discord message with the answer.


### To use
In 'credentials.py', input a Piazza email and password, Discord bot token, and Piazza network IDs with their coressponding Discord channel IDs.

Install the needed libraries:
'''
pip install -U discord.py
pip install piazza-api
pip install urllib
pip install beautifulsoup4
'''
