__author__ = 'Atef'
import tweepy
from tweepy.auth import OAuthHandler
import asyncio
import datetime as dt
import logging
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=os.path.join(os.environ['robocimp_home'], "logs/robocimp.log"),
                    filemode='w')

tweets_list = []


class StdOutListener(tweepy.StreamListener):
    ''' Handles data received from the stream. '''

    def on_status(self, status):
        # Prints the text of the tweet
        # There are many options in the status object,
        # hashtags can be very easily accessed.
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening

    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening


consumer_key = "rpN9592M5h1urByjrYwdQAqCK"
consumer_secret = "BpAJA6e5rUAD59marhtqY51e4l9Nn5rE0bwTOtmXWhGG4SkZOv"
access_token = '238750569-00GxH2Ic7d1uToR2DU4blu1RpWwnZqi6C2MmNolc'
access_token_secret = 'JHADa4gAyD1oOugbay0xIg48nNsT8oXP1hrsefUHI2HQH'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

test_channel_id = []
channel_id = ['143010473342664704', '143010743342727168']

client_id = ['1955349374', '749367812272062464']
base_url = 'https://twitter.com/immersedCimp/status/'
test_base_url = 'https://twitter.com/MaximuYondaimus/status'


class TwitterBot:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    async def twitter_checker(self, client):
        """checks if new tweets have been tweeted."""
        # Sleep time in seconds.
        while self == self.bot.get_cog("TwitterBot"):
            delay = 60
            # Getting current time and converting to datetime object
            now = dt.datetime.utcnow()
            logging.debug('TwitterBot is up checking for tweets...' + str(now))
            for client in client_id:
                tweet = client.user_timeline(id=client, count=1)[0]
                logging.debug('latest tweet was tweeted in: ' + str(tweet.created_at))
                tweet_time = tweet.created_at
                if dt.timedelta(seconds=0) < now-tweet_time < dt.timedelta(seconds=delay):
                    logging.debug('A NEW TWEET HAS BEEN DETECTED...')
                    logging.debug('tweet id is: ' + str(tweet.id))
                    logging.debug('tweet time is: ' + str(tweet.created_at))
                    for ch in channel_id:
                        logging.debug('Writing in discord channel' + str(ch))
                        await self.bot.send_message(self.bot.get_channel(ch), base_url+str(tweet.id))
                        logging.debug('Successfully written on discord !')
            await asyncio.sleep(delay)


def setup(bot):
    t = TwitterBot(bot)
    consumer_key = "rpN9592M5h1urByjrYwdQAqCK"
    consumer_secret = "BpAJA6e5rUAD59marhtqY51e4l9Nn5rE0bwTOtmXWhGG4SkZOv"
    access_token = '238750569-00GxH2Ic7d1uToR2DU4blu1RpWwnZqi6C2MmNolc'
    access_token_secret = 'JHADa4gAyD1oOugbay0xIg48nNsT8oXP1hrsefUHI2HQH'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    client = tweepy.API(auth)
    twitter_loop = asyncio.get_event_loop()
    twitter_loop.create_task(t.twitter_checker(client))
    bot.add_cog(t)

