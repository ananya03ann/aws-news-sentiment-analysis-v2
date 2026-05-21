import json
import pg8000
import requests

from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------

DB_HOST = "database-1.c3qm2yq0clyo.ap-south-1.rds.amazonaws.com"
DB_NAME = "newsdb"
DB_USER = "postgres"
DB_PASSWORD = "postgres-123"
DB_PORT = 5432

# -----------------------------
# NEWS API
# -----------------------------

NEWS_API_KEY = "09c5ffa098854520935f6121e5f146d8"

analyzer = SentimentIntensityAnalyzer()

# -----------------------------
# LAMBDA FUNCTION
# -----------------------------

def lambda_handler(event, context):

    try:

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

        response = requests.get(url)

        data = response.json()

        articles = data.get("articles", [])

        conn = pg8000.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            ssl_context=True
        )

        cur = conn.cursor()

        for article in articles:

            title = article.get("title", "No Title")

            source = article.get("source", {}).get("name", "Unknown")

            score = analyzer.polarity_scores(title)

            compound_score = score["compound"]

            if compound_score >= 0.05:
                sentiment = "Positive"

            elif compound_score <= -0.05:
                sentiment = "Negative"

            else:
                sentiment = "Neutral"

            cur.execute(
    """
    INSERT INTO news_sentiment
    (title, source, published_at, sentiment_score, sentiment)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (title) DO NOTHING
    """,
    (
        title,
        source,
        datetime.now(),
        compound_score,
        sentiment
    )
)

        conn.commit()

        cur.close()
        conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps("News inserted successfully")
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": str(e)
        }