# Advertiser-Adversaries
Automatic sponsor detection for Youtube *Incomplete

To run the software
- First run the requirements.txt to get the dependencies by going to the directory command line and typing in:
```bash
pip install -r requirements.txt
```
- Then go to the directory where the project is saved in the command line and type in:
```bash
python main.py <Youtube Video Link>
```
Development Steps:
1. Get sponsor segments using sponsorblock API, and download data using youtube dlp - Callum
  - Creates our data set (Mainly caption data & description data)
  -   - Created a datapuller script to get data from
2. Caption Sentiment Analysis
  - Start & end of sponsor segments Detection - Sean & Callum
      - Aspect extraction of sponsors: Use sentiment fluctuation to detect start & end of segments based on sponsor locations           detected from description - Sean
3. Description Sentiment Analysis - Ashton & Klent
  - Detect if video has sponsors - Klent
  - Detect what sponsors are in the description 
      - Aspect extraction of sponsors: Use definite articles to identify what may be the sponsor in a video - Ashton
4. Evaluate on existing sponsorblock videos
  - Check if the resulted detections are accurate compared to manual input
5. Evaluate on New Videos
  - Test it out on new videos without using sponsor

Extra Stuff
  - Possibly train on auto generated captions
  - See if we can submit to sponsor block (DO NOT DO THIS IF IT SUCKS)
  - Make it an actual extension (Use firefox cos chrome sucks)

