import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event #This event tells you that the bot is online
async def on_ready():
	print(f'Bot {bot.user} is online! Id: {bot.user.id}')

@bot.event #This event prevents the bot from responding to itself and creating a loop
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message mentions the bot
    if bot.user.mentioned_in(message):
        # Respond with "hello"
        await message.channel.send("Hellooo!")

# @bot.command(name='hello')
# async def say_hello(ctx):
#     print('command decorator')
#     await ctx.send("Hello!")

reaction_count = {}

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message contains attachments (images or videos)
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await message.channel.send(f"User {message.author.mention} posted an image or video!")
                if message.id not in reaction_count.keys():
                    reaction_count[message.id] = 0
                

    # Process commands
    await bot.process_commands(message)

# @bot.event
# async def on_message(message):
#     # Ignore messages sent by the bot itself to prevent a loop
#     if message.author == bot.user:
#         return

#     # Check if the message contains attachments (images or videos)
#     if message.attachments:
#         for attachment in message.attachments:
#             print(attachment)
#             if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
#                 await message.channel.send(f"User {message.author.mention} posted an image or video!")

#     # Process commands
#     await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is on an image or video message
    if reaction.message.attachments:
        for attachment in reaction.message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await reaction.message.channel.send(f"User {user.mention} reacted to an image or video!")
                reaction_count[reaction.message.id] += 1
                print(reaction_count)

# Run the bot with your token
bot.run(TOKEN)
