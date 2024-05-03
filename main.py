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

from description_training import descProcessing, bertProcessing
from demo import testNGrams
# from Description import find_sponsors
from data_puller import getVideoData

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
    desc = descProcessing(desc_path)
    encoded_text = bertProcessing(desc).reshape(1,-1).tolist()

    # Get caption path
    # Do all the preprocessing for captions here as well

    # Predict if the description has a label or not
    filename = "svm_desc.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(encoded_text)
    print(result)

    # Do terminology extraction and pre-processing if a sponsor is detected.
    if result == 1:
        testNGrams(videoID)
        
    else:
        print("No sponsor")


if __name__ == '__main__':
    # Passes through a parameter (URL)
    main(sys.argv[1])
    
    # url = "https://www.youtube.com/watch?v=Pv0iVoSZzN8"
    # main(url)
