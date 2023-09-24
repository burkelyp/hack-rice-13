# Author: Burkely Pettijohn and Nikita Naumov
# GitHub username: burkelyp BummerBobby
# Date: 9/22-24/2023
# Description:  Rice Hack-a-thon 13: HackRice 13
#               We have built a Discord bot that manages media files sent
#               to a discord server. Once the bot joins a server it manages
#               the url's of images and videos posted to the discord. It
#               then tracks how often a member of the discord interacts with
#               the media via likes, laughing, etc. reactions. You can then
#               call the !spotlight function to display the top n media posts
#               n defaults to 5 but can be specified to any number.




import os
import csv
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')   # store token in .env file

datapath = Path(os.path.dirname(__file__))    # for writing the url data to /storage.csv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """
    Notify user when bot is online
    """
    print(f'Bot {bot.user} is online! Id: {bot.user.id}')

# @bot.event
# async def on_message(message):
#     """
#     This was a test function to get the bot to say hello to us upon asking   
#     """
#     # Ignore messages sent by the bot itself to prevent a loop
#     if message.author == bot.user:
#         return

#     # Check if the message mentions the bot
#     if bot.user.mentioned_in(message):
#         # Respond with "hello"
#         await message.channel.send("Hellooo!")

@bot.command(name='hello')
async def say_hello(ctx):
    """
    To say hello to our bot, just type <!hello>
    """
    await ctx.send("Hello!")
    
@bot.event
async def on_message(message):
    """
    This function collects the url of every image or video posted to the discord,
    and stores it in media_storage.csv
    The function also notifies the discord that someone has posted media
    """
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message contains attachments (images or videos)
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                with (datapath / "media_storage.csv").open("a") as f:
                    f.write(attachment.url + ',')
            if attachment.content_type.startswith('image'):
                await message.channel.send(f"User {message.author.mention} posted an image!")
            elif attachment.content_type.startswith('video'):
                await message.channel.send(f"User {message.author.mention} posted a video!")

    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    """
    Adds url to media_storage.csv to count
    """
    # Check if the reaction is on an image or video message
    if reaction.message.attachments:
        for attachment in reaction.message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await reaction.message.channel.send(f"User {user.mention} reacted to media!")
                with (datapath / "media_storage.csv").open("a") as f:
                    f.write(attachment.url + ',')

@bot.command(name='spotlight')
async def spotlight(ctx, n: int = 5):
    """
    !spotlight function to display the top n media posts to the group

    example:
    !spotlight 7      the top 7 media 
    !spotlight        the top 5 media

    """
    media_data = str(Path(os.path.dirname(__file__))) + '/media_storage.csv'

    count_dict = {}
    with open(media_data, 'r') as csvfile:
        reader_variable = csv.reader(csvfile)
        for items in reader_variable:
            for item in items[:-1]:
                if item in count_dict:
                    count_dict[item] += 1
                else:
                    count_dict[item] = 0

    sorted_count = sorted(count_dict.items(), key=lambda x:x[1], reverse=True)

    await ctx.send(f'Your top {n} most interacted with image(s)/video(s) are: \n')

    index = 1
    for key, value in sorted_count[:n]:
        await ctx.send(f"#{index}: {str(value)} reaction(s) \n")
        await ctx.send(key)
        index += 1

    
bot.run(TOKEN)
