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

 
def subReader(vID, path = "dataset/subtitles", lang = "en", ft = "vtt") -> dict:
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
    sub_dict = dict()
    for event in subs.events:
        sub_dict[event.end] = event

    return sub_dict

    
def getSubEndFromTime(sub_ends: list, time, min_time = 0):
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
        
    subI = bisect_right(a=sub_ends, x=time, lo = min_time)
    return subI
    
    
def getSubsFromTimeRange(subs: dict, start_time, end_time = None) -> dict:
    """Gets all subtitles between 2 timecodes
    
    Params:
        subs: dict of all subtitles
        startTime: start timecode
        endTIme: end timecode
    
    Returns:
        dict of all identified subtitles {endTime : Event}

    Author: Sean
    """
    sub_ends = list(subs.keys())

    start_sub_i = getSubEndFromTime(sub_ends, start_time)
    range_subs = dict()
    for i in range(start_sub_i, len(sub_ends)):
        range_subs[sub_ends(i)] = subs[sub_ends(i)]

    return range_subs
 

def termMatch(subs: dict, terms: list) -> dict:
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

        word_dict = dict()
        for word in event.plaintext.split(" "):
            for term in terms:
                if word.lower() in term.lower() and word.lower() not in stopwords.words('english') and len(word) >3 :
                    try:
                        if word in word_dict.keys():
                            word_dict[word] += 1
                        else:
                            word_dict[word] = 1
                    except:
                        logging.warning(f"Sponsor match invalid word: {word}")

        for word in word_dict.keys():
            if word in matches.keys():
                matches[word][event.end] = word_dict[word]
            else:
                matches[word] = {event.end : word_dict[word]}
    print(matches)
    return matches


def plotTermMatches(matches: dict, subs: dict, title = None, segments = None):
    """Draw a pyplot of terms from the description found in the video subtitles over the video's runtime
    
    Params:
        matches: Dict of terminology matches {{matchWord : {endTime : instances} }
        subs: dict of all subtitles
        segments: list of nested arrays giving the start and end times of sponsor segments

    Author: Sean
    """
    if segments != None:
        for segment in segments:
            plt.axvspan(segment[0], segment[1], color = 'green', alpha = 0.5)
    
    for term in matches.keys(): 
        x_points = np.array(list(dict(matches[term]).keys()))
        y_points = np.array(list(dict(matches[term]).values()))

        plt.scatter(x_points, y_points, label = term)
    
    if title == None:
        plt.title("Description Terminology Extration")
    else:
        plt.title(title)
    plt.ylabel("Matches")
    plt.xlabel("Video Duration")
    plt.xlim(0, max(subs.keys()))

    

    plt.legend(loc = "upper left", title = "Terms")
    plt.show()
    

# %%
