#!/usr/bin/python

'''
A small personal project to correct orthography in LaTeX and html files
Author: Robin Milosz

it checks:
french and english orthography spelling
french plural with determiners

optionnal:
french/english language switch checking
french "a" and "'a" (accent) listing

to run:
python words_correction_program.py [the path of your target file "/u/username/Documents/example.tex"]
'''

#imports
import time
import sys

#start counting the time
nm = 0
ts = time.time()

#this method tests if a word is "normal" and can be check in a dictionary
# it prevents a lot of LaTeX formatting words to be checked
def okKey(key):
    if key.find("$") != -1:
        return False
    elif key.find("(") != -1:
        return False
    elif key.find(")") != -1:
        return False
    elif key.find("[") != -1:
        return False
    elif key.find("]") != -1:
        return False
    elif key.find("{") != -1:
        return False
    elif key.find("}") != -1:
        return False
    elif key.find("<") != -1:
        return False
    elif key.find(">") != -1:
        return False
    elif key.find("%") != -1:
        return False
    elif key.find("\\") != -1:
        return False
    elif key.find("/") != -1:
        return False
    elif key.find("*") != -1:
        return False
    elif key.find("+") != -1:
        return False
    elif key.find("^") != -1:
        return False
    elif key.find("=") != -1:
        return False
    elif key.find("&") != -1:
        return False
    elif key.find("_") != -1:
        return False
    elif key.find("|") != -1:
        return False
    elif key.find("#") != -1:
        return False
    elif key.find(".") != -1: #websites
        return False
    elif key == "-":
        return False
    elif key.isdigit():
        return False
    else:
        return True

#welcome print
print " "
print " *** Word Correction Program ***"
print "  (originaly intended for french/english LaTeX or html files)"
print " "

#create empty dictionaries
frenchDictionary = {}
englishDictionary = {}
bilingualWordsDictionary = {}
extraDictionary = {}

#load the french dictionary
dictionaryFileName = "french_words.txt"
filePath = "data/%s" % dictionaryFileName
count = 1
with open(filePath,"r") as dataFile:
    for line in dataFile:
        #array.append(line)
        #print line
        word = line.rstrip().strip()
        frenchDictionary[word] = count
        count += 1

dataFile.close()

#load the english dictionary
dictionaryFileName = "english_words.txt"
filePath = "data/%s" % dictionaryFileName
count = 1
with open(filePath,"r") as dataFile:
    for line in dataFile:
        #array.append(line)
        #print line
        word = line.rstrip().strip().lower()
        englishDictionary[word] = count
        count += 1

dataFile.close()

#load the bilingual words dictionary
dictionaryFileName = "bilingual_words.txt"
filePath = "data/%s" % dictionaryFileName
count = 1
with open(filePath,"r") as dataFile:
    for line in dataFile:
        #array.append(line)
        #print line
        word = line.rstrip().strip()
        bilingualWordsDictionary[word] = count
        count += 1

dataFile.close()
#load the extra words dictionary
dictionaryFileName = "extra_words.txt"
filePath = "data/%s" % dictionaryFileName
count = 1
with open(filePath,"r") as dataFile:
    for line in dataFile:
        #array.append(line)
        #print line
        word = line.rstrip().strip()
        extraDictionary[word] = count
        count += 1

dataFile.close()


#load the a file
dictionaryFileName = "a.txt"
filePath = "data/%s" % dictionaryFileName
with open(filePath,"r") as dataFile:
    for line in dataFile:
        #array.append(line)
        #print line
        aAccent = line.rstrip().strip()

dataFile.close()

#print the sizes of the dictionaries
print "frenchDictionary size:", len(frenchDictionary)
print "englishDictionary size:", len(englishDictionary)
print "bilingualWordsDictionary size:", len(bilingualWordsDictionary)
print "extraDictionary size:", len(extraDictionary)
print " "

#specify the target file
if (len(sys.argv) > 1):
    filePath = sys.argv[1]
else:
    filePath = "my_text.txt"

#for plurality checking
lastKeyFrPlural = False
#from http://test.alloprof.qc.ca/francais/le-systeme-des-accords/le-pluriel-des-determinants.aspx
pluralFrDeterminers = ["les","des","mes","tes","ses","nos","vos","leurs","ces","quels","quelles","deux","trois","quatres","cinq"]
pluralFrExceptions = ["top","arn","deux","trois","quatres","cinq"]

#for language variation checking
lastKeyLanguageIs = "Empty" # "French", "English", "Extra", "Error", "Empty"
languageVariationChecking = True #warning it's a first version, a little bit inneficient due to some names inserted in the dictionnaries

#other
lastKey = ""

#a checking switch
aChecking = False

