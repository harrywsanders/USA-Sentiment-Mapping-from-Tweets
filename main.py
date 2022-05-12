import pandas as pd
import spacy
import re
import string
from textblob import TextBlob
from langdetect import detect
import geocoder
import geopandas
import seaborn
from math import e
import numpy as np
seaborn.set(style='ticks')



##Load init. data
nlp = spacy.load("en_core_web_sm")
Dtweets = pd.read_pickle('cleaned-county-tweets')
countyPolarity = pd.read_pickle('county-polarity-scores')
tweetsGDF = geopandas.GeoDataFrame(
    Dtweets, geometry=geopandas.points_from_xy(Dtweets.long, Dtweets.lat))




##Int. Parallel processing
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

##Defs. for cleaning
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
pattern = r'[' + string.punctuation + ']'
all_stopwords = nlp.Defaults.stop_words


##Functions
def remove_usernames_links(tweet):
    tweet = re.sub('@[^\s]+','',tweet)
    tweet = re.sub('http[^\s]+','',tweet)
    tweet = re.sub(pattern, '', tweet)
    return tweet
def polarity(x):
    res = TextBlob(x)
    return res.sentiment.polarity
def subjectivity(x):
    res = TextBlob(x)
    return res.sentiment.subjectivity
def subject(x):
    doc = nlp(x)
    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]
    return sub_toks
def isEnglish(x):
    try:
        x.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True
def lang(x):
    lang = detect(x)
    return lang
def county(x):
    g = geocoder.osm([x.lat, x.long], method='reverse').json
    if g:
        return g.get('county')
    else:
        return 'no county'
def pandas_entropy(column, base=None):
    vc = pd.Series(column).value_counts(normalize=True, sort=False)
    base = e if base is None else base
    return -(vc * np.log(vc) / np.log(base)).sum()


countylist = Dtweets.NAME.unique()

polarity = []
polarRange = []
countUnique = []
entropyList = []

Dtweets['pidentity'] = Dtweets['polarity'].astype(float).round(1)


for county in countylist:
    range  = Dtweets.loc[Dtweets['NAME'] == county, 'polarity'].quantile(0.99) - Dtweets.loc[Dtweets['NAME'] == county, 'polarity'].quantile(0.01)
    polarRange.append(range)

for county in countylist:
    unique = Dtweets.loc[Dtweets['NAME'] == county, 'user_id'].unique()
    count = len(unique)
    countUnique.append(count)

for county in countylist:
    entropy = pandas_entropy(Dtweets.loc[Dtweets['NAME'] == county, 'pidentity'])
    entropyList.append(entropy)


#for county in countylist:
    #score = Dtweets.loc[Dtweets['NAME'] == county, 'polarity'].sum() / len(Dtweets.loc[Dtweets['NAME'] == county, 'polarity'])
    #polarity.append(score)

##Treatment of Text
##Dtweets['cleaned'] = Dtweets['tweet'].parallel_apply(lambda x : remove_usernames_links(x))
#Dtweets['subjectivity'] = Dtweets['cleaned'].apply(lambda x: subjectivity(x))
#Dtweets['subjects'] = Dtweets['cleaned'].apply(lambda x : subject(x))
##Dtweets['county'] = Dtweets[['lat', 'long']].apply(county, axis=1)




##columnMOVE = Dtweets.pop("topSubj")
##Dtweets.insert(0, "topSubj", columnMOVE)

##counties = pd.DataFrame(list(zip(countylist, polarity)),
               ##columns =['Name', 'polarity'])


# Printing stuff?
cols = list(Dtweets.columns.values)
countyPolarity['range'] = list(polarRange)
countyPolarity['uniqueUsers'] = list(countUnique)
countyPolarity['entropy'] = list(entropyList)
countyPolarity = countyPolarity.round(3)
countyPolarity.sort_values('polarity', ascending = False, inplace = True)

print(countyPolarity)