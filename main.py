from src.datastructure.labeled_data import LabeledData, parse_labeled_data
from src.parse_from_file import parse_from_file
from src.preflop_check.zeros_preflop_checker import open_raise_check
import os



def get_all_files(path:str = "./secret/input/") -> list[LabeledData]:
    datasets = []
    input_files = os.listdir(path)
    for i in input_files:
        datasets.extend(parse_from_file(path + i))
    ret: list[LabeledData] = []
    for i in datasets:
        ret.append(parse_labeled_data(i))
    return ret


def get_single_file(path:str = "./secret/input/test_data.txt") -> list[LabeledData]:
    dataset = parse_from_file(path, debug=True)
    ret: list[LabeledData] = []
    for i in dataset:
        ret.append(parse_labeled_data(i))
    return ret


def main():

    labeled_datas = get_single_file(path="secret/input/GG20241008-1116 - RushAndCash2847770 - 0.01 - 0.02 - 6max.txt")

    for i in labeled_datas:
        if not open_raise_check(i):
            print("NG action")
            print(f"hand: {i.hero_hand}, position: {i.hero_position}")
            print(i.preflop_actions)
            print(" ======== ")


def test():
    # ./secret/test/test_data.txt を取得
    path = "./secret/test/test_data.txt"
    dataset: list[LabeledData] = parse_from_file(path, debug=True)

    labeled_datas = []
    for i in dataset:
        labeled_datas.append(parse_labeled_data(i))

    for i in labeled_datas:
        if not open_raise_check(i):
            print("NG action")
            print(i)
            print("\n ======== \n\n")
        else:
            print("OK action")
            print(i)
            print("\n ======== \n\n")


if __name__ == "__main__":
    main()
    # test()
