import os
import csv
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

datapath = Path(os.path.dirname(__file__))

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
	print(f'Bot {bot.user} is online! Id: {bot.user.id}')

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message mentions the bot
    if bot.user.mentioned_in(message):
        # Respond with "hello"
        await message.channel.send("Hellooo!")

@bot.command(name='hello')
async def say_hello(ctx):
    await ctx.send("Hello!")
    
@bot.event
async def on_message(message):
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
    # Check if the reaction is on an image or video message
    if reaction.message.attachments:
        for attachment in reaction.message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await reaction.message.channel.send(f"User {user.mention} reacted to media!")
                with (datapath / "media_storage.csv").open("a") as f:
                    f.write(attachment.url + ',')

@bot.command(name='spotlight')
async def spotlight(ctx, n: int = 5):
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
