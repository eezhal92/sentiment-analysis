import os
import sys
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from textblob import TextBlob
from dotenv import load_dotenv
import json
import re

load_dotenv()

def create_twitter_auth():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")

    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return auth

class TweetAnalyzer():
    def clean_tweet(self, tweet_text):
        return " ".join(re.sub("(@[a-zA-Z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet_text).split())

    def analyse(self, tweet_text):
        analysis = TextBlob(self.clean_tweet(tweet_text))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity < 0:
            return -1

        return 0

class TwitterStreamer():
    def stream_tweets(self, topics):
        listener = TwitterStreamListener()
        auth = create_twitter_auth()
        stream = Stream(auth, listener)
        stream.filter(track=topics)

class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        parsed_data = dict(json.loads(data))
        print(parsed_data['text'])
        analyzer = TweetAnalyzer()
        analysis = analyzer.analyse(parsed_data['text'])
        print(analysis)

        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    try:
        twitter_streamer = TwitterStreamer()
        twitter_streamer.stream_tweets(topics=["waste problem", "climate change", "climate crisis"])
    except KeyboardInterrupt:
        print('Interrupted. Program exited')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    