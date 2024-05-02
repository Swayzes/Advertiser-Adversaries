from transformers import BertTokenizer, BertModel
from pathlib import Path
import numpy as np
import yt_dlp #pip install yt-dlp https://github.com/yt-dlp/yt-dlp
import pickle

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
        # 'keepvideo': False,
        # 'skip_download': True,
        # 'playliststart': 0,
        # 'playlistend': 20
}

def getVideoData(url):
    ytDownloader = yt_dlp.YoutubeDL(ytdlOptions)
    ytDownloader.download(url)
    videoData = ytDownloader.extract_info(url, download = False)
    videoDataDict = {
        "videoTitle": videoData.get('title', None),
        "videoLength": videoData.get('duration', None),
        "videoChannel": videoData.get('channel', None),
        "videoID": videoData.get('id', None)
    }
    return videoDataDict

def BERT_Processing(text):
    """
    Processes text into BERT to encode the words
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
    """
    text = open(Path(desc), encoding="utf8")
    description = [text.read()]

    return description

def getVideoData(url):
    ytDownloader = yt_dlp.YoutubeDL(ytdlOptions)
    ytDownloader.download(url)
    videoData = ytDownloader.extract_info(url, download = False)
    videoDataDict = {
        "videoTitle": videoData.get('title', None),
        "videoLength": videoData.get('duration', None),
        "videoChannel": videoData.get('channel', None),
        "videoID": videoData.get('id', None)
    }
    return videoDataDict

# url = "https://www.youtube.com/watch?v=Pv0iVoSZzN8"
# video_data = getVideoData(url)
# videoID = video_data["videoID"]
videoID = "Pv0iVoSZzN8"
desc_path = "dataset/descriptions/" + videoID + ".description"
desc = desc_processing(desc_path)
encoded_text = BERT_Processing(desc)
print(encoded_text)
# Predict if the description has a label or not
# filename = "svm_desc.pkl"
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.predict(encoded_text)
# print(result)