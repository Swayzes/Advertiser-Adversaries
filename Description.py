import sqlite3
import io
from pathlib import Path
import os
# https://scikit-learn.org/stable/modules/feature_extraction.html

import sklearn

def desc_processing(desc):
   text = open(Path(str(desc[0])), encoding="utf8")
   description = text.read()
   return 

con = sqlite3.connect("VideoDatabase.db")
cur = con.cursor()
cur.execute("SELECT Description_File_Path FROM Dataset")
desclist = cur.fetchall()

for d in desclist:
    desc_processing(d)
    break

# Load up a bunch of video data to make a dataset
# Create a dataframe with all the description based data
# Aspect Extraction:
# Use Bag of Words?
# Hashing is a thing?
# Sentiment Analysis:
