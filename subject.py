import pandas as pd
import sys
import re
import pprint
import math
import csv
import matplotlib.pyplot as plt

fileNumber = 1
fileCount = []

emptyCount = 0
emptyTrend = []

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

while fileNumber < 51 :
        emails = pd.read_csv('email_set_%d.csv' % fileNumber)
        for index, row in emails.iterrows() :
            email = parse_raw_message(row['message'])
            subject = email.get('subject')
            re.sub("[^\w\']", " ",  subject)
            strippedSubject = subject.strip();
            if len(subject) == 0 or subject.isspace() or strippedSubject.lower() == 're:' :
                emptyCount += 1

        print ('Empty Count: %d' % emptyCount)
        emptyTrend.append(emptyCount)
        fileCount.append(fileNumber)

        fileNumber += 1


plt.plot(fileCount, emptyTrend, '-b', label='Group')
plt.ylabel('Number of Empty Subject Lines')
plt.xlabel('Emails (x10k)')
plt.legend(loc='upper left')
plt.title('Empty Subject Lines in Emails')
ax = plt.gca()
plt.savefig('empty_subject.png')
plt.show()
