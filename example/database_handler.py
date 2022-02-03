import sqlite3

from typing import List
import datetime

from model import ModelObject


"""
General Database Handler

"""


class SimpleDatabase:
    def __init__(self, database_name="sample.db", table_name="main") -> None:
        self.conn = sqlite3.connect(database_name)
        self.c = self.conn.cursor() 

        self.table_name = table_name
        self.create_table(table_name)

    def __str__(self) -> str:
        pass
    
    def create_table(self, table_name):
        self.c.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            key1 integer,
            key2 integer,
            name text,
            date_added text,
            date_completed text,
            status integer
        )""")

    def insert_data_point(self, data_point: ModelObject):
        # self.c.execute(f"select count(*) FROM {self.table_name}")

        # count = self.c.fetchone()[0]

        with self.conn:
            self.c.execute(f"INSERT INTO {self.table_name} VALUES (:key1, :key2, :name, :date_added, :date_completed, :status)",
            {
                'key1': data_point.key1,
                'key2': data_point.key2,
                'name': data_point.name,
                'date_added': data_point.date_added,
                'date_completed': data_point.date_completed,
                'status': data_point.status                
            })

        return True
    
    def get_all(self) -> List[ModelObject]:
        self.c.execute(f"select * from {self.table_name}")
        results = self.c.fetchall()
        objects = []
        for result in results:
            objects.append(ModelObject(*result))
        return objects

    def delete_data_point(self, key):
        with self.conn:
            self.c.execute(f"DELETE from {self.table_name} WHERE key2=:key", {'key': key})

