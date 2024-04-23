import sqlite3
import io
from pathlib import Path
import os
# https://scikit-learn.org/stable/modules/feature_extraction.html

# pip install -U scikit-learn
import sklearn
from sklearn.feature_extraction.text import CountVectorizer

#pip install transformers
from transformers import BertTokenizer, BertModel

#pip install nltk
from nltk import word_tokenize, pos_tag


def BoW_Processing(text):
    # create the vocabulary
    vectorizer = CountVectorizer()

    # fit the vocabulary to the text data
    vectorizer.fit(text)

    # create the bag-of-words model
    bow_model = vectorizer.transform(text)

    # print the bag-of-words model
    print("BoW")
    print(bow_model)
    return

def BERT_Processing(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")
    encoded_input = tokenizer(text, return_tensors='pt')
    tokens = tokenizer.convert_ids_to_tokens(encoded_input)
    output = model(**encoded_input)
    print("BERT")
    print()
    return

def desc_processing(desc, label):
    text = open(Path(desc[0]), encoding="utf8")
    description = [text.read()]

    description.append(label)
    # BoW_Processing(description)
    # BERT_Processing(description)

    return description

# con = sqlite3.connect("VideoDatabase.db")
# cur = con.cursor()

# # cur.execute("SELECT Description_File_Path FROM DatasetAds")
# # desclist = cur.fetchall()
# # for d in desclist:
# #     desc_processing(d)
# #     print(d)

# descList = []
# cur.execute("SELECT Description_File_Path FROM DatasetAds")
# descListAds = cur.fetchall()
# cur.execute("SELECT Description_File_Path FROM DatasetNoAds")
# descListNoAds = cur.fetchall()


# for d in descListAds:
#     descList.append(desc_processing(d, 1))

# for d in descListNoAds:
#     descList.append(desc_processing(d, 0))

# print(descList)

# for d in descList:
    # BoW_Processing(description)
    # BERT_Processing(description)

# Load up a bunch of video data to make a dataset
# Create a dataframe with all the description based data
# Aspect Extraction:
# Use Bag of Words?
# Hashing is a thing?
# Sentiment Analysis:
# 


def getDescriptionFromFile(vID, path = "dataset/descriptions", ft = "description"):
    """Return the description of a given video

    Params: 
        vID: video ID, 
        path: relative directory of subtitles folder
        ft: file type
    
    Returns:
        dict of all subtitle events {endTimecode : Event}

    Author: Sean
    """
    file = open(f"{path}/{vID}.{ft}", "r")

    print(file.read())
    

def splitDesc(desc: str):
    """Split a description string into a list of lines, removing empty lines

    Params:
        desc: description 

    Returns: 
        List of strings

    Author: Sean
    """

    inputDesc = desc.split("\n")

    outputDesc = list()
    for line in inputDesc:
        if line != "":
            outputDesc.append(line)

    return outputDesc


def aspect_extration(desc):
    """Extract potential aspects from a description

    Params:
        desc: Description text

    Return:
        list of potential features

    Author: Sean
    """
    descLines = splitDesc(desc)

    for line in descLines:
        text = word_tokenize(line)


    return None

    #https://www.nltk.org/book/ch05.html