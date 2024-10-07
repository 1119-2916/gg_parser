from src.datastructure.labeled_data import LabeledData, parse_labeled_data
from src.parse_from_file import parse_from_file
import os


def main():
    datasets = []

    # ./secret/input/ 以下のファイルを全て取得
    path = "./secret/input/"
    input_files = os.listdir(path)

    for i in input_files:
        datasets.extend(parse_from_file(path + i))

    labeled_datas = []
    for i in datasets:
        labeled_datas.append(parse_labeled_data(i))

    print(len(datasets))


if __name__ == "__main__":
    main()
