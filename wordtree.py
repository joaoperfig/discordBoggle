
class wordtree():
    def __init__(self, wordfile, fixqu=False, upper=False):
        print ("Starting wordtree")
        f = open(wordfile, "r")
        self.words = eval(f.read())
        f.close()
        if fixqu:
            for i in range(len(self.words)):
                self.words[i] = self.words[i].replace("qu", "4")
        if upper:
            for i in range(len(self.words)):
                self.words[i] = self.words[i].upper() 
        print ("Loaded words")
        self.root = wordnode(self.words)
        print ("Built tree with "+str(self.root.countnodes())+" nodes")
        
    def hasword(self, word):
        return self.root.hasword(word)
    
    def getnode(self, subword):
        return self.root.getnode(subword)
        
class wordnode():
    def __init__(self, words):
        self.isword = False
        while "" in words:
            self.isword = True
            words.remove("")
        self.nodes = {}
        self.nextwords = {}
        for word in words:
            start = word[0]
            if not (start in self.nextwords):
                self.nextwords[start] = [word[1:]]
            else:
                self.nextwords[start] += [word[1:]]
        for nextletter in list(self.nextwords):
            self.nodes[nextletter] = wordnode(self.nextwords[nextletter])
            
    def countnodes(self):
        res = 1
        for nextletter in list(self.nodes):
            res += self.nodes[nextletter].countnodes()
        return res
    
    def hasnext(self, letter):
        return letter in list(self.nodes)
    
    def hasword(self, word):
        if (word == ""):
            return self.isword
        start = word[0]
        if start in list(self.nodes):
            return self.nodes[start].hasword(word[1:])
        else:
            return False
        
    def getnode(self, subword):
        if (subword == ""):
            return self
        start = subword[0]
        if start in list(self.nodes):
            return self.nodes[start].getnode(subword[1:])
        else:
            return None
        