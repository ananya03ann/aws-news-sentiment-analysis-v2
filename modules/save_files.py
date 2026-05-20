import json

def save_json(data, file_path):

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_csv(df, file_path):

    df.to_csv(file_path, index=False)