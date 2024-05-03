""" Subtitle anlysis """
#%%

import pysubs2
#pip install pysubs2
from bisect import bisect_right

import matplotlib.pyplot as plt
import numpy as np

#pip install nltk
from nltk import download
download('stopwords')
from nltk.corpus import stopwords

import logging

 
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
    """Get the end timecode of the subtitle which coveres a given timecode.
    
    Params:
        subEnds: list of all subtitle end timecodes
        time: search timecode
        minTime: earliest possible timecode used to narrow search
    
    Returns:
        index of matching subtitle

    Todo:
        Test and evaluate

    Note:
        Unused and untested

    Author: Sean
    """
        
    subI = bisect_right(a=subEnds, x=time, lo = minTime)
    return subI
    
    
def get_subs_from_time_range(subs: dict, startTime, EndTime = None) -> dict:
    """Gets all subtitles between 2 timecodes
    
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
 

def term_match(subs: dict, terms: list) -> dict:
    """Returns the timecodes at which potential sponsor related terms appear in the subtitles

    Params:
        subs: dict of all subtitles
        terms: list of all potential sponsor words

    Returns:
        nested dict of all identified sponsor words {matchWord : {endTime : instances} }

    Author: Sean
    """
    matches = dict()
    for event in subs.values():

        wordDict = dict()
        for word in event.plaintext.split(" "):
            for term in terms:
                if word.lower() in term.lower() and word.lower() not in stopwords.words('english') and len(word) >3 :
                    try:
                        if word in wordDict.keys():
                            wordDict[word] += 1
                        else:
                            wordDict[word] = 1
                    except:
                        logging.warning(f"Sponsor match invalid word: {word}")

        for word in wordDict.keys():
            if word in matches.keys():
                matches[word][event.end] = wordDict[word]
            else:
                matches[word] = {event.end : wordDict[word]}
    print(matches)
    return matches


def plot_term_matches(matches: dict, subs: dict, segments = None):
    """Draw a pyplot of terms from the description found in the video subtitles over the video's runtime
    
    Params:
        matches: Dict of terminology matches {{matchWord : {endTime : instances} }
        subs: dict of all subtitles
        segments: list of nested arrays giving the start and end times of sponsor segments

    Author: Sean
    """
    
    for term in matches.keys(): 
        xPoints = np.array(list(dict(matches[term]).keys()))
        yPoints = np.array(list(dict(matches[term]).values()))

        plt.scatter(xPoints, yPoints)
        
    plt.title("Description Term Extration")
    plt.ylabel("Matches")
    plt.xlabel("Video Duration")
    plt.xlim(0, max(subs.keys()))

    if segments != None:
        for segment in segments:
            plt.axvspan(segment[0], segment[1], color = 'green', alpha = 0.5)

    plt.show()
    

# %%
