import os

from model import ModelObject
from database_handler import SimpleDatabase


def process_input(raw_input, min_length=6):
    inputs = raw_input.split(" ")
    
    # Decide which are optional and which are not
    if len(inputs) < min_length:
        # Do SOmething
        ...

    final_output = {
        "key1": int(inputs[0]),
        "key2": int(inputs[1]),
        "name": inputs[2],
        "date_added": inputs[3],
        "date_completed": inputs[4],
        "status": int(inputs[5]),
    }

    return final_output


def main():
    # Start Database
    main_database = SimpleDatabase("random.db", "rando")

    cols, rows = os.get_terminal_size()

    # Intro
    title = "Insert Object (space seperated):\n"
    example = "    key1 key2 name date_added date_completed status"
    line = f"{cols*'_'}"

    print(f"""
{title}
{example}
{line}
""")

    while True:
        user_input = input(">>> ")

        if user_input.lower() == 'q':
            break
        
        new_object = process_input(user_input)
        new_model_obj = ModelObject(**new_object)
        main_database.insert_data_point(new_model_obj)

        
        # print(new_object)
        # print(new_model_obj)
    
    all_objs = main_database.get_all()

    print()
    print(all_objs)

    # Delete all objs, beacuse we just testing
    for obj in all_objs:
        main_database.delete_data_point(obj.key2)
        
    return 1


if __name__ == "__main__":
    main()

