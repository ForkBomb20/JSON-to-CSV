"""
Nathan Kawamoto
02/23/2022
JSON To CSV
Parses three local JSON files and creates three new CSV files with that data. Preserves
leading zeros and includes all possible fields.
"""

# Libraries
import json
import csv
from collections import OrderedDict

# Gets and returns all unique keys from an array of dictionaries
def getUniqueKeys(dicts):
    keys = []
    for d in dicts:
        for key in d.keys():
                if key not in keys:
                    keys.append(key)
    return keys

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

# Converts all values in an array of dicts with the provided keys (fields) to a literal in csv format i.e. '="value"'
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

# Creates a CSV file at the given filepath given the columns (fields) and rows (an array of dicts)
### CURRENTLY UNUSED ###
def createCSV(fields, rows, filepath):
    with open(filepath, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

# Open each json. Encoding differs,
community_file_str = open("jsons/community.json", "r").read()
samaritan_file_str = open("jsons/samaritan.json", "r", encoding="latin-1").read()
soldier_file_str = open("jsons/soldiers.json", "r", encoding="latin-1").read()

# Split the lines in the community file as the recored in the JSON or not in an array, but just on separate lines
community_records = community_file_str.split("\n")

# Iterate through, parse, and store each json record
community_dicts = []

# -1 accounting for extra newline at end of community if that line is removed, this will need to be changed
for i in range(len(community_records)-1):
    community_dicts.append(json.loads(community_records[i]))

# Parse samaritan and soldier jsons. Soldiers records are stored under "item"
samaritan_dicts = json.loads(samaritan_file_str)
soldier_lst = json.loads(soldier_file_str)
soldier_dicts = soldier_lst[0]["item"]

# Get unique keys for each array of dicts and store as the fields to be used as columns in the CSV files
community_fields = getUniqueKeys(community_dicts)
soldier_fields = getUniqueKeys(soldier_dicts)
samaritan_fields = getUniqueKeys(samaritan_dicts)

# Convert each arrays of dicts to an array of ordered dicts
community_ordereds = toOrdered(community_dicts, community_fields)
soldier_ordereds = toOrdered(soldier_dicts, soldier_fields)
samaritan_ordereds = toOrdered(samaritan_dicts, samaritan_fields)

# Create the rows comprised of the keys from each dictionary returned after parsing and making any field with a code a string literal so leading zeros will not be dropped in CSV
community_rows = [d.values() for d in toLiteral(community_ordereds, [field for field in community_fields if ("codes" in field.lower() or "code" in field.lower()) and "description" not in field.lower()])]
soldier_rows = [d.values() for d in toLiteral(soldier_ordereds, [field for field in soldier_fields if ("codes" in field.lower() or "code" in field.lower()) and "description" not in field.lower()])]
samaritan_rows = [d.values() for d in toLiteral(samaritan_ordereds, [field for field in samaritan_fields if ("codes" in field.lower() or "code" in field.lower()) and "description" not in field.lower()])]


# Write each set of fields and rows to their corresponding CSV files.
### NOTE much of this relies on relative paths for the json files. These should be adjusted if changed ###
with open("./csvs/community.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(community_fields)
    csvwriter.writerows(community_rows)

with open("./csvs/soldiers.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(soldier_fields)
    csvwriter.writerows(soldier_rows)

with open("./csvs/samaritan.csv", "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(samaritan_fields)
    csvwriter.writerows(samaritan_rows)


