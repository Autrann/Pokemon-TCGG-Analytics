import json
import time
from pathlib import Path

from tcgdexsdk import TCGdex, Query


tcgdex = TCGdex()

SETS_FILE = Path("data/raw/sets.json")
OUTPUT_DIR = Path("data/raw/cards")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def serialize(obj):
    """
    Convierte objetos del SDK a estructuras compatibles con JSON.
    """

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


def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def main():
    start = time.time()

    with SETS_FILE.open("r", encoding="utf-8") as file:
        sets = json.load(file)

    total_cards = 0

    for set_number, current_set in enumerate(sets, start=1):

        set_id = current_set["id"]

        print(
            f"[{set_number}/{len(sets)}] "
            f"Downloading set {set_id}..."
        )

        # Obtiene resúmenes de las cartas del set
        card_resumes = tcgdex.card.listSync(
            Query().equal("set.id", set_id)
        )

        complete_cards = []

        for card_number, card_resume in enumerate(
            card_resumes,
            start=1
        ):
            try:
                # Obtiene la carta COMPLETA
                card = tcgdex.card.getSync(card_resume.id)

                complete_cards.append(
                    serialize(card)
                )

                print(
                    f"    [{card_number}/{len(card_resumes)}] "
                    f"{card_resume.id}",
                    end="\r"
                )

            except Exception as error:
                print()
                print(
                    f"    ERROR en {card_resume.id}: {error}"
                )

        output_file = OUTPUT_DIR / f"{set_id}.json"

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                complete_cards,
                file,
                indent=4,
                ensure_ascii=False
            )

        total_cards += len(complete_cards)

        print()
        print(
            f"    Guardadas: {len(complete_cards)} cartas"
        )

    elapsed = int(time.time() - start)

    print()
    print("=" * 50)
    print(f"Sets encontrados   : {len(sets)}")
    print(f"Cartas descargadas : {total_cards}")
    print(f"Tiempo             : {format_time(elapsed)}")
    print("=" * 50)


if __name__ == "__main__":
    main()