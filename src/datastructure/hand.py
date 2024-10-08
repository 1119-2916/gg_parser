import dataclasses

@dataclasses.dataclass
class Hand:
    """hand data structure"""
    cards: tuple[str, str]

def rank_compare(l: str, r: str) -> bool:
    ranks = "AKQJT98765432"
    lval: int = 0
    rval: int = 0
    for i in range(len(ranks)):
        if ranks[i] == l:
            lval = i + 1
        if ranks[i] == r:
            rval = i + 1

    return lval < rval
