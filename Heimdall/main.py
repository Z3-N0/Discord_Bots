import os
import discord
from Trackers.solana.server import activate

client = discord.Client()

@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
  msgID = 995691209181909122

  if msgID == payload.message_id:
    member = payload.member
    guild = member.guild
    emoji = payload.emoji.name
    if emoji == '☀️':
      role = discord.utils.get(guild.roles, name = 'Degen')
    await member.add_roles(role)

@client.event
async def on_message(message): 
  if message.author == client.user:
    return

  if '(╯°□°）╯︵ ┻━┻' in message.content:
    embed = discord.Embed(title = "No tables left unflipped", description = '┬─┬ ノ( ゜-゜ノ)', color = discord.Color.blue())
    await message.channel.send(embed = embed)


    

  

activate()
client.run(os.getenv('TOKEN'))