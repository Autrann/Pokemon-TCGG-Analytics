import json
import time
from collections import Counter
from pathlib import Path


CARDS_DIR = Path("data/raw/cards")


def load_all_cards():
    """
    Lee todos los archivos JSON dentro de data/raw/cards/
    y devuelve una lista con todas las cartas.
    """

    cards = []

    for json_file in CARDS_DIR.glob("*.json"):

        with json_file.open("r", encoding="utf-8") as file:
            set_cards = json.load(file)

        cards.extend(set_cards)

    return cards


def main():

    start = time.time()

    print("Loading cards...")

    cards = load_all_cards()

    # =========================
    # CONTADORES GENERALES
    # =========================

    total_cards = len(cards)

    categories = Counter(
        card.get("category")
        for card in cards
        if card.get("category") is not None
    )

    total_pokemon = categories.get("Pokemon", 0)
    total_trainers = categories.get("Trainer", 0)
    total_energy = categories.get("Energy", 0)

    # =========================
    # PRESENCIA DE ATRIBUTOS
    # =========================

    cards_with_attacks = sum(
        1
        for card in cards
        if card.get("attacks")
    )

    cards_with_abilities = sum(
        1
        for card in cards
        if card.get("abilities")
    )

    cards_with_resistances = sum(
        1
        for card in cards
        if card.get("resistances")
    )

    cards_without_description = sum(
        1
        for card in cards
        if card.get("description") is None
    )

    cards_without_illustrator = sum(
        1
        for card in cards
        if card.get("illustrator") is None
    )

    cards_with_regulation_mark = sum(
        1
        for card in cards
        if card.get("regulationMark") is not None
    )

    # =========================
    # TOP RAREZAS
    # =========================

    rarities = Counter(
        card.get("rarity")
        for card in cards
        if card.get("rarity") is not None
    )

    # =========================
    # TOP TIPOS
    # =========================

    types = Counter()

    for card in cards:

        card_types = card.get("types")

        if card_types:

            for card_type in card_types:
                types[card_type] += 1

    # =========================
    # TOP ILUSTRADORES
    # =========================

    illustrators = Counter(
        card.get("illustrator")
        for card in cards
        if card.get("illustrator") is not None
    )

    # =========================
    # CAMPOS NULL
    # =========================

    null_fields = Counter()

    all_fields = set()

    # Primero descubrimos todos los campos existentes
    for card in cards:
        all_fields.update(card.keys())

    # Después contamos NULL por campo
    for card in cards:

        for field in all_fields:

            if card.get(field) is None:
                null_fields[field] += 1

    # =========================
    # TIEMPO
    # =========================

    elapsed = int(time.time() - start)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    # =========================
    # RESULTADOS
    # =========================

    print()
    print("=" * 60)
    print("GENERAL")
    print("=" * 60)

    print(f"Total cartas   : {total_cards}")
    print(f"Total Pokémon  : {total_pokemon}")
    print(f"Total Trainers : {total_trainers}")
    print(f"Total Energy   : {total_energy}")

    print()
    print("=" * 60)
    print("ATRIBUTOS")
    print("=" * 60)

    print(f"Con ataques          : {cards_with_attacks}")
    print(f"Con habilidades      : {cards_with_abilities}")
    print(f"Con resistencia      : {cards_with_resistances}")
    print(f"Sin descripción      : {cards_without_description}")
    print(f"Sin ilustrador       : {cards_without_illustrator}")
    print(f"Con regulationMark   : {cards_with_regulation_mark}")

    print()
    print("=" * 60)
    print("TOP 10 RAREZAS")
    print("=" * 60)

    for rarity, count in rarities.most_common(10):
        print(f"{rarity:30} {count}")

    print()
    print("=" * 60)
    print("TOP 10 TIPOS")
    print("=" * 60)

    for card_type, count in types.most_common(10):
        print(f"{card_type:30} {count}")

    print()
    print("=" * 60)
    print("TOP 10 ILUSTRADORES")
    print("=" * 60)

    for illustrator, count in illustrators.most_common(10):
        print(f"{illustrator:30} {count}")

    print()
    print("=" * 60)
    print("CAMPOS CON MAYOR CANTIDAD DE NULL")
    print("=" * 60)

    for field, count in null_fields.most_common():
        percentage = (
            count / total_cards * 100
            if total_cards > 0
            else 0
        )

        print(
            f"{field:25} "
            f"{count:8} "
            f"({percentage:6.2f}%)"
        )

    print()
    print("=" * 60)
    print(f"Tiempo: {hours:02}:{minutes:02}:{seconds:02}")
    print("=" * 60)


if __name__ == "__main__":
    main()