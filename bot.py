# bot.py
import os

import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    random_messages = ['prueba 1', 'prueba 2', 'prueba 3']

    if message.content == '99!':
        response = random.choice(random_messages)
        await message.channel.send(response)

client.run(TOKEN)
