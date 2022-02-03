import datetime
from dataclasses import dataclass, field


@dataclass
class ModelObject:
    key1:int = 0
    key2:int = 0
    name:str = ""
    date_added:str = field(default_factory=datetime.datetime.now)
    date_completed:str = ""
    status:int = 1

    # def __post_init__(self):
    #     if self.date_added == "":
    #         self.date_added = datetime.datetime.now()

