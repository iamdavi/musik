# bot.py
import os

# import discord
import random
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands

# Establecemos que el prefijo de los comandos para este BOT sea "$"
client = commands.Bot(command_prefix="!")
# Obtenemos el token de seguridad
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@client.command()
async def play(ctx, url = str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Espera a que la pista actual finalice o usa el comando '!stop'")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Global')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_connected():
        await voiceChannel.connect()

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("El bot no está conectado a ningún chat de voz")

@client.comment()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.send("El audio no está en reproducción")

@client.comment()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("El audio no está pausado")

@client.comment()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()



# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     random_messages = ['prueba 1', 'prueba 2', 'prueba 3']

#     if message.content == '99!':
#         response = random.choice(random_messages)
#         await message.channel.send(response) 
# Ian

client.run(TOKEN)
