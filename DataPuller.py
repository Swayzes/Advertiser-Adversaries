import sqlite3 #https://docs.python.org/3/library/sqlite3.html
import yt_dlp #pip install yt-dlp https://github.com/yt-dlp/yt-dlp
import sponsorblock #pip install sponsorblock.py https://sponsorblockpy.readthedocs.io/en/latest/

database = "VideoDatabase.db"

ytdlOptions = {
        'outtmpl': 'dataset/%(id)s', #where to put the files
        'windowsfilenames': True,
        'writedescription': True, #downloads the description
        'writesubtitles': True, #downloads the subtitles
        'subtitleslangs': ['en'], #specifies  to download english subtitles
        'keepvideo': False,
        'skip_download': True 
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
    sponsorBlockClient = sponsorblock.Client()
    segments = sponsorBlockClient.get_skip_segments(url)
    sponsorSegments = ""
    for segment in segments:
        if segment.category == "sponsor":
            sponsorSegments += (str(segment.start) + "-" + str(segment.end) + ",")
    return sponsorSegments

#adds the data to the database

def addToDatabase(url, videoDataDict, sponsorSegments):
    con = sqlite3.connect(database)
    cur = con.cursor()
    SQL = "INSERT INTO Dataset(Video_Title,URL,VideoID,Video_Length,Channel,Sponsor_Segments,Description_File_Path,Captions_File_Path) VALUES(?,?,?,?,?,?,?,?)"
    data = (videoDataDict["videoTitle"],"https://www.youtube.com/watch?v="+videoDataDict["videoID"],videoDataDict["videoID"],videoDataDict["videoLength"],videoDataDict["videoChannel"],sponsorSegments[:-1],"dataset/"+videoDataDict["videoID"]+".description","dataset/"+videoDataDict["videoID"]+".en.vtt")
    cur.execute(SQL, data)
    con.commit()

#function that will download the data from url provided, if provided a URL formatted like this: https://www.youtube.com/@MrBeast/videos it will download all video data from the channel

def getData(url):
    videoDataDict = getVideoData(url)
    sponsorSegments = getSponsorBlockData(url)
    addToDatabase(url, videoDataDict, sponsorSegments)
    print(videoDataDict["videoTitle"]," (" + url + ") Done")
