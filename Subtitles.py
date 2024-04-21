"""
Subtitle anlysis
author: Sean Johnson
"""
#%%
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
#pip install nltk
import pysubs2
#pip install pysubs2
from bisect import bisect_right
import matplotlib.pyplot as plt
import numpy as np
from DataPuller import getSponsorBlockData
import sqlite3

class Subttiles():

    """
    Read subtitle file into dictonary
    Args: 
        vID: video ID, 
        path: relative directory of subtitles folder
        ft: file type
    Return:
        dict {endTimecode : Event}
    """
    def subreader(vID, 
            path = "dataset/subtitles", 
            lang = "en", 
            ft = "vtt") -> dict:
        
        subs = pysubs2.load(f"{path}/{vID}.{lang}.{ft}")
        subDict = dict()
        for event in subs.events:
            subDict[event.end] = event

        return subDict

    """
    get the end timecode of the subtitle which coveres a given timecode
    Args:
        subEnds: list of all subtitle end timecodes
        time: search timecode
        minTime: earliest possible timecode used to narrow search
    return:
        index of matching subtitle
    """
    def get_subEnd_from_time(subEnds: list, time, minTime = 0):
        
        subI = bisect_right(a=subEnds, x=time, lo = minTime)
        print(subI)
        return subI
    
    """
    gets all subtitles between 2 timecodes
    Args:
        subs: dict of all subtitles
        startTime: start timecode
        endTIme: end timecode
    return:
        dict of all identified subtitles {endTimecode : Event}
    """
    def get_subs_from_time_range(subs: dict, startTime, EndTime) -> dict:
        
        subEnds = list(subs.keys())

        startSubI = subttiles.get_subEnd_from_time(subEnds, startTime)
        rangeSubs = dict()
        for i in range(startSubI, len(subEnds)):
            rangeSubs[subEnds(i)] = subs[subEnds(i)]

        return rangeSubs


    """
    Retrun a sentiment score for single subtitle event
    Args:
        subEvent: the subtitle event to be analysised
        polarity: the types of sentiment polarity to be returned
            ("neg", "neu", "pos", "compound")
    Return:
        float, compond sentiment score
    """    

class Sentiments():
    
    def get_sentiment(subEvent: pysubs2.SSAEvent, polarity = None):
        
        analyzer = SentimentIntensityAnalyzer()
        score = analyzer.polarity_scores(subEvent.plaintext)

        if polarity == None:
            return score["compound"]
        else:
            return score[polarity]
    
    """
    Return a dict of each subtitle event 
    Args:
        subs: subtitle dict
    return:
        dict: in format {endTime: sentimentScore}
    """
    def get_sub_sentiments(subs: dict, polarity = None) -> dict:

        sentiments = dict()

        for key in subs.keys():
            sentiments[key] = Subttiles.get_sentiment(subs[key], polarity)

        return sentiments
    
    def plot_sentiments(sentiments: dict, title, sponStarts = None, sponEnds = None) -> plt:

        xPoints = np.array(list(sentiments.keys()))
        yPoints = np.array(list(sentiments.values()))

        plt.plot(xPoints, yPoints)
        plt.title(f"{title} Sentiments")
        plt.ylabel("Sentiment Score")
        plt.xlabel("Video Duration")
        plt.show()


def test(vID ="7dYTw-jAYkY"):
    subs = Subttiles.subreader(vID)

    posSentiments = Sentiments.get_sub_sentiments(subs, polarity = "pos")
    neuSentiments = Sentiments.get_sub_sentiments(subs, polarity = "neu")
    negSentiments = Sentiments.get_sub_sentiments(subs, polarity = "neg")
    compSentiments = Sentiments.get_sub_sentiments(subs, polarity = "compound")
    Sentiments.plot_sentiments(posSentiments, "Positive")
    Sentiments.plot_sentiments(neuSentiments, "Neutral")
    Sentiments.plot_sentiments(negSentiments, "Negative")
    Sentiments.plot_sentiments(compSentiments, "Compound")

test()
# %%
