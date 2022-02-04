import os

import json

from typing import List, Dict


def make_sql_create(raw_attrs:Dict[str, str]):
    # Make Attribute Text
    """
            key1 integer,
            key2 integer,
            name text,
            date_added text,
            date_completed text,
            status integer
    """
    output = ""
    count = 1
    for attr_name, attr_type in raw_attrs.items():
        t = "text"
        if attr_type == "int":
            t = "integer"
        
        if count == len(raw_attrs)-1:
            output += f"            {attr_name} {t}\n"
            continue
        count += 1
        output += f"            {attr_name} {t},\n"
    return output

def make_sql_insert(attributes:Dict[str,str]):
    # Make Data Text
    """
                'key1': data_point.key1,
                'key2': data_point.key2,
                'name': data_point.name,
                'date_added': data_point.date_added,
                'date_completed': data_point.date_completed,
                'status': data_point.status      
    
    """
    output = ""
    count = 1
    for data_key in attributes.keys():
        if count == len(attributes)-1:    
            if attributes[data_key] == "int":
                output += f"                '{data_key}': data_point.{data_key}\n"
                continue
            output += f"                '{data_key}': f'{'{'}data_point.{data_key}{'}'}'\n"
            continue
        if attributes[data_key] == "int":
            output += f"                '{data_key}': data_point.{data_key},\n"
            continue
        output += f"                '{data_key}': f'{'{'}data_point.{data_key}{'}'}',\n"
    return output

def make_sample_object(sample_data, attributes):
    output = ""
    count = 1
    for k, v in sample_data.items():
        # if count == len(attributes):    
        #     if attributes[k] == "int":
        #         output += f"{k}={v}"
        #         continue
        #     output += f"{k}='{v}'" 
        count += 1
        if attributes[k] == "str":
            output += f"{k}='{v}', "
            continue
        output += f"{k}={v}, "
    
    return output

def make_sql_protect(attrs):
    '''
    :key1, :key2, :name, :date_added, :date_completed, :status
    '''
    output = ""
    for _, k in enumerate(attrs.keys()):
        if _ == len(attrs)-1:
            output += f":{k}" 
            continue
        output += f":{k}, "
    
    return output

def make_db_handler(attributes: Dict[str,str], sample_data: Dict[str, str]=None, model_name:str="AutoObject", handler_name:str="auto_db_handler.py", file_name:str=None, database:List[str]=None, ref_index:str=""):
    # make new text file
    
    # Make Attribute Text
    sql_create_attr = make_sql_create(attributes)

    # Make Data Text
    sql_insert_attr = make_sql_insert(attributes)

    sql_inject_protection = make_sql_protect(attributes)

    test_data = make_sample_object(sample_data, attributes)

    parsed_filename = file_name.split("/")[1]
    removed_ext = parsed_filename.split(".")[0]

    print(sql_create_attr)
    print(sql_insert_attr)
    print(sql_inject_protection)
    print(removed_ext)

    new_text = f"""import sqlite3

from typing import List
import datetime

from {removed_ext} import {model_name}


'''
General Database Handler

'''


class {model_name}DbHandler:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('{database[0]}')
        self.c = self.conn.cursor() 

        self.table_name = '{database[1]}'
        self.create_table()

    def __str__(self) -> str:
        pass
    
    def create_table(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {database[1]} (
{sql_create_attr})''')

    def insert_data_point(self, data_point: {model_name}):
        with self.conn:
            self.c.execute(f'INSERT INTO {'{'}self.table_name{'}'} VALUES ({sql_inject_protection})',
            {'{'}
                {sql_insert_attr}             
            {'}'})

        return True
    
    def get_all(self) -> List[{model_name}]:
        self.c.execute(f'select * from {'{'}self.table_name{'}'}')
        results = self.c.fetchall()
        objects = []
        for result in results:
            objects.append({model_name}(*result))
        return objects

    def delete_data_point(self, key):
        with self.conn:
            self.c.execute(f'DELETE from {'{'}self.table_name{'}'} WHERE {ref_index}=:key', {'{'}'key': key{'}'})



new_database = {model_name}DbHandler()

def main():
    m1 = {model_name}({test_data})

    new_database.insert_data_point(m1)

    all_models = new_database.get_all()
    
    new_database.delete_data_point(m1.{ref_index})
    
    print(all_models)


if __name__ == '__main__':
    main()

""" 
    with open(handler_name, 'w') as new_file:
        new_file.write(new_text)


def main():
    # Load settings from json
    with open("auto_settings.json", 'r') as input_settings:
        new_settings = json.load(input_settings)
    
    make_db_handler(**new_settings)

if __name__ == "__main__":
    main()