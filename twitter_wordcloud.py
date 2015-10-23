'''
Created on Sep 21, 2015

@author: Kenny
'''
##
from TwitterSearch import *
import requests
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
##

## fetch tweets using given query 
tweet_query = "job hunt" # search query
language = "en" # search tweets in specific language only
max_count = 20; # maximum number or tweets to fetch

try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords([tweet_query]) # query word(s)
    tso.set_language(language) # Set language
    tso.set_include_entities(False) # do not include entity information
    
    # create a TwitterSearch object
    ts = TwitterSearch(
        consumer_key = 'LBLIPNZjFEtMGYykYZGh4A7cl',
        consumer_secret = '5o8MyXViL1Xxrk9c8Krj9P1vtS6DxVKCp7YtpaCLOUo7Iq5cYG',
        access_token = '357225157-CDBYSd1OL3VZQfMzTwMOzkQtCRazTaKSVjQGkUC7',
        access_token_secret = 'wmMcZW70IwpkJSZfOKbRanVE20Mj1GbdC9YgEityYhMta'
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

## plot as a wordcloud
# Data to plot
wordcloud = WordCloud(
                      font_path='G:/Eclipse projects/Python-Twitter_Visualizer/DroidSansMono.ttf',
                      stopwords=STOPWORDS,
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(words)

plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('./my_twitter_wordcloud_1.png', dpi=300)
plt.show()

