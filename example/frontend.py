from cProfile import run
import os

from model import ModelObject
from database_handler import SimpleDatabase

"""
add custom table making/ custom model making
"""


def clear_screen():
    cols, rows = os.get_terminal_size()
    # os.system("cls")
    print(f"{cols*'-'}")

class DatabaseFrontend:
    def __init__(self, reference_file="db_list.txt", model_object=None) -> None:
        # Terminal Size
        self.cols, self.rows = os.get_terminal_size()

        # Variables
        self.file_name = reference_file
        
        self.db_list = []

        self.db_name = ""
        self.table_name = ""
        self.running_database = None
        self.models = []

        self.load_list()
        self.select_database()
        

    def __str__(self):
        # Make sure models are up to date
        if self.running_database is not None:
            self.get_models()
        
        txt = f"\n[{self.db_name.capitalize()}]: {self.table_name}\n{self.cols*'_'}\n"    
        
        for model in self.models:
                txt += f"\n{model}\n"
        
        txt += f"{self.cols*'_'}"

        return txt

    # Managing
    def load_list(self):
        with open(self.file_name, 'r') as ref_file:
            for _, line in enumerate(ref_file):
                if _ == 0:
                    continue
                entry = line.strip().split(" ")
                self.db_list.append(entry)
    
    def save_list(self):
        first_line = "DATABASE_NAME TABLE_NAME\n"
        with open(self.file_name, 'w') as new_file:
            new_file.write(first_line)
            for item in self.db_list:
                new_line = f"{item[0]} {item[1]}\n"
                new_file.write(new_line)

    def load_database(self):
        if self.db_name is None:
            # maybe close running database
            return
        self.running_database = SimpleDatabase(self.db_name, self.table_name)
        self.get_models()

    def get_models(self):
        if self.running_database is None:
            return
        self.models = self.running_database.get_all()

    # Helper Functions
    def process_model_input(self, raw_input:str, min_length:int=6) -> dict:
        inputs = raw_input.split(" ")
        
        # Decide which are optional and which are not
        if len(inputs) < min_length:
            # Do SOmething
            ...

        parsed_input = {
            "key1": int(inputs[0]),
            "key2": int(inputs[1]),
            "name": inputs[2],
            "date_added": inputs[3],
            "date_completed": inputs[4],
            "status": int(inputs[5]),
        }

        return parsed_input

    # Actions
    def select_database(self, create_new=False):
        empty_condition = len(self.db_list) == 0

        if empty_condition or create_new:
            new_db = input("Enter a Database Name and a Table Name, separated by a space:\nex. db_name tb_name\n>>> ").split()
            self.db_list.append(new_db)
            self.save_list()
            self.db_name, self.table_name = new_db
            self.running_database = SimpleDatabase(new_db[0], new_db[1])
            # Save new database
        else:
            print("Select a Database( use number or new ): \n")
            for _, choice in enumerate(self.db_list):
                print(f" [{_}]: {choice[0]} {choice[1]}")

            db_choice = input("\n>>> ")

            if db_choice == "new":
                self.select_database(True)
                return
            self.db_name, self.table_name = self.db_list[int(db_choice)]
            self.load_database()
            
    def insert_objects(self):
        insert_text = f"""
Insert Object (space seperated):
    key1 key2 name date_added date_completed status
{self.cols*'_'}
"""
        print(insert_text)

        while True:
            user_input = input(">>> ")
            
            if user_input.lower() == 'q':
                break

            new_object = self.process_model_input(user_input)
            new_model = ModelObject(**new_object)
            self.running_database.insert_data_point(new_model)

    def delete_all(self):
        # Delete all objs, beacuse we just testing
        for model in self.models:
            self.running_database.delete_data_point(model.key2)

    def run(self):
        clear_screen()
        top_text = "Welcome! Choose an Option to Start!:"
        run_options = f"""
    [S]: Select New Database
    
    [I]: Insert Models
    [V]: View Models
    [D]: Delete Models

    [Q]: Quit Program
{self.cols*'_'}"""
        while True:
            current_database = f"Current Database: {self.db_name} Table: {self.table_name}"
            
            final_text = f"""
{top_text}
{self}
{current_database}
{run_options}
"""
            clear_screen()
            print(final_text)
            user_input = input(">>> ")

            if user_input.lower() == 'q':
                print("\n[ Quit Program ]\n")
                break

            # Select
            if user_input.lower() == 's':
                self.select_database()
            
            # Insert
            if user_input.lower() == 'i':
                self.insert_objects()
            
            # View
            if user_input.lower() == 'v':
                print(self)
            
            # Remove
            if user_input.lower() == 'd':
                print(f"TBI: HeHeHe sorry!")
            
            input("\nPress [Enter] to Continue...")


if __name__ == "__main__":
    new_db = DatabaseFrontend()
    new_db.run()

