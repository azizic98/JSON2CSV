
# JSON2CSV

The JSON2CSV module is designed to convert JSON files or JSON objects into flattened Pandas DataFrames. Once converted to a DataFrame, you can easily export the data to a CSV file using Pandas' .to_csv method. This utility is particularly useful for handling JSON data structures that contain nested dictionaries or lists, providing a seamless way to convert complex JSON into a tabular format.


## Features

- Flexible Input: Accepts both JSON file paths and JSON objects.
- Data Flattening: Recursively flattens nested JSON structures into a flat dictionary.
- Pandas Integration: Converts JSON to Pandas DataFrame for easy manipulation and export.


## Installation

Ensure you have Python and the required packages installed. You can install the necessary packages using pip:


```bash
    pip install pandas
```
    
## Usage/Examples

- First, import the module and create an instance of the JSON2CSV class:

```python
    from json2csv import JSON2CSV
    json2csv = JSON2CSV()
```

- Convert JSON File to DataFrame
```python
    try:
        df_from_file = json2csv.convert('json_file.json')
        print(df_from_file)
    except (FileNotFoundError, ValueError) as e:
        print(e)
```

- Convert JSON Object to DataFrame
```python
    json_data = [
        {"name": ["Mayur"], "age": [28], "city": ["Mumbai"]},
        {"name": ["Ahmed"], "age": [24], "city": ["Kolkata"]}
    ]

    try:
        df_from_json = json2csv.convert(json_data)
        print(df_from_json)
    except (ValueError) as e:
        print(e)
```
- Export DataFrame to CSV
```python
    df_from_json.to_csv('output.csv', index=False)

```

