from analytics_data import *
from producer import send_event_to_kafka


def managment(image_id, image_text):
    weapons = load_weaons_data()
    dict_count_words = count_words(image_text)
    top_10 = find_top_10(dict_count_words)
    score_emotion = emotion_analyzer(image_text)
    sentiment = get_sentiment(score_emotion)
    analytics_dict = {
        'id':image_id,
        'top_10': top_10,
        'weapons': weapons,
        'sentiment': sentiment}
    send_event_to_kafka(analytics_dict)