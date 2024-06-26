import json
import os
import pandas as pd

class JSON2CSV:
    """
    A module to convert JSON data to a flattened CSV format using Pandas DataFrame.
    """

    def replace_newline_with_space(self, data):
        """
        Recursively replace newline characters with spaces in a JSON data structure.

        Args:
            data (str, dict, list, or other): Input data to process.

        Returns:
            Data with newline characters replaced with spaces.
        """
        if isinstance(data, str):
            return data.replace('\r', '\n')
        elif isinstance(data, dict):
            return {key: self.replace_newline_with_space(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.replace_newline_with_space(item) for item in data]
        else:
            return data

    def flatten_json(self, json_data, parent_key='', separator='.'):
        """
        Recursively flatten a JSON data structure.

        Args:
            json_data (dict): JSON data to flatten.
            parent_key (str): The parent key when processing nested dictionaries.
            separator (str): Separator to use for flattened keys.

        Returns:
            Flattened dictionary.
        """
        items = {}
        for key, value in json_data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key

            value = self.replace_newline_with_space(value)

            if isinstance(value, list):
                if all(isinstance(item, (str, int)) for item in value):  # List contains only strings or integers
                    items[new_key] = ', '.join(map(str, value))
                else:
                    dict_count = 0
                    for i, item in enumerate(value):
                        if isinstance(item, dict):  # List contains dictionaries
                            dict_count += 1
                            for sub_key, sub_value in item.items():
                                sub_new_key = f"{new_key}{separator}{sub_key}"
                                if sub_new_key in items:
                                    old_value = str(items[sub_new_key])
                                    to_add_value = str(sub_value)
                                    new_value = [old_value] + [to_add_value]
                                    items[sub_new_key] = ', '.join(new_value)
                                else:
                                    items[sub_new_key] = sub_value
                    if dict_count == 0:
                        items[new_key] = value
            elif isinstance(value, dict):
                items.update(self.flatten_json(value, new_key, separator))
            else:
                items[new_key] = value
        return items

    def convert(self, input_json):
        """
        Convert JSON data to a Pandas DataFrame. Input can be a file path or JSON data.

        Args:
            input_json (str or list of dict): Path to the input JSON file or JSON data.

        Returns:
            Pandas DataFrame containing the flattened data.

        Raises:
            ValueError: If input is not a string or a list of dictionaries.
            FileNotFoundError: If the input file does not exist.
        """
        if isinstance(input_json, str):
            if not os.path.exists(input_json):
                raise FileNotFoundError(f"The file '{input_json}' does not exist.")
            with open(input_json, 'r') as json_file:
                json_data = json.load(json_file)
        
        elif isinstance(input_json, list) and all(isinstance(item, dict) for item in input_json):
            json_data = input_json
        
        else:
            raise ValueError("Input must be a string (file path) or a list of dictionaries (JSON data).")

        # Flatten JSON data and convert to DataFrame
        flattened_data = [self.flatten_json(entry) for entry in json_data]
        df = pd.DataFrame(flattened_data)

        return df
