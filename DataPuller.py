import sqlite3 #https://docs.python.org/3/library/sqlite3.html
import yt_dlp #pip install yt-dlp https://github.com/yt-dlp/yt-dlp
import sponsorblock #pip install sponsorblock.py https://sponsorblockpy.readthedocs.io/en/latest/

database = "VideoDatabase.db"

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

#gets the video data using youtibe downloader and downloads the subtitles and description

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

#gets sponsorblock data from the video using sponsorblock api

def getSponsorBlockData(url):
    dataCollected = False
    sponsorSegments = ""
    sponsorBlockClient = sponsorblock.Client()
    while dataCollected == False:
        try:
            segments = sponsorBlockClient.get_skip_segments(url)
            print(segments)
            for segment in segments:
                if segment.category == "sponsor":
                    sponsorSegments += (str(segment.start) + "-" + str(segment.end) + ",")
            dataCollected = True
        except:
            pass
    return sponsorSegments

#adds the data to the database

def addToDatabase(url, videoDataDict, sponsorSegments):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if sponsorSegments != "":
        SQL = "INSERT INTO DatasetAds(Video_Title,URL,VideoID,Video_Length,Channel,Sponsor_Segments,Description_File_Path,Captions_File_Path) VALUES(?,?,?,?,?,?,?,?)"
        data = (videoDataDict["videoTitle"],"https://www.youtube.com/watch?v="+videoDataDict["videoID"],videoDataDict["videoID"],videoDataDict["videoLength"],videoDataDict["videoChannel"],sponsorSegments[:-1],"dataset/descriptions/"+videoDataDict["videoID"]+".description","dataset/subtitles/"+videoDataDict["videoID"]+".en.vtt")
        cur.execute(SQL, data)
        con.commit()
    else:
        SQL = "INSERT INTO DatasetNoAds(Video_Title,URL,VideoID,Video_Length,Channel,Description_File_Path,Captions_File_Path) VALUES(?,?,?,?,?,?,?)"
        data = (videoDataDict["videoTitle"],"https://www.youtube.com/watch?v="+videoDataDict["videoID"],videoDataDict["videoID"],videoDataDict["videoLength"],videoDataDict["videoChannel"],"dataset/descriptions/"+videoDataDict["videoID"]+".description","dataset/subtitles/"+videoDataDict["videoID"]+".en.vtt")
        cur.execute(SQL, data)
        con.commit()
#functions to use to pull data

"""
Author: Sean
Return sponsor segments stored in the datbase for a video of given videoID 
Params:
    vID: video ID for lookup
Return:
    list of nested float array of format ( (Spon1 Start, Spon1 End), (Spon2 Start, Spon2 End), ... )
        Start and end times are video timecodes in ms
"""
def getSponsorSegments(vID):
    con = sqlite3.connect(database)
    cur = con.cursor()
    SQL = "SELECT Sponsor_Segments FROM DatasetAds WHERE VideoID = ?"
    params = (vID,)
    res = cur.execute(SQL, params).fetchone()
    segments = list()
    if res != None:
        for segemnt in res[0].split(","):
            segSplit = segemnt.split("-")
            segments.append((float(segSplit[0]) * 1000, float(segSplit[1]) * 1000))
        
        return segments
    else:
        return None

#function that will download the data from a video url provided. Example usage: getData('https://www.youtube.com/watch?v=tWYsfOSY9vY')

def getData(url):
    videoDataDict = getVideoData(url)
    sponsorSegments = getSponsorBlockData(url)
    addToDatabase(url, videoDataDict, sponsorSegments)
    print(videoDataDict["videoTitle"]," (" + url + ") Done")

#function that will download the data from the channel url provided, from the start to the end number. Example usage: getDataFromChannel('https://www.youtube.com/@MrBeast/videos', 0, 20)

def getDataFromChannel(url, start, end):
    ytdlgetVideoOptions = {
        'skip_download': True,
        'keepvideo': False,
        'playliststart': start,
        'playlistend': end
        }
    ytDownloader = yt_dlp.YoutubeDL(ytdlgetVideoOptions)
    videoData = ytDownloader.extract_info(url, download = False)
    for item in videoData['entries']:
        getData('https://www.youtube.com/watch?v=' + item['id'])
    print("Channel Done")

#getDataFromChannel('https://www.youtube.com/@MrBeast/videos', 0, 20)
#getDataFromChannel('https://www.youtube.com/@LinusTechTips/videos', 0, 20)
#getDataFromChannel('https://www.youtube.com/@mkbhd/videos', 0, 20)
