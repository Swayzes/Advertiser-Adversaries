import os
import re
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter

import nltk
nltk.download('punkt')

# Function to extract the n-grams from the text in the description files.

def extractNGrams(text, num):
    
    n_grams = ngrams(word_tokenize(text), num)
    
    return [' '.join(grams) for grams in n_grams]

# Function to search for the sponsor related n-grams 
# (More words can be added if needed) 
def findSponsors(text, ngram_size):
    
    sponsor_keywords = ['sponsored by', 'thanks to','brought to you by', 'Sponsor', 'Sponsoring', 'for sponsoring']
    
    ngrams_list = extractNGrams(text, ngram_size)
    
    sponsors = [phrase for phrase in ngrams_list if any(keyword in phrase for keyword in sponsor_keywords)]
    
    return sponsors

# Path to the directory containing all the description files
folder_path = r'C:\\Users\\ashto\\Complex Systems Group\\descriptions'

# Dictionary to hold all of the potential sponsors along with the associated file names
sponsors_info = {}

# Reads each file and extracts the sponsor related n-grams
for filename in os.listdir(folder_path):
    
    if filename.endswith('.description'): 
        
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            
            content = file.read()
            
            # Cleans the content of the file if necessary (e.g., removes URLs, spaces etc..)
            content = re.sub(r'http\S+', '', content)
            
            # Finds the potential sponsors (The ngram_size can be changed as needed).
            sponsors = findSponsors(content, ngram_size=2) 
            
            if sponsors:
                sponsors_info[filename] = sponsors

# Prints the file names and the associated sponsor related n-grams
for filename, sponsor_ngrams in sponsors_info.items():
    
    print(f"File: {filename}")
    
    for ngram in sponsor_ngrams:
        
        print(f"  - {ngram}")
