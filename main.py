import requests
import pandas as pd
from textblob import TextBlob
from datetime import datetime
import json
import os
from sqlalchemy import create_engine

# ==============================
# NEWS API CONFIGURATION
# ==============================

API_KEY = "09c5ffa098854520935f6121e5f146d8"

URL = (
    f"https://newsapi.org/v2/top-headlines?"
    f"country=us&"
    f"category=business&"
    f"apiKey={API_KEY}"
)

# ==============================
# POSTGRESQL CONFIGURATION
# ==============================

DB_USER = "postgres"
DB_PASSWORD = "postgres-123"
DB_HOST = "database-1.c3qm2yq0clyo.ap-south-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "newsdb"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create PostgreSQL connection
engine = create_engine(DATABASE_URL)

# ==============================
# CREATE DATA FOLDER IF NOT EXISTS
# ==============================

os.makedirs("data", exist_ok=True)

# ==============================
# FETCH NEWS DATA
# ==============================

response = requests.get(URL)

if response.status_code != 200:
    print("Failed to fetch news")
    print(response.text)
    exit()

news_data = response.json()

# ==============================
# SAVE RAW JSON FILE
# ==============================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

json_file_path = f"data/news_raw_{timestamp}.json"

with open(json_file_path, "w", encoding="utf-8") as file:
    json.dump(news_data, file, indent=4)

print(f"Raw JSON saved: {json_file_path}")

# ==============================
# PROCESS ARTICLES
# ==============================

articles = news_data.get("articles", [])

processed_data = []

for article in articles:

    title = article.get("title", "")
    description = article.get("description", "")
    source = article.get("source", {}).get("name", "")
    published_at = article.get("publishedAt", "")

    # Combine text for sentiment analysis
    text = f"{title} {description}"

    # Sentiment Analysis
    sentiment_score = TextBlob(text).sentiment.polarity

    # Convert score to label
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    # Store processed record
    processed_data.append({
        "title": title,
        "description": description,
        "source": source,
        "published_at": published_at,
        "sentiment_score": sentiment_score,
        "sentiment": sentiment
    })

# ==============================
# CREATE DATAFRAME
# ==============================

df = pd.DataFrame(processed_data)

# ==============================
# SAVE TO POSTGRESQL
# ==============================

try:
    df.to_sql(
        "news_sentiment",
        engine,
        if_exists="append",
        index=False
    )

    print("Data saved to PostgreSQL successfully!")

except Exception as e:
    print("Error saving to PostgreSQL:")
    print(e)

# ==============================
# SAVE TO CSV
# ==============================

csv_file_path = f"data/news_processed_{timestamp}.csv"

df.to_csv(csv_file_path, index=False)

print(f"Processed CSV saved: {csv_file_path}")

# ==============================
# DISPLAY OUTPUT
# ==============================

print("\n===== NEWS SENTIMENT ANALYSIS =====\n")

print(df[[
    "title",
    "source",
    "sentiment",
    "sentiment_score"
]])

print("\nTotal Articles Processed:", len(df))