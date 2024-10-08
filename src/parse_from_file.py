def parse_from_file(path: str, debug=False) -> list:
    # read raw data
    if debug:
        print("read from" + path)
    with open(path, "r") as f:
        raw_data = f.readlines()

    dataset = []
    datasets = []
    for i in raw_data:
        line = i.replace("\n", "")
        if line == "":
            if len(dataset) > 0:
                datasets.append(dataset)
            dataset = []
        else:
            dataset.append(line)

    if len(dataset) > 0:
        datasets.append(dataset)

    if debug:
        print("read " + str(len(datasets)) + " datasets")

    return datasets
