import dataclasses
from datetime import datetime
from .hand import Hand

@dataclasses.dataclass
class LabeledData:
    """labeled data structure"""
    time: datetime
    hash: str
    game_type: str

    """players"""
    # hash, cash
    # indexing : ["BU", "SB", "BB", "UTG", "HJ", "CO"]
    seats: list[str, float]
    # hero data
    hero_position: str
    hero_cash: float

    """hand"""
    hero_hand: Hand

    """actions"""
    preflop_actions: list[str]
    flop_actions: list[str]
    turn_actions: list[str]
    river_actions: list[str]

    """board"""
    flop: tuple[str, str, str]
    turn: str
    river: str

    """results"""
    showdown: str
    summary: list[str]


def _from_index_to_position(index: int) -> str:
    pos = ["BU", "SB", "BB", "UTG", "HJ", "CO"]
    return pos[index]


# only rush and cash
def parse_labeled_data(data: list[str]) -> LabeledData:

    # first line parse, following example
    # Poker Hand #RCdddddddddd: Hold'em No Limit ($0.01/$0.02) - 2024/10/06 15:45:23
    first_line = data[0].split(" ")
    data.pop(0)
    time: datetime = datetime.strptime(first_line[-2] + " " + first_line[-1], "%Y/%m/%d %H:%M:%S")
    hash: str = first_line[2]

    # second line parse, following example
    # Table 'RushAndCash1299843' 6-max Seat #1 is the button
    second_line = data[0].split(" ")
    data.pop(0)
    game_type: str = second_line[1]

    # seats parse, following example
    # Seat 1: Player1 ($2.00 in chips)
    seats: list[str, float] = [] # hash, cash
    hero_index = -1
    for i in range(6):
        target = data[0].split(" ")
        data.pop(0)
        cash = float(target[3][2:])
        seats.append((target[2], cash))
        if target[2] == "Hero":
            hero_index = i

    # parse HOLE CARDS
    while data[0] != "*** HOLE CARDS ***":
        data.pop(0)
    data.pop(0)
    hero_hand: Hand = None
    for i in range(6):
        target = data[0].split(" ")
        data.pop(0)
        if target[2] == "Hero":
            hero_hand = Hand(cards=(target[3][1:], target[4][:-1]))

    # parse preflop actions
    preflop_actions = []
    while data[0][:3] != "***":
        preflop_actions.append(data[0])
        data.pop(0)

    # parse flop cards
    target = data[0].split(" ")
    flop = None
    flop_actions = None
    if target[1] == "FLOP":
        data.pop(0)
        flop = (target[3][1:], target[4], target[5][:-1])

        # parse flop actions
        flop_actions = []
        while data[0][:3] != "***":
            flop_actions.append(data[0])
            data.pop(0)

    # parse turn card
    target = data[0].split(" ")
    turn = None
    turn_actions = None
    if target[1] == "TURN":
        data.pop(0)
        turn = target[-1][1:-1]

        # parse turn actions
        turn_actions = []
        while data[0][:3] != "***":
            turn_actions.append(data[0])
            data.pop(0)

    # parse river card
    target = data[0].split(" ")
    river = None
    river_actions = None
    if target[1] == "RIVER":
        data.pop(0)
        river = target[-1][1:-1]

        # parse river actions
        river_actions = []
        while data[0][:3] != "***":
            river_actions.append(data[0])
            data.pop(0)

    # parse showdown
    data.pop(0)
    showdown = data[0]
    data.pop(0)

    # parse summary
    data.pop(0)
    summary = []
    for i in data:
        summary.append(i)

    return LabeledData(
        time = time,
        hash = hash,
        game_type=game_type,
        seats = seats,
        hero_position = _from_index_to_position(hero_index),
        hero_cash = seats[hero_index][1],
        hero_hand = hero_hand,
        preflop_actions=preflop_actions,
        flop_actions=flop_actions,
        turn_actions=turn_actions,
        river_actions=river_actions,
        flop=flop,
        turn=turn,
        river=river,
        showdown=showdown,
        summary=summary
    )


