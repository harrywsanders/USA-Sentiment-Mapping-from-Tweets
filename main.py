import pandas as pd

tweets = pd.read_csv('data sources!/bidentweets.csv', low_memory=False, lineterminator='\n')
tweets = tweets.head(50)

##Cleaning Tweet data.
from cleaning import *
tweets = clean(tweets)

##NLP Stage.
from nlp_apply import *
tweets = nlp_apply(tweets)

from reverse_geocoding import *
tweets = reverse_geo(tweets)

print(tweets)