"""Sentiment anlysis """

import pysubs2
import matplotlib.pyplot as plt
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')


def getSentiment(sub_event: pysubs2.SSAEvent, polarity = None):
    """Retrun a sentiment score for single subtitle event

    Params:
        subEvent: the subtitle event to be analysised
        polarity: the type of sentiment polarity to be returned ("neg", "neu", "pos", "compound")
        
    Returns:
        float, compond sentiment score

    Author: Sean
    """   
        
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(sub_event.plaintext)

    if polarity == None:
        return score["compound"]
    else:
        return score[polarity]
    
    
def getSubSentiments(subs: dict, polarity = None) -> dict:
    """Return a dict of each subtitle event 

    Params:
        subs: subtitle dict
        polarity: the type of sentiment polarity to be returned ("neg", "neu", "pos", "compound")
    
    Returns:
        dict of sentiment scores {endTime: sentimentScore}

    Author: Sean
    """

    sentiments = dict()

    for key in subs.keys():
        sentiments[key] = getSentiment(subs[key], polarity)

    return sentiments
    

def plotSentiments(sentiments: dict, title, segments = None):
    """Draw a pyplot of the sentiment scores for each subtitle event over the video's runtime
    
    Params:
        sentiments: Dict of sentiment scores {startTime : sentiment score}
        segments: list of nested arrays giving the start and end times of sponsor segments

    Author: Sean
    """
    if segments != None:
            for segment in segments:
                plt.axvspan(segment[0], segment[1], color = 'green', alpha = 0.5)
                
    x_points = np.array(list(sentiments.keys()))
    y_points = np.array(list(sentiments.values()))

    plt.plot(x_points, y_points)
    plt.title(f"{title} Sentiments")
    plt.ylabel("Sentiment Score")
    plt.xlabel("Video Duration")

    

    plt.show()
