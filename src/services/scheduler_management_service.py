
from typing import List, Tuple, Optional
from datetime import date, time, datetime, timedelta
from src.data.in_memory_data_store import InMemoryDataStore
from src.models.day import Day
from src.models.timeslot import Timeslot

class SchedulerManagementService:
    def __init__(self, data_store: InMemoryDataStore):
        self.data_store:InMemoryDataStore = data_store
    

    def get_busy_slots(self, date_str:str) -> List[Tuple[time,time]]:
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            raise ValueError(f"Некорректный формат даты: {date_str}")

        all_days:List[Day] = self.data_store.get_days()
        all_timeslots:List[Timeslot] = self.data_store.get_timeslots()
        
        found_days = [d for d in all_days if d.date == target_date]

        if found_days:
            target_day = found_days[0]
        else:
            return []
        
        busy_timeslots = [(ts.start, ts.end) for ts in all_timeslots if ts.day_id == target_day.id]
        busy_timeslots.sort(key=lambda x: x[0])

        return busy_timeslots
    
    def get_free_slots(self, date_str:str) -> List[Tuple[time,time]]:
        try:
            target_date = date.fromisoformat(date_str)
        except ValueError:
            return []

        all_days:List[Day] = self.data_store.get_days()
        all_timeslots:List[Timeslot] = self.data_store.get_timeslots()
        
        found_days = [d for d in all_days if d.date == target_date]

        if found_days:
            target_day = found_days[0]
        else:
            return []
        
        start_day = target_day.start
        end_day = target_day.end
        
        free_slots = []
        current_time = start_day
        busy_timeslots = [(ts.start, ts.end) for ts in all_timeslots if ts.day_id == target_day.id]
        busy_timeslots.sort(key=lambda x: x[0])

        for busy_start, busy_end in busy_timeslots:
            if busy_start > current_time:
                free_slots.append((current_time, busy_start))

            current_time = max(current_time, busy_end)

        if current_time < end_day:
            free_slots.append((current_time, end_day))

        return free_slots
                
    def is_available(self, date_str:str, time_start_str:str, time_end_str:str) -> bool:
        try:
            target_date = date.fromisoformat(date_str)
            target_start = time.fromisoformat(time_start_str)
            target_end = time.fromisoformat(time_end_str)
            if target_start >= target_end:
                raise ValueError("Время начала должно быть раньше времени окончания.")
        except ValueError as e:
            raise ValueError(f"Некорректный формат даты или времени: {e}")
        
        all_days = self.data_store.get_days()
        all_slots = self.data_store.get_timeslots()

        found_days = [d for d in all_days if d.date == target_date]

        if found_days:
            target_day = found_days[0]
        else:
            raise ValueError(f"День {date_str} не занесен в базу.")

        busy_slots = [s for s in all_slots if s.day_id == target_day.id]
        is_available = all(target_start>=s.end or target_end<=s.start for s in busy_slots) 

        return is_available
    
    def _calculate_duration_minutes(self, start_time: time, end_time: time) -> int:
        ref_date = date.min 
        dt_start = datetime.combine(ref_date, start_time)
        dt_end = datetime.combine(ref_date, end_time)
        
        duration = dt_end - dt_start
        return int(duration.total_seconds() / 60)

    def _add_minutes_to_time(self, start_time: time, minutes_to_add: int) -> time:
        ref_datetime = datetime.combine(date.min, start_time)
        new_datetime = ref_datetime + timedelta(minutes=minutes_to_add)
        return new_datetime.time()
    
    def find_slot_for_duration(self, minutes_str:str) -> Optional[Tuple[date,time,time]]:
        try:
            minutes = int(minutes_str)
        except ValueError as e:
            raise ValueError(f"Некорректный формат времени, ожидается целое число минут: {e}")
        
        all_days:List[Day] = self.data_store.get_days()
        all_days.sort(key=lambda x: x.date)

        for d in all_days:
            current_time = d.start
            current_busy_slots = self.get_busy_slots(d.date.isoformat())
            for s in current_busy_slots:

                duration_in_minutes = self._calculate_duration_minutes(current_time, s[0])

                if duration_in_minutes >= minutes:
                    end_time = self._add_minutes_to_time(current_time, minutes)
                    return (d.date, current_time, end_time)

                current_time = max(current_time, s[1])
            
            if current_time < d.end:
                duration_in_minutes = self._calculate_duration_minutes(current_time, d.end)

                if duration_in_minutes >= minutes:
                    end_time = self._add_minutes_to_time(current_time, minutes)
                    return (d.date, current_time, end_time)
        return None



   


        




