# Import the necessary package to process data in JSON format
try:
    import JSON
except ImportError:
   import simplejson as json

# Import the necessary methods from 'twitter' library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import operator, argparse, json


def twitter_cred():
    """loads in keys and tokens"""

    # Variables that contains the user credentials to access Twitter API
    CONSUMER_KEY = 'BCvCGMyuiWR2fTOCrwNvbEDhC'
    CONSUMER_SECRET = 'Qpd3nG62cQkVvugcUsHA5Ft2nJli7b8vIWv6HMOlVhrCQQofAf'
    ACCESS_TOKEN_KEY = '1499467398-1pJ7cY3AW9GJF5Hqi4GxWGTpJROXldGObARSQuh'
    ACCESS_TOKEN_SECRET = 'RcaJ7j4g5ZrhpBcxPX0osOIXDBLrMAYiAwMKi1DoXNjTE'

    oauth = OAuth(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    return oauth


def twitter_scrape(search):

    # Initiate the connection to Twitter Streaming API
    twitter = Twitter(auth=twitter_cred())

    # Get a sample of the public data following through Twitter
    # iterator = twitter_stream.statuses.filter(track = '$' + search[0], language = 'en')
    # iterator = twitter_stream.statuses.sample(language = 'en')

    # Twitter Search API
    iterator = twitter.search.tweets(q=search, result_type='recent', lang='en', count=10)
    package_tweets(iterator)


def twitter_trend():

    ## Initiate the connection to Twitter API
    twitter = Twitter(auth=twitter_cred())

    # Get all the locations where Twitter provides trends service
    sfo_trends = twitter.trends.place(_id=1)  # 2487956)
    print(json.dumps(sfo_trends, indent=4))


def package_tweets(iterator):
    hashtags = []
    # Print each tweet in the stream to the screen
    # Here we set it to stop after getting n tweets.
    # You don't have to set it to stop, but can continue running
    # the Twitter API to collect data for days or even longer.

    for tweet in iterator['statuses']:

        try:
            # Read in one line of the file, convert it into a json object
            if 'text' in tweet:  # only messages contains 'text' field is a tweet
                print('ID:\t\t', tweet['id'])  # This is the tweet's id
                print('Created at:\t',tweet['created_at'])  # when the tweet posted
                response = tweet['text'] + ' ' + tweet['user']['location'] + '\n' # content of the tweet
                obj.write(response)
                print('User ID:\t',tweet['user']['id'])  # id of the user who posted the tweet
                print('User Name:\t',tweet['user']['name'])  # name of the user, e.g. "Wei Xu"
                print('Screen Name:\t',tweet['user']['screen_name'])  # name of the user account, e.g. "cocoweixu"
                print('Tweet:\t\t', tweet['text'])
                print('Location:\t',tweet['user']['location'])
                for hashtag in tweet['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                print("**********************************************")
        except Exception as e:
            # read in a line is not in JSON format (sometimes error occured)
            print(e)
            continue

        # The command below will do pretty printing for JSON data, try it out
        # print json.dumps(tweet, indent=4)

    parse_tweet(hashtags)


def parse_tweet(hashtags):
    topHashtag = {}
    for n in hashtags:
        if n in topHashtag:
            topHashtag[n] += 1
        topHashtag[n] = topHashtag.get(n, 1)

    t = sorted(topHashtag.items(), key = operator.itemgetter(1), reverse = True)
    for key, value in t[:10]:
        print(key, value)
    print(topHashtag)


def location_lookup(location):
    woeid = json.load(open('woeid.json'))
    woeid['locations'][0]['name']
	
def main():
    parser = argparse.ArgumentParser(description = "Twitter Tweet Scraper based on search terms")
    parser.add_argument('-s', '--search', type=str, nargs='+', help='enter terms to be search on twitter')
    parser.add_argument('-t', '--trend', type=str, nargs="+", help='will display the trending tweets')
    args = parser.parse_args()
    if args.search:
        twitter_scrape(args.search)
    else:
        location_lookup(args.search)
        #twitter_trend()


if __name__ == '__main__':
    obj = open('data.txt', 'w')
    main()
    obj.close
