import sqlite3 #https://docs.python.org/3/library/sqlite3.html
import yt_dlp #pip install yt-dlp https://github.com/yt-dlp/yt-dlp
import sponsorblock #pip install sponsorblock.py https://sponsorblockpy.readthedocs.io/en/latest/

database = "VideoDatabase.db"

ytdlOptions = {
        'outtmpl': 'dataset/%(id)s', #where to put the files
        'windowsfilenames': True,
        'writedescription': True, #downloads the description
        'writesubtitles': True, #downloads the subtitles
        'subtitleslangs': ['en'], #specifies english subtitles to download
        'keepvideo': False, #dont download video
        'skip_download': True #skips downloading video
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

def getSponsorBlockData(url):
    sponsorBlockClient = sponsorblock.Client()
    segments = sponsorBlockClient.get_skip_segments(url)
    sponsorSegments = ""
    for segment in segments:
        if segment.category == "sponsor":
            sponsorSegments += (str(segment.start) + "-" + str(segment.end) + ",")
    return sponsorSegments

def addToDatabase(url, videoDataDict, sponsorSegments):
    con = sqlite3.connect(database)
    cur = con.cursor()
    SQL = "INSERT INTO Dataset(Video_Title,URL,VideoID,Video_Length,Channel,Sponsor_Segments,Description_File_Path,Captions_File_Path) VALUES(?,?,?,?,?,?,?,?)"
    data = (videoDataDict["videoTitle"],url,videoDataDict["videoID"],videoDataDict["videoLength"],videoDataDict["videoChannel"],sponsorSegments[:-1],"Data/"+videoDataDict["videoID"]+".description","Data/"+videoDataDict["videoID"]+".en.vtt")
    cur.execute(SQL, data)
    con.commit()

def getData(url):
    videoDataDict = getVideoData(url)
    sponsorSegments = getSponsorBlockData(url)
    addToDatabase(url, videoDataDict, sponsorSegments)
    print("Done")

getData("https://www.youtube.com/watch?v=tWYsfOSY9vY")
