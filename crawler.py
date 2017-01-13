import requests
import json
import boto3
from botocore.client import Config

params = {
    "q": "SELECT * FROM html WHERE url='https://unsplash.com/new' and xpath='//*[@id=\"gridSingle\"]/div'",
    "format": "json",
    "diagnostics": True,
    "callback": ""
}

r = requests.get("https://query.yahooapis.com/v1/public/yql", params=params)
results = json.loads(r.text)

start = 'background-image:url("'
end = '")'

wallpapers = []

for item in results['query']['results']['div']:
    s = item['a']['style']
    wallpapers.append((s.split(start))[1].split(end)[0])

s3 = boto3.resource(
    's3',
    aws_access_key_id='', # TO be replaced with your AWS ACCESS KEY ID
    aws_secret_access_key='', # TO be replaced with your AWS SECRET KEY 
    config=Config(signature_version='s3v4')
)
s3.Bucket('unsplash-wallpapers').put_object(Key='wallpapers.json', Body=json.dumps(wallpapers))
