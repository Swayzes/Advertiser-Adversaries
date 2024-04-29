import sqlite3
import io
from pathlib import Path
import os
# https://scikit-learn.org/stable/modules/feature_extraction.html
import json
# pip install -U scikit-learn
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from transformers import BertTokenizer, BertModel

encoded_text = {"data":[], "labels":[]}

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

def BERT_Processing(text, label):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")
    encoded_input = tokenizer(text, return_tensors='pt', max_length=500)
    # tokens = tokenizer.convert_ids_to_tokens(encoded_input)
    output = model(**encoded_input)
    output.last_hidden_state.mean(dim=1).squeeze().detach().cpu().numpy()
    encoded_text["data"].append(output)
    encoded_text["labels"].append(label)
    return

def desc_processing(desc, label):
    text = open(Path(desc[0]), encoding="utf8")
    description = [text.read()]

    description.append(label)
    # BoW_Processing(description)
    # BERT_Processing(description)

    return description

con = sqlite3.connect("VideoDatabase.db")
cur = con.cursor()

# cur.execute("SELECT Description_File_Path FROM DatasetAds")
# desclist = cur.fetchall()
# for d in desclist:
#     desc_processing(d)
#     print(d)

descList = []
cur.execute("SELECT Description_File_Path FROM DatasetAds")
descListAds = cur.fetchall()
cur.execute("SELECT Description_File_Path FROM DatasetNoAds")
descListNoAds = cur.fetchall()


for d in descListAds:
    descList.append(desc_processing(d, 1))

for d in descListNoAds:
    descList.append(desc_processing(d, 0))

# print(descList)
BERT_Processing(descList[0][0], descList[0][1])
# for d in descList:
#     # BoW_Processing(description)
#     BERT_Processing(d[0], d[1])

# Load up a bunch of video data to make a dataset
# Create a dataframe with all the description based data
# Aspect Extraction:
# Use Bag of Words?
# Hashing is a thing?
# Sentiment Analysis

# SVM, gradient boosting
print(encoded_text)

def save(dir, name):
    if(not os.path.exists(dir)):
        os.makedirs(dir)
    path = os.path.join(dir, name)
    with open(path, "w") as f:
        json.dump(encoded_text, f, indent=4)

save("encoded_description", "training_data_all.json")
