import uuid
from datetime import date, time

class Day:
    def __init__(self, date:date, start:time, end:time, id:str=None):
        if(id is None):
            self.id = str(uuid.uuid4())
            self.date = date
            self.start = start
            self.end = end
    
    @classmethod
    def from_dict(cls, data: dict):
        parsed_date = date.fromisoformat(data["date"])
        parsed_start = time.fromisoformat(data["start"])
        parsed_end = time.fromisoformat(data["end"])
        
        day_id = data.get("id") 

        return cls(date=parsed_date, start=parsed_start, end=parsed_end, id=day_id)