from textblob import TextBlob

def analyze_sentiment(text):

    score = TextBlob(text).sentiment.polarity

    if score > 0:
        sentiment = "Positive"

    elif score < 0:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return sentiment, score