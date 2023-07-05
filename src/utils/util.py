import json
from types import Dict, List

from path_utils import SIDE_EFFECTS_DATA_FOLDER

SIDE_EFFECTS_DATA = None


def load_side_effects_data():
    global SIDE_EFFECTS_DATA
    with open(SIDE_EFFECTS_DATA_FOLDER / 'medlineplus_side_effects.json',
              'r') as f:
        loaded_side_effects = json.load(f)

    SIDE_EFFECTS_DATA = {
        k.lower(): v
        for item in loaded_side_effects for k, v in item.items()
    }


def search_side_effects(drug: str) -> Dict[str, List[str]]:
    """Search for side effects of a given drug.

    Args:
        drug (str): Drug name.

    Returns:
        Dict[str, List[str]]: Side effects of the given drug.
    """
    global SIDE_EFFECTS_DATA
    if not SIDE_EFFECTS_DATA:
        load_side_effects_data()

    drug_name = drug.lower()
    matches_side_effects = [
        v for k, v in SIDE_EFFECTS_DATA.items() if drug_name in k
    ]
    side_effects = matches_side_effects[0] if matches_side_effects else {
        'normal': [],
        'serious': []
    }

    return side_effects