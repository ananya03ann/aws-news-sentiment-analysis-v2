def display_output(df):

    print("\n===== NEWS SENTIMENT ANALYSIS =====\n")

    print(df[[
        "title",
        "source",
        "sentiment",
        "sentiment_score"
    ]])

    print("\nTotal Articles Processed:", len(df))