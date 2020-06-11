import discord
import random
import operations
import game
import time

def savedata(data):
    f = open("data", "w", encoding="utf8")
    f.write(str(data))
    f.close()
    return

def getdata():
    f = open("data", "r", encoding="utf8")
    t = f.read()
    f.close()
    return eval(t)

def clean(word):
    word = word.strip()
    word = word.lower()
    return word


class MyClient(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.operations = []
        self.operations += [operations.HelpOperation()]
        self.operations += [operations.SessionOperation()]
        self.operations += [operations.JoinOperation()]
        self.operations += [operations.GameOperation()]
        
        self.operations += [operations.ExitOperation()]
        print(self.operations)
        self.state = "waiting"
        self.scores = {}
        self.words = {}
        self.mainchannel = None
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        
        if message.author == client.user:
            return
        if (self.state == "gaming"):
            try:
                if (message.channel.name == self.mainchannel.name):
                    await message.channel.send("Please do not use this channel while a game is ongoing.")
                else:
                    print("messages on unrelated channels while game ongoing")
            except:
                #dm channel
                player = message.author.name
                if (player in list(self.words)):
                    thisword = clean(message.content)
                    if (thisword in self.words[player]):
                        self.forgets[player] += 1
                        await message.channel.send("You already did that one!")
                    else:
                        thiswait = time.time() - self.lastwordtime[player]
                        self.lastwordtime[player] = time.time()
                        if (thiswait > self.maxwaits[player]):
                            self.maxwaits[player] = thiswait
                        
                        self.words[player] += [thisword]
                        print(player+" got word "+thisword)
        elif (self.state == "scoring"):
            None
        else:
            if not message.content.startswith("#"):
                return
            
            for operation in self.operations:
                if(operation.check(message.content)):
                    await operation.run(message, message.content, self)
  

client = MyClient()
client.run('your key here')