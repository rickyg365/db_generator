import os
import json

from generate_py import make_file
from generate_db_handler import make_db_handler




def main():
    # Load json data
    with open("test_settings.json", 'r') as json_settings:
        new_settings = json.load(json_settings)

    # Create base directory
    dir_name = new_settings['file_name'].split('/')[0]
    os.mkdir(dir_name)
    
    # Pass into make_file to create new file
    make_file(**new_settings)

    # Pass into make_db_handler to create new db handler
    make_db_handler(**new_settings)

    return 1


if __name__ == "__main__":
    main()


