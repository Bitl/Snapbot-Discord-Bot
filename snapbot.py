#include files
import discord
from discord.ext import commands
import asyncio
import logging
import random
import aiohttp
from time import localtime, strftime
from datetime import date
import json

#logger for the internal console, the discordAPI, and Snapbot itself.
logger = logging.getLogger('snapbot_console')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

logger2 = logging.getLogger('discord')
logger2.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='snapbot_discordAPI.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger2.addHandler(handler)

logger3 = logging.getLogger('snapbot')
logger3.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='snapbot_logfile.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger3.addHandler(handler)

#init Snapbot
print('Snapbot Loading...')
logger3.debug("Snapbot Loading...")

#init bot
bot = commands.Bot(command_prefix="sn!", description="Intelligent Discord chat bot.")
aiosession = aiohttp.ClientSession(loop=bot.loop)

#game list. for fun.
game_list = ["Team Fortress 2", "Garry's Mod", "Portal", "Portal 2", "Left 4 Dead", "Left 4 Dead 2", "Half-Life 2", "Half-Life", "Counter-Strike: Global Offensive", 
"BioShock Infinite", "BioShock", "BioShock 2", "Killing Floor", "Killing Floor 2", "Borderlands", "Borderlands 2", "Fallout 3", "Fallout New Vegas", "Fallout 4", "DOOM", 
"Wolfenstein: The New Order", "Wolfenstein: The Old Blood", "The Ultimate DOOM", "DOOM II", "Final DOOM", "Quake", "Quake II", "Quake III Arena", "Wolfenstein 3D",
"Quake Live", "Synergy", "Terraria", "Minecraft", "ROBLOX", "Spore", "System Shock 2", "Duke Nukem 3D", "POSTAL 2", "Shadow Warrior", "Shadow Warrior 2", "Shadow Warrior Classic",
"Counter-Strike", "Counter-Strike Source", "Serious Sam: The First Encounter", "Serious Sam: The Second Encounter", "Serious Sam 3: BFE", "Pong", "Tetris", "Super Mario Bros.",
"Pac-Man", "Mrs. Pac-Man", "Sonic the Hedgehog", "Reflex Arena", "Overwatch", "League Of Legends", "Dota 2", "Halo Combat Evolved", "Halo Custom Edition", "Halo Online", 
"ElDewrito", "Team Fortress 2 Classic", "Synergy", "FIREFIGHT RELOADED", "Unreal Tournament", "GZDOOM", "ZDOOM", "GLQuake", "WinQuake", "Spacewar!"]

data = {}
config = {}

with open('sayings.json') as json_data_file:
     data = json.load(json_data_file)
	 
with open('config.json') as json_config_file:
     config = json.load(json_config_file)
	 
#global vars.
gamermode_config = config["gamermode"]

if gamermode_config == "True":
     gamermode = True
else:
     gamermode = False

#number of seconds that we are idle for when typing
idletime = float(config["idletime"])
        
#ready event.
@bot.event
async def on_ready():
  print('Logged in!')
  print('---------')
  print('Name: ' + bot.user.name)
  print('ID: ' + bot.user.id)
  print('---------')
  print('Modes enabled:')
  print('---------')
  if gamermode == True:
    print('Gamer Mode: Enabled')
  else:
    print('Gamer Mode: Disabled')
  print('---------')
  print('Snapbot Loaded.')
  print('---------')
  print('To invite to your server use')
  print('https://discordapp.com/api/oauth2/authorize?client_id=' + bot.user.id + '&scope=bot&permissions=0')
  print('---------')
  if gamermode == True:
     bot.loop.create_task(change_game())
  
async def change_game():
  await bot.wait_until_ready()
  while gamermode == True:
    chosen_game = random.choice(game_list)
    logger.debug("Now Playing:")
    logger.debug(chosen_game)
    await bot.change_presence(game=discord.Game(name=chosen_game))
    await asyncio.sleep(1800)

#event on message.
@bot.event
async def on_message(message):
  #make sure we don't mention ourselves.
  if message.author == bot.user:
    return

  splitcontent = message.content.split()
  for i in splitcontent:
     if i in data:
         await doresponsepattern(message, message.content, i)
         
  await bot.process_commands(message)
  
async def doresponsepattern(message, content, saying):
  try:
    msg_content = data[saying]
    await response(message, msg_content)
    logger.debug("Sent a message!")
    logger3.debug("Sent a message!")
  except Exception as e:
    logger.debug("Failed to send a message!")
    logger3.debug("Failed to send a message!")
  
async def response(message, content):
  await bot.send_typing(message.channel)
  await asyncio.sleep(idletime)
  await bot.send_message(message.channel, content)

print('Connecting...')
logger3.debug("Snapbot Connecting...")
try:
 file = open('token.txt', 'r') 
 bot.run(file.readline())
 file.close()
 logger3.debug("Snapbot Connected!")
except Exception as e:
 logger3.debug("Snapbot failed to connect with Discord!")
except:
 bot.logout()
