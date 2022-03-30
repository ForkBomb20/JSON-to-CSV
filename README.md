# JSON-to-CSV

Simple script to convert specific JSON files to CSVs

## Usage

```
json_csv_general.py -i {The directory of your input json files} -o {The directory for your output csv files}
```
## Parameters
`-i/--input `: The input directory of your json files

`-o/--output`: The output directory for your csv files

`-k/--objkey`: If the input json is in object format this should be they key value of the list where the row objects is stored

## JSON Formats
JSON files should be in one of the two acceptable formats.

### Object Format
 ```
 {
  optionalKey: []
  optionalKey: {}
   // This is the only required key value pair
  dataKey: [
  {column: value, column: value, column: value},
  {column: value, column: value, column: value},
  {column: value, column: value, column: value},
  {column: value, column: value, column: value, column: value}
  ]
 }
 ```
 ### Array Format
 ```
 [
  {column: value, column: value, column: value},
  {column: value, column: value, column: value},
  {column: value, column: value, column: value},
  {column: value, column: value, column: value, column: value}
 ]
 ```
 ## Usage Notes
 * JSON files should be modified in any ways to ensure they are in the required formats.
 * The script can handle converting extra or missing columns into csv format. It will take all the different column values that occur across all rows and fill in "N/A" if that value is missing in certain rows.
 * The script will make all field values literals so that leading zeros and special charcaters are not dropped in parsing.
 * If a JSON file has multiple arrays of rows that need to be converted into separate CSV files they should be separated into separate JSON files and then fed into the script that way
