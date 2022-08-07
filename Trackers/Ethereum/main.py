import discord
import os
import requests
from server import activate
import asyncio
import locale
locale.setlocale( locale.LC_ALL, '' )

#accessing client 
client = discord.Client()

@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))

async def change_stat():
  await client.wait_until_ready()

  while not client.is_closed():

    URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
    URL2 = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    req = requests.get(url = URL)
    req2 = requests.get(url = URL2)
    data = req.json()
    data2 = req2.json()
    
    sol_inr = data[1]['current_price']
    sol_inr = locale.currency( sol_inr, grouping=True )
    
    sol_usd = data2[1]['current_price']
    sol_usd = locale.currency( sol_usd, grouping=True )
    
    change = data2[1]['price_change_percentage_24h']
    change = round(change, 2)
    if change < 0:
      change = '⭸'+str(change)
    else: 
       change = '⭷'+str(change)

    
    await client.change_presence(status=discord.Status.do_not_disturb, activity = discord.Activity(type=discord.ActivityType.watching,name=(f'{sol_usd}$ |{change}%')))

    await asyncio.sleep(10)
    
    await client.change_presence(status=discord.Status.do_not_disturb, activity = discord.Activity(type=discord.ActivityType.watching,name=(f'{sol_inr}₹')))
    await asyncio.sleep(5)
  

client.loop.create_task(change_stat())
activate()
client.run(os.getenv('TOKEN'))