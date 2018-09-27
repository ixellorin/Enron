import pandas as pd
import sys
import re
import matplotlib.pyplot as plt

fileNumber = 1

emails = pd.read_csv('email_set_%d.csv' % fileNumber)
weOcurrance = float(0)
iOcurrance = float(0)

weTrend = []
iTrend = []
fileCount = []

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
            re.sub("[^\w\']", " ",  message)
            weCount = 0
            iCount = 0
            weCount += message.lower().count(' we ') + message.lower().count(' us ') + message.lower().count(' ourselves ')
            iCount += message.lower().count(' i ') + message.lower().count(' me ') + message.lower().count(' myself ')
        print ('We: %d, I: %d' % (weCount, iCount))
        if weCount > 0:
            weOcurrance += 1

        if iCount > 0:
            iOcurrance += 1

        weTrend.append(weOcurrance / (fileNumber * 10000))
        iTrend.append(iOcurrance / (fileNumber * 10000))
        fileCount.append(fileNumber)

        fileNumber += 1


print ('Group: %d, Individual: %d' % (weCount, iCount))
#
plt.plot(fileCount, weTrend, 'r-o', label='Group')
plt.plot(fileCount, iTrend, 'b-o', label='Individual')
plt.ylabel('\% of Emails Containing Expressions')
plt.xlabel('Emails (x10k)')
plt.legend(loc='upper left')
plt.title('Frequency of Expressions as Groups vs. Individuals: \n Language such as \'We\', \'Us\', vs \'I\', \'Myself\'')
plt.savefig('i-we_frequency_comparison.png')
plt.show()
