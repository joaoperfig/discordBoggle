import random
from PIL import Image, ImageFont, ImageDraw
import copy

def getrandletter():
    f = open("corpus.txt", "r", encoding="utf8")
    content = f.read()
    f.close()
    text = content.lower()
    char = random.choice(text)
    while not (char in "abcdefghijklmnopqrstuvwxyz"):
        char = random.choice(text)
    char = char.upper()
    if (char == "Q"):
        char = "Q"
    return char


class BoggleGame():
    def __init__(self):
        self.board = []
        for i in range(4):
            line = []
            for j in range(4):
                line += [getrandletter()]
            self.board += [line]
                
    def stringshow(self):
        res = ""
        for line in self.board:
            res += " "
            for char in line:
                res += char + " "
            res += "\n"
        return res
    
    def stringshow2(self):
        res = "\n"
        for line in self.board:
            res += "                    "
            for char in line:
                res += char + "         "
            res += "\n\n"
        return res    
    
    def stringshow3(self):
        res = "\n"
        for line in self.board:
            res += "               "
            for char in line:
                res += char + "    "
            res += "\n"
        return res        
    
    def makeImage(self):
        image = Image.new("RGBA", (800,800), (36,84,99))
        font = ImageFont.truetype("futurab.otf", 120)
        y = 100
        for line in self.board:
            x = 100
            for char in line:     
                draw = ImageDraw.Draw(image)
                draw.rectangle(((x-90, y-90), (x+90, y+90)), fill=(50,139,158))
                draw = ImageDraw.Draw(image)
                w,h = draw.textsize(char, font=font)
                draw = draw.text((x-(w/2),y-(h/2)), char,(235,235,235), font=font)
                x += 200
            y += 200   
        image.save("img.png")
        
    def hasword(self, word):
        word=word.upper()
        first = word[0]
        first = first.upper()
        word = word[1:]
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == first:
                    if self.crawl(i, j, copy.deepcopy(self.board), word):
                        return True
        return False
                    
    def crawl(self, i, j, board, word):
        if (i<0) or (i>3) or (j<0) or (j>3): #arranjar isto Qu
            return False
        if (len(word) == 0):
            return True    
        board[i][j] = "?"  
        first = word[0]
        first = first.upper()
        word = word[1:]
        for deltai in range(-1, 2):
            for deltaj in range(-1, 2):
                try:
                    if board[i+deltai][j+deltaj] == first:
                        if self.crawl(i+deltai, j+deltaj, copy.deepcopy(board), word):
                            return True
                except:
                    None
        return False