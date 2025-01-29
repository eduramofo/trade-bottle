from pathlib import Path
from ia.ia import ia


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    file_path = BASE_DIR / 'dados.json'
    ia(file_path)
