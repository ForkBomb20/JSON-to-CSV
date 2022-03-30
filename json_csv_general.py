import csv
from collections import OrderedDict
import ujson
import argparse
import os

# Returns the json string from a file tested with multiple encodings
def getJsonStr(filepath):
    encodings = ["utf-8", "iso-8859-1", "latin-1", "utf-16", "utf-32", "ascii",  "cp1252"]

    for encoding in encodings:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                return f.read()
        except:
            pass

    raise Exception("Could not decode file or parsing error")

# Returns an array of row dictionaries from a json parsed json string
def get_rows(json_str, dict_key=None):
    data = ujson.loads(json_str)

    # Attempt to get rows from known array json formatting types
    if json_str[0] == "[":
        return data

    # Attempt to get rows from known object json formatting types
    elif json_str[0] == "{":
        return data[dict_key]
            
# Writes the given rows to a csv file with the given fields
def create_csv(fields, rows, filepath):
    with open(filepath, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

# Returns an array of unique keys from a given array json object rows
def getUniqueKeys(dicts):
    keys = []
    for d in dicts:
        for key in d.keys():
                if key not in keys:
                    keys.append(key)

    return keys

# Converts values in json object rows to excel friendly literals
def toLiteral(dicts, fields):
    literals = []

    for d in dicts:
        for field in fields:
            if field in d:
                current = d[field]
                new = f'="{current}"'
                d[field] = new

        literals.append(d)

    return literals

# Converts an array of dicts into an arrray of ordered dictionaries with the given keys (fields)
def toOrdered(dicts, fields):
    # Array of new ordered dictionaries to return
    ordereds = []
    for d in dicts:
        # Array of key/value pairs that will be made into an OredredDict
        pairs = []
        # Iterates through every given dictionary and adds its key/value pair to pairs so long has the dictionary has that pair
        for field in fields:
            if field in d:
                pairs.append((field, d[field]))
            else:
                pairs.append((field, "N/A"))

        ordereds.append(OrderedDict(pairs))
        
    return ordereds


def main():

    parser = argparse.ArgumentParser(description="Converts a json files to csv files")

    parser.add_argument("-i", "--input", help="The path to the input directory for the jsons", required=True)
    parser.add_argument("-o", "--output", help="The path to the output directory for the csvs", required=True)
    parser.add_argument("-k", "--objkey", help="If the json file is in an object format this should be given as the key which holds the array of json objects to act as rows", required=False)
    
    args = parser.parse_args()
    files = os.listdir(args.input)

    for file in files:
        json_str = getJsonStr(args.input + "/" + file)
        if args.objkey:
            rows = get_rows(json_str, args.objkey.strip())
        else:
            rows = get_rows(json_str)
        fields = getUniqueKeys(rows)
        ordereds = toOrdered(rows, fields)
        literals = toLiteral(ordereds, fields)
        write_rows = [list(row.values()) for row in literals]
        create_csv(fields, write_rows, args.output + "/" + file.split(".")[0] + ".csv")
    
if __name__ == "__main__":
    main()



