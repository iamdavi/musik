# bot.py
import os

import discord
import random
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands

# Establecemos que el prefijo de los comandos para este BOT sea "$"
client = commands.Bot(command_prefix="$")
# Obtenemos el token de seguridad
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@client.command()
async def hola(ctx):
	usuario = ctx.message.author.name
	await ctx.send("Hola "+usuario)

@client.command()
async def prueba(ctx):
	await ctx.send("No implementado")

@client.command()
async def play(ctx, url):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Espera a que la pista actual finalice o usa el comando '!stop'")
        return

    channel =  ctx.message.author.voice.channel
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=str(channel))
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([str(url)])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("El bot no está conectado a ningún chat de voz")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.send("El audio no está en reproducción")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.send("El audio no está pausado")

@client.command()
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

client.run(TOKEN)
