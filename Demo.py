#%%
from DataPuller import get_sponsor_segments
from Subtitles import sub_reader
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

#test("qcH2wgRLiV8")
desc = get_description_from_file("qcH2wgRLiV8")
aspect_extration(desc)