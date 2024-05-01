""" Subtitle anlysis """
#%%

#pip install nltk
import pysubs2
#pip install pysubs2
from bisect import bisect_right

import matplotlib.pyplot as plt
import numpy as np



 
def sub_reader(vID, path = "dataset/subtitles", lang = "en", ft = "vtt") -> dict:
    """Read subtitle file into dictonary
    
    Params: 
        vID: video ID, 
        path: relative directory of subtitles folder
        lang: subtitle language ID
        ft: file type
    
    Returns:
        dict of all subtitle events {endTimecode : Event}

    Author: Sean
    """
        
    subs = pysubs2.load(f"{path}/{vID}.{lang}.{ft}")
    subDict = dict()
    for event in subs.events:
        subDict[event.end] = event

    return subDict

    
def get_subEnd_from_time(subEnds: list, time, minTime = 0):
    """get the end timecode of the subtitle which coveres a given timecode
    
    Params:
        subEnds: list of all subtitle end timecodes
        time: search timecode
        minTime: earliest possible timecode used to narrow search
    
    Returns:
        index of matching subtitle

    Author: Sean
    """
        
    subI = bisect_right(a=subEnds, x=time, lo = minTime)
    return subI
    
    
def get_subs_from_time_range(subs: dict, startTime, EndTime) -> dict:
    """gets all subtitles between 2 timecodes
    
    Params:
        subs: dict of all subtitles
        startTime: start timecode
        endTIme: end timecode
    
    Returns:
        dict of all identified subtitles {endTime : Event}

    Author: Sean
    """
        
    subEnds = list(subs.keys())

    startSubI = get_subEnd_from_time(subEnds, startTime)
    rangeSubs = dict()
    for i in range(startSubI, len(subEnds)):
        rangeSubs[subEnds(i)] = subs[subEnds(i)]

    return rangeSubs
 

def sponsor_match(subs: dict, aspects: list) -> dict:
    """returns the timecodes at which potential sponsor related words appear in the subtitles

    Params:
        subs: dict of all subtitles
        aspects: list of all potential sponsor words

    Returns:
        nested dict of all identified sponsor words {matchWord : {endTime : instances} }

    Author: Sean
    """
    matches = dict()
    for event in subs.values():

        wordDict = dict()
        for word in event.plaintext.split(" "):
            for aspect in aspects:
                if word == aspect:
                    wordDict[word] += 1

        for word in wordDict.keys():
            matches[word] = {event.end : wordDict[word]}

    return matches


def plot_match_words(matches: dict, subs: dict, segments = None):
    
    for aspect in matches.keys(): 
        xPoints = np.array(list(dict(matches[aspect]).keys()))
        yPoints = np.array(list(dict(matches[aspect]).values()))

        plt.plot(xPoints, yPoints)
        
    plt.title("Description Aspect Extration")
    plt.ylabel("Matches")
    plt.xlabel("Video Duration")
    plt.xlim(0, max(subs.keys()))

    if segments != None:
        for segment in segments:
            plt.axvspan(segment[0], segment[1], color = 'green', alpha = 0.5)

    plt.show()
    


# %%
