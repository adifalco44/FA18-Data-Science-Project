import time, tweepy, os, sys
from textblob import TextBlob
import json


### DICT MAPS NON_CONT TWEETS TO STOCK DATA ###
map_dict = {1:'2018-10-05',2:'2018-10-08',3:'2018-10-08',4:'2018-10-09',5:'2018-10-10',6:'2018-10-11',\
            7:'2018-10-12',8:'2018-10-15',9:'2018-10-15',10:'2018-10-22',11:'2018-10-22',12:'2018-10-22',13:'2018-10-22',\
            14:'2018-10-23',15:'2018-10-25',16:'2018-10-29',17:'2018-10-30',18:'2018-11-01',19:'2018-11-02',20:'2018-11-05',\
            21:'2018-11-06',22:'2018-11-07',23:'2018-11-08'}


stocks = {}
with open('stock_info.csv','r+') as f:
    text = f.readlines()
    for line in text:
        split = line.split(',')
        try:
            stocks[split[0]].append(split[1:])
        except:
            stocks[split[0]] = [split[1:]]


def touch(path):
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    '''with open(path,'w+'):

        os.utime(path,None)'''

if __name__ == "__main__":
    line = []
    with open('companies.csv',"r+") as f:
        lines = f.readlines()
        f.close()
    titles = ["name","ticker","ceo"]
    for DAY in range(4,26):
        date = map_dict[DAY-3]
        for line in lines:
            query = line.split(',')
            company = query[1]
            print ("COMPANY: ", (company))

            for i in range(1,len(query)-2):
                titles.append("key{0}".format(i))
            n = 0
            sum = 0
            total_followers = 0.0000
            stock_data_point = []
            for line in stocks[company]:
                if str(line[2])==str(date):
                    stock_data_point = line

            change = 0.99
            open_ =  0.01
            writeData = []
            for i in range(0,len(query)-1):
                print ("TYPE: ",type(titles[i]))
                readPath = "data/tweets/d{}/{}-{}.txt".format(str(DAY),query[0],titles[i])
                print(readPath)
                data = []
                print (type(readPath))
                with open(readPath,'r') as fp:
                    data = fp.readlines()

                n += len(data)
                for twt in data:
                    try:
                        tweet = json.loads(twt)
                        total_followers+=int(tweet['user']['followers_count'])
                    except UnicodeEncodeError:
                        continue
                for twt in data:
                    try:
                        tweet = json.loads(twt)
                        testimonial = TextBlob(tweet['text'])
                        polarity, confidence = testimonial.sentiment
                        value = polarity*confidence*float(float(tweet['user']['followers_count'])/float(total_followers))*float(change/open_)
                        writeData.append('{0},{1},{2},{3}\n'.format(tweet['user']['followers_count'],polarity,confidence,value))
                    except UnicodeEncodeError:
                        continue
            writePath ="data/clean/d{0}/{1}-cleaned.txt".format(DAY-3,query[0])
            exists = os.path.isfile(writePath)
            if (exists==False):
                touch(writePath)
            writeFp = open(writePath,'a')
            for data in writeData:
                writeFp.write(data)
            writeFp.close()