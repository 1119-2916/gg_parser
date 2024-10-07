import dataclasses

@dataclasses.dataclass
class Hand:
    """hand data structure"""
    cards: tuple[str, str]