#open the target file
lineNumber = 0
numberOfPotentialMistakes = 0
numberOfPotentialLanguageSwitch = 0
numberOfLinesInFile = 0
numberOfCheckedKeysInFile = 0
with open(filePath,"r") as dataFile:
    for line in dataFile: #read all the lines
        lineNumber += 1
        #print lineNumber," lines done         \r",
	#linePure = line.rstrip().strip().replace(';',' ').replace(',',' ').replace('.',' ').replace('\'',' ')
	linePure = line.rstrip().strip().replace(';',' ').replace(',',' ').replace('\'',' ')
	linePure2 = linePure.rstrip().strip().replace('\"',' ').replace('?','.').replace(':',' ').replace('-',' ').replace('!','.').replace('`',' ')
	#linePure3 = linePure.rstrip().strip().replace('(',' ').replace(')',' ').replace('{',' ').replace('}',' ')
        for word in linePure2.split(" "): #split the line into words
            pureWord = word.rstrip().strip() #take the blank spaces before and after
            if pureWord.find(".") != -1: #if there is a dot at the end of the word, take it off
                if pureWord[len(pureWord)-1] == '.':#so that website stay but no ending words
                    pureWord = pureWord[0:len(pureWord)-1]
                    lastKeyLanguageIs = "Empty"


            #key = pureWord.decode('utf-8').lower()
            key = pureWord.lower() #put it in lowercase
            if len(key) > 0:
                if key in pluralFrDeterminers:#checking if its a plural determiner
                    lastKeyFrPlural = True
                else:
                    lastKeyFrPlural = False

                if okKey(key):
                    numberOfCheckedKeysInFile += 1
                    if key in frenchDictionary: #if it's in the french dictionary
                        #print "ok"
                        if (lastKeyLanguageIs == "English" and languageVariationChecking):
                            if (not(key in bilingualWordsDictionary or lastKey in bilingualWordsDictionary)):
                                if (not(key in extraDictionary or lastKey in extraDictionary)):
                                    print "%s %s (%s), en-fr language switch?" % (lastKey,key,lineNumber) #print the potential mistake
                                    numberOfPotentialLanguageSwitch += 1
                        lastKeyLanguageIs = "French"
                        pass
                    elif key in englishDictionary: #if it's in the english dictionary
                        #print "ok"
                        if (lastKeyLanguageIs == "French" and languageVariationChecking):
                            if (not(key in bilingualWordsDictionary or lastKey in bilingualWordsDictionary)):
                                if (not(key in extraDictionary or lastKey in extraDictionary)):
                                    print "%s %s (%s), fr-en language switch?" % (lastKey,key,lineNumber) #print the potential mistake
                                    numberOfPotentialLanguageSwitch += 1
                        lastKeyLanguageIs = "English"
                        pass
                    elif key in extraDictionary: #if it's in the extra words dictionary
                        #print "ok"
                        lastKeyLanguageIs = "Extra"
                        pass
                    else: #else it my be an error
                        numberOfPotentialMistakes += 1
                        print "%s (%s), orthography?" % (key,lineNumber) #print the potential mistake
                        lastKeyLanguageIs = "Error"
                        #print "%s" % (key)
                        #print "%s" % (pureWord)

                    if (lastKeyFrPlural):#if the last key was a french plural determiner
                        if (key[len(key)-1] == 's' or key[len(key)-1] == 'x'):
                            pass
                        elif key in pluralFrExceptions:
                            pass
                        else:
                            numberOfPotentialMistakes += 1
                            print "%s (%s), plural?" % (key,lineNumber) #print the potential mistake

                    if (lastKey == "tout"):#commun error: "tout les" -> "tous les"
                        if (key in pluralFrDeterminers):
                            numberOfPotentialMistakes += 1
                            print "%s %s (%s), tous?" % (lastKey, key, lineNumber) #print the potential mistake

		    if (aChecking):
                        if (lastKey == "a" or lastKey == aAccent):
                            print "%s %s (%s), aaa?" % (lastKey,key,lineNumber) #print the potential mistake
                        if (key == "a" or key == aAccent):
                            print "%s %s (%s), aaa?" % (lastKey,key,lineNumber) #print the potential mistake


                    lastKey = key
                else:
                    lastKeyLanguageIs = "Empty"


#close the file
dataFile.close()
numberOfLinesInFile = lineNumber

#print the number of potential mistakes found
print ""
print "numberOfPotentialMistakes: %s" %numberOfPotentialMistakes
print "numberOfPotentialLanguageSwitch: %s" %numberOfPotentialLanguageSwitch
print "numberOfLinesInFile: %s" %numberOfLinesInFile
print "numberOfCheckedKeysInFile: %s" %numberOfCheckedKeysInFile
print ""


#print the execution time
st = time.time()-ts
print "total time:", st, "sec"

