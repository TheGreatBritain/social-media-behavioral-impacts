import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys
import logging
from __future__ import print_function

def sentiment_with_vader(sentence):
    sentiment_analyzer = SentimentIntensityAnalyzer()
    logging.info("Performing sentiment analysis on :"+sentence)
    sentence_sentiment = sentiment_analyzer.polarity_scores(sentence)
    return sentence_sentiment
