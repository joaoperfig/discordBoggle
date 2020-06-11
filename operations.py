import time
import game
import discord
import asyncio
import spellcheck
import random
import math
from threading import Timer

async def messageall(channel, client, time, message, showboard):
    await asyncio.sleep(time) # wait 2 minutes
    await channel.send(message)
    for player in list(client.scores):
            await client.usernames[player].send(message)    
            if (showboard):
                await client.usernames[player].send(file=discord.File('img.png'))

async def endtimer(channel, client, wait):
    await asyncio.sleep(wait) 
    await channel.send("**Time's up!**")
    for player in list(client.scores):
            await client.usernames[player].send("**Time's up!** Let's see how you did over on the main channel.")
            thiswait = time.time() - client.lastwordtime[player]
            client.lastwordtime[player] = time.time()
            if (thiswait > client.maxwaits[player]):
                client.maxwaits[player] = thiswait            
    client.status = "scoring"
    await asyncio.sleep(6)
    await channel.send("Here are people's words!")
    words = {}
    for player in list(client.words):
        for word in client.words[player]:
            word = spellcheck.clean(word)
            if word in list(words):
                words[word] += [player]
            else:
                words[word] = [player]
    sortedwords = list(words)
    sortedwords.sort()
    sortedwords.sort(key=len)
    scores = {}
    
    awards = {}
    awards["3letter"] = {}
    awards["length"] = {}
    awards["blind"] = {}
    awards["creative"] = {}
    awards["unique"] = {}
    awards["copier"] = {}
    awards["forgetful"] = {}
    awards["erudite"] = {}
    awards["typer"] = {}
    awards["loser"] = {}
    awards["wait"] = {}
    
    awname = {}
    awname["3letter"] = "3 Letter King"
    awname["length"] = "Eloquent Speaker"
    awname["blind"] = "Board Skipper"
    awname["creative"] = "Creative Genius"
    awname["unique"] = "Original Writer"
    awname["copier"] = "Derivative Bore"
    awname["forgetful"] = "Most Forgetful"
    awname["erudite"] = "Erudite Scholar"
    awname["typer"] = "Typing Ninja"
    awname["loser"] = "Greatest Loser"
    awname["wait"] = "Slowpoke"
    
    awdesc = {}
    awdesc["3letter"] = " words with only 3 letters."
    awdesc["length"] = " average word length."
    awdesc["blind"] = " words that are not on the board."
    awdesc["creative"] = " words that do not exist."
    awdesc["unique"] = "% words that only you wrote."
    awdesc["copier"] = "% words were also written by other players."
    awdesc["forgetful"] = " times you tried to input the same word again."
    awdesc["erudite"] = " total words."
    awdesc["typer"] = " total key presses."   
    awdesc["loser"] = " total points lost."  
    awdesc["wait"] = " seconds without writing a word."
    
    for player in list(client.scores):
        scores[player] = 0
        awards["3letter"][player] = 0
        awards["length"][player] = 0
        awards["blind"][player] = 0
        awards["creative"][player] = 0
        awards["unique"][player] = 0
        awards["copier"][player] = 0
        awards["forgetful"][player] = client.forgets[player]
        awards["erudite"][player] = 0
        awards["typer"][player] = 0
        awards["loser"][player] = 0
        awards["wait"][player] = client.maxwaits[player]
        
        
    for word in sortedwords:
        points = 0
        string = "**" + word + "** - "
        wplayers = words[word]
        for player in wplayers:
            string += player + " "
        string += "- "
        
        length = len(word)
        onboard = client.game.hasword(word) # exists on the board
        exists = spellcheck.check(word) # 
        unique = len(wplayers) == 1 # only one player got it
        
        if unique:
            awards["unique"][wplayers[0]] += 1
        else:
            for player in wplayers:
                awards["copier"][player] += 1            
        
        if (length<=2):
            wordtype = "Too short!"
            points = 0
        elif not onboard:
            for player in wplayers:
                awards["blind"][player] += 1      
                awards["loser"][player] += 2
            wordtype = "**NOT** on the board!"
            points = -2
        elif not exists:
            for player in wplayers:
                awards["creative"][player] += 1      
                awards["loser"][player]  += 3
            wordtype = "Does **NOT** exist!"
            points = -3
        elif (length==3):
            for player in wplayers:
                awards["3letter"][player] += 1     
            wordtype = "Okay word."
            points = 1
        else:
            points = length - 2 #math.floor((length+1)/2)
            if unique:
                points += 1
            wordtypes = ["Good word.", "Cool word.", "Great word!", "Awesome word!", "INCREDIBLE word!", "UNBELIEVABLE!!!", "YOU ARE A GOD!!!"]+[("A"*(7+(n*3)))+("!"*(3+(n*2))) for n in range(10)]
            wordtype = wordtypes[points-2]
        
        for player in wplayers:
            awards["typer"][player] += length   
            awards["erudite"][player] += 1
        
        string += wordtype + " **"+str(points)+"** point"
        if (points != 1):
            string += "s"
        if (onboard):
            string += " - "+spellcheck.priblink(word)
        
        
        for player in words[word]:
            scores[player] += points
        await channel.send(string)
        await asyncio.sleep(1)
        
    for player in list(scores):
        try:
            awards["length"][player] = awards["typer"][player] / awards["erudite"][player]
            awards["unique"][player] = (awards["unique"][player] / awards["erudite"][player])*100
            awards["copier"][player] = (awards["copier"][player] / awards["erudite"][player])*100
        except:
            print("some error with awards calculation")
            awards["length"][player] = 0
            awards["unique"][player] = 0
            awards["copier"][player] = 0
        for award in list(awards):
            print(player+" - "+award+" - "+str(awards[award][player]))
        
    await channel.send("Those are all the words!")
    await asyncio.sleep(1)
    await channel.send("Here are the round's awards:")
    await asyncio.sleep(2)
    taken = []
    for i in range(3):
        found = False
        award = None
        while not found:
            award = random.choice(list(awards))
            if (not (award in taken)) and (max([awards[award][player] for player in list(scores)]) > 1):
                found = True
                taken += [award]
        winner = None
        record = 0
        for player in list(scores):
            if awards[award][player] > record:
                winner = player
                record = awards[award][player]
        string = "" + awname[award] + " - **" +winner+"** - **"+(str(record)[:5])+"**"+awdesc[award]
        await channel.send(string)
        await asyncio.sleep(4)        
    
    
    await channel.send("and here are the round's scores:")
    await asyncio.sleep(4)
    string = ""
    for player in list(scores):
        string += "**" + player + "** -> **" + str(scores[player])+ "** points\n"
    await channel.send(string)
    await asyncio.sleep(5)
    await channel.send("Which adds up to these session scores:")
    await asyncio.sleep(4)
    for player in list(scores):
        client.scores[player] += scores[player]
    string = ""
    for player in list(scores):
        string += "**" + player + "** -> **" + str(client.scores[player]) + "** points\n"    
    await channel.send(string)
    await asyncio.sleep(5)
    await channel.send("Use #game to play another game!")
    client.state = "finish"
        
    
