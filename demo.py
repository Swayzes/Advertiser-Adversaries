#%%
from data_puller import getSponsorSegments
from subtitles import subReader, termMatch, plotTermMatches
from sentiment import getSubSentiments, plotSentiments
from description import getDescriptionFromFile, domainNameExtration
from description_training import descProcessing, getKeywords, bertProcessing
import pickle

def testSentiment(v_id ="7dYTw-jAYkY"):
    """Test functions of the Subtitles module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    subs = subReader(v_id)
    sponsors = getSponsorSegments(v_id)

    pos_sentiments = getSubSentiments(subs, polarity = "pos")
    neu_sentiments = getSubSentiments(subs, polarity = "neu")
    neg_sentiments = getSubSentiments(subs, polarity = "neg")
    comp_sentiments = getSubSentiments(subs, polarity = "compound")
    plotSentiments(pos_sentiments, "Positive", sponsors)
    plotSentiments(neu_sentiments, "Neutral", sponsors)
    plotSentiments(neg_sentiments, "Negative", sponsors)
    plotSentiments(comp_sentiments, "Compound", sponsors)

testSentiment("fpayOqZNWUo")

def testTerminologyExtraction(v_id = "7dYTw-jAYkY"):
    """Test functions of the terminology extraction functions from the description module
    
    Params:
        vID: Video ID

    Author: Sean    
    """
    
    subs = subReader(v_id)
    sponsors = getSponsorSegments(v_id)
    desc = getDescriptionFromFile(v_id)
    terms = domainNameExtration(desc)
    matches = termMatch(subs, terms)
    plotTermMatches(matches, subs, title="Domain Name Extraction", segments= sponsors)

#test_terminology_extraction("fpayOqZNWUo")
    

def testNGrams(vID):
    """
    Test functions of the terminology extraction functions from the description module edited to be more modular
    
    Params:
        vID: Video ID
        terms: list of keywords

    Author: Klent    
    """

    desc_path = "dataset/descriptions/" + vID + ".description"
    desc = descProcessing(desc_path)
    encoded_text = bertProcessing(desc).reshape(1,-1).tolist()

    filename = "svm_desc.pkl"
    loaded_model = pickle.load(open(filename, 'rb'))
    result = loaded_model.predict(encoded_text)
    print(result)

    # Do terminology extraction and pre-processing if a sponsor is detected.
    if result == 1:
        kw = getKeywords(desc)
        print(kw)
        kwlist = list()
        for word in kw:
            kwlist.append(word[0])
    
    subs = subReader(vID)
    sponsors = getSponsorSegments(vID)
    matches = termMatch(subs, kwlist)
    plotTermMatches(matches, subs, segments=sponsors)

#test_ngrams("fpayOqZNWUo")

#%%
