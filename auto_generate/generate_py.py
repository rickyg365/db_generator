import os

import json

from typing import List, Dict


def make_attr_text(raw_attrs:Dict[str, str]):
    # Make Attribute Text
    output = ""
    for attr_name, attr_type in raw_attrs.items():
        output += f"    {attr_name}: {attr_type}\n"
    return output

def make_data_text(raw_data:Dict[str, str], attributes:Dict[str,str]):
    # Make Data Text
    output = ""
    for data_key, data_val in raw_data.items():
        if attributes[f'{data_key}'] == "str":
            output += f"{data_key}='{data_val}', "
            continue
        output += f"{data_key}={data_val}, "
    return output

def make_file(attributes: Dict[str,str], sample_data: Dict[str, str]=None, model_name:str="AutoObject", file_name:str="auto_generated.py", handler_name:str=None, database:List[str]=None, ref_index:str=""):
    # make new text file
    
    # Make Attribute Text
    attribute_text = make_attr_text(attributes)

    # Make Data Text
    data_text = make_data_text(sample_data, attributes)

    new_text = f"""import os
from dataclasses import dataclass
from typing import List

@dataclass
class {model_name}:
{attribute_text}

def main():
    sample_object = {model_name}({data_text})
    print('My Data: \\n', sample_object)
    return 1
    
if __name__ == '__main__':
    main() 
""" 
    with open(file_name, 'w') as new_file:
        new_file.write(new_text)


def main():
    # Load settings from json
    with open("auto_settings.json", 'r') as input_settings:
        new_settings = json.load(input_settings)
    
    make_file(**new_settings)


if __name__ == "__main__":
    main()
