from sqlalchemy import create_engine
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def save_to_database(df):

    try:

        df.to_sql(
            "news_sentiment",
            engine,
            if_exists="append",
            index=False
        )

        print("Data saved to PostgreSQL successfully!")

    except Exception as e:

        print("Database Error:")
        print(e)