"""
Description Training
author: Klent Wasawas
"""

# https://scikit-learn.org/stable/modules/feature_extraction.html
# pip install -U scikit-learn
import sqlite3
from pathlib import Path
import os
import pickle
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score
from transformers import BertTokenizer, BertModel
from sklearn.model_selection import train_test_split

data = []
labels =[]
combined = pd.DataFrame()

## Predicts if a description has a sponsor or not
def BERT_Processing(text):
    """
    Processes the description text into BERT to encode the words
    param text: The body of text of the description
    param label: The label assigned
    """
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")
    encoded_input = tokenizer(text, return_tensors='pt', max_length=500, truncation = True)
    # tokens = tokenizer.convert_ids_to_tokens(encoded_input)
    output = model(**encoded_input)
    output = output.last_hidden_state.mean(dim=1).squeeze().detach().cpu().numpy()

    return output

def desc_processing(desc):
    """
    Processes the dataset with no labels
    param desc: The path to the description
    param label: The assigned label
    """
    text = open(Path(desc), encoding="utf8")
    description = [text.read()]

    return description

def save(dir, name):
    """
    Saves the processed datasets into JSON
    param dir: The directory
    param name: The name of the file
    """

    if(not os.path.exists(dir)):
        os.makedirs(dir)
    path = os.path.join(dir, name)

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
    """Processes the Training dataset"""
    descList = []
    cur.execute("SELECT Description_File_Path FROM DatasetAds")
    descListAds = cur.fetchall()
    cur.execute("SELECT Description_File_Path FROM DatasetNoAds")
    descListNoAds = cur.fetchall()

    for d in descListAds:
        description = desc_processing(d[0])
        description.append(1)
        descList.append(description)
            

    for d in descListNoAds:
        description = desc_processing(d[0])
        description.append(0)
        descList.append(description)

    for d in descList:
        data.append(BERT_Processing(d[0]))
        labels.append(d[1])

    save("encoded_description", "BERT_training_data.json")
    return

def Testing_processing():
    """Processes the testing dataset"""
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
        data.append(BERT_Processing(d[0]))
        labels.append(d[1])
        index=index+1

    save("encoded_description", "BERT_testing_data.json")
    return

def Combined():
    descList=[]
    cur.execute("SELECT Description_File_Path FROM DatasetAds")
    descListAds = cur.fetchall()
    cur.execute("SELECT Description_File_Path FROM DatasetNoAds")
    descListNoAds = cur.fetchall()

    for d in descListAds:
        descList.append(desc_processing(d, 1))

    for d in descListNoAds:
        descList.append(desc_processing(d,0))

    cur.execute("SELECT Description_File_Path FROM DatasetTesting")
    testList = cur.fetchall()
    cur.execute("SELECT Has_Sponsor FROM DatasetTesting")
    labelList = cur.fetchall()

    index = 0
    for d in testList:
        # text = open(Path(d[0]), encoding="utf8")
        # descList.append([text.read()])
        descList.append(desc_processing(d, labelList[index][0]))
        index=index+1

    for d in descList:
        data.append(BERT_Processing(d[0]))
        labels.append(d[1])
    
    save("encoded_description", "BERT_combined_data.json")

    return

def SVM():
    """Classifies the dataset through an SVM model"""
    train_df = pd.read_json("encoded_description\BERT_training_data.json", lines=True)
    test_df = pd.read_json("encoded_description\BERT_testing_data.json", lines=True)
    svm = SVC(kernel='poly')
    
    train_body = list(train_df["data"])
    train_labels = train_df["labels"]

    test_body = list(test_df["data"])
    test_labels = test_df["labels"]

    svm.fit(train_body, train_labels)
    predicted_test_labels = svm.predict(test_body)

    # Uncomment if on f score is needed
    # metrics = f1_score(test_label, predicted_test_labels, average="weighted")
    # print(metrics) 
    metrics = classification_report(test_labels, predicted_test_labels)
    print(metrics)

    # Saves model for future use 
    with open('svm_desc.pkl', 'wb') as f:
        pickle.dump(svm, f)

    return

def SVM_Again():
    combined_df = pd.read_json("encoded_description\BERT_combined_data.json", lines=True)
    combined_body = list(combined_df["data"])
    combined_labels = combined_df["labels"]
    svm = SVC(kernel='poly')
    
    x_train, x_test, y_train, y_test = train_test_split(combined_body, combined_labels, test_size=0.25, random_state=28)
    svm.fit(x_train, y_train)
    predicted_test_labels = svm.predict(x_test)
    # Uncomment if on f score is needed
    # metrics = f1_score(test_label, predicted_test_labels, average="weighted")
    # print(metrics) 
    metrics = classification_report(y_test, predicted_test_labels)
    print(metrics)

    with open('svm_desc.pkl', 'wb') as f:
        pickle.dump(svm, f)
    
# Training_processing()
# Testing_processing()
# Combined()
# SVM()

SVM_Again()
