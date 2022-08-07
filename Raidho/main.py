from ast import alias
from asyncio.windows_events import NULL
from cgitb import text
from turtle import color
import discord
from discord.utils import get
from discord.ext import commands
from discord.ui import Button, View
from discord.ext import commands
import sqlite3
import random
import asyncio
import time
import datetime



###         ACCESSING CLIENT
client = commands.Bot(command_prefix = '!', help_command = None)

###         DECLARING EMOJIS AND VARIABLES
name = "PlaceHolder"
mp = "TBA"
dt = "TBA"
ts = "TBA"
timestamp = "TBA"
supp = "TBA"
wl = "Waiting"
hf = "PlaceHolder"
whitepaper = "TBA"
wallet = "Waiting"
thumbs_emoji = '\N{THUMBS UP SIGN}'
val = 0
param = NULL 

##  Creating users DB 
maindb = sqlite3.connect('Users.db')
cur = maindb.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS Users(
        id BLOB PRIMARY KEY, 
        disc BLOB NOT NULL
    )''')
maindb.commit()


##############################################################################################
#                                   FUNCTIONS   
##############################################################################################

##                              RETURN ALL NAMES IN TRACKING LIBRARY 
async def trk_name(ctx):
    name = ctx.author.name 
    userdb = sqlite3.connect(f'{name}.db')
    uc = userdb.cursor()
    uc.execute('''SELECT COUNT(name) FROM tracking''')
    n = uc.fetchone()

    if n[0] == 0:
        prompt = discord.Embed(title="Database Empty!", color = discord.Color.blue())
        await ctx.send(embed = prompt)
        return 0
    elif n[0] < 25:
        json_list = []
        #       store all data in db as list
        uc.execute('SELECT name FROM tracking')
        for row in uc.fetchall():
            json_list.append(row)
        
        return json_list


##                              GET AUTHOR'S TRIMMED-ID
def getid(ctx):
    id = ctx.author.id
    id = str(id)
    id = id[-5:]
    return(id)

##                              ADD NEW USER TO DB
def add_new_user(ctx, id, name):
    cur.execute(f"INSERT INTO Users(id, disc) VALUES('{id}', '{name}')")
    maindb.commit()
    id = getid(ctx)
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()
    uc.execute(f'''
        CREATE TABLE tracking(
        name BLOB PRIMARY KEY, 
        Mint_Price TEXT,
        date TEXT,
        timestamp TEXT,
        supply INTEGER,
        WL_status TEXT,
        HF TEXT,
        Whitepaper TEXT,
        Wallet_status TEXT  
    )''')
    userdb.commit()
    uc.execute(f'''
        CREATE TABLE holding(
        name BLOB PRIMARY KEY, 
        Entry_price TEXT,
        date INTEGER,
        Floor_price TEXT,
        Number_Holding TEXT,
        Growth TEXT,
        Roadmap Blob,
        Hold_Sell TEXT  
    )''')
    userdb.commit()


##                          CHECK IF USER IS REGISTERED
def check_reg(ctx):
    json_list = []  

    cursor = maindb.execute('SELECT id FROM  {}'.format('Users'))

    for row in cursor.fetchall():
        json_list.append(row[0])
    
    for id in json_list:
        if int(ctx.author.id) == int(id):
            return True

    return False


##                          ADD VALUES TO TRACKING DB 
def add_values_trcking(ctx, proj_name, mp = 'TBA', dt = 'TBA', ts = 'TBA', supp = 'TBA', wl = 'Waiting', hf = 'placeholder', Whitepap = 'TBA', wallet = 'Waiting'):
    id = getid(ctx)
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()
    uc.execute(f'''
        INSERT INTO tracking(
        name, 
        Mint_Price,
        date,
        timestamp,
        supply,
        WL_status,
        HF,
        Whitepaper,
        Wallet_status) 
        VALUES(
            '{proj_name}',
            '{mp}',
            '{dt}',
            '{ts}',
            '{supp}',
            '{wl}',
            '{hf}',
            '{Whitepap}',
            '{wallet}'
        ) ''')
    userdb.commit()
    userdb.close()


##                          FUNCTION TO SEND DM
async def DM(ctx, user:discord.Member, key, link):
    try:
        prompt = discord.Embed(title = 'Link:', description= f"security key: {key}", color= discord.Color.blue())
        prompt.add_field(name = link , value = "Currently a placeholder with our static website link.")
        await user.send(embed = prompt)
    except:
        prompt = discord.Embed(title = 'Unable to send messages', description=f"security key: {key}", color= discord.Color.blue())
        prompt.add_field(name = "Error" , value = "Your DMs are closed from server members")
        await user.send(embed = prompt)


##                          FUNCTION TO GET SOL NEEDED FOR NEXT 3 DAYS
def getsol(ctx):
    jlist = []
    
    id = getid(ctx)
    
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()
    
    tm = time.time()
    tm = int(tm)   
    timelim = tm + 259200

    uc.execute(f'SELECT Mint_price FROM tracking WHERE timestamp < {timelim} AND timestamp > {tm}')

    for row in uc.fetchall():
        jlist.append(row)

    sm = 0
    for s in jlist:
        sm = sm + float(s[0])

    return(sm)


##                          FUNCTION TO GET PROJECTS IN THE NEXT 3 DAYS 
def getprojects(ctx):
    jlist = []
    id = getid(ctx)
    
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()
    
    tm = time.time()
    tm = int(tm)   
    timelim = tm + 259200

    uc.execute(f'SELECT name FROM tracking WHERE timestamp < {timelim} AND timestamp > {tm}')
    for row in uc.fetchall():
        jlist.append(row[0])

    return(jlist)



##                          GET NEW PROJECT DETAILS
async def get_trk_deets(ctx):
    promp = discord.Embed(title="Enter name of the project", description= "Try using an **inactive channel** while adding info to your database to avoid mix-up", color= discord.Color.blue())
    psend = await ctx.send(embed = promp)

    ##              TAKING NAME
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
    
    try: 
        msg = await client.wait_for("message", check = check)
        name = msg.content
        await msg.add_reaction(thumbs_emoji)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)
    except:
        await name_error(ctx)
    

     ##              TAKING MINT PRICE
    await psend.delete()
    promp = discord.Embed(title="Enter **MINT PRICE** of the project", description= "Enter **only NUMERIC VALUES**\nEnter '-' to store default values for parameter", color= discord.Color.blue())
    psend = await ctx.send(embed = promp)
    

    try:
        msg = await client.wait_for("message", check = check)
        if msg.content == '-':
            mp = 'TBA'
        else:
            mp = msg.content 
        await msg.add_reaction(thumbs_emoji)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)
    except:
        await attribute_error
    

     ##              TAKING MINT DATE
    await psend.delete()
    promp = discord.Embed(title="Enter **MINT DATE** of the project", description= "**Format: DD/MM/YYYY**\nEnter '-' to store default values for parameter", color= discord.Color.blue())
    psend = await ctx.send(embed = promp)

    try:
        msg = await client.wait_for("message", check = check)
        if msg.content == '-' :
            global dt
            global ts
            dt = 'TBA'
            ts = 'TBA'
        else:
            dt = msg.content
            s = time.mktime(datetime.datetime.strptime(dt, "%d/%m/%Y").timetuple())
            s = str(s)
            ts = s[:-2]
            
            
        await msg.add_reaction(thumbs_emoji)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)

    except ValueError:
        await time_error(ctx)
    except:
        await attribute_error(ctx)
    


     ##              TAKING SUPPLY
    await psend.delete()
    promp = discord.Embed(title="Enter **SUPPLY** of the project", description= "Enter '-' to store default values for parameter", color= discord.Color.blue())
    psend = await ctx.send(embed = promp)

    try:
        msg = await client.wait_for("message", check = check)
        if msg.content == '-' :
            supp = 'TBA'
        else:
            supp = msg.content
        await msg.add_reaction(thumbs_emoji)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)
    except:
        await attribute_error


     ##              TAKING WL
    await psend.delete()

    try:
        promp = discord.Embed(title="Choose WL STATUS", description="5 seconds to choose", color= discord.Color.blue())
        obt = Button(label = "Whielisted", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
        sec = Button(label= "Non guarenteed WL", style = discord.ButtonStyle.blurple, emoji= "<:pogchamp:918026925396606976>")
        nobt = Button(label= "Public", style = discord.ButtonStyle.danger, emoji = "<:xcross:957521575551316028>")

        async def Obtained_callback(interaction):
            global wl 
            wl = "Whitelisted"
            subprm = discord.Embed(title="Whitelisted!", description= "Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()
        
        async def sec_callback(interaction):
            global wl 
            wl = "Secondary Whitelisted"
            subprm = discord.Embed(title="Non guarenteed Whitelist/Secondary Whitelisted!", description= "Smol Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()

        async def nobt_callback(interaction):
            global wl 
            wl = "Not Whitelisted"
            subprm = discord.Embed(title="Not Whitelisted!", description= "No Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()
        
        obt.callback = Obtained_callback
        sec.callback = sec_callback
        nobt.callback = nobt_callback

        view = View()
        view.add_item(obt)
        view.add_item(sec)
        view.add_item(nobt)
        psend = await ctx.send(embed = promp, view = view)
        await asyncio.sleep(4)

    except:
        await attribute_error


     ##              TAKING HF
    await psend.delete()

    try:
        promp = discord.Embed(title="Holding or Flipping this project?", description="5 seconds to choose", color= discord.Color.blue())
        yes = Button(label = "Holding", style = discord.ButtonStyle.green, emoji = "<:holding:957518500279222302>")
        no = Button(label= "Flipping", style = discord.ButtonStyle.danger, emoji= "<:flip:958605744746426378>")


        async def yes_callback(interaction):
            global hf 
            hf = "Holding"
            subprm = discord.Embed(title="HODL Time!", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()
        
        async def no_callback(interaction):
            global hf
            hf = "Flipping"
            subprm = discord.Embed(title="Happy Flips!", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()

        yes.callback = yes_callback
        no.callback = no_callback


        view = View()
        view.add_item(yes)
        view.add_item(no)
    
        psend = await ctx.send(embed = promp, view = view)
        await asyncio.sleep(4)

    except:
        await attribute_error



     ##              TAKING WHITEPAPER INFO 
    await psend.delete()

    try:
        promp = discord.Embed(title="Status of Project's Whitepaper", description="5 seconds to choose", color= discord.Color.blue())
        yes = Button(label = "Released", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
        no = Button(label= "Un-released", style = discord.ButtonStyle.danger, emoji= "<:xcross:957521575551316028>")
        
        async def yes_callback(interaction):
            global whitepaper 
            whitepaper = "Released"
            subprm = discord.Embed(title="Whitepaper has been released", description= "Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()
        
        async def no_callback(interaction):
            global whitepaper 
            whitepaper = "Un-released"
            subprm = discord.Embed(title="Whitepaper has not been released", description= "No Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

            await asyncio.sleep(2)
            await subpsend.delete()

        
        yes.callback = yes_callback
        no.callback = no_callback


        view = View()
        view.add_item(yes)
        view.add_item(no)
    
        psend = await ctx.send(embed = promp, view = view)
        await asyncio.sleep(4)
    except:
        await attribute_error(ctx)


    ##              TAKING WALLET INFO
    await psend.delete()

    if wl == "Whitelisted" or wl == "Secondary whitelisted":
        try:
            promp = discord.Embed(title="Wallet submission status:", description="5 seconds to choose", color= discord.Color.blue())
            yes = Button(label = "Submitted", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
            no = Button(label= "Not submitted", style = discord.ButtonStyle.danger, emoji= "<:xcross:957521575551316028>")
        
            async def yes_callback(interaction):
                global wallet 
                wallet = "Submitted"
                subprm = discord.Embed(title="You have submitted you wallet!", description= "Yeet", color= discord.Color.blue())
                subprm.set_footer(text = ctx.author.name)
                subpsend = await ctx.send(embed = subprm)

                await asyncio.sleep(2)
                await subpsend.delete()
                await psend.delete()
        
            async def no_callback(interaction):
                global wallet 
                wallet = "Not-Submitted"
                subprm = discord.Embed(title="You have not submitted your wallet", description= "No Yeet", color= discord.Color.blue())
                subprm.set_footer(text = ctx.author.name)
                subpsend = await ctx.send(embed = subprm)

                await asyncio.sleep(2)
                await subpsend.delete()
                await psend.delete()

        
            yes.callback = yes_callback
            no.callback = no_callback


            view = View()
            view.add_item(yes)
            view.add_item(no)
    
            psend = await ctx.send(embed = promp, view = view)
            await asyncio.sleep(4)

        except:
            await attribute_error


    try:      
        add_values_trcking(ctx, name, mp, dt, ts, supp, wl, hf, whitepaper, wallet)
        promp = discord.Embed(title="New project added to Tracking database!", color = discord.Color.blue())
        await ctx.send(embed = promp)
    except sqlite3.IntegrityError:
        await duplicate_name_error(ctx)
    except: 
        await add_error(ctx)
    

##                          DELETE VALUES FROM TRACKING DB 
async def delete_rec(ctx):
    prompt = discord.Embed(title="Enter Project name as entered in record", color = discord.Color.blue())
    prompt.set_footer(text='ctx.author.name')
    id = getid(ctx)
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()

    json_list = await trk_name(ctx)
    n = len(json_list)
    if json_list != 0:
        i = 0
        for name in json_list:
            prompt.add_field(name = name[0], value = i+1, inline = False)
            i+=1

    psend = await ctx.send(embed = prompt)
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel
 
    msg = await client.wait_for("message", check = check)
    name = msg.content

    await psend.delete()
    await msg.add_reaction(thumbs_emoji)

    
    uc.execute(f'DELETE FROM tracking WHERE name = "{name}" ')
    userdb.commit()

    await asyncio.sleep(1)
    await ctx.channel.purge(limit = 1)
    

    jl2 = await trk_name(ctx)
    m = len(jl2)

    if m < n:
        subp = discord.Embed(title="Record Successfully deleted!", color = discord.Color.blue())
        subp.set_footer(text = ctx.author.name)
        await ctx.send(embed = subp)
    else:
        await del_error(ctx)
    
    userdb.close()



##                          UPDATE VALUES FROM TRACKING DB 
async def update_rec(ctx):
    prompt = discord.Embed(title="Enter Project name as entered in record", color = discord.Color.blue())
    prompt.set_footer(text='ctx.author.name')
    
    json_list = await trk_name(ctx)
    if json_list != 0:
        i = 0
        for name in json_list:
            prompt.add_field(name = name[0], value = i+1, inline = False)
            i+=1

    psend = await ctx.send(embed = prompt)


    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await client.wait_for("message", check = check)
    proj = msg.content

    await psend.delete()

    subp = discord.Embed(title = 'Enter number coresponding to parameter you want to change', description='1 - Mint price\n2 - Mint date\n3 - Supply \n4 - Whitelist status\n5 - Holding/Flipping\n6 - Whitepaper\n7 - Wallet status ', color = discord.Color.blue())
    subprm = await ctx.send(embed = subp)
    msg = await client.wait_for("message", check = check)
    num = msg.content
    num = int(num) 
    await subprm.delete()
    if num > 2:
        num = num+1
    
    if num <= 4:  
        subsub = discord.Embed(title = 'Enter new value: ', description = "Make sure the data is in the right format.", color = discord.Color.blue())
        subsub.set_footer(text = ctx.author.name)
        await ctx.send(embed = subsub)
        msg = await client.wait_for("message", check = check)
        global val
        val = msg.content 

        if num == 2:
            try:
                global ts
                s = time.mktime(datetime.datetime.strptime(val, "%d/%m/%Y").timetuple())
                s = str(s)
                ts = s[:-2]
            except ValueError:
                await time_error(ctx)
        
    if num == 5:
        param = 'WL_status'
        promp = discord.Embed(title="Choose WL STATUS", description="5 seconds to choose", color= discord.Color.blue())
        obt = Button(label = "Whielisted", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
        sec = Button(label= "Non guarenteed WL", style = discord.ButtonStyle.blurple, emoji= "<:pogchamp:918026925396606976>")
        nobt = Button(label= "Public", style = discord.ButtonStyle.danger, emoji = "<:xcross:957521575551316028>")

        async def Obtained_callback(interaction):
            global val
            val = "Whitelisted"
            subprm = discord.Embed(title="Whitelisted!", description= "Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

        
        async def sec_callback(interaction):
            global val
            val = "Secondary Whitelisted"
            subprm = discord.Embed(title="Non guarenteed Whitelist/Secondary Whitelisted!", description= "Smol Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)


        async def nobt_callback(interaction):
            global val
            val = "Not Whitelisted"
            subprm = discord.Embed(title="Not Whitelisted!", description= "No Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

        
        obt.callback = Obtained_callback
        sec.callback = sec_callback
        nobt.callback = nobt_callback

        view = View()
        view.add_item(obt)
        view.add_item(sec)
        view.add_item(nobt)
        await ctx.send(embed = promp, view = view)

    if num == 6: 
        param = 'HF'
        promp = discord.Embed(title="Holding or Flipping this project?", description="5 seconds to choose", color= discord.Color.blue())
        yes = Button(label = "Holding", style = discord.ButtonStyle.green, emoji = "<:holding:957518500279222302>")
        no = Button(label= "Flipping", style = discord.ButtonStyle.danger, emoji= "<:flip:958605744746426378>")


        async def yes_callback(interaction):
            global val
            val = "Holding"
            subprm = discord.Embed(title="HODL Time!", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)
        
        async def no_callback(interaction):
            global val
            val = "Flipping"
            subprm = discord.Embed(title="Happy Flips!", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

        yes.callback = yes_callback
        no.callback = no_callback


        view = View()
        view.add_item(yes)
        view.add_item(no)
    
        await ctx.send(embed = promp, view = view)
    
    if num == 7:
        param = 'Whitepaper'
        promp = discord.Embed(title="Status of Project's Whitepaper", description="5 seconds to choose", color= discord.Color.blue())
        yes = Button(label = "Released", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
        no = Button(label= "Un-released", style = discord.ButtonStyle.danger, emoji= "<:xcross:957521575551316028>")
        
        async def yes_callback(interaction):
            global val
            val = "Released"
            subprm = discord.Embed(title="Whitepaper has been released", description= "Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

        async def no_callback(interaction):
            global val 
            val = "Un-released"
            subprm = discord.Embed(title="Whitepaper has not been released", description= "No Yeet", color= discord.Color.blue())
            subprm.set_footer(text = ctx.author.name)
            subpsend = await ctx.send(embed = subprm)

        
        yes.callback = yes_callback
        no.callback = no_callback


        view = View()
        view.add_item(yes)
        view.add_item(no)
    
        await ctx.send(embed = promp, view = view)
    
    if num == 8:
        param = 'Wallet_status'
        promp = discord.Embed(title="Wallet submission status:", description="5 seconds to choose", color= discord.Color.blue())
        yes = Button(label = "Submitted", style = discord.ButtonStyle.green, emoji = "<:tick:957521575547142235>")
        no = Button(label= "Not submitted", style = discord.ButtonStyle.danger, emoji= "<:xcross:957521575551316028>")
        
        async def yes_callback(interaction):
                global val 
                val = "Submitted"
                subprm = discord.Embed(title="You have submitted you wallet!", description= "Yeet", color= discord.Color.blue())
                subprm.set_footer(text = ctx.author.name)
                subpsend = await ctx.send(embed = subprm)
        
        async def no_callback(interaction):
                global val 
                val = "Not-Submitted"
                subprm = discord.Embed(title="You have not submitted your wallet", description= "No Yeet", color= discord.Color.blue())
                subprm.set_footer(text = ctx.author.name)
                subpsend = await ctx.send(embed = subprm)
        
        yes.callback = yes_callback
        no.callback = no_callback


        view = View()
        view.add_item(yes)
        view.add_item(no)
    
        await ctx.send(embed = promp, view = view)

    if num == 4:
        param = 'supply'
    else:
        param = 'Mint_price'
    
    try:
        id = getid(ctx) 
        userdb = sqlite3.connect(f'{id}.db')
        uc = userdb.cursor()

        if num == 2:
            uc.execute(f'''UPDATE tracking 
            SET date = "{val}",
                timestamp = "{ts}"
            WHERE name = "{proj}" ''')
            userdb.commit()
        else:
            uc.execute(f'''UPDATE tracking 
            SET {param} = "{val}"
            WHERE name = '{proj}'
            ''')
            userdb.commit()
        
        await ctx.channel.purge(limit = 1)
        fn = discord.Embed(title = f"{proj} has been Updated", description = f"{param} value is now {val}", color = discord.Color.Blue())
        await ctx.send(embed = fn) 

    except:
        update_error(ctx)



##                          DISPLAY TRACKING DB
async def trackingdb(ctx):
    json_list = []
    id = getid(ctx)
    userdb = sqlite3.connect(f'{id}.db')
    uc = userdb.cursor()
    uc.execute('''SELECT COUNT(name) FROM tracking''')
    n = uc.fetchone()
    
    prompt = discord.Embed(title= "Currently Tracking:", color = discord.Color.blue())
    prompt.set_footer(text=ctx.author.name)

    if n[0] == 0:
        prompt.add_field(name="Database Empty!", value="Add more values.", inline = True)
    elif n[0] < 25:
        #       store all data in db as list
        uc.execute('SELECT * FROM tracking')
        for row in uc.fetchall():
            json_list.append(row)
        #       make embed and send 
        for name in json_list:
            nm = name[0].upper()
            prompt.add_field(name= nm, value = f"Mint price: **{name[1]} Sol** ┃ Supply: **{name[4] }** ┃ Date: **{name[2]} <t:{name[3]}:R>**\n┃\nWL Status: **{name[5]}** ┃ Wallet: **{name[8]}**\n┃\nHold/Flip: **{name[6]}** ┃ Whitepaper: **{name[7]}**\n‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒‒", inline = False)
    add = Button(label = "Add", style=discord.ButtonStyle.green, emoji = "<:plus:957518536622874634>")
    delete = Button(label = "Delete", style=discord.ButtonStyle.red, emoji = "<:minus:957518536492843058>")
    update = Button(label= "Update", style = discord.ButtonStyle.blurple, emoji = "<:Update:957518538917150810>")
    dash = Button(label= "Dashboard", style = discord.ButtonStyle.gray, emoji = "<:dashboard:957520990492045352>")

    async def add_prompt(interaction):
        await psend.delete()
        adprm = discord.Embed(title="Enter project details:", description= " Project Name is compulsary", color= discord.Color.blue())
        sendprm = await ctx.send(embed = adprm)
        await get_trk_deets(ctx)
        await sendprm.delete()

    async def del_prompt(interaction):
        await psend.delete()
        await delete_rec(ctx)


    async def update_prompt(interaction):
        await psend.delete()
        await update_rec(ctx)

    async def dash_prompt(interaction):
        await psend.delete()
        await main_dash(ctx)  #displays main dash

    add.callback = add_prompt # fin func
    delete.callback = del_prompt  #not done
    update.callback = update_prompt #not done
    dash.callback = dash_prompt

    view = View()
    view.add_item(add)
    view.add_item(delete)
    view.add_item(update)
    view.add_item(dash)

    psend = await ctx.send(embed = prompt, view=view)


##                          DISCPLAY MAIN DASHBOARD 
async def main_dash(ctx):
    title = ctx.message.author.name+"'s DASHBOARD"
    bal = getsol(ctx)
    projs = getprojects(ctx)
    dash = discord.Embed(title=title, color = discord.Color.blue())
    dash.set_footer(text = f'{ctx.message.author.name}')
    dash.add_field(name = 'Total Floor value:', value = "Placeholder", inline=True)
    dash.add_field(name = 'Required wallet balance:', value = f"**{bal} Sol** (next 3 days)", inline=True)
    psend1 = await ctx.send(embed = dash)

    dashmid = discord.Embed(title='Upcoming mints:', color = discord.Color.blue())
    i = 1
    for nm in projs:
        dashmid.add_field(name=f'{nm}', value = i)
        i = i + 1
    psend2 = await ctx.send(embed = dashmid)

    dashbot = discord.Embed(title='Top Assests', description="Unlinked", color = discord.Color.blue())
   
    tracking = Button(label = "Tracking", style=discord.ButtonStyle.green, emoji = "<:tracking:957518538137014342>")
    holding = Button(label = "Holding", style=discord.ButtonStyle.blurple, emoji = "<:holding:957518500279222302>")
    portfolio = Button(label= "Portfolio", style = discord.ButtonStyle.danger, emoji = "<:portfolio:957518537352683580>")
    website = Button(label = "Web-view",style=discord.ButtonStyle.grey) 
    async def tracking_dash(interaction):
        await psend1.delete()
        await psend2.delete()
        await psend3.delete()
        await trackingdb(ctx)
    
    async def holding_dash(interaction):
        await psend1.delete()
        await psend2.delete()
        await psend3.delete()
        prompt = discord.Embed(title="Current Holdings:", color= discord.Colour.blue())
        prompt.add_field(name = "currently unlinked", value = "coming soon!")
        await ctx.send(embed = prompt)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)
        
    
    async def portfolio_dash(interaction):
        await psend1.delete()
        await psend2.delete()
        await psend3.delete()
        prompt = discord.Embed(title="Portfolio:", color= discord.Colour.blue())
        prompt.add_field(name = "currently unlinked", value = "coming soon!")
        await ctx.send(embed = prompt)
        await asyncio.sleep(1)
        await ctx.channel.purge(limit = 1)
    
    async def website_callback(interaction):
        await psend1.delete()
        await psend2.delete()
        await psend3.delete()
        key = random.randint(0000, 9999)
        link = "https://odin-nfts.com"
        try:
            await ctx.channel.purge(limit = 1)
            await DM(ctx, ctx.author, key, link)
            prompt = discord.Embed(title = "Private link generated", color = discord.Color.blue())
            prompt.add_field(name = "Link sent in DM", value = f"security key = {key}")
            await ctx.send(embed = prompt)
        except:
            await dm_error(ctx, link)

            


    tracking.callback = tracking_dash # connect db 
    holding.callback = holding_dash  #not done
    portfolio.callback = portfolio_dash #not done
    website.callback = website_callback #done

    view = View()
    view.add_item(tracking)
    view.add_item(holding)
    view.add_item(portfolio)
    view.add_item(website)

    psend3 = await ctx.send(embed = dashbot, view = view)


##############################################################################################
#                                   EXCEPTIONS   
##############################################################################################

##                          USER EXISTS IN DB
async def user_exists(ctx, name):
    prompt = discord.Embed(title = 'Already registered!', color= discord.Color.blue())
    prompt.set_footer(text = name)
    prompt.set_thumbnail(url=f'{ctx.author.avatar}')
    prompt.add_field(name = 'You Id already exists in the database!', value = " Please use !help for more commands." )
    await ctx.send(embed = prompt)

##                          UNKOWN ERROR
async def unknown_error(ctx, name):
    prompt = discord.Embed(title = 'Error 404', color= discord.Color.blue())
    prompt.set_footer(text = name)
    prompt.add_field(name = 'Unknown error!', value = " Please use !help for more commands." )
    await ctx.send(embed = prompt)

##                          DM ERROR
async def dm_error(ctx, key):
    prompt = discord.Embed(title = 'Unable to send messages', description = key, color= discord.Color.blue())
    prompt.add_field(name = "Error" , value = "Unknown DM error!")
    await ctx.send(embed = prompt)


##                          ADDING PROJECT - NAME ERROR

async def name_error(ctx):
    prompt = discord.Embed(title = 'Name error Triggered',  color= discord.Color.blue())
    await ctx.send(embed = prompt)

##                          ADDING PROJECT - ATTRIBUTE ERROR

async def attribute_error(ctx):
    prompt = discord.Embed(title = 'Attribute error Triggered', description= "Please update info after this procedure.", color= discord.Color.blue())
    await ctx.send(embed = prompt)

##                          ADDING PROJECT - DB adding error

async def add_error(ctx):
    prompt = discord.Embed(title = 'Adding to DB error Triggered',  color= discord.Color.blue())
    await ctx.send(embed = prompt)

##                          ADDING PROJECT - duplicate name
async def duplicate_name_error(ctx):
    prompt = discord.Embed(title = 'Project with the same name already exists in Database!', description= 'Please refer to database or enter a different name.\nProject not added to database.',  color= discord.Color.blue())
    await ctx.send(embed = prompt)

##                          ADDING PROJECT - bad time value

async def time_error(ctx):
    prompt = discord.Embed(title = 'Invalid date value!', description= "Please update info after this procedure.",color= discord.Color.blue())
    psend = await ctx.send(embed = prompt)
    await asyncio.sleep(5)
    psend.delete

##                          DELETING PROJECT - record not deleted
async def del_error(ctx):
    prompt = discord.Embed(title= "Record not deleted!",description='Please check spelling and capitalization or the record does not exist in database. ' , color = discord.Color.blue())
    prompt.set_footer(ctx.author.name)
    psend = await ctx.send(embed = prompt)



##                          UPDATING PROJECT - record not updated
async def update_error(ctx):
    prompt = discord.Embed(title= "Record not Updated!",description='Please retry.' , color = discord.Color.blue())
    prompt.set_footer(ctx.author.name)
    await ctx.send(embed = prompt)

##############################################################################################
#                                   COMMANDS   
##############################################################################################
@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))
  

##              REGISTER command
@client.command()
@commands.has_role("BetaTester")
async def register(ctx):
    try:
        add_new_user(ctx, ctx.message.author.id, ctx.message.author.name)
        prompt = discord.Embed(title = 'Registered!', color= discord.Color.blue())
        prompt.set_footer(text = f'{ctx.message.author.name}')
        prompt.set_thumbnail(url=f'{ctx.author.avatar}')
        prompt.add_field(name = 'Welcome!\nYour Id has been added to the database!', value = "Please use !help for more commands.")
        await ctx.send(embed = prompt)
    except sqlite3.IntegrityError:
        await user_exists(ctx, ctx.message.author.name)
    except:
        await unknown_error(ctx, ctx.message.author.name)
    
    


#               MAIN DASHBOARD COMMAND
@client.command()
@commands.has_role("BetaTester")
async def dash(ctx):
    if check_reg(ctx) == False:
        prompt = discord.Embed(title="Unregistered User!", description='Please use the **!register** command', color = discord.Color.blue())
        await ctx.send(embed = prompt)
    else:
        await main_dash(ctx)


#               TRACKING DASHBOARD COMMAND
@client.command()
@commands.has_role("BetaTester")
async def track(ctx):
    if check_reg(ctx) == False:
        prompt = discord.Embed(title="Unregistered User!", description='Please use the **!register** command', color = discord.Color.blue())
        await ctx.send(embed = prompt)
    else:
        await trackingdb(ctx)


#               HOLDING DASHBOARD COMMAND
@client.command()
@commands.has_role("BetaTester")
async def hold(ctx):
    if check_reg(ctx) == False:
        prompt = discord.Embed(title="Unregistered User!", description='Please use the **!register** command', color = discord.Color.blue())
        await ctx.send(embed = prompt)
    else:
        await ctx.channel.purge(limit = 1)
        prompt = discord.Embed(title="Current Holdings:", color= discord.Colour.blue())
        prompt.add_field(name = "currently unlinked", value = "coming soon!")
        await ctx.send(embed = prompt)


#               PORTFOLIO DASHBOARD COMMAND
@client.command()
@commands.has_role("BetaTester")
async def pf(ctx):
    if check_reg(ctx) == False:
        prompt = discord.Embed(title="Unregistered User!", description='Please use the **!register** command', color = discord.Color.blue())
        await ctx.send(embed = prompt)
    else:
        await ctx.channel.purge(limit = 1)
        prompt = discord.Embed(title="Portfolio", color= discord.Colour.blue())
        prompt.add_field(name = "currently unlinked", value = "coming soon!")
        await ctx.send(embed = prompt)


##              NEW ENTRY DASHBOARD COMMAND
@client.command()
@commands.has_role("BetaTester")
async def addnew(ctx):
    if check_reg(ctx) == False:
        prompt = discord.Embed(title="Unregistered User!", description='Please use the **!register** command', color = discord.Color.blue())
        await ctx.send(embed = prompt)
    else:
        await get_trk_deets(ctx)

@client.command()
@commands.has_role("Admins")
async def remuser(ctx, id):
    cur.execute(f'DELETE FROM Users where id = "{id}"')
    maindb.commit()

    await ctx.send('User removed!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        promp = discord.Embed(title = "Unknown command!", description="Please check the spelling or use **!help** to view all commands!", color = discord.Color.blue())
        await ctx.send(embed = promp)

@client.command(alias=['Help', 'HELP'])
async def help(ctx):
    promp = discord.Embed(title = "Commands", description="Use '!' as prefix for each command.\nHere are the list of commands currently supported by Raidho", color=discord.Color.blue())
    promp.add_field(name="register", value="Used to register a new user to Raidho's DB.", inline = False)
    promp.add_field(name="dash", value="View your main dashboard.", inline = False)
    promp.add_field(name="track", value="View your tracking DB.", inline = False)
    promp.add_field(name="hold", value="View your Holding DB. (Currently unlinked)", inline = False)
    promp.add_field(name="pf", value="View your Portfolio. (Currently unlinked)", inline = False)
    promp.add_field(name="addnew", value="Add a new project to your tracking database directly.", inline = False)
    promp.set_footer(text= ctx.author.name)

    await ctx.send(embed = promp)

    

client.run('OTQ0OTkwMTEyMTA4OTI5MTI1.YhJonw.4WkPG1W8rlxtHhz5sSpMApfxkAY')