
import uuid
from datetime import time

class Timeslot:
    def __init__(self, day_id:str, start:time, end:time, id:str=None):
        self.id: str = id if id is not None else str(uuid.uuid4())
        self.day_id = day_id
        self.start = start
        self.end = end

            
    @classmethod
    def from_dict(cls, data: dict):
        parsed_day_id = data["day_id"]
        parsed_start = time.fromisoformat(data["start"])
        parsed_end = time.fromisoformat(data["end"])
        
        day_id = data.get("id") 

        return cls(day_id=parsed_day_id, start=parsed_start, end=parsed_end, id=day_id)