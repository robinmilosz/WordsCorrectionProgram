#!/usr/bin/python

'''
A small personal project to correct orthography in LaTeX and html files
Author: Robin Milosz

it checks:
french and english orthography spelling
french plural with determiners
other french mistakes (tout les, elision, unstackable determiners)

optionnal:
french/english language switch checking
french "a" and "'a" (accent) listing
repetition of words checking


to run:
python words_correction_program.py [the path of your target file "/u/username/Documents/example.tex"]
'''

#imports
import time
import sys
import math

#start counting the time
nm = 0
ts = time.time()

class queueOfKeys:
	def __init__(self,desiredLength):
		self.length = desiredLength
		self.queue = [""] * desiredLength
	def addKey(self,key):
		for i in reversed(range(1,self.length)):
			self.queue[i]=self.queue[i-1]
		self.queue[0]=key
	def verifyRepetition(self):
		maxSizeOfRepetition = int(math.floor(self.length/2))
		for j in range(1,maxSizeOfRepetition+1):
			repetition = True
			for i in range(j):
				if (self.queue[i] != self.queue[i+j]):
					repetition = False
			if (repetition):
				return j
		return 0
				


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


#list of parameters to
#for plurality checking
lastKeyFrPlural = False
#from http://test.alloprof.qc.ca/francais/le-systeme-des-accords/le-pluriel-des-determinants.aspx
pluralFrDeterminers = ["les","des","mes","tes","ses","nos","vos","leurs","ces","quels","quelles","leurs","plusieurs","deux","trois","quatres","cinq"]
pluralFrExceptions = ["top","arn","deux","trois","quatre","cinq","ou"]
simpleFrDeterminersAndOthers = ["la","le","de","se","ce","si"]
frVowelsPlusH= ["a","e","i","o","u","y","\xc3\xa9"]#I took out the H because there is two kinds of H in french language that obey different rules
unstackableFrDeterminers = ["les","des","mes","tes","ses","nos","vos","ces","le","la","ce","mon","ma","ton","ta","son","sa","l"]

#for language variation checking
lastKeyLanguageIs = "Empty" # "French", "English", "Extra", "Error", "Empty"
languageVariationChecking = True #warning it's a first version, a little bit inneficient due to some names inserted in the dictionnaries

#other
lastKey = ""

#a checking switch
aChecking = False

#repetition checking switch
repetitionChecking = True
lastKeys = queueOfKeys(10)

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
	linePure2 = linePure.rstrip().strip().replace('\"',' ').replace('?','.').replace(':',' ').replace('!','.').replace('`',' ')
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
                            
                    if (lastKey in unstackableFrDeterminers):#french error
                        if (key in unstackableFrDeterminers):
                            numberOfPotentialMistakes += 1
                            print "%s %s (%s), unstackable?" % (lastKey, key, lineNumber) #print the potential mistake

                    if (lastKey == "tout"):#commun french error: "tout les" -> "tous les"
                        if (key in pluralFrDeterminers):
                            numberOfPotentialMistakes += 1
                            print "%s %s (%s), tous?" % (lastKey, key, lineNumber) #print the potential mistake
                            
                    if (repetitionChecking):#repetition check: "I was there there yesterday"
                        #if (lastKey == key ):
                        #    numberOfPotentialMistakes += 1
                        #    print "%s %s (%s), repetition?" % (lastKey,key,lineNumber) #print the potential mistake
                        lastKeys.addKey(key)
                        #print lastKeys.queue
                        #print key
                        repetitionValue = lastKeys.verifyRepetition()
                        if (repetitionValue != 0):
							repetitionSequence = ""
							for i in range(repetitionValue*2):
								repetitionSequence = lastKeys.queue[i] + " " + repetitionSequence
							print "%s (%s), repetition?" % (repetitionSequence,lineNumber) #print the potential mistake
							#make exception for "nous nous" and "vous vous"?
							
                    if (lastKey in simpleFrDeterminersAndOthers):#french elision: "la eau" -> "l'eau", "de arbre" -> "d'arbre", "ce est" -> "c'est"
                        if (key[0] in frVowelsPlusH):
							if (key == "ou"):
								pass
							else
								numberOfPotentialMistakes += 1
								print "%s %s (%s), l'/d'/s'/c' %s ?" % (lastKey, key, lineNumber, key) #print the potential mistake
                        elif (len(key)>= 2):
							if (key[0] == '\xc3' and key[1] == '\xa9'):
								numberOfPotentialMistakes += 1
								print "%s %s (%s), l'/d'/s'/c' %s ?" % (lastKey, key, lineNumber, key) #print the potential mistake
					if (lastKey == "si"):#french elision: "si il" -> "s'il"
						if (key == "il" or key == "ils"):
							numberOfPotentialMistakes += 1
							print "%s %s (%s), s' %s ?" % (lastKey, key, lineNumber, key) #print the potential mistake
							
                    if (aChecking):
                        if (lastKey == "a" or lastKey == aAccent):
                            print "%s %s (%s), aaa?" % (lastKey,key,lineNumber) #print the potential mistake
                        if (key == "a" or key == aAccent):
                            print "%s %s (%s), aaa?" % (lastKey,key,lineNumber) #print the potential mistake
                            
                    
						
								
                    if key in pluralFrDeterminers:#checking if its a plural determiner
						lastKeyFrPlural = True
                    else:
						lastKeyFrPlural = False


                    lastKey = key
                else:
                    lastKeyLanguageIs = "Empty"
                    lastKeyFrPlural = False
                    lastKey = ""
                    if (repetitionChecking):
                        lastKeys.addKey(key)


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

