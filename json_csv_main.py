import csv
from collections import OrderedDict
import shutil
import ujson
import argparse
import os

# Returns a loaded json object from the provided file
def load_json(filepath):
    encodings = ["utf-8", "iso-8859-1", "latin-1", "utf-16", "utf-32", "ascii",  "cp1252"]

    for encoding in encodings:
        try:
            with open(filepath, "r", encoding=encoding) as f:
                return ujson.loads(f.read())
        except:
            pass

    raise Exception("Could not decode file or parsing error")

            
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

    # Sets up parser for arguments
    parser = argparse.ArgumentParser(description="Converts a json files to csv files")

    parser.add_argument("-i", "--input", help="The path to the input directory for the jsons", required=True)
    parser.add_argument("-o", "--output", help="The path to the output directory for the csvs", required=True)
    
    args = parser.parse_args()
    files = os.listdir(args.input)

    # Creates an output directory if there is none and if ther is one empty it
    try:
        os.mkdir(args.output)
    except FileExistsError:
        # remove all files in output
        for file in os.listdir(args.output):
            shutil.rmtree(args.output)
            os.mkdir(args.output)

    # For each file in the input directory load in the json object
    for file in files:
        tabs = load_json(args.input + "/" + file)

        # If there are multiple keys in the object, meaning multiple tabs then for each parse the rows and create
        # multiple csv files for each tab
        if len(tabs) > 1:
            os.mkdir("./csvs/" + file.strip(".json"))
            for tab in tabs:
                fields = getUniqueKeys(tabs[tab])
                ordereds = toOrdered(tabs[tab], fields)
                literals = toLiteral(ordereds, fields)
                write_rows = [list(row.values()) for row in literals]
                no_spaces = "".join(tab.split(" "))
                name = args.output + "/" + file.strip(".json") + "/" + file.split(".")[0] + f"_{no_spaces}" + ".csv"
                create_csv(fields, write_rows, name)
                
        # If there is only one tab create only one csv file
        else:
            for tab in tabs:
                fields = getUniqueKeys(tabs[tab])
                ordereds = toOrdered(tabs[tab], fields)
                literals = toLiteral(ordereds, fields)
                write_rows = [list(row.values()) for row in literals]
                no_spaces = "".join(tab.split(" "))
                name = args.output + "/" + file.split(".")[0] + f"_{no_spaces}" + ".csv"
                create_csv(fields, write_rows, name)
    
if __name__ == "__main__":
    main()
