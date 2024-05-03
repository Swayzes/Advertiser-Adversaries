#%%
import sqlite3
import io
from pathlib import Path
from regex import search
import os
# https://scikit-learn.org/stable/modules/feature_extraction.html

# pip install -U scikit-learn
import sklearn
from sklearn.feature_extraction.text import CountVectorizer

#pip install transformers
from transformers import BertTokenizer, BertModel

#pip install tldextract
import tldextract

#pip install nltk
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def get_description_from_file(vID, path = "dataset/descriptions", ft = "description"):
    """Return the description of a given video

    Params: 
        vID: video ID, 
        path: relative directory of subtitles folder
        ft: file type
    
    Returns:
        dict of all subtitle events {endTimecode : Event}

    Author: Sean
    """
    file = open(f"{path}/{vID}.{ft}", "r", encoding='utf-8')

    return str(file.read())
    

def split_desc(desc: str):
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


#https://www.nltk.org/book/ch05.html
def domain_name_extration(desc: str):
    """Extract potential sponsor brand names from URLs in the video's description

    Params:
        desc: Description text

    Return:
        list of potential terms

    Author: Sean
    """
    descLines = split_desc(desc)

    domainMatch = list()
    
    for line in descLines:

        domain = url_search(line)

        if domain != None:
            domainMatch.append(domain)

    return domainMatch


def url_search(line: str):
    """Detect and return domain names from a line of the description
    
    Params:
        line: a line of the description
        
    Returns:
        A domain name or empty string
        
    Author: Sean
    """

    domain = ""
    if "www." in line or "http" in line:
        url =  search("(?P<url>https?://[^\s]+)", line).group("url")
        domain = tldextract.extract(url).domain
        if domain != "" or domain != " ":
            return domain
    return None
    
# %%
