import time
import game
import discord
import asyncio
import spellcheck
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
    for player in list(client.scores):
        scores[player] = 0
    for word in sortedwords:
        points = 0
        string = "**" + word + "** - "
        for player in words[word]:
            string += player + " "
        string += "- "
        if (len(word)> 2) and (client.game.hasword(word)):
            if spellcheck.check(word):
                if len(word) == 3:
                    string += "Short word. - **1** point - "+spellcheck.priblink(word)
                    points = 1
                else:
                    if len(words[word]) == 1: # only one player got it
                        string += "Great word! - **3** points - "+spellcheck.priblink(word)
                        points = 3                        
                    else:
                        string += "Good word! - **2** points - "+spellcheck.priblink(word)
                        points = 2                               
            else:
                #word does not exist
                string += "Is **not** a real word! - **0** points - "+spellcheck.priblink(word)
        else:
            if (len(word) <= 2):
                string += "Is too short! - **0** points"
            else:
                string += "Is **not** on the board! - **0** points"
        for player in words[word]:
            scores[player] += points
        await channel.send(string)
        await asyncio.sleep(2)
    await channel.send("Those are all the words! Here are the round's scores:")
    await asyncio.sleep(4)
    string = ""
    for player in list(scores):
        string += "     **" + player + "** -> **" + str(scores[player]) + "** points\n"
    await channel.send(string)
    await asyncio.sleep(5)
    await channel.send("Which adds up to these session scores:")
    await asyncio.sleep(4)
    for player in list(scores):
        client.scores[player] += scores[player]
    string = ""
    for player in list(scores):
        string += "     **" + player + "** -> **" + str(client.scores[player]) + "** points\n"    
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
        for player in list(client.scores):
            client.words[player] = []
            await client.usernames[player].send("Thank you for joining this game!\nYou have three minutes!\nType one word per message underneath.\nThe board is:")
            await client.usernames[player].send(file=discord.File('img.png'))
        await messageall(message.channel, client, 60, "Two minutes remaining!", True)    
        await messageall(message.channel, client, 60, "One minute remaining!", True)    
        await messageall(message.channel, client, 50, "Only ten seconds remaining!", False)     
        await endtimer(message.channel, client, 10)     