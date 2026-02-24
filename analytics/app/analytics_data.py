from operator import itemgetter
import nltk
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def emotion_analyzer(tweet):
    nltk.download('vader_lexicon')
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score['compound']


def get_sentiment(compound):
    if 0.5000 < compound < 1.000:
        return "affirmative"
    elif 0.4999 > compound > -0.4991:
        return "neutral"
    else: 
        return "negative"
    
def load_weaons_data():
    path = "./app/weapons.txt"
    with open(path, "r") as f:
        data = f.read().split()
    return data


def count_words(data):
    sum_words = {}
    for word in data:
        if word in sum_words:
            sum_words[word] += 1
        else: sum_words[word] = 1
    return sum_words


def find_top_10(dict_count_words, N=10):
    dict_count_words = count_words()
    print(dict_count_words)
    res = dict(sorted(dict_count_words.items(), key=itemgetter(1), reverse=True)[:N])
    return res.keys()

