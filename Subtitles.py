"""
Subtitle anlysis
author: Sean Johnson
"""

from textblob import TextBlob
# pip install -U textblob
# python -m textblob.download_corpora
import pysubs2
#pip install pysubs2
class subttiles():

    def  subreader(vID, 
                path = "dataset/subtitles", 
                lang = "en", 
                ft = "vtt"):
        
        subs = pysubs2.load(f"{path}/{vID}.{lang}.{ft}")
        print(subs)

    #def nextSubtitle()

subttiles.subreader("VdOlqcg9uMQ")
pass