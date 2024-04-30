
# https://scikit-learn.org/stable/modules/feature_extraction.html
# pip install -U scikit-learn
import json
import sqlite3
import io
from pathlib import Path
import os
import numpy as np
import sklearn
import torch
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from transformers import BertTokenizer, BertModel
from sklearn.model_selection import train_test_split

# encoded_text = {"data":[], "labels":[]}
data = []
labels =[]
combined = pd.DataFrame()

def BoW_Processing(text):
    """
    
    """
    # Create the vocabulary
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
    encoded_input = tokenizer(text, return_tensors='pt', max_length=500, truncation = True)
    # tokens = tokenizer.convert_ids_to_tokens(encoded_input)
    output = model(**encoded_input)
    output = output.last_hidden_state.mean(dim=1).squeeze().detach().cpu().numpy()

    # encoded_text["data"].append(output)
    # encoded_text["labels"].append(label)

    data.append(output)
    labels.append(label)
    return

def desc_processing(desc, label):
    text = open(Path(desc[0]), encoding="utf8")
    description = [text.read()]

    description.append(label)
    return description

class NumpyTypeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.generic):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
    
def save(dir, name):
    if(not os.path.exists(dir)):
        os.makedirs(dir)
    path = os.path.join(dir, name)

    # json_data = json.dumps(encoded_text, indent=4, cls=NumpyTypeEncoder)
    # with open(path, "w") as f:
    #         f.write(json_data)
    combined = pd.DataFrame({
    "data": data,
    "labels": labels
    })
    output = combined.to_json(orient="records", lines=True)
    with open(path, "w") as f: # Change as needed
        f.write(output)

con = sqlite3.connect("VideoDatabase.db")
cur = con.cursor()

def Training_processing():
    descList = []
    cur.execute("SELECT Description_File_Path FROM DatasetAds")
    descListAds = cur.fetchall()
    cur.execute("SELECT Description_File_Path FROM DatasetNoAds")
    descListNoAds = cur.fetchall()

    for d in descListAds:
        descList.append(desc_processing(d, 1))

    for d in descListNoAds:
        descList.append(desc_processing(d,0))

    for d in descList:
        # BoW_Processing(description)
        BERT_Processing(d[0], d[1])

    save("encoded_description", "BERT_training_data.json")
    return

def Testing_processing():
    descList=[]
    cur.execute("SELECT Description_File_Path FROM DatasetTesting")
    testList = cur.fetchall()
    cur.execute("SELECT Has_Sponsor FROM DatasetTesting")
    labelList = cur.fetchall()

    for d in testList:
        text = open(Path(d[0]), encoding="utf8")
        descList.append([text.read()])

    index = 0
    for d in descList:
        BERT_Processing(d, labelList[index][0])
        index=index+1

    save("encoded_description", "BERT_testing_data.json")
    return

def Gradient_Boosting():
    
    with open('encoded_description/BERT_training_data.json') as f:
        train_df = json.load(f)

    with open('encoded_description/BERT_testing_data.json') as f:
        test_df = json.load(f)

    train_df =''
    test_df = ''
    
    return

def SVM():
    
    train_df = pd.read_json("encoded_description\BERT_training_data.json", lines=True)
    test_df = pd.read_json("encoded_description\BERT_testing_data.json", lines=True)
    svm = SVC(kernel='poly')
    
    train_body = list(train_df["data"])
    train_labels = train_df["labels"]

    test_body = list(test_df["data"])
    test_labels = test_df["labels"]

    svm.fit(train_body, train_labels)
    predicted_test_labels = svm.predict(test_body)

    # metrics = f1_score(test_label, predicted_test_labels, average="weighted")
    # print(metrics) 
    metrics = classification_report(test_labels, predicted_test_labels)
    print(metrics)

    return

# Training_processing()
# Testing_processing()
SVM()

# Training_processing()
# Testing_processing()
# print("Done")

# Load up a bunch of video data to make a dataset
# Create a dataframe with all the description based data
# Aspect Extraction:
# Use Bag of Words?
# Hashing is a thing?
# Sentiment Analysis

# SVM, gradient boosting