class ExitOperation():
    def helpmessage(self):
        return "#selfdestruct -> :("
    
    def check(self, message):
        return message.startswith("#selfdestruct")
    
    async def run(self, message, content , client):
        exit()  

class HelpOperation():
    def helpmessage(self):
        return "#help -> Show help"
    
    def check(self, message):
        return message.startswith("#help")
    
    async def run(self, message, content , client):
        res = "Figueira discordbogglebot:"
        for operation in client.operations:
            res = res + "\n" + operation.helpmessage() 
        await message.channel.send(res)   
            
class SessionOperation():
    def helpmessage(self):
        return "#session -> Start new game session"
    
    def check(self, message):
        return message.startswith("#session")
    
    async def run(self, message, content, client):
        client.scores = {}
        client.usernames = {}
        client.state = "register"
        client.mainchannel = message.channel
        await message.channel.send("Starting new session! Please use #join to participate. After everyone joined use #game to start!")   
        
class JoinOperation():
    def helpmessage(self):
        return "#join -> Join session that has just been created"
    
    def check(self, message):
        return message.startswith("#join")
    
    async def run(self, message, content, client):
        if not (client.state == "register"):
            await message.channel.send("A new session must be created for players to join. Please use #session.")
            return
        client.scores[message.author.name] = 0
        client.usernames[message.author.name] = message.author
        await message.channel.send("Thank you for joining, "+message.author.name+".")
        
class GameOperation():
    def helpmessage(self):
        return "#game -> Start a game, after a session has been created and players have joined"
    
    def check(self, message):
        return message.startswith("#game")
    
    async def run(self, message, content, client):
        if (client.state == "waiting"):
            await message.channel.send("A new session must be created before a game can start. Please use #session.")
            return
        if (len(list(client.scores)) == 0):
            await message.channel.send("Noone has joined this session! Please use #join.")
            return      
        if (client.mainchannel.name != message.channel.name):
            await message.channel.send("A new game can only be started on the same channel where the session was started.")
            return               
        client.state = "gaming"
        client.gamestart = time.time()
        client.game = game.BoggleGame()
        client.game.makeImage()
        await message.channel.send("**Starting  game!**\nPlease don't type your messages on this thread.\nYou have three minutes!\nThe board is:")
        await message.channel.send(file=discord.File('img.png'))
        client.words = {}
        client.forgets = {}
        client.maxwaits = {}
        client.lastwordtime = {}
        for player in list(client.scores):
            client.words[player] = []
            client.forgets[player] = 0
            client.lastwordtime[player] = time.time()
            client.maxwaits[player] = 0
            await client.usernames[player].send("Thank you for joining this game!\nYou have three minutes!\nType one word per message underneath.\nThe board is:")
            await client.usernames[player].send(file=discord.File('img.png'))
        await messageall(message.channel, client, 60, "Two minutes remaining!", True)    
        await messageall(message.channel, client, 60, "One minute remaining!", True)    
        await messageall(message.channel, client, 50, "Only ten seconds remaining!", False)     
        await endtimer(message.channel, client, 10)     