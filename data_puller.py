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

"""
Author: Callum
gets the video data using youtube downloader as well as downloads the subtitles and description of the video and puts them into their respective folders
Args:
    url: the url of the video to download the subtitles and description for
Return:
    Dictionary that contains the title of the video.length of the video,the channel the video is from and the videos ID.
"""
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

"""
Author: Callum
gets the sponsors from the video using sponsorblock api
Args:
    url: the url of the video to get the sponsor segements for
Return:
    String that contains all of the start and end times of each sponsor segment.
"""
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


"""
Author: Callum
adds the video data to the database, in the ads or noAds table
Args:
    url: the url of the video
    videoDataDict: Dictionary that contains the title of the video.length of the video,the channel the video is from and the videos ID.
    sponsorSegments: String that contains all of the start and end times of each sponsor segment.
"""
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

"""
Author: Sean
Return sponsor segments stored in the datbase for a video of given videoID 
Args:
    vID: video ID for lookup
Return:
    list of nested float array of format ( (Spon1 Start, Spon1 End), (Spon2 Start, Spon2 End), ... )
        Start and end times are video timecodes in ms
"""
def getSponsorSegments(v_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    SQL = "SELECT Sponsor_Segments FROM DatasetAds WHERE VideoID = ?"
    params = (v_id,)
    res = cur.execute(SQL, params).fetchone()
    segments = list()
    if res != None:
        for segemnt in res[0].split(","):
            seg_split = segemnt.split("-")
            segments.append((float(seg_split[0]) * 1000, float(seg_split[1]) * 1000))
        
        return segments
    else:
        return None

"""
Author: Callum
function that will download the data from a youtbe video url provided and store it into the ads or no ads table in the database
Args:
    url: the url of the video
"""
def getData(url):
    videoDataDict = getVideoData(url)
    sponsorSegments = getSponsorBlockData(url)
    addToDatabase(url, videoDataDict, sponsorSegments)
    print(videoDataDict["videoTitle"]," (" + url + ") Done")

"""
Author: Callum
gets the video data using youtube downloader as well as downloads the subtitles and description of the video and puts them into the respective testing folder
Args:
    url: the url of the video to download the subtitles and description for
Return:
    Dictionary that contains the title of the video.length of the video,the channel the video is from and the videos ID.
"""
def getTestVideoData(url):
    ytDownloader = yt_dlp.YoutubeDL({
        'paths': {
            "subtitle": "dataset/testSubtitles/",
            "description": "dataset/testDescriptions/"
            },
        'outtmpl': '%(id)s', 
        'windowsfilenames': True,
        'writedescription': True, 
        'writesubtitles': True, 
        'writeautomaticsub': True,
        'subtitleslangs': ['en'], 
        'keepvideo': False,
        'skip_download': True,
        'playliststart': 0,
        'playlistend': 20
    })
    ytDownloader.download(url)
    videoData = ytDownloader.extract_info(url, download = False)
    videoDataDict = {
        "videoTitle": videoData.get('title', None),
        "videoLength": videoData.get('duration', None),
        "videoChannel": videoData.get('channel', None),
        "videoID": videoData.get('id', None)
    }
    return videoDataDict

"""
Author: Callum
function that will download the data from a youtbe video url provided and store it into the testing table in the database
Args:
    url: the url of the video
"""
def getTestData(url):
    videoDataDict = getTestVideoData(url)
    sponsorSegments = getSponsorBlockData(url)
    con = sqlite3.connect(database)
    cur = con.cursor()
    if sponsorSegments != "":
        hasSponsor = 1
    else:
        hasSponsor = 0
    SQL = "INSERT INTO DatasetTesting(Video_Title,URL,VideoID,Video_Length,Channel,Sponsor_Segments,Description_File_Path,Captions_File_Path,Has_Sponsor) VALUES(?,?,?,?,?,?,?,?,?)"
    data = (videoDataDict["videoTitle"],"https://www.youtube.com/watch?v="+videoDataDict["videoID"],videoDataDict["videoID"],videoDataDict["videoLength"],videoDataDict["videoChannel"],sponsorSegments[:-1],"dataset/testDescriptions/"+videoDataDict["videoID"]+".description","dataset/testSubtitles/"+videoDataDict["videoID"]+".en.vtt",hasSponsor)
    cur.execute(SQL, data)
    con.commit()
"""
Author: Callum
function that will download the data from the channel url provided, from the start to the end number.
Args:
    url: the url of the video
    start: the start number
    end: the end number
    testData: whether the data is testdata or not
"""
def getDataFromChannel(url, start, end, testData):
    ytdlgetVideoOptions = {
        'skip_download': True,
        'keepvideo': False,
        'playliststart': start,
        'playlistend': end
        }
    ytDownloader = yt_dlp.YoutubeDL(ytdlgetVideoOptions)
    videoData = ytDownloader.extract_info(url, download = False)
    if testData == False:
        for item in videoData['entries']:
            getData('https://www.youtube.com/watch?v=' + item['id'])
    else:
        for item in videoData['entries']:
            getTestData('https://www.youtube.com/watch?v=' + item['id'])
    print("Channel Done")

#getDataFromChannel('https://www.youtube.com/@MrBeast/videos', 0, 20, False)
#getDataFromChannel('https://www.youtube.com/@LinusTechTips/videos', 0, 20, False)
#getDataFromChannel('https://www.youtube.com/@mkbhd/videos', 0, 20, False)

#getDataFromChannel('https://www.youtube.com/@MrBeast/videos', 40, 60, True)
#getDataFromChannel('https://www.youtube.com/@LinusTechTips/videos', 40, 60, True)
#getDataFromChannel('https://www.youtube.com/@mkbhd/videos', 40, 60, True)
