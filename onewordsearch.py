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
    doclist = []
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
       # print(docIndex.get(str(i[0]))[1])
        resultList.append(docIndex.get(str(i[0]))[1])
        #print(docIndex.get(str(i[0]))[0])
        resultList.append(docIndex.get(str(i[0]))[0])
       # print("\n")

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
window.state("zoomed")


bg = PhotoImage(file="background.png")
bglbl = Label(window, image=bg)
bglbl.place(x=0, y=0)


queryText = ""
newDoc = ""

resultSelector = 0




def get_query():
    newWindow = Tk()
    newWindow.title("Search Results")
    newWindow.geometry("1280x1000")
    
    def getResults(num,label):
        tempStr = ''
        for i in range (num*5,(num*5)+15):
            if num*5 >= len(resultList):
                return
            tempStr+= resultList[i] + '\n'
            if i%2 == 0:
                tempStr += '\n''\n'
        label.config(text = tempStr)

    def next():
        global resultSelector
        tempStr = ''
        resultSelector +=1
        getResults(resultSelector,urlLabel)

    def prev():
        global resultSelector
        tempStr = ''
        resultSelector -=1
        getResults(resultSelector,urlLabel)
    
    

    urlLabel = Label(newWindow,height=50,width=200,background="light blue", anchor='nw', font="TimesNewRoman 15")
    urlLabel.place(x=0,y=0)
    queryText = entrywidget.get()
    search(queryText)
    tempStr=''
    for i in range (0,15):
        tempStr+= resultList[i] + '\n'
        if i%2 == 0:
            tempStr += '\n''\n'

    urlLabel.config(text = tempStr)

    button1 = ttk.Button(newWindow, text="Next",command= next)
    button1.place(x= 900,y=50)

    button2 = ttk.Button(newWindow,text="Previous",command=prev)
    button2.place(x=900,y=100)

def moveDoc(entry):
    newDoc = entry.get()
    destinationPath = "E:\sample1"
    shutil.move(newDoc,destinationPath)

def addNewDoc():
    aNewWindow = Tk()


    aNewWindow.title("Add Document")


    aNewWindow.geometry("800x600+200+100")


    entry1 = ttk.Entry(aNewWindow, width=50, font="Ariel 12 bold")
    entry1.pack(pady=10)


    btn2 = ttk.Button(aNewWindow, text="Add", command=lambda: moveDoc(entry1))
    btn2.pack(pady=10)


    aNewWindow.mainloop()



inputText = StringVar()


mylabel = Label(window,text="GBW", bd=3 , font="Ariel 32", foreground="black", background="light blue", relief=RAISED)
mylabel.pack(pady=10)

entrywidget = ttk.Entry(window, textvariable=inputText, width=50 ,font="Ariel 30")
entrywidget.place(x=400,y=500)


mybtn = ttk.Button(window, text="Search", command=get_query,width=30)
mybtn.place(x=820,y=600)

btn1 = ttk.Button(window, text="Add A New Document", command=addNewDoc)
btn1.place(x=1600,y=10)



window.mainloop()

start = time.time()    
print("time:", time.time()-start)
