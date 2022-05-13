from textblob import TextBlob
import spacy
nlp = spacy.load("en_core_web_sm")


##Labels we WANT to appear in analyses– i.e., excluding money and percentages.
labelList = ['ORG', 'PERSON','GPE']

##Polarity of a Tweet
def polarity(x):
    res = TextBlob(x)
    return res.sentiment.polarity
##Subjectivity Measure
def subjectivity(x):
    res = TextBlob(x)
    return res.sentiment.subjectivity
##What people or Geopolitical entities are being talked about?
def subject(x):
    doc = nlp(x)
    for ent in doc.ents:
        return(ent.text)
##SPACY specific label of the entity.
def label(x):
    doc = nlp(x)
    for ent in doc.ents:
        return(ent.label_)

##Applies all our analyses, and cuts out any rows we aren't interested in.
def nlp_apply(df):
    df['polarity'] = df['cleaned'].apply(lambda x: polarity(x))
    df['subjectivity'] = df['cleaned'].apply(lambda x: subjectivity(x))
    df['subject'] = df['cleaned'].apply(lambda x: subject(x))
    df['label'] = df['cleaned'].apply(lambda x: label(x))
    df = df[df['label'].isin(labelList)]
    return df



