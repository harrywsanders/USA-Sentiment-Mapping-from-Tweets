from langdetect import detect
from pandarallel import pandarallel
import re

##Initializes Parallel Processing
pandarallel.initialize(progress_bar=False)

#Removes errant usernames or links
def remove_usernames_links(tweet):
    tweet = re.sub('@[^\s]+','',tweet)
    tweet = re.sub('http[^\s]+','',tweet)
    tweet = re.sub('#', '', tweet)
    return tweet

#Checks if the Tweet characters are English.
def isEnglish(x):
    try:
        x.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return 'False'
    else:
        return 'True'

##Checks if the Tweet is in English– if we don't check for English characters, this will throw an error.
def lang(x):
    lang = detect(x)
    return lang


##Cleaning function
def clean(df):
    df['cleaned'] = df['tweet'].parallel_apply(lambda x : remove_usernames_links(x))
    df['isEnglish'] = df['tweet'].parallel_apply(lambda x : isEnglish(x))
    df.drop(df.index[df['isEnglish'] == 'False'], axis=0, inplace=True)
    df.drop('isEnglish', axis = 1, inplace=True)
    df['lang'] = df['tweet'].apply(lambda x : lang(x))
    df = df.drop(df[df.lang != 'en'].index)
    return df