import time

from model import ModelObject
from database_handler import SimpleDatabase


new_database = SimpleDatabase("test.db", "my_table")

def main():
    m1 = ModelObject(0, 0, "n1")
    time.sleep(1)
    m2 = ModelObject(1, 1, "n1")

    new_database.insert_data_point(m1)
    new_database.insert_data_point(m2)

    all_models = new_database.get_all()
    
    new_database.delete_data_point(m1.key2)
    new_database.delete_data_point(m2.key2)
    
    print(all_models)
    return 1


if __name__ == "__main__":
    main()


