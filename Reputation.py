from firebase import firebase
import discord
client = discord.Client()
mfirebase = firebase.FirebaseApplication('https://firepython-6ed4c.firebaseio.com/', authentication=None)
authentication = firebase.FirebaseAuthentication('wiifitplus2', 'alexandrstrizjnev@gmail.com')

@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))

def up(e):
    print("saving...")
    a = mfirebase.get("/Reputation", str(e.id))
    b = 0 if a == None else str(list(a.values())[0])
    mfirebase.post("/Reputation/" + str(e.id), str(int(b) + 1))
    if a != None:
        mfirebase.delete("/Reputation/" + str(e.id), str(list(a.keys())[0]))

def down(e):
    print("saving...")
    a = mfirebase.get("/Reputation", str(e.id))
    b = 0 if a == None else str(list(a.values())[0])
    mfirebase.post("/Reputation/" + str(e.id), str(int(b) - 1))
    if a != None:
        mfirebase.delete("/Reputation/" + str(e.id), str(list(a.keys())[0]))
@client.event
async def on_reaction_remove(reaction, user):
    mname = user.id
    e = reaction.message.mentions[0]
    if reaction.message.channel.name != "tipstrucksnews":
        return
    if reaction.emoji == "👍":
        if mname != e.id:
            down(e)
    elif reaction.emoji == "👎":
        if mname != e.id:
            up(e)
    print(reaction.emoji)
@client.event
async def on_reaction_add(reaction, user):
    mname = user.id
    e = reaction.message.mentions[0]
    if reaction.message.channel.name != "tipstrucksnews":
        return
    if reaction.emoji=="👍":
        if mname != e.id:
            up(e)
    elif reaction.emoji=="👎":
        if mname != e.id:
            down(e)
    print(reaction.emoji)
@client.event
async def on_message(message):
    mname=message.author.id
    if message.content.startswith("/up"):
        for e in message.mentions:
            if e.id!=mname:
                up(e)
        print("Done!")
    if message.content.startswith("/down"):
        for e in message.mentions:
            if e.id!=mname:
                down(e)
        print("Done!")
    if message.content.startswith("/top"):
        rep = {}
        for e in message.server.members:
            a = mfirebase.get("/Reputation", str(e.id))
            b = 0 if a == None else str(list(a.values())[0])
            rep[e.name]=b
        fsend = [k+" : "+str(v) for k , v in rep.items()]
        fsend.sort(key = lambda e:int(e.split(" : ")[1]))
        fsend = fsend[11:0:-1]
        await client.send_message(message.channel,"Top:\n"+"\n".join(fsend))
        print("Done!!!")
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
client.run("MzMyMTMyMDY5NzA0NzI4NTc2.DD5ppw.bBCgasTj6L95Mk0EZCobyICr-bI")
