from typing import List, Union
from models.day import Day
from models.timeslot import Timeslot

SupportedModel = Union[Day, Timeslot]


class InMemoryDataStore:
    def __init__(self):
        self.days:List[Day] = []
        self.timeslots:List[Timeslot] = []


    def add_item(self, item: SupportedModel):
        if isinstance(item, Day):
            self.days.append(item)
        elif isinstance(item, Timeslot):
            self.timeslots.append(item)

        else:
            raise TypeError(f"Тип:{type(item)} не поддерживается, для объекта.")

    def get_days(self) -> List[Day]:
        return list(self.days) 

    def get_timeslots(self) -> List[Timeslot]:
        return list(self.timeslots)

    def add_initial_data(self, initial_data: dict):
        if "days" in initial_data:
            for day_data in initial_data["days"]:
                self.add_item(Day.from_dict(day_data)) 
        if "timeslots" in initial_data:
            for timeslot_data in initial_data["timeslots"]:
                self.add_item(Timeslot.from_dict(timeslot_data)) 
            
            