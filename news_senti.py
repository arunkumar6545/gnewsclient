import nltk
import warnings
from urllib.request import urlopen
from textblob import TextBlob
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import pprint

from textblob.en.sentiments import NaiveBayesAnalyzer

warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
f = open("goldmansachs.csv", "w")
f.write("polarity, subjectivity, positive, negative, date, url \n")
sia = SentimentIntensityAnalyzer()
date_sentiments = {}

for i in range(1,11):
    page = urlopen('https://www.businesstimes.com.sg/search/goldman%20sachs?page='+str(i)).read()
    soup = BeautifulSoup(page, features="html.parser")
    posts = soup.findAll("div", {"class":"media-body"})
    for post in posts:
        time.sleep(1)
        url = post.a['href']
        date = post.time.text
        # print(date, url)
        try:
            link_page = urlopen(url).read()
        except:
            continue

        link_soup = BeautifulSoup(link_page)
        sentences = link_soup.findAll("p")
        passage = ""
        for sentence in sentences:
            passage += sentence.text
        blob = TextBlob(passage)

        sent = TextBlob(passage, analyzer=NaiveBayesAnalyzer())
        positive = sent.sentiment.p_pos
        negative = sent.sentiment.p_neg

        # for sentence in blob.sentences:
        f.write(str(blob.sentiment.polarity) + "," + str(blob.sentiment.subjectivity) +  "," + str(positive) + "," + str(negative) + "," + date + ",\"" + url + "\"\n")
        sentiment = sia.polarity_scores(passage)['compound']
        date_sentiments.setdefault(date,[]).append(sentiment)
#
# date_sentment = {}
# for k,v in date_sentiments.items():
#     date_sentment[datetime.strptime(k, '%d %b %Y'). date() + timedelta(days=1)] = round(sum(v)/float(len(v)), 3)
#
# earliest_date = min(date_sentment.keys())
f.close()
print('done')

# print(date_sentment)