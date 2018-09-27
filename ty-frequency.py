import pandas as pd
import sys
import re
import matplotlib.pyplot as plt

fileNumber = 1

emails = pd.read_csv('email_set_%d.csv' % fileNumber)
count = 0
fileCount = []
freq = []

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
            message = email.get('body')
            occurance = 0
            re.sub("[^\w\']", " ",  message)
            occurance += message.lower().count('thanks') + message.lower().count('thank you') + message.lower().count('no, but thanks')
            occurance -= message.lower().count('no thanks') + message.lower().count('no thank you') + message.lower().count('no, thanks') + message.lower().count('no, thank you') + message.lower().count('no, but thank you')
            occurance += message.lower().count('appreciate') - message.lower().count('don\'t appreciate')
            occurance += message.lower().count('grateful')

            if occurance > 0:
                count += 1

        print count
        freq.append(float(count)/(fileNumber * 10000))
        fileCount.append(fileNumber)
        fileNumber += 1
print count

plt.plot(fileCount, freq, '-o')
plt.ylabel('Gratitude Frequency')
plt.xlabel('Emails (x10k)')
plt.title('Frequency of Emails Containing Expressions of Gratitude \n Words such as \'Thanks\', \'Grateful\', \'Appreciate\', etc.')
ax = plt.gca()
plt.savefig('gratitude_frequency.png')
plt.show()
