import requests 
import json 
import tweepy
import wget
import ssl
from dotenv import dotenv_values

ssl._create_default_https_context=ssl._create_unverified_context

secrets = dotenv_values(".env")

wordurl = "https://wordsapiv1.p.rapidapi.com/words/" 

headers = { "X-RapidAPI-Key" : secrets["rapidapi_key"],
"X-RapidAPI-Host" : "wordsapiv1.p.rapidapi.com" 
} 
querystring = { "random" : "true" } 

r = requests.get ( wordurl, headers = headers, params = querystring ) 
worddata = json.loads ( r.text )
print ( worddata [ "word" ] )

randomword = ( worddata [ "word" ] )

metsearchurl = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={randomword}"
print(metsearchurl)
r = requests.get ( metsearchurl )
metdata = json.loads ( r.text )
metobjectids = ( metdata [ "objectIDs" ] )
print(metobjectids)

metobjecturl = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/544720"
r = requests.get ( metobjecturl )
image = wget.download(r.json()["primaryImage"], out="/tmp/temp_image.jpg")

client = tweepy.Client(consumer_key=secrets["consumer_key"], consumer_secret=secrets["consumer_secret"], access_token=secrets["access_token"], access_token_secret=secrets["access_token_secret"]
)
auth = tweepy.OAuthHandler(secrets["consumer_key"], secrets["consumer_secret"])
auth.set_access_token(secrets["access_token"], secrets["access_token_secret"])
api = tweepy.API(auth)

image_response = api.media_upload(image)
response = client.create_tweet(text=f"{randomword}", media_ids=[image_response.media_id_string])