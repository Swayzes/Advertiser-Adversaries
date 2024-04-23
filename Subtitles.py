""" Subtitle anlysis """
#%%

#pip install nltk
import pysubs2
#pip install pysubs2
from bisect import bisect_right

from DataPuller import getSponsorSegments
from Sentiment import get_sub_sentiments, plot_sentiments
from Description import getDescriptionFromFile, aspect_extration


 
def subreader(vID, path = "dataset/subtitles", lang = "en", ft = "vtt") -> dict:
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
    print(subI)
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
 
    


def test(vID ="7dYTw-jAYkY"):
    subs = subreader(vID)
    sponsors = getSponsorSegments(vID)

    posSentiments = get_sub_sentiments(subs, polarity = "pos")
    neuSentiments = get_sub_sentiments(subs, polarity = "neu")
    negSentiments = get_sub_sentiments(subs, polarity = "neg")
    compSentiments = get_sub_sentiments(subs, polarity = "compound")
    plot_sentiments(posSentiments, "Positive", sponsors)
    plot_sentiments(neuSentiments, "Neutral", sponsors)
    plot_sentiments(negSentiments, "Negative", sponsors)
    plot_sentiments(compSentiments, "Compound", sponsors)

#test("qcH2wgRLiV8")
desc = getDescriptionFromFile("qcH2wgRLiV8")
aspect_extration(desc)
# %%
