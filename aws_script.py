import os
import requests 
import json 
import tweepy
import wget

def lambda_handler(event, context):
    
    wordurl = "https://wordsapiv1.p.rapidapi.com/words/" 

    headers = { "X-RapidAPI-Key" : os.environ["rapidapi_key"],
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
    
    metobjecturl = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{metobjectids[0]}"
    r = requests.get ( metobjecturl )
    image = wget.download(r.json()["primaryImage"], out="/tmp/temp_image.jpg")
    
    client = tweepy.Client(consumer_key=os.environ["consumer_key"], consumer_secret=os.environ["consumer_secret"], access_token=os.environ["access_token"], access_token_secret=os.environ["access_token_secret"]
    )
    auth = tweepy.OAuthHandler(os.environ["consumer_key"], os.environ["consumer_secret"])
    auth.set_access_token(os.environ["access_token"], os.environ["access_token_secret"])
    api = tweepy.API(auth)
    
    image_response = api.media_upload(image)
    response = client.create_tweet(text=f"{randomword}", media_ids=[image_response.media_id_string])
    
    return 200