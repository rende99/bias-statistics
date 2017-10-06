import requests
import datetime
import os
import glob
import re
from termcolor import colored
os.chdir(r"C:\Users\Jerrett\Desktop\STOCK output")
from bs4 import BeautifulSoup
class BreakIt(Exception): pass

# NYT WORLD: http://www.nytimes.com/pages/world/index.html?module=SectionsNav&action=click&version=BrowseTree&region=TopBar&contentCollection=World&pgtype=Homepage
# NYT BUSINESS: http://www.nytimes.com/pages/business/index.html?action=click&region=TopBar&pgtype=SectionFront&module=SectionsNav&version=BrowseTree&contentCollection=Business&t=qry593
# NYT TECH: https://www.nytimes.com/section/technology?action=click&contentCollection=Tech&module=SectionsNav&pgtype=sectionfront&region=TopBar&version=BrowseTree
# BBC WORLD: http://www.bbc.com/news/world/middle_east
# BBC BUSINESS: http://www.bbc.com/news/business
# BBC TECH: http://www.bbc.com/news/technology
# CNN WORLD: http://www.cnn.com/world
# CNN BUSINESS: http://money.cnn.com/
# CNN TECH: http://money.cnn.com/technology/
#
# http://newsmap.jp/#/b,m,n,t,w/us/view/
#
#       NYT method:
#           each URL comes with a date. basically, just search for article urls by date
#           class="story"
#
#       BBC Method:
#           each URL I want goes like this: position 1, \n "url": "URL HERE". hopefully I can use the newline character to differentiate...
#
#       CNN Method:
#           CNN is a bit weird in that the order of the URL changes. use same method as NYT, except be SURE to only search with DATE. not order of URL
#
#


def cleanOld(f):
    os.remove(f)

def removeEmpty(file, numRemoved):
    if os.stat(str(file) + ".txt").st_size < 5:
        print("FILE # REMOVED: " + str(file))
        os.remove(str(file) + ".txt")
        numRemoved += 1


oldFiles = glob.glob('*.txt')
for f in oldFiles:
    cleanOld(f)

#Can't I resolve the function above to just do cleanOld()'s job in one line?

now = datetime.datetime.now()
currentDateURL = "/%s/" % str(now.year)
prevDateURL = "/%s/" % str(now.year - 1)

source = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
source[0] = requests.get("http://tinyurl.com/jkmvqp8")
source[1] = requests.get("http://tinyurl.com/gqogebc")
source[2] = requests.get("http://tinyurl.com/hkl7azq")
source[3] = requests.get("http://www.bbc.com/news/world")
source[4] = requests.get("http://www.bbc.com/news/business")
source[5] = requests.get("http://www.bbc.com/news/technology")
source[6] = requests.get("http://www.cnn.com/world")
source[7] = requests.get("http://money.cnn.com/")
source[8] = requests.get("http://money.cnn.com/technology/")
source[9] = requests.get("http://www.breitbart.com/big-government/")
source[10] = requests.get("http://www.breitbart.com/big-journalism/")
source[11] = requests.get("http://www.breitbart.com/national-security/")

stringArticles = list()
URLArticles = list()
NYT = 0
BBC = 0
CNN = 0
CNNM = 0
BBT = 0
i = 0
print("Finding Article Links...")

