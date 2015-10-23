'''
Created on Sep 21, 2015

@author: Kenny
'''
##
from TwitterSearch import *
import requests
import re
import matplotlib.pyplot as plt
##

## fetch tweets using given query 
tweet_query = "job hunt" # search query
language = "en" # search tweets in specific language only
max_count = 200; # maximum number or tweets to fetch

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([tweet_query]) # query word(s)
    tso.set_language(language) # Set language
    tso.set_include_entities(False) # do not include entity information
    
    # create a TwitterSearch object
    ts = TwitterSearch(
        consumer_key = '???',
        consumer_secret = '???',
        access_token = '???',
        access_token_secret = '???'
     )
    
    ## tweets content cleaning
    words = ""
    tweet_texts = []
    tweet_opinions = []
    i = 0
    for tweet in ts.search_tweets_iterable(tso):
        t_text = str((tweet['text']).encode('utf-8'))
        
        ## clean up the RT, tags and urls in tweet text
        t_text.replace("RT", "")
        t_text = re.sub(r"(?:\@|https?\://)\S+", "", t_text)
        t_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", t_text).split())
        t_text = " ".join([word for word in t_text.split() if word != 'RT'])
        #print (t_text)
        tweet_texts.append(t_text)
        words += t_text
        
        ## send http POST for sentiment analysis feedback 
        payload = {'text': t_text}
        r = requests.post("http://text-processing.com/api/sentiment/", data=payload)
        p = r.json()
        
        ## print the result: negative or positive
        print(p["label"])
        tweet_opinions.append(p["label"])
        i += 1
        if i > max_count :
            break;
    
except TwitterSearchException as e: # if error happens
    print(e)

## plot as a pie chart
# Data to plot
pos_count = 0
neg_count = 0
neut_count = 0
    
for opinion in tweet_opinions :
    if opinion == "pos" :
        pos_count += 1
    if opinion == "neg" :
        neg_count += 1
    if opinion ==  "neutral" :
        neut_count += 1

labels = 'Positive', 'Neutral', 'Negative'
sizes = [pos_count, neut_count, neg_count]
colors = ['blue', 'yellowgreen', 'lightcoral'] 
explode = (0.1, 0, 0)  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Tweeter Opinions about: ' + tweet_query, bbox = {'facecolor': '0.8', 'pad': 5}) 
plt.axis('equal')
plt.savefig('./piechart.png', dpi=300)
plt.show()

