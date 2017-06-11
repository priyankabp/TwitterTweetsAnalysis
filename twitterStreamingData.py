#importing required methods from tweepy liabrary
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import threading

#Variables that contain the user credentials to access TwitterAPI
TWITTER_APP_KEY = 'eNMg4hN0KKQkAAXEQd2HtNkU5'
TWITTER_APP_SECRET = 'dVPBcXsNtj3G3jhXtI5krSZv1bDP9UKfVgVo8PPymGUeqcuOZ6'
TWITTER_KEY = '2314892245-oF7MigqkMVM3koh429nFNFiCVuIKKldxAMWAtC9'
TWITTER_SECRET = 'qmhY8X6owWu22ZiDHjkucXL8nkrRhlrgqg7arukW9xeGO'

class TweetsListener(StreamListener):

    def on_data(self, data):
            print(data)
            return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # twitter authentication and connection to twitter streaming api
    lis = TweetsListener()
    auth = OAuthHandler(TWITTER_APP_KEY,TWITTER_APP_SECRET)
    auth.set_access_token(TWITTER_KEY,TWITTER_SECRET)
    stream = Stream(auth,lis)

    #filtering twitter stream to capture data by keywords: 'datascience','python','datamining'
    stream.filter(track=['javascript','python','ruby'])