for s in source:

    currentSource = BeautifulSoup(s.content, 'html.parser')
    # for each source in my list, create the soup of content
    for link in set(currentSource.find_all('a')):
        # finds all the links in my soup, but also some that I don't want. Clean this up.
        StrLink = str(link)
        if -1 < i < 3:  # NYT handling
            if currentDateURL in StrLink and "interactive" not in StrLink and "/es/" not in StrLink and "nytimes" in StrLink:
                stringArticles.insert(-1, link.get('href'))
                NYT += 1
            elif prevDateURL in StrLink and now.month == 1 and "interactive" not in StrLink and "/es/" not in StrLink and "nytimes" in StrLink:
                # NEW YEAR EXCEPTION HANDLING
                stringArticles.insert(-1, link.get('href'))
                NYT += 1

        if 2 < i < 5:  # BBC handling
            if "/news/" in StrLink and link.get('href')[0] == "/" and ("technology-" in StrLink or "business-" in StrLink or "world-" in StrLink) and link.get('href')[-8]:
                stringArticles.insert(-1, "http://www.bbc.co.uk" + link.get('href'))
                BBC += 1

        if i == 6 and currentDateURL in StrLink and link.get('href')[0] == "/" and "/video" not in StrLink and "gallery" not in StrLink and "money.cnn.com" in StrLink:
            # for TRADITIONAL ARTICLES IN NORMAL CNN SITES
            stringArticles.insert(-1, "http://www.cnn.com" + link.get('href'))
            CNN += 1
        elif i == 6 and prevDateURL in StrLink and now.month == 1 and link.get('href')[0] == "/" and "/video" not in StrLink and "money.cnn.com" in StrLink:
            # for TRADITIONAL NEW YEAR HANDLING
            stringArticles.insert(-1, "http://www.cnn.com" + link.get('href'))
            CNN += 1
        if 6 < i < 9:
            if currentDateURL in StrLink and "money.cnn.com" not in StrLink and "luxury" not in StrLink and "gallery" not in StrLink and "/video" not in StrLink and "www.cnn.com" not in StrLink and "/blog/" not in StrLink and "edition.cnn.com" not in StrLink:
                stringArticles.insert(-1, "http://money.cnn.com" + link.get('href'))
                CNNM += 1
            elif prevDateURL in StrLink and now.month == 1 and "money.cnn.com" not in StrLink and "luxury" not in StrLink and "gallery" not in StrLink and "/video" not in StrLink and "www.cnn.com" not in StrLink and "/blog/" not in StrLink and "edition.cnn.com" not in StrLink:
                stringArticles.insert(-1, "http://money.cnn.com" + link.get('href'))
                CNNM += 1

        if 8 < i < 12:  # BBT handling
            if currentDateURL in StrLink and "www.breitbart.com" not in StrLink and "#disqus_thread" not in StrLink:
                stringArticles.insert(-1, "http://www.breitbart.com" + link.get('href'))
                BBT += 1
            elif currentDateURL in StrLink and "www.breitbart.com" in StrLink and "#disqus_thread" not in StrLink:
                stringArticles.insert(-1, link.get('href'))
                BBT += 1
            if prevDateURL in StrLink and now.month == 1 and "www.breitbard.com" not in StrLink and "#disqus_thread" not in StrLink:
                stringArticles.insert(-1, "http://www.breitbart.com" + link.get('href'))
                BBT += 1
            elif prevDateURL in StrLink and now.month == 1 and "www.breitbard.com" in StrLink and "#disqus_thread" not in StrLink:
                stringArticles.insert(-1, "http://www.breitbart.com" + link.get('href'))
                BBT += 1
    i += 1  # increment for i
print("Done")
print("Scraping Articles...")

j = 0
for x in stringArticles:
    # make requests to server
    # TEMPORARY J
    if j < len(stringArticles):
        print(x)
        URLArticles.insert(-1, requests.get(x))
        j += 1

textFiles = list(range(j))
# len(stringArticles)
# ^^^^ put this where 'j < 10' is above when you want to go back to doing all the links. also put this at the bottom
# where I get the text from each saved file!


k = 0
for s in URLArticles:
    # each article
    currentBody = BeautifulSoup(s.content, 'html.parser')
    if k <= NYT:
        # NYT HERE
        # OPEN FILE FOR WRITING HERE
        currentFile = open(str(k) + ".txt", "w")
        for title_tag in currentBody.find_all('title'):
            try:
                currentFile.write(title_tag.text)
                currentFile.write(":\n")
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for body_tag in currentBody.find_all('p', class_="story-body-text story-content"):
            try:
                currentFile.write(body_tag.text)
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        currentFile.close()
    if NYT < k <= BBC + NYT:
        # BBC HERE
        currentFile = open(str(k) + ".txt", "w")
        for title_tag in currentBody.find_all('title'):
            if title_tag.text != "BBC News":
                try:
                    currentFile.write(title_tag.text)
                    currentFile.write(":\n")
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        for intro_tag in currentBody.find_all('p', attrs={'class': "story-body__introduction"}):
            try:
                currentFile.write(intro_tag.text)
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for body_tag in currentBody.find_all('p', attrs={'class': None}):
            if body_tag.text != "Copy this link" and "BBC journalist" not in body_tag.text:
                try:
                    currentFile.write(body_tag.text)
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        currentFile.close()

    if BBC + NYT < k <= BBC + NYT + CNN:
        # CNN HERE
        currentFile = open(str(k) + ".txt", "w")

        for title_tag in currentBody.find_all('h1', class_="pg-headline"):
            try:
                currentFile.write(title_tag.text)
                currentFile.write(":\n")
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for intro_tag in currentBody.find_all('p', class_="zn-body__paragraph"):
            try:
                currentFile.write(intro_tag.text)
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for body_tag in currentBody.find_all('div', class_="zn-body__paragraph"):
            try:
                currentFile.write(body_tag.text)
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        currentFile.close()

    if BBC + NYT + CNN < k <= BBC + NYT + CNN + CNNM:
        # CNNM HERE
        currentFile = open(str(k) + ".txt", "w")

        for title_tag in currentBody.find_all('title'):
            try:
                currentFile.write(title_tag.text)
                currentFile.write(":\n")
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for intro_tag in currentBody.find_all('h2'):
            if "Terms of Service and Privacy Policy" not in intro_tag:
                try:
                    currentFile.write(intro_tag.text)
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        for body_tag in currentBody.find_all('p'):
            if "Most stock quote data provided by BATS" not in body_tag and "Cable News Network. A Time Warner Company." not in body_tag:
                try:
                    currentFile.write(body_tag.text)
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        currentFile.close()
    if BBC + NYT + CNN + CNNM < k <= BBC + NYT + CNN + CNNM + BBT:
        # BBT HERE
        currentFile = open(str(k) + ".txt", "w")
        for title_tag in currentBody.find_all('title'):
            try:
                currentFile.write(title_tag.text)
                currentFile.write(":\n")
            except UnicodeEncodeError:
                currentFile.write("ERROR")
        for intro_tag in currentBody.find_all('h2'):
            if "MOST POPULAR" or "FROM THE HOMEPAGE" not in intro_tag.text:
                try:
                    currentFile.write(intro_tag.text)
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        for body_tag in currentBody.find_all('p', attrs={'class': None}):
            if "Pre-Viral" not in body_tag.text and ("Follow" and "on Twitter") not in body_tag.text and "Breitbart Sports" not in body_tag.text:
                try:
                    currentFile.write(body_tag.text)
                except UnicodeEncodeError:
                    currentFile.write("ERROR")
        currentFile.close()
    k += 1

