from json import JSONDecodeError
from json_csv_main import load_json
import os
import ujson
import argparse

parser = argparse.ArgumentParser(description="Converts a json files to proper format")

parser.add_argument("-i", "--input", help="The path to the input directory for the jsons", required=True)
parser.add_argument("-o", "--output", help="The path to the output directory for the corrected jsons", required=True)

args = parser.parse_args()
files = os.listdir(args.input)

# Read in all file names from jsons directory and ignore hidden files
file_names = [f for f in os.listdir(args.input) if not f.startswith(".") and f[-4:] == "json"]

try:
    os.mkdir(args.output)
except FileExistsError:
    pass

try:
    os.mkdir("./original")
except FileExistsError:
    pass

try:
    os.mkdir("./errors")
except FileExistsError:
    pass

try:
    os.mkdir("./unknown")
except FileExistsError:
    pass

for name in file_names:
    try:
        data = load_json(args.input + "/" + name)

        if isinstance(data, dict):
            if "File Summary" in data:
                del data["File Summary"]
                del data["Discounted Cash Pricing Policy"]

            elif "Updated" in data:
                data["data"] = data[data.keys()[0]]

            elif len(data.keys()) == 1 and "updated" in data.keys()[0].lower():
                data = {"data": data[data.keys()[0]]}

            elif "charges" in data:
                data = {"data": data["charges"]}

            elif "columns" in data:
                del data["columns"]
                data_lists = data["data"][1:]
                data = {"data": [lst[0] for lst in data_lists]}

            elif "MRF" in data:
                data = {"MRF": data["MRF"]}
            elif "data" in data:
                pass
            elif len(data) == 1:
                data = {"data": data[data.keys()[0]]}
            else:
                os.rename(args.input + "/" + name, "./unknown/" + name)
                data = None
            if data != None:
                with open(args.output + "/" + name, "w") as f:
                    ujson.dump(data, f)
                    os.rename(args.input + "/" + name, "./original/" + name)
        else:
            if "item" in data:
                data = {"data": data["item"]}
            elif "item" in data[0]:
                data = {"data": data[0]["item"]}
            elif "data" in data:
                data = {"data": data}
            elif isinstance(data[0], dict) and ("Type" in data[0] or "Associated_Codes" in data[0]):
                data = {"data": data}
            else:
                os.rename(args.input + "/" + name, "./unknown/" + name)
                data = None
            if data != None:
                with open(args.output + "/" + name, "w") as f:
                    ujson.dump(data, f)
                    os.rename(args.input + "/" + name, "./original/" + name)

    except:
        os.rename(args.input + "/" + name, "./errors/" + name)
    

        