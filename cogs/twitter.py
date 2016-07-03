__author__ = 'Atef'
import tweepy
from tweepy.auth import OAuthHandler
import asyncio
import datetime as dt


tweets_list=[]
new_tweet = False
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
channel_id='143010473342664704'
client_id = '749367812272062464'



class TwitterBot:
    """General commands."""

    def __init__(self, bot):
        self.bot = bot

    async def twitter_checker(self, client):
        """checks if new tweets have been tweeted."""
        # Sleep time in seconds.
        while self == self.bot.get_cog("TwitterBot"):
            CHECK_DELAY = 60
            base_url ='https://twitter.com/immersedCimp/status/'
            # Getting current time and converting to datetime object
            now = dt.datetime.utcnow()
            tweet = client.user_timeline(id = client_id, count = 1)[0]
            # tweet_time = dt.datetime.strptime(tweet.created_at, "%Y-%m-%d %H:%M:%S")
            tweet_time = tweet.created_at
            if dt.timedelta(seconds=0)<now-tweet_time<dt.timedelta(seconds=60):
                print('A NEW TWEET HAS BEEN DETECTED!')
                await self.bot.send_message(self.bot.get_channel(channel_id),base_url+str(tweet.id))
            await asyncio.sleep(CHECK_DELAY)


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

