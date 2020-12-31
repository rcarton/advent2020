from typing import Dict, Iterator, Optional, Set, Tuple


def parse_line(line: str) -> Tuple[Set[str], Set[str]]:
    """Parse a line of the input and return the list of ingredients and allergens."""

    # mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    ingredients_str, allergens_str = line.strip().split("(")

    ingredients = ingredients_str.strip().split()
    allergens = allergens_str[len("contains "): -1].split(", ")

    return (set(ingredients), set(allergens))


def find_allergens(puzzle_input: Iterator[str]) -> Dict[str, Optional[str]]:
    """Return a dictionary of ingredient -> allergen."""

    puzzle_input = list(puzzle_input)

    allergens_to_ingredients = {}
    found = {}
    found_ingredients = set()

    all_ingredients = set()

    def mark_found(ingredient, allergen):
        found[allergen] = ingredient
        found_ingredients.add(ingredient)

        # Remove the ingredient from all the other allergens
        for other_allergen, ingredients in allergens_to_ingredients.items():
            if other_allergen in found or ingredient not in ingredients:
                continue

            ingredients.remove(ingredient)

            # If we are down to one, then we've found another one, mark this one as found too
            if len(ingredients) == 1:
                mark_found(next(iter(ingredients)), other_allergen)

    for line in puzzle_input:
        ingredients, allergens = parse_line(line)
        all_ingredients |= ingredients

        for allergen in allergens:
            if allergen in found:
                continue

            # Remove the ingredients already found
            ingredients -= found_ingredients

            if allergen not in allergens_to_ingredients:
                allergens_to_ingredients[allergen] = ingredients.copy()
            else:
                allergens_to_ingredients[allergen] &= ingredients

            if len(allergens_to_ingredients[allergen]) == 1:
                # We found the ingredient for this allergen
                ingredient = next(iter(allergens_to_ingredients[allergen]))
                mark_found(ingredient, allergen)

    # Sanity check
    for allergen, ingredients in allergens_to_ingredients.items():
        if len(ingredients) > 1:
            raise ValueError(
                "Error: unable to find a single ingredient for allergen={allergen}"
            )

    ingredients_to_allergens = {
        ingredient: allergen for allergen, ingredient in found.items()
    }

    # Add the ones without an allergen
    for ingredient in all_ingredients:
        if ingredient not in ingredients_to_allergens:
            ingredients_to_allergens[ingredient] = None

    return ingredients_to_allergens


def first(puzzle_input: Iterator[str]) -> int:
    ingredients_to_allergens = find_allergens(puzzle_input)

    ingredients_without_allergens = {
        ingredient
        for ingredient, allergen in ingredients_to_allergens.items()
        if not allergen
    }

    # Count the ingredients without allergens
    count = 0
    for line in puzzle_input:
        ingredients, _ = parse_line(line)
        count += sum(
            1
            for ingredient in ingredients
            if ingredient in ingredients_without_allergens
        )

    return count


def second(puzzle_input: Iterator[str]) -> int:
    ingredients_to_allergens = find_allergens(puzzle_input)

    # Make a list of tuple of the allergens with their ingredient
    allergen_ingredient_tuples = [
        (allergen, ingredient)
        for ingredient, allergen in ingredients_to_allergens.items()
        if allergen
    ]

    # List the ingredients sorted alphabetically by their corresponding allergen
    return ",".join(
        [
            iwa[1]
            for iwa in sorted(
                allergen_ingredient_tuples,
                key=lambda allergen_ingredient: allergen_ingredient[0],
            )
        ]
    )
