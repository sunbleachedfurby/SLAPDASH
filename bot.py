import requests 
import json 
from dotenv import dotenv_values

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

metobjecturl = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{metobjectids[0]}"
r = requests.get ( metobjecturl )
print ( r.text )
