"""
Subtitle anlysis
author: Sean Johnson
"""

from textblob import TextBlob
# pip install -U textblob
# python -m textblob.download_corpora
import pysubs2
#pip install pysubs2
from bisect import bisect_right

class subttiles():

    """
    Read subtitle file into dictonary
    Args: 
        vID: video ID, 
        path: relative directory of subtitles folder
        ft: file type
    Return:
        dict {endTimecode : Event}

    """
    def  subreader(vID, 
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
