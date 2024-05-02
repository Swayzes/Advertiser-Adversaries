#%%
from DataPuller import get_sponsor_segments
from Subtitles import sub_reader, sponsor_match, plot_match_words
from Sentiment import get_sub_sentiments, plot_sentiments
from Description import get_description_from_file, aspect_extration

def testSentiment(vID ="7dYTw-jAYkY"):
    """Test functions of the Subtitles module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    subs = sub_reader(vID)
    sponsors = get_sponsor_segments(vID)

    posSentiments = get_sub_sentiments(subs, polarity = "pos")
    neuSentiments = get_sub_sentiments(subs, polarity = "neu")
    negSentiments = get_sub_sentiments(subs, polarity = "neg")
    compSentiments = get_sub_sentiments(subs, polarity = "compound")
    plot_sentiments(posSentiments, "Positive", sponsors)
    plot_sentiments(neuSentiments, "Neutral", sponsors)
    plot_sentiments(negSentiments, "Negative", sponsors)
    plot_sentiments(compSentiments, "Compound", sponsors)

#testSentiment("qcH2wgRLiV8")

def test_aspect_extraction(vID = "7dYTw-jAYkY"):
    """Test functions of the aspect extraction functions from the description module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    
    subs = sub_reader(vID)
    sponsors = get_sponsor_segments(vID)
    desc = get_description_from_file(vID)
    aspects = aspect_extration(desc)
    matches = sponsor_match(subs, aspects)
    plot_match_words(matches, subs, sponsors)

# test_aspect_extraction("fpayOqZNWUo")
    

# %%

def test_ngrams(vID, aspects):
    """
    Test functions of the aspect extraction functions from the description module edited to be more modular
    
    Params:
        vID: Video ID
        aspects: list of keywords

    Author: Klent    
    """
    
    subs = sub_reader(vID)
    sponsors = get_sponsor_segments(vID)
    matches = sponsor_match(subs, aspects)
    plot_match_words(matches, subs, sponsors)