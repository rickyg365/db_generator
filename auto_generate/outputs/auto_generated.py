import os
from dataclasses import dataclass
from typing import List

@dataclass
class TestModel:
    key1: int
    key2: int
    name: str
    tags: List[str]
    status: int


def main():
    sample_object = TestModel(key1=0, key2=0, name='a name', tags=['cool', 'new'], status=0, )
    print('My Data: \n', sample_object)
    return 1
    
if __name__ == '__main__':
    main() 
