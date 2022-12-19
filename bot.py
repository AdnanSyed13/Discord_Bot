import os
import json
import random
import requests

import discord
from discord.ext import commands
from dotenv import load_dotenv
from weather import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('weather_api_key')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Changes the bot status to "Listening to w.<location>".
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='w.<location>'))

# Retreives the weather for the location input specified.
@bot.event
async def on_message(message):
    command_prefix = 'w.'
    if message.author != bot.user and message.content.startswith(command_prefix):
        if len(message.content.replace(command_prefix, '')) >= 1:
            location = message.content.replace(command_prefix, '').lower()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=imperial'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=error_message(location))
    await bot.process_commands(message)

# Retrives a random Brooklyn 99 quote.
@bot.command(name='99', help='Responds with a random quote from Brooklyn 99, example: !99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.channel.send(response)

# Simulates dice rolling.
@bot.command(name='roll_dice', help='Simulates rolling dice. Specify number of dice, dice sides. Example: !roll_dice 3 6')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

# Creates a channel for input channel specified. It defaults to "real-python" as channel output if no input specified.
@bot.command(name='create-channel', help='Creates a channel. Optionally, type the channel name. Example: !create-channel food')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

# Gives an error message if the command is invalid.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)