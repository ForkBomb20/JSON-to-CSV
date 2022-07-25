import os
import ujson
import argparse

parser = argparse.ArgumentParser(description="Converts a json files to proper format")

parser.add_argument("-i", "--input", help="The path to the input directory for the jsons", required=True)
parser.add_argument("-o", "--output", help="The path to the output directory for the corrected jsons", required=True)

args = parser.parse_args()

files = os.listdir(args.input)
files = [file for file in files if not file.startswith(".")]
encodings = ["utf-8", "iso-8859-1", "latin-1", "utf-16", "utf-32", "ascii",  "cp1252"]

for file in files:
    for encoding in encodings:
        try:
            json_str = open(args.input + "/" + file, "r").read()
        except:
            pass
    rows = json_str.split("\n")
    rows = [ujson.loads(row) for row in rows if row != ""]
    data = {"data": rows}
    with open(args.output + "/" + file, "w") as f:
        ujson.dump(data, f)
