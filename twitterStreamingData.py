#############################################################################################################
# Filename    : twitterStreamingData.py                                                                     #
# Description : This script is used for reading live tweets from twitter which have the specified keywords. #
#               The analysis of the tweets is done on the basis of the number of occurrences of the keyword #
#               and then the graph is drawn.                                                                #
#############################################################################################################

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import logging
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv

#twitter account details to access live data from twitter
TWITTER_APP_KEY = 'eNMg4hN0KKQkAAXEQd2HtNkU5'
TWITTER_APP_SECRET = 'dVPBcXsNtj3G3jhXtI5krSZv1bDP9UKfVgVo8PPymGUeqcuOZ6'
TWITTER_KEY = '2314892245-oF7MigqkMVM3koh429nFNFiCVuIKKldxAMWAtC9'
TWITTER_SECRET = 'qmhY8X6owWu22ZiDHjkucXL8nkrRhlrgqg7arukW9xeGO'

# twitter lisntener class which reads live data from twitter and stores it in .csv file.
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

    # filtering twitter stream to capture data by keywords: 'python','javascript','java'
    keywords = ['python', 'javascript', 'java']
    listener = TweetsListener(keywords)

    # reading twitter data for 60 seconds and then performing analysis on the stored data in file.
    time.sleep(60)
    listener.disconnect()

    # filtering the tweets and storing only 'created_at' and 'text' parameter of the tweet.
    f = open("twitterStreamingData.csv")
    final = csv.writer(open('tweets.csv', 'w'))
    final.writerow(['created_at', 'text'])
    for row in csv.reader(f):
        final.writerow(row)

    tweets = pd.read_csv('tweets.csv', error_bad_lines=False)
    tweets.head()

    # Counting the occurrence of each keyword in tweets.
    def get_tweets(row):
        languages = []
        if type(row['text']) is str:
            text = row['text'].lower()
            if 'python' in text:
                languages.append('py')
            if 'java' in text:
                languages.append('java')
            if 'javascript' in text:
                languages.append('js')
            return ",".join(languages)

    tweets['language'] = tweets.apply(get_tweets, axis=1)

    counts = tweets['language'].value_counts()
    del counts['']

    # plotting the bar graph with the analysis of data from the tweets.
    plt.bar(range(len(counts)),counts)
    plt.title('Programming languages mostly spoken about')
    plt.xlabel('Languages')
    plt.ylabel('# number of tweets')
    language = counts.keys()
    x_pos = np.arange(len(language))
    plt.xticks(x_pos,language)
    print(counts)
    plt.show()