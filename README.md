# Advertiser-Adversaries
Automatic sponsor detection for Youtube

Steps (Divide Between ourselves):
1. Get sponsor segments using sponsorblock API, and download data using youtube dlp - Callum
  - Creates our data set (Mainly caption data & description data)
  -   - Created a datapuller script to get data from
2. Caption Sentiment Analysis
  - Start & end of sponsor segments Detection - Sean & Callum
      - Aspect extraction of sponsors: Use sentiment fluctuation to detect start & end of segments based on sponsor locations           detected from description (Implement manuallu for now) - Sean
      - Sponsor block segment based extraction: Use the segments labeled in sponsor blow to bag of words/cluster the common             words and phrases for the start & end of sponsor segments - Callum
  - Compare the two methods?
3. Description Sentiment Analysis - Ashton & Klent
  - Detect what sponsors are in the description
      - Aspect extraction of sponsors: Use definite articles to identify what may be the sponsor in a video - Ashton
      - Perform sentiment analysis: Find fluctuations to identify sponsors - Klent
  - Compare the two methods?
4. Evaluate on existing sponsorblock videos
  - Check if the resulted detections are accurate compared to manual input
5. Evaluate on New Videos
  - Test it out on new videos without using sponsor

Extra Stuff
  - Possibly train on auto generated captions
  - See if we can submit to sponsor block (DO NOT DO THIS IF IT SUCKS)
  - Make it an actual extension (Use firefox cos chrome sucks)
