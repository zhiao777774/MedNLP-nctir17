import json
from types import Dict, List


def search_side_effects(drug: str) -> Dict[str, List[str]]:
    """Search for side effects of a given drug.

    Args:
        drug (str): Drug name.

    Returns:
        Dict[str, List[str]]: Side effects of the given drug.
    """

    with open('src/data/sideeffects/medlineplus_side_effects.json', 'r') as f:
        tmp_side_effect = json.load(f)
    side_effect = {
        k.lower(): v
        for item in tmp_side_effect for k, v in item.items()
    }
    drug = drug.lower()
    side_effect = {k: v for k, v in side_effect.items() if drug in k}

    return side_effect
