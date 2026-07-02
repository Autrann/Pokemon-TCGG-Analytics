import json
import time
from pathlib import Path

from tcgdexsdk import TCGdex, Query


tcgdex = TCGdex()

SETS_FILE = Path("data/raw/sets.json")
OUTPUT_DIR = Path("data/raw/cards")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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

    start = time.time()

    with SETS_FILE.open("r", encoding="utf-8") as file:
        sets = json.load(file)

    total_cards = 0

    for current_set in sets:

        set_id = current_set["id"]

        print(f"Downloading {set_id}...")

        cards = tcgdex.card.listSync(
            Query().equal("set.id", set_id)
        )

        data = [serialize(card) for card in cards]

        with (OUTPUT_DIR / f"{set_id}.json").open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        total_cards += len(data)

    elapsed = int(time.time() - start)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    print()
    print("=" * 40)
    print(f"Sets encontrados : {len(sets)}")
    print(f"Cartas descargadas: {total_cards}")
    print(f"Tiempo            : {hours:02}:{minutes:02}:{seconds:02}")


if __name__ == "__main__":
    main()