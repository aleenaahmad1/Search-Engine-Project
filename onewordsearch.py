import json
import re
import math
import time
from nltk.stem.snowball import SnowballStemmer
from tkinter import *
from tkinter import ttk
import shutil



snow_stemmer = SnowballStemmer(language='english')


file1 = open("E:\indexfilesfinal\lexiconFinal.json")
lex = json.load(file1)

file2 = open("E:\indexfilesfinal\invertedIndexContentFinal.json")
invIndex = json.load(file2)

file3 =  open("E:\indexfilesfinal\\fwdIndexContentFinal.json")
fwdIndex = json.load(file3)

file4 = open("E:\indexfilesfinal\docIndexFinal.json")
docIndex = json.load(file4)

file4 = open("E:\indexfilesfinal\\titlelexFinal.json")
titlelex = json.load(file4)

file4 = open("E:\indexfilesfinal\\fwdIndexTitleFinal.json")
titlefwd = json.load(file4)

file4 = open("E:\indexfilesfinal\invertedIndexTitleFinal.json")
titleinv = json.load(file4)

docScores = {}

resultsFound = "Results Found: "
resultList = []


def titlesearch(wordlist):
    for i in wordlist:
        if titlelex.get(i) is not None:
            ID = str(titlelex.get(i)) #getting ID from lexicon
            doclist = titleinv.get(ID) #LIST OF DOCS THAT HAVE WORD IN TITLE
    for i in doclist:
        docScores.update({i:1})


def search(input):
    querydocs = []
    input = input.lower()
    input = re.sub("[^\w\s]", "", input)

    
    wordlist = input.split(" ")
    wordsfinal = []
    for word in wordlist:
        wordsfinal.append(snow_stemmer.stem(word))
    
    titlesearch(wordsfinal)
    
    for i in wordsfinal:
        if lex.get(i) is None:
            ID=-1
        else:
            ID = str(lex.get(i)) #getting ID from lexicon
            doclist = invIndex.get(ID) #LIST OF DOCS THAT HAVE WORD
            querydocs.append(doclist)
            getRank(doclist, ID)
    sortingdocs()

def sortingdocs(): #sorting docs for multiple word query
    global resultsFound
    finaldocs = sorted(docScores.items(), key=lambda i:i[1], reverse=True)
    resultsFound += str(len(finaldocs))
    resultList.append(resultsFound)
    for i in finaldocs:
        print(docIndex.get(str(i[0]))[1])
        resultList.append(docIndex.get(str(i[0]))[1])
        print(docIndex.get(str(i[0]))[0])
        resultList.append(docIndex.get(str(i[0]))[0])
        print("\n")

def getRank(doclist, ID):
    global docScores
    termdoc = len(doclist)
    totaldoc = len(fwdIndex)
    for i in doclist:
        totalwords = len(fwdIndex.get(str(i)))
        termfreq = (fwdIndex.get(str(i)).get(ID))/(totalwords) #*need to divide by total num of words in doc
        idf = math.log((totaldoc/termdoc))
        tfidf = termfreq*idf
        if docScores.get(i) is not None: 
            docScores[i]+=tfidf
        else:
            docScores.update({i:tfidf})

window = Tk()


window.title("GBW")


window.geometry("800x600+200+100")


bg = PhotoImage(file="photo.png")
bglbl = Label(window, image=bg)
bglbl.place(x=0, y=0)


queryText = ""
newDoc = ""


def get_query():
    newWindow = Tk()
    newWindow.title("Search Results")
    newWindow.geometry("1280x1000")

    tempStr = ''
    urlLabel = Label(newWindow,height=100,width=200,background="light blue", anchor='nw', font="TimesNewRoman 20")
    urlLabel.place(x=0,y=0)
    queryText = entrywidget.get()
    search(queryText)

    for i in range (len(resultList)):
        tempStr+= resultList[i] + '\n'
        if i%2 == 0:
            tempStr += '\n''\n'

    urlLabel.config(text = tempStr)

def moveDoc(entry):
    newDoc = entry.get()
    destinationPath = "E:\sample1"
    shutil.move(newDoc,destinationPath)

def addNewDoc():
    aNewWindow = Tk()


    aNewWindow.title("Add Document")


    aNewWindow.geometry("800x600+200+100")


    entry1 = ttk.Entry(aNewWindow, width=50)
    entry1.pack(pady=10)


    btn2 = ttk.Button(aNewWindow, text="Add", command=lambda: moveDoc(entry1))
    btn2.pack(pady=10)


    aNewWindow.mainloop()


inputText = StringVar()

mylabel = Label(window, text="GBW", font="TimesNewRoman 20", foreground="orange", background="light blue")
mylabel.pack(pady=10)

entrywidget = ttk.Entry(window, textvariable=inputText, width=50)
entrywidget.pack(pady=10)


mybtn = ttk.Button(window, text="Search", command=get_query)
mybtn.pack(pady=10)

btn1 = ttk.Button(window, text="Add A New Document", command=addNewDoc)
btn1.pack(pady=10)


window.mainloop()

start = time.time()    
print("time:", time.time()-start)
