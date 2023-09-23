#auth key MTE1NDk3MTkzMjQ2NzQxNzE5MQ.Gm8d8O.le6J1lpqnsIinZGhmv-uTqePkL3qgl5pQJYgjc

import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

@bot.event
async def on_ready():
	print(f'Bot {bot.user} is online! Id: {bot.user.id}')

async def main():
	await bot.start('MTE1NDk3MTkzMjQ2NzQxNzE5MQ.Gm8d8O.le6J1lpqnsIinZGhmv-uTqePkL3qgl5pQJYgjc')

@bot.command()
async def timer(ctx: commands.Context, time: int):
	await asyncio.sleep(time)
	await ctx.send("your time is up!")

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot itself to prevent a loop
    if message.author == bot.user:
        return

    # Check if the message mentions the bot
    if bot.user.mentioned_in(message):
        # Respond with "hello"
        await message.channel.send("Hello!")

asyncio.run(main())
