from transformers import BertTokenizer, BertModel
from pathlib import Path
import numpy as np
import yt_dlp #pip install yt-dlp https://github.com/yt-dlp/yt-dlp
import pickle
import sys
import os
import re
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter

import nltk
# nltk.download('punkt')

from Description_Training import BERT_Processing, desc_processing, get_keywords
from Demo import test_ngrams
# from Description import find_sponsors
from DataPuller import getVideoData

ytdlOptions = {
        'paths': { #where to put the files
            "subtitle": "dataset/subtitles/",
            "description": "dataset/descriptions/"
            },
        'outtmpl': '%(id)s', 
        'windowsfilenames': True,
        'writedescription': True, #downloads the description
        'writesubtitles': True, #downloads the subtitles
        'writeautomaticsub': True,
        'subtitleslangs': ['en'], #specifies  to download english subtitles
        'keepvideo': False,
        'skip_download': True,
        'playliststart': 0,
        'playlistend': 20
}

def main(url):
    video_data = getVideoData(url)
    videoID = video_data["videoID"]

    ## Test data so you don't need to download the vid everytime
    # videoID = "Pv0iVoSZzN8"
    # videoID = "7dYTw-jAYkY"
    # videoID = "YjkEVrJP7jI"
    ##

    ## Description sponsor detection preprocessing
    desc_path = "dataset/descriptions/" + videoID + ".description"
    desc = desc_processing(desc_path)
    encoded_text = BERT_Processing(desc).reshape(1,-1).tolist()

    # Get caption path
    # Do all the preprocessing for captions here as well

    # Predict if the description has a label or not
    filename = "svm_desc.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(encoded_text)
    print(result)

    # Do aspect extraction and stuff if a sponsor is detected.
    if result == 1:
        kw = get_keywords(desc)
        print(kw)
        kwlist = list()
        for word in kw:
            kwlist.append(word[0])
        print(kwlist)
        test_ngrams(videoID, kwlist)
        
    else:
        print("No sponsor")


if __name__ == '__main__':
    # Passes through a parameter (URL)
    main(sys.argv[1])
    
    # url = "https://www.youtube.com/watch?v=Pv0iVoSZzN8"
    # main(url)
