import json
import pandas as pd
from pathlib import Path


def process_table(data):
    headers = data[0]
    df = pd.DataFrame(data[1:], columns=headers)
    df = df.iloc[:, :-2].join(df.iloc[:, -1])
    df.columns = headers[:-2] + ["Data/Hora"]
    return df

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / 'dados.json'
    with open(file_path, "r") as file:
        data = json.load(file)
        titulos_df = process_table(data["titulos"])
        principais_df = process_table(data["principais"])
        titulos_df.to_json("titulos_df.json", orient="records", lines=True)
        principais_df.to_json("principais_df.json", orient="records", lines=True)

