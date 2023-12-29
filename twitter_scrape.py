import tweepy

# Replace with your own Twitter API credentials
consumer_key = 'TEsiWEIdS5x9rdQGq51VXDCxt'
consumer_secret = 'ImcW9oWZmOmkiLwvnGk5utcXKK2Gojs6gVjA6Eu50b6EXtcvXC'
access_token = '1214570308369186816-L87aeqNHfTGVQtCzskvvd843OYVeD9'
access_token_secret = 'aeZ84XdjwIPios0BhkzTWH8bkQBgjZJOAHBk6eKZgZzIV'

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)

#Instantiate the tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)

# Screen name of the Twitter user you want to scrape
screen_name = input()

# Get user profile information
user = api.get_user(screen_name=screen_name)    
print("User Profile Information:")
print("Name:", user.name)
print("Username:", user.screen_name)
print("Description:", user.description)
print("Followers Count:", user.followers_count)
print("Friends Count:", user.friends_count)
print("Tweets Count:", user.statuses_count)