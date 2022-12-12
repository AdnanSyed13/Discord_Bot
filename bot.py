import os
import random

import discord
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
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
    await ctx.send(response)

@bot.command(name='roll_dice', help='Simulates rolling dice. Specify number of dice, dice sides. Example: !roll_dice 3 6')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='create-channel', help='Creates a channel. Optionally, type the channel name. Example: !create-channel food')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)

# # Client handles events, tracks state, and interacts with Discord APIs.
# client = discord.Client(intents=discord.Intents.all())

# # # Welcome members to the server.
# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)  
#     print(
#         f'{client.user} has connected to the following guild:\n!'
#         f'{guild.name}(id: {guild.id})'
#     )


# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to Addy\'s Discord server!'
#     )

# # Bot sends a B99 quote when '99!' is typed. 
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     brooklyn_99_quotes = [
        
#     ]

#     if message.content == '99!':
#         response = random.choice(brooklyn_99_quotes)
#         await message.channel.send(response)
#     elif message.content == 'raise-exception':
#         raise discord.DiscordException

# # Creates an error log and message when 'raise-exception' is typed in the server.
# @client.event
# async def on_error(event, *args, **kwargs):
#     with open('err.log', 'a') as f:
#         if event == 'on_message':
#             f.write(f'Unhandled message: {args[0]}\n')
#         else:
#             raise

# @client.event
# async def on_message(message):
#     if 'happy birthday' in message.content.low():
#         await message. channel.send('Happy Birthday! 🎈🎉')

# client.run(TOKEN)

# NOTES:
# find() is a predicate which identifies some characteristic of the element in the iterable that you're looking for. We are using lambda as the predicate
# This case finds the same name as the one stored in the DISCORD_GUILD environment variable. The predicate located the variable, is satisfied, and
# returns the element. It is similar to a break statement but cleaner.