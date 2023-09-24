This is the repository for our Hack Rice 13 

Team members:
Burkely Pettijohn,
Nikita Naumov

Nikita and I decided to create a Discord bot that organizes media
posted by members of the discord and monitors the amount of interactions 
the members have with each one. On command, it will provide the favorite 
images posted to the discord.

The primary code is stored in:     /bot/bot.py

The token and guild are stored in .env files locally

The data is stored in:     /bot/media_storage.csv

To run the bot, first create the bot on the discord developer webpage and 
generate a new token. Clone this repo and update the .env file with your 
token Run bot.py. Then add your bot you created on the developer page to 
your discord server and use command !spotlight n, where n is the top n 
number of images/videos you would like to see. 
