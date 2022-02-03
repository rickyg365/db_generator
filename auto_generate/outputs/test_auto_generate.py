import os
from dataclasses import dataclass
from typing import List

@dataclass
class TestObject:
    key: int
    name: str
    tags: List[str]
    status: int


def main():
    sample_object = TestObject(key=0, name='test name', tags=['new', 'test'], status=1, )
    print('My Data: \n', sample_object)
    return 1
    
if __name__ == '__main__':
    main() 
