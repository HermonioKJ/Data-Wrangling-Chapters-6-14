from tweepy.streaming import StreamingClient as StreamListener
from tweepy import OAuthHandler, Stream
import keys


class Listener(StreamListener):
    def on_data(self, data):
        print(data)
        return True


auth = OAuthHandler(keys.api_key(), keys.api_key_secret(
), access_token=keys.token_key(), access_token_secret=keys.token_key_secret())
stream = Stream(auth, Listener(bearer_token=keys.bearer_token(
)), access_token=keys.token_key(), access_token_secret=keys.token_key_secret())
stream.filter(track=['child labor'])
