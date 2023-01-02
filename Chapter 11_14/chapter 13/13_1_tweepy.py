import tweepy
import keys
import json
import dataset


def store_tweet(item):
    db = dataset.connect('sqlite:///data_wrangling.db')
    table = db['tweets']
    item_json = item._json.copy()
    for k, v in item_json.items():
        if isinstance(v, dict):
            item_json[k] = str(v)
    table.insert(item_json)


auth = tweepy.OAuthHandler(keys.api_key(), keys.api_key_secret())
auth.set_access_token(keys.token_key(), keys.token_key_secret())

api = tweepy.API(auth)

query = '#childlabor'
cursor = tweepy.Cursor(api.search_tweets, q=query, lang='en')

for page in cursor.pages():
    tweets = []
    for item in page:
        tweets.append(item._json)

with open('data/hashchildlabor.json', 'w', encoding='utf-8') as outfile:
    json.dump(tweets, outfile)
