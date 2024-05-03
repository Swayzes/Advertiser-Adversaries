#%%
from DataPuller import getSponsorSegments
from Subtitles import sub_reader, term_match, plot_term_matches
from Sentiment import get_sub_sentiments, plot_sentiments
from Description import get_description_from_file, domain_name_extration

def testSentiment(vID ="7dYTw-jAYkY"):
    """Test functions of the Subtitles module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    subs = sub_reader(vID)
    sponsors = getSponsorSegments(vID)

    posSentiments = get_sub_sentiments(subs, polarity = "pos")
    neuSentiments = get_sub_sentiments(subs, polarity = "neu")
    negSentiments = get_sub_sentiments(subs, polarity = "neg")
    compSentiments = get_sub_sentiments(subs, polarity = "compound")
    plot_sentiments(posSentiments, "Positive", sponsors)
    plot_sentiments(neuSentiments, "Neutral", sponsors)
    plot_sentiments(negSentiments, "Negative", sponsors)
    plot_sentiments(compSentiments, "Compound", sponsors)

#testSentiment("qcH2wgRLiV8")

def test_terminology_extraction(vID = "7dYTw-jAYkY"):
    """Test functions of the terminology extraction functions from the description module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    
    subs = sub_reader(vID)
    sponsors = getSponsorSegments(vID)
    desc = get_description_from_file(vID)
    terms = domain_name_extration(desc)
    matches = term_match(subs, terms)
    plot_term_matches(matches, subs, sponsors)

# test_terminology_extraction("fpayOqZNWUo")
    

# %%

def test_ngrams(vID, terms):
    """
    Test functions of the terminology extraction functions from the description module edited to be more modular
    
    Params:
        vID: Video ID
        terms: list of keywords

    Author: Klent    
    """
    
    subs = sub_reader(vID)
    sponsors = getSponsorSegments(vID)
    matches = term_match(subs, terms)
    plot_term_matches(matches, subs, sponsors)