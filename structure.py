import os
from json_csv_main import load_json

files = [file for file in os.listdir("./input") if not file.startswith(".")]

try:
    os.mkdir("./errors")
except FileExistsError:
    pass

try:
    os.mkdir("./structures")
except FileExistsError:
    pass


def traverse(ds):
    if isinstance(ds, dict):
        for elem in ds:
            if isinstance(ds[elem], dict):
                return({traverse(ds[elem])})
            elif isinstance(ds[elem], list):
                return([traverse(ds[elem])])
    elif isinstance(ds, list):
        for elem in ds:
            if isinstance(elem, dict):
                return(dict(traverse(elem)))
            elif isinstance(elem, list):
                return(list(traverse(elem)))


# for file in files:
#     try:
#         data = load_json(file)
#     except:
#         os.rename("./inputs/" + file, "./errors/" + file)

#     structure = None

    # def traverse(ds):
    #     for elem in ds:
    #         if isinstance(elem, dict):
    #             return(dict(traverse(elem)))
    #         elif isinstance(elem, list):
    #             return(list(traverse(elem)))
    #         return

test = {"a": 1, "b": {"a": 1, "b": [1,2,3], "c":[1,2,3], "d":1}, "c":[{"a":1, "b": 2, "c":3}, {"a":1, "b": 2, "c":3}, {"a":1, "b": 2, "c":3}]}
print({traverse(test)})
            






