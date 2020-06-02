import urllib.request

def clean(word):
    word = word.strip()
    word = word.lower()
    return word

def browsercontent(url):
    try:
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()    
    except:
        print ("ERROR: COULD NOT RECEIVE WEB DATA")
        return "ERROR"
    return mystr

def priblink(word):
    return "https://dicionario.priberam.org/"+clean(word)

def check(word):
    web = browsercontent(priblink(word))
    return not (("Palavra n"+chr(227)+"o encontrada.") in web) 