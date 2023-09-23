import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


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
    print('command decorator')
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
                await message.channel.send(f"User {message.author.mention} posted an image or video!")

    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message contains attachments (images or videos)
    if message.attachments:
        for attachment in message.attachments:
            print(attachment)
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await message.channel.send(f"User {message.author.mention} posted an image or video!")

    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is on an image or video message
    if reaction.message.attachments:
        for attachment in reaction.message.attachments:
            if attachment.content_type.startswith('image') or attachment.content_type.startswith('video'):
                await reaction.message.channel.send(f"User {user.mention} reacted to an image or video!")

    
bot.run(TOKEN)
