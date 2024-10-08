from src.handrange.zeros import open_raise, rank_to_index
from src.datastructure.hand import Hand, rank_compare
from src.datastructure.labeled_data import LabeledData

pos = ["UTG", "HJ", "CO", "BU", "SB", "BB"]

def _open_raise_value(hand: Hand, position: str) -> int:
    """
    Check if the hand is in the open raise range for the given position.
    :param hand: str: the hand to check
    :param position: str: pos = ["BU", "SB", "BB", "UTG", "HJ", "CO"]
    :return: bool: True if the hand is in the open raise range, False otherwise
    """
    if position == "BB":
        # BB has no open raise range
        raise Exception("BB has no open raise range")

    # get the index of the hand in the handrange
    hand_index = -1
    for i in range(5):
        if pos[i] == position:
            hand_index = i
            break

    # get hand status
    is_suited: bool = hand.cards[0][1] == hand.cards[1][1]
    large_rank = hand.cards[0][0] if rank_compare(hand.cards[0][0], hand.cards[1][0]) else hand.cards[1][0]
    small_rank = hand.cards[1][0] if rank_compare(hand.cards[0][0], hand.cards[1][0]) else hand.cards[0][0]

    # check if the hand is in the open raise range
    if is_suited:
        return open_raise[hand_index][rank_to_index(large_rank)][rank_to_index(small_rank)]
    else:
        return open_raise[hand_index][rank_to_index(small_rank)][rank_to_index(large_rank)]


# def open_raise_check(hand: Hand, position: str, bet: float) -> bool:
def open_raise_check(data: LabeledData, BB: float = 0.02) -> bool:
    hand: Hand = data.hero_hand
    position: str = data.hero_position
    if position == "BB":
        # BB has no open raise range
        return True
    target = _open_raise_value(hand, position)

    # ベット金額をログから取得する
    bet: float = -1.0
    # まずオープンレイズか確認する
    for line in data.preflop_actions:
        items = line.split(" ")
        if items[0] != "Hero:":
            if items[1] == "raises":
                # オープンレイズではない
                return True
            elif items[1] == "calls":
                # リンプイン
                return True
            elif items[1] != "to" and items[1] != "folds":
                # 想定外
                print(data)
                print(items[1])
                raise Exception("想定外のアクションです")
        else:
            if items[1] == "folds":
                bet = 0.0
            elif items[1] == "raises":
                bet = float(items[-1][1:])
            elif items[1] == "calls":
                bet = float(items[-1][1:])
            break

    bet /= BB
    return abs(target - bet) < 0.0001

