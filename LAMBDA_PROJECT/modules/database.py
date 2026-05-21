import pg8000

from modules.config import *

def get_connection():

    conn = pg8000.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        ssl_context=True
    )

    return conn


def insert_news(cur, title, source, published_at,
                sentiment_score, sentiment):

    cur.execute(
        """
        INSERT INTO news_sentiment
        (title, source, published_at,
         sentiment_score, sentiment)

        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            title,
            source,
            published_at,
            sentiment_score,
            sentiment
        )
    )