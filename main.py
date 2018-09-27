import pandas as pd
import sys
import re
import pprint
import math
import csv

fileNumber = 1
messageNumber = 1
documentList = []
termFrequencyList = []
tfidfList = []

def parse_raw_message(raw_message):
    lines = raw_message.split('\n')
    email = {}
    message = ''
    keys_to_extract = ['from', 'to', 'subject']
    for line in lines:
        if ':' not in line:
            message += line.strip()
            email['body'] = message.lower()
        else:
            pairs = line.split(':', 1)
            key = pairs[0].lower()
            val = pairs[1].strip()
            if key in keys_to_extract:
                email[key] = val
    return email

def getAllWords(message) :
    myStr = message
    wordList = re.sub("[^\w\']", " ",  myStr).split()
    return wordList

def countAllWordsInMessage(wordList, message) :
    wordCountDict = {}
    for word in wordList :
        wordCountDict[word] = message.lower().count(word)
    return wordCountDict

def computeTermFrequency(wordCountDict, message) :
    tfDict = {}
    totalWords = 0

    for word, count in wordCountDict.items() :
        totalWords += count

    for word, count in wordCountDict.items() :
        tfDict[word] = count/float(totalWords)

    return tfDict

#documentList is a list of maps (word : count) for each document
def computeInverseDocumentFrequency(documentList, tfDict) :
    idfDict = {}
    N = len(documentList)

    idfDict = dict.fromkeys(tfDict.keys(), 0)

    for word in tfDict.keys():
            for document in documentList:
                if word in document:
                    if document.get(word) > 0:
                        idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))

    return idfDict

def computeTFIDF(tfDict, idfDict) :
    pprint.pprint('Finally, computing TF-IDF...')
    tfidfDict ={}
    for word, val in tfDict.items():
        tfidfDict[word] = val * idfDict.get(word)

    return  tfidfDict

while fileNumber < 3:

    emails = pd.read_csv('email_set_%d.csv' % fileNumber)
    for index, row in emails.iterrows():
        pprint.pprint('Computing TF of message %d...' % messageNumber)
        rawMessage = row['message']
        emailMap = parse_raw_message(rawMessage)
        message = emailMap.get('body')
        wordList = getAllWords(message)
        wordCountDict = countAllWordsInMessage(wordList, message)
        tfDict = computeTermFrequency(wordCountDict, message)
        termFrequencyList.append(tfDict.copy())
        documentList.append(wordCountDict.copy())
        messageNumber += 1

    print(len(documentList))

    fileNumber +=1

pprint.pprint(len(documentList))

messageNumber = 1

for tfDict in termFrequencyList:
    pprint.pprint('Computing IDF of terms from message %d ...' % messageNumber)
    idfDict = computeInverseDocumentFrequency(documentList, tfDict)
    pprint.pprint('Computing TF-IDF of terms from message %d ...' % messageNumber)
    tfidfList.append(computeTFIDF(tfDict, idfDict).copy())
    messageNumber += 1

pprint.pprint("Done!")
