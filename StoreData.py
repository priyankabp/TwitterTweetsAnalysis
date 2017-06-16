# importing required methods from tweepy liabrary
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import threading
import logging
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
import json

TWITTER_APP_KEY = 'eNMg4hN0KKQkAAXEQd2HtNkU5'
TWITTER_APP_SECRET = 'dVPBcXsNtj3G3jhXtI5krSZv1bDP9UKfVgVo8PPymGUeqcuOZ6'
TWITTER_KEY = '2314892245-oF7MigqkMVM3koh429nFNFiCVuIKKldxAMWAtC9'
TWITTER_SECRET = 'qmhY8X6owWu22ZiDHjkucXL8nkrRhlrgqg7arukW9xeGO'


class TweetsListener(StreamListener):

    def __init__(self, keywords):
        auth = OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
        auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
        self.__stream = Stream(auth, listener=self)
        self.__stream.filter(track=keywords, async=True)
        self.count = 0

    def on_data(self, data):
        try:
            tweet = data.split(',"text":"')[1].split('","source"')[0]
            createdAt = data.split('"created_at":"')[1].split('","id"')[0]
            print(createdAt + '::' + tweet)
            saveTweet = createdAt + ',' + tweet
            saveTwitterData = open('twitterStreamingData.csv', "a")
            saveTwitterData.write(saveTweet)
            saveTwitterData.write('\n')
            #self.count = self.count + 1
            saveTwitterData.close()
            return True
        except BaseException as e:
            print('Failed on data',str(e))
            time.sleep(5)

    def on_error(self, status):
        print(status)

    def on_disconnect(self, notice):
        self.__stream.disconnect()

    def disconnect(self):
        self.__stream.disconnect()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # filtering twitter stream to capture data by keywords: 'datascience','python','datamining'
    keywords = ['python', 'javascript', 'ruby']
    listener = TweetsListener(keywords)

    time.sleep(30)
    #print(listener.count)
    listener.disconnect()

    f = open("twitterStreamingData.csv")
    final = csv.writer(open('tweets.csv', 'w'))
    final.writerow(['created_at', 'text'])
    for row in csv.reader(f):
        print(row)
        final.writerow(row)

    tweets = pd.read_csv('tweets.csv',error_bad_lines=False)
    tweets.head()

    def get_tweets(row):
        languages = []
        text = row['text'].lower()
        if 'python' in text:
            languages.append('python')
        if 'ruby' in text:
            languages.append('ruby')
        if 'javascript' in text:
            languages.append('javascript')
        return ",".join(languages)

    tweets['language'] = tweets.apply(get_tweets,axis=1)

    counts = tweets['language'].value_counts()
    plt.bar(range(len(counts)),counts)
    plt.show()

    print(counts)

