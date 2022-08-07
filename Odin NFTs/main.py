import discord
from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select
from discord.ext import commands
import requests
import os
from Trackers.solana.server import activate
import asyncio
import datetime
import pytz





client = commands.Bot(command_prefix = '$', help_command = None)
DiscordComponents(client)

##          check project
def checkexs(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()

  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return True
  return False

##          Get an entire row
def findRec(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]

  return checkexs(projName)

##        Get category list
def getCatList(cat):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  list = []
  for i in range(len(data)):
    if cat == data[i]['Category'].lower():
      list.append(data[i]['Project name'])

  return list

##                sort by price

def getPriceLow(price, cryp):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  list = []
  for i in range(len(data)):
    if data[i]['Mint price'] != 'TBA' and data[i]['Mint price'] != 'free mint':
      if float(data[i]['Mint price'])  <= price and data[i]['Currency'] == cryp:
        list.append(data[i]['Project name'])
    elif data[i]['Mint price'] == 'free mint' and data[i]['Currency'] == cryp:
      list.append(data[i]['Project name'])
  return list

def getPriceHigh(price, cryp):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  list = []
  for i in range(len(data)):
    if data[i]['Mint price'] != 'TBA' and data[i]['Mint price'] != 'free mint':
      if float(data[i]['Mint price'])  >= price and data[i]['Currency'] == cryp:
        list.append(data[i]['Project name'])

  return list

##              population
def getPopAbove(pop):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  list = []
  for i in range(len(data)):
    x = int(data[i]['Population'])
    if x > pop:
        list.append(data[i]['Project name'])

  return list

##           Project name

def findName(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]['Project name']

  return 'empty'
 
##          dev status 
def findDevStat(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]['Devs status']
  
  return 'empty'

##        server population 
def findpop(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name'].lower():
      return data[i]['Population']

  return 'empty'

##        Project Roadmap
def findRM(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name']:
      return data[i]['Roadmap']

  return 'empty'

##        Project artwork
def findart(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]['Artwork']

  return 'empty'

##        Project thumbnail
def findimg(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]['Image']

  return 'empty'

##        Project WL status
def findWLStat(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name'].lower():
      return data[i]['WL acquired']

  return 'empty'

##        Project category
def findCat(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name'].lower():
      return data[i]['Category']

  return 'empty'

##        Project mint date
def findDate(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName in data[i]['Project name']:
      return data[i]['Mint date']

  return 'empty'

##        Project mint price
def findPrice(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name']:
      return data[i]['Mint price']

  return 'empty'

##        Project Supply
def findSupply(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name'].lower():
      return data[i]['Supply']

  return 'empty'

##        Project currency
def findCur(projName):
  URL = os.getenv('all API')
  req = requests.get(url = URL)
  data = req.json()
  for i in range(len(data)):
    if projName == data[i]['Project name'].lower():
      return data[i]['Currency']

  return 'empty'


#accessing client 

@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching,name=('$help | in NFTs')))



##                                        All details
@client.command(aliases=['Find', 'FIND', 'details'])
async def find(ctx, NFT):

  NFT = NFT.lower() 
  if checkexs(NFT):
    data = []
    data = findRec(NFT)
    emb1 = discord.Embed(title =  data['Project name'] , description = ctx.message.author.mention, color = discord.Color.blue())
    emb1.set_thumbnail(url = data['Image'])
    emb1.add_field(name = data['Mint date'], value = 'Mint Date', inline = True)
    emb1.add_field(name = data['Mint price'], value = 'Mint Price', inline = True)
    emb1.add_field(name = data['Supply'], value = 'Supply', inline = True)
    emb1.add_field(name = data['Devs status'], value = 'Dev Status', inline = True)
    emb1.add_field(name = data['Population'], value = 'Users on discord', inline = True)
    emb1.add_field(name = data['Roadmap'], value = 'Roadmap', inline = True)
    emb1.add_field(name = data['Artwork'], value = 'Art Style', inline = True)
    emb1.add_field(name = data['Category'], value = 'Category', inline = True)
    emb1.add_field(name = data['WL acquired'], value = 'WL acquired', inline = True)
    emb1.add_field(name = data['Currency'], value = 'Blockchain', inline = True)
    await ctx.send(embed = emb1)
  else:
    emb1 = discord.Embed(title = 'PROJECT NOT RECOGNIZED', color = discord.Color.blue())
    emb1.add_field(name = 'Project *does not exist* in Odin database/Project is *not tracked*.', value = '**$allprojects** to find all tracked projects\n**$help** to view all commands.', inline = False)
    await ctx.send(embed = emb1)


##                  search by type 
@client.command(aliases=['Type', 'TYPE', 'category'])
async def type(ctx, cat):
  cat = cat.lower()

  catlist = []
  catlist = getCatList(cat)

  if len(catlist) != 0:
    emb1 = discord.Embed(title =  f'{cat} Projects' , description = ctx.message.author.mention, color = discord.Color.blue())
    for i in range(len(catlist)):
      x = findRM(catlist[i])
      emb1.add_field(name = catlist[i], value = x, inline = False)        
    await ctx.send(embed = emb1) 
  else:
    emb1 = discord.Embed(title =  f' No {cat} Projects available at the moment' , description = ctx.message.author.mention, color = discord.Color.blue())
    await ctx.send(embed = emb1)



##                search by mint price low
@client.command(aliases=['Mintpricelow', 'MINTPRICELOW', 'mintpricebelow'])
async def mintpricelow(ctx, price):
  first = discord.Embed(title =  f'Choose blockchain' , description = '1 - Solana\n2 - Ethereum', color = discord.Color.blue())
  await ctx.send(embed = first)

  def check(m):
    return m.author.id == ctx.message.author.id and m.channel == ctx.message.channel  
  msg = await client.wait_for('message', check = check)
    
  if msg.content == '1':
    cryp = 'Solana'
    short = 'sol'
  else:
    cryp = 'Ethereum'
    short = 'eth'

  if float(price) < 0.01:
    emb1 = discord.Embed(title =  f'Price too low' , description = ctx.message.author.mention, color = discord.Color.blue())
    emb1.add_field(name = 'Free mints cost more!', value = 'Please enter a valid amont', inline = False)  

    await ctx.send(embed = emb1)

  else:
    projectlist = []
    projectlist = getPriceLow(float(price), cryp)


  if len(projectlist) != 0:
    emb1 = discord.Embed(title =  f'Projects below {price} {short}' , description = ctx.message.author.mention, color = discord.Color.blue())
    for i in range(len(projectlist)):
      x = findPrice(projectlist[i])
      if x != 'free mint':
        emb1.add_field(name = projectlist[i], value = f'{x} {short}', inline = False) 
      else: 
        emb1.add_field(name = projectlist[i], value = x, inline = False)

    await ctx.send(embed = emb1) 
  else:
    emb1 = discord.Embed(title =  f' No projects available in that price range' , description =   ctx.message.author.mention, color = discord.Color.blue())
    await ctx.send(embed = emb1)

  ##                search by mint price high
@client.command(aliases=['Mintpricehigh', 'MINTPRICEHIGH', 'mintpriceabove'])
async def mintpricehigh(ctx, price):

  first = discord.Embed(title =  f'Choose blockchain' , description = '1 - Solana\n2 - Ethereum', color = discord.Color.blue())
  await ctx.send(embed = first)

  def check(m):
    return m.author.id == ctx.message.author.id and m.channel == ctx.message.channel  
  msg = await client.wait_for('message', check = check)
    
  if msg.content == '1':
    cryp = 'Solana'
    short = 'sol'
  else:
    cryp = 'Ethereum'
    short = 'eth'
  prompt = discord.Embed(title = 'Choose Category:', description = ctx.message.author.mention, color = discord.Color.blue()) 
  prompt.add_field()
  await ctx.send()
  projectlist = []
  projectlist = getPriceHigh(float(price), cryp)
    
  if len(projectlist) != 0:
    emb1 = discord.Embed(title =  f'Projects above {price} {short}' , description = ctx.message.author.mention, color = discord.Color.blue())
    for i in range(len(projectlist)):
      x = findPrice(projectlist[i])
      emb1.add_field(name = projectlist[i], value = f'{x} {short}', inline = False)        
    await ctx.send(embed = emb1) 
  else:
    emb1 = discord.Embed(title =  f' No projects available in that price range' , description = ctx.message.author.mention, color = discord.Color.blue())
    await ctx.send(embed = emb1)


@client.command()
async def popabove(ctx, pop):



  projectlist = []
  projectlist = getPopAbove(int(pop))
    
  if len(projectlist) != 0:
    emb1 = discord.Embed(title =  f'Projects above {pop} ' , description = ctx.message.author.mention, color = discord.Color.blue())
    for i in range(len(projectlist)):
      emb1.add_field(name = projectlist[i], value = 'members', inline = False)        
    await ctx.send(embed = emb1) 
  else:
    emb1 = discord.Embed(title =  f' No projects available in that price range' , description = ctx.message.author.mention, color = discord.Color.blue())
    await ctx.send(embed = emb1)



@client.command(aliases=['converttime', 'time', 'findtimein'])
async def findtimeIN(ctx, hour, mn):
  
  hr = int(hour)
  mn = int(mn)

  tm = datetime.datetime(2022, 12, 12, hr, mn, tzinfo=pytz.UTC)
  converted = tm.astimezone(pytz.timezone('Asia/Kolkata'))

  emb = discord.Embed(title =  f'Converted to IST' , description = f"{converted.time()} IST", color = discord.Color.blue())
  await ctx.send(embed = emb)


@client.command(aliases=['Converttime', 'Time', 'Gettime'])
async def findtime(ctx, hr, mn, tz):
  
  hr = int(hr)
  mn = int(mn)

  tm = datetime.datetime(2022, 12, 12, hr, mn, tzinfo=pytz.UTC)
  converted = tm.astimezone(pytz.timezone(tz))
  emb = discord.Embed(title =  f'Converted to IST' , description = f"{converted.time()} {tz}", color = discord.Color.blue())
  await ctx.send(embed = emb)



  ##                        help command
@client.command(aliases = ['HELP', 'fuck off', 'Help'])
async def help(ctx):
  emb1 = discord.Embed(title = 'Commands:', description = "'$' is the prefix for this bot." , color = discord.Color.blue())
  emb1.add_field(name = '$find <project_name>', value = 'Shows base stats about the project.\nex: **$find nekoverse**\nAlias - details', inline = False)  
  emb1.add_field(name = '$type <investment_type>', value = 'Shows all the projects in the databse of a certain category.\nex: **$type short term, $type long term or $type flip**\nAlias - category', inline = False) 
  emb1.add_field(name = '$mintpricelow <mint_price>', value = 'Shows all projects at and under the given mint price. (Sol NFTs)\nex: **$mintpricelow 0.5**\nAlias - mintpricebelow', inline = False)
  emb1.add_field(name = '$mintpricehigh <mint_price>', value = 'Shows all projects above the given mint price. (Sol NFTs)\nex: **$mintpricehigh 0.5**\nAlias - mintpriceabove', inline = False)
  emb1.add_field(name = '$findtimeIN <time>', value = 'Converts UTC time to IST.\n ex: **$findtimeIN 16 30 ** Enter hours according to 24 clock.', inline = False)
  emb1.add_field(name = '$findtimeIN <time>', value = 'Converts UTC time to given time zone.\nex: **$findtime 16 30 America/Detroit**. Enter hours according to 24 clock\n find time zones here: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568', inline = False)
  emb1.add_field(name = '$popabove <time>', value = 'Finds all projects over given population.\n**ex: $popabove 1500**. ', inline = False)
  await ctx.send(embed = emb1)
  
      

  
activate()
client.run(os.getenv('TOKEN'))








