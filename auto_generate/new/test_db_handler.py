import sqlite3

from typing import List
import datetime

from test_auto_generate import TestObject


'''
General Database Handler

'''


class TestObjectDbHandler:
    def __init__(self) -> None:
        self.conn = sqlite3.connect('random.db')
        self.c = self.conn.cursor() 

        self.table_name = 'rando'
        self.create_table()

    def __str__(self) -> str:
        pass
    
    def create_table(self):
        self.c.execute(f'''CREATE TABLE IF NOT EXISTS rando (
            key integer,
            name text,
            tags text
            status integer
)''')

    def insert_data_point(self, data_point: TestObject):
        with self.conn:
            self.c.execute(f'INSERT INTO {self.table_name} VALUES (:key, :name, :tags, :status)',
            {
                                'key': data_point.key,
                'name': f'{data_point.name}',
                'tags': f'{data_point.tags}',
                'status': data_point.status,
             
            })

        return True
    
    def get_all(self) -> List[TestObject]:
        self.c.execute(f'select * from {self.table_name}')
        results = self.c.fetchall()
        objects = []
        for result in results:
            objects.append(TestObject(*result))
        return objects

    def delete_data_point(self, key):
        with self.conn:
            self.c.execute(f'DELETE from {self.table_name} WHERE key=:key', {'key': key})



new_database = TestObjectDbHandler()

def main():
    m1 = TestObject(key=0, name='test name', tags=['new', 'test'], status=1, )

    new_database.insert_data_point(m1)

    all_models = new_database.get_all()
    
    new_database.delete_data_point(m1.key)
    
    print(all_models)


if __name__ == '__main__':
    main()

