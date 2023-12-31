import tweepy
import pandas as pd
from kafka import KafkaProducer
from json import loads, dumps
from time import sleep, strftime

with open('twitterAPISulisB.json') as myapi:
    apiku=loads(myapi.read())
CONSUMER_KEY=apiku['consumer_key']
CONSUMER_SECRET=apiku['consumer_secret']
ACCESS_TOKEN=apiku['access_token']
ACCESS_TOKEN_SECRET=apiku['access_token_secret']
auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

producer=KafkaProducer(bootstrap_servers=['localhost:9092'],
        value_serializer=lambda K:dumps(K).encode('utf-8'))
topic="projek5"

# scrape 1 tweet setiap 6 detik, agar tidak melampaui rate limit.
# jika tweet yang discrape masih sama seperti sebelumnya,
# maka tidak dikirim ke kafka topic
tweetmp={'id':0}
while(True):
    api=tweepy.API(auth)
    cursor=tweepy.Cursor(api.search_tweets,q="#covid19",
            tweet_mode='extended').items(1)
    for tweet in cursor:
        if tweet.id_str==tweetmp['id']:
            sleep(6)
            continue
        else:
            tweet_data={
                'id':tweet.id_str,
                'user_name':tweet.user.screen_name,
                'created_at':tweet.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'text':tweet.full_text,
                'language':tweet.lang,
                'user_id':tweet.user.id_str,
                'user_location':tweet.user.location,
                }
            producer.send(topic, tweet_data)
            tweetmp=tweet_data
            sleep(6)