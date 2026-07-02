import json
from pathlib import Path

from tcgdexsdk import TCGdex

#La funcion de este archivo es generar un JSON con todos los sets, para que al ejecutar extract_cards se genere un json con las cartas para cada set
tcgdex = TCGdex()

OUTPUT = Path("data/raw/sets.json")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def serialize(obj):

    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, list):
        return [serialize(item) for item in obj]

    if isinstance(obj, tuple):
        return [serialize(item) for item in obj]

    if isinstance(obj, dict):
        return {
            key: serialize(value)
            for key, value in obj.items()
        }

    if hasattr(obj, "__dict__"):
        return {
            key: serialize(value)
            for key, value in vars(obj).items()
            if key != "sdk"
        }

    return str(obj)


def main():

    print("Downloading sets...")

    sets = tcgdex.set.listSync()

    data = [serialize(s) for s in sets]

    with OUTPUT.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Sets encontrados: {len(data)}")


if __name__ == "__main__":
    main()