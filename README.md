# Advertiser-Adversaries
Automatic sponsor detection for Youtube

Steps (Divide Between ourselves):
1. Get sponsor segments using sponsorblock API, and download data using youtube dlp
  - Creates our data set (Mainly caption data & description data)
2. Caption Sentiment Analysis
  - Start & end of sponsor segments
3. Description Sentiment Analysis
  - Detect what sponsors are in
  - Combine the 2 Sentiment Analyses
4. Evaluate on existing sponsorblock videos
  - Check if the resulted detections are accurate compared to manual input
5. Evaluate on New Videos
  - Test it out on new videos without using sponsor
  - See if we can submit to sponsor block (DO NOT DO THIS IF IT SUCKS)
