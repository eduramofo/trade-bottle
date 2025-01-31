from app.panorama_laatus import panorama_laatus
from app.models import History
from app.database import db

db.connect()

def get_data():
    dfs = panorama_laatus()
    df_titulos = dfs['titulos']
    df_principais = dfs['principais']
    df_nasdaq = dfs['nasdaq']
    History.create(identifier="titulos", data=df_titulos.to_json(orient="records", indent=4))
    History.create(identifier="principais", data=df_principais.to_json(orient="records", indent=4))
    History.create(identifier="nasdaq", data=df_nasdaq.to_json(orient="records", indent=4))


if __name__ == "__main__":
    get_data()