print("Done")
print("Cleaning up empty files...")
numRemoved = 0
# empty file check:

for file in range(k):
    removeEmpty(file, numRemoved)

print("Done")

# os.chdir(r"C:\Users\Jerrett\Desktop\STOCK resources")
# companyFile = open("companies.txt", 'r')

# num_lines = len(companyFile.readlines())

# m = 0;
# with open("companies.txt") as f:
# companyFormalNames = f.readlines()

os.chdir(r"C:\Users\Jerrett\Desktop")
print("Checking Bias...")
print("_____________________________________________________________")

#LIBERAL FILE HERE
with open('liberal.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

dataL = data.split(",")

#CONSERVATIVE FILE HERE
with open('conservative.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

dataC = data.split(",")

#FLIP FILE HERE
with open('flip.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

dataF = data.split(",")

#DOUBLE FILE HERE
with open('double.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')

dataD = data.split(",")



# Because left = liberal and right = conservative, I'm going to say that hitting a liberal keyword is -1, and hitting
# a conservative keyword is +1.

os.chdir(r"C:\Users\Jerrett\Desktop\STOCK output")
NYTbias = 0
BBCbias = 0
CNNbias = 0
BBTbias = 0
bias = 0
bp = 0
cMultiplier = 1


def checkFlipsDoubles(s, e, splitList,index):
    splitList.extend(['',''])
    m = 1
    try:
        for x in range(s, e):
            for fl in dataF:
                if splitList[x] == fl or ((splitList[index-1] == "\"" or splitList[index-2] == "\"") and (splitList[index+1] == "\"" or splitList[index+2] == "\"")):
                    m *= -1
                    raise BreakIt
    except BreakIt:
        pass

    for x in range(s, e):
        for db in dataD:
            if splitList[x] == db and m <= 64 and m >= -64:
                m *= 2
    return m


def mSort(artString, word, ntf):
    #find word in artString. It's there, i can assume that. Then, using the known index of it, based on
    # artString.split(), I can use list logic to perform searching for words that may affect multiplication.
    # Pretty sure that's all.
    m = 1
    artString = artString.replace("’", "")
    artString = artString.replace("\'", "")
    artString = artString.replace("“","\"")
    artString = artString.replace("”","\"")
    artSplit = re.compile('\w+|"|\.|\?|\!').findall(artString)
    firstP = 0
    lastP = 0
    artSplit2 = artSplit
    while ntf > 0:
        artSplit[artSplit.index(word)] = ''
        ntf -= 1
        # delete occurances based on how many times i've already found the word.

    index = artSplit.index(word)

    try:
        for i in artSplit:
            if artSplit.index(i) < artSplit.index(word):
                if i == '.' and artSplit[artSplit.index(i)-2] != '.' and (artSplit[artSplit.index(i)-1] != 'r'
                        or artSplit[artSplit.index(i)-2] != 'm') and (artSplit[artSplit.index(i)-1] != 's'
                        or artSplit[artSplit.index(i)-2] != 'r' or artSplit[artSplit.index(i)-3] != 'm') and (artSplit[artSplit.index(i)-1] != 's'
                        or artSplit[artSplit.index(i)-2] != 'm') or i == '?' or i == '!' or artSplit.index(i) == 0:

                    #this was the period/end of the last sentence before the word occurs
                    firstP = artSplit.index(i)
                    artSplit[artSplit.index(i)] = '' # need to do this in case there are 2 of the same word. .index only finds first occurance.

            else:
                if i == '.' or i == '?' or i == '!':
                    #this was the period/end of the end of the sentence containing the word
                    lastP = artSplit.index(i)
                    artSplit[artSplit.index(i)] = '' # need to do this in case there are 2 of the same word. .index only finds first occurance.
                    m = checkFlipsDoubles(firstP,lastP,artSplit2,index)
                    raise BreakIt # exit once it hits the first time. we dont need this going twice.
    except BreakIt:
        pass

    return m

# work probably in here. I should add something that says if in an extended quote (more than just the string is
# surrounded by "", I can ignore. But, if only the string is encapsulated in "", it's multiplied by -1.
# Multipliers can be "_____", not, very, super,

#This will be where I think out loud. currentArticleS will be the string that holds the entire article. from there,
# I can just pretend I'll be performing a simple string search for multipliers.
# Ok, so this is how the function below works. If bp, the number of articles gone through, is less than how many there
# are, it keeps going. It opens the next article, converts it to a string. Then comes the interesting parts.
# 1st: for each word in the Liberal keyword file, it checks if that word is in the current article. if it is, it
# subtracts 1. Same for the Conservative side, except it adds one instead of subtracting.
#
#
#
#
#
maxCatches = 4

for x in stringArticles:
    if bp < len(stringArticles) - numRemoved:
        bias = 0
        currentArticle = open(str(bp) + ".txt", "r")
        currentArticleS = str.lower(currentArticle.read())

        for w in dataL:
            currentCatches = 0
            for pepe in currentArticleS.split():
                if pepe == w and currentCatches < maxCatches:
                    # where w is a Liberal keyword
                    cMultiplier = mSort(currentArticleS, w, currentCatches)
                    bias -= 1 * cMultiplier
                    print("L: " + w + ".\t| Multiplier = " + colored(cMultiplier, 'green') + " x " + colored("-1",'blue') + " = " + str(cMultiplier*-1))
                    currentCatches += 1

        for w in dataC:
            currentCatches = 0
            for pepe in currentArticleS.split():
                if pepe == w and currentCatches < maxCatches:
                    # where w is a Conservative keyword
                    cMultiplier = mSort(currentArticleS, w, currentCatches)
                    bias += 1 * cMultiplier
                    print("C: " + w + ".\t| Multiplier = " + colored(cMultiplier, 'green') + " x " + colored("1",'red') + " = " + str(cMultiplier*1))
                    currentCatches += 1

        if bp <= NYT:
            # Just read a NYT article
            NYTbias += bias
        if NYT < bp <= NYT + BBC:
            # Just read a BBC article
            BBCbias += bias
        if NYT + BBC < bp < NYT + BBC + CNN + CNNM:
            # Just read a CNN or CNNM article
            CNNbias += bias
        if NYT + BBC + CNN + CNNM < bp < NYT + BBC + CNN + CNNM + BBT:
            # Just read a BBT article
            BBTbias += bias
        if bias > 0:
            print(colored("Article #" + str(bp) + ":\t\t", 'white'), colored(str(bias), 'red', attrs=['bold']))
        if bias < 0:
            print(colored("Article #" + str(bp) + ":\t\t", 'white'), colored(str(bias), 'blue', attrs=['bold']))
        if bias == 0:
            print(colored("Article #" + str(bp) + ":\t\t", 'white'), colored(str(bias), attrs=['bold']))
        bp += 1



print("_____________________________________________________________")
print("Summary:\n\n")
print("NYT: Articles " + str(0) + " - " + str(NYT))
print("BBC: Articles " + str(NYT+1) + " - " + str(NYT+BBC))
print("CNN: Articles " + str(NYT+BBC+1) + " - " + str(NYT+BBC+CNN+CNNM))
print("BBT: Articles " + str(NYT+BBC+CNN+CNNM+1) + " - " + str(NYT+BBC+CNN+CNNM+BBT))
print("_____________________________________________________________")

print("Total articles: n = " + str(NYT+BBC+CNN+CNNM+BBT))
print("New York Times Average Bias: " + str(NYTbias/NYT))
print("BBC Average Bias: " + str(BBCbias/BBC))
print("CNN Average Bias: " + str(CNNbias/(CNN+CNNM)))
print("Breitbart Average Bias: " + str(BBTbias/BBT))

# known issues:
#   duplicate articles by searching content
#   new year's day handling [SOLVED]
#   not deleting previous articles from folder when run again [SOLVED]
#   only finds one instance of keyword then stops looking for more[SOLVED]
#   multi-word searches, i.e. bernie sanders vs. sarah sanders - I should distinguish.
#   sentence - boundary disambiguation. Basically, periods can mean a lot of things in writing.[SEMI-FIXED, NOT PERFECT]