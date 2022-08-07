import discord
from discord.ext import commands
import requests
import os
from Trackers.solana.server import activate
from replit import db

client = commands.Bot(command_prefix = '$')
limit = 2

def inDB(id):
  if id in db.keys():
    return True
  else:
    return False

def addID(id):
  db[f'{id}'] = 1

def limCheck(id):
  if int(db[f'{id}']) >= limit:
    return True
  else:
    return False

def useCnt(id):
  db[f'{id}'] = int(db[f'{id}']) + 1
  


#getting crypto prices 
def getPrices(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['current_price']

  return(0)

def getPricesUS(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['current_price']

  return(0)

#conversion from crypto to fiat
def convertcryp(crypto, amt):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      val = data[i]['current_price']

  return(val*amt)

def convertcrypUS(crypto, amt):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      val = data[i]['current_price']
  
  return(val*amt)


#conversion from fiat to crypto
def convertfiat(crypto, amt):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      val = data[i]['current_price']

  return(amt/val)

def convertfiatUS(crypto, amt):
  URL = os.getenv('API US')
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      val = data[i]['current_price']
  
  return(amt/val)


#getting thumbnail
def getImage(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['image']

  return(0)

#getting list of tracked cryptos
def getList(cryptolist):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    cryptolist.append(data[i]['id']) 

  return(cryptolist)
    
#checking if its supported for user
def isSupported(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return ('The currency is SUPPORTED.')
    else:
      return ('The currency is NOT SUPPORTED.')

#checking if its supported for program
def isSupportedP(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()
  f = 0

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      f = 1
  
  if f == 1:
    return True
  else:
    return False


#checking for rank
def getRank(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['market_cap_rank'] 
  
  return 0


#checking for last 24 hour change
def getChange(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['price_change_24h']

  return 0


#checking for last 24 hour change %
def getChangePer(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['price_change_percentage_24h']

  return 0

#checking for Highest in last 24 hour 
def get24high(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['high_24h']

  return 0
    

#checking for lowest in last 24 hour 
def get24low(crypto):
  URL = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr'
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if data[i]['id'] == crypto or data[i]['symbol'] == crypto:
      return data[i]['low_24h']

  return 0

#accessing client 
@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching,name=('$help | in CRYPTO')))

@client.command(aliases=['value', 'find'])
async def val(ctx, crypto):

  if not inDB(ctx.message.author.id):
    addID(ctx.message.author.id)
  else:
    await useCnt(ctx.message.author.id)
  
 
  if limCheck(ctx.message.author.id):
    await ctx.send('Limit reached!')
    return


  
  x = getPrices(crypto)
  z = getPricesUS(crypto)
  y = getImage(crypto)
  if x != 0 :
    emb1 = discord.Embed(title = f'Price of {crypto}', color = discord.Color.blue())
    emb1.set_thumbnail(url = y)
    emb1.add_field(name = f'➜ {z} USD', value = 'OR', inline = False)
    emb1.add_field(name = f'➜ {x} INR', value = f'{ctx.message.author.mention}', inline = False)
    await ctx.send(embed = emb1)
  else:
    emb1 = discord.Embed(title = 'Invalid value', color = discord.Color.blue())
    emb1.add_field(name = 'Coin does not exist/Coin is not tracked.', value = 'Use $help to view all commands.', inline = False)
    await ctx.send(embed = emb1)






  
activate()
client.run(os.getenv('TOKEN'))


