# piazza_discord_bot

When given a list of Piazza classes, this Discord bot will scan each class for unread questions every minute, then send a message into the class's coressponding Discord channel to notify the user.  
By using `prettify.py`, it will preserve text formatting, automatically link images, and render LaTex.  
If a student/instructor answer is created/updated for a Piazza post that the user follows, the bot will reply to the original Discord message with the answer.  
![Piazza Discord Bot](https://user-images.githubusercontent.com/67713010/208268100-b5c5010f-c184-406d-9878-5aa0964a0878.jpg | width=100)

### Instructions
In `credentials.py`, input a Piazza email and password, Discord bot token, and Piazza network IDs with their corresponding Discord channel IDs.  

Install the needed libraries:  
```
pip install -U discord.py  
pip install piazza-api  
pip install urllib  
pip install beautifulsoup4  
```
Run `bot.py`
