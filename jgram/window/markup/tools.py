from typing import Dict


def apply_formatting_to_map(map: Dict, formatting: Dict) -> Dict:
    result = {}
    for k, v in map.items():
        if isinstance(v, str):
            v = v.format(**formatting)
        result[k] = v
    return result
