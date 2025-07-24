from src.services.scheduler_management_service import SchedulerManagementService

class SchedulerHandler:
    def __init__(self, scheduler_management_service: SchedulerManagementService):
        self.scheduler_service = scheduler_management_service
    

    def get_busy_slots_command(self, args_str: str) -> str:
        parts = args_str.split(" ") 
        if len(parts) != 1:
            raise ValueError("Неверный формат команды. get_busy_slots принимает один аргумент - дата")
        
        date_str = parts[0]

        try:
            busy_timeslots = self.scheduler_service.get_busy_slots(date_str) 
        except Exception as e:
            return f"Ошибка получения занятых слотов: {e}"
        
        if not busy_timeslots:
            return str([])
        
        formatted_slots = [(start.strftime("%H:%M"), end.strftime("%H:%M")) for start, end in busy_timeslots]

        return str(formatted_slots)
            
    def get_free_slots_command(self, args_str:str) -> str:
        parts = args_str.split(" ") 
        if len(parts) != 1:
            raise ValueError("Неверный формат команды. get_free_slots принимает один аргумент - дата")
        
        date_str = parts[0]

        try:
            free_timeslots = self.scheduler_service.get_free_slots(date_str) 
        except Exception as e:
            return f"Ошибка получения свободных слотов: {e}"
        
        try:
            busy_timeslots = self.scheduler_service.get_busy_slots(date_str) 
        except Exception as e:
            busy_timeslots = []

        if not free_timeslots and busy_timeslots:
            return(f"Нет свободных слотов для {date_str}.")
        elif not free_timeslots and not busy_timeslots:
            return(f"День {date_str} не занесен в базу как занятый.")

        formatted_slots = [(start.strftime("%H:%M"), end.strftime("%H:%M")) for start, end in free_timeslots]

        return str(formatted_slots)

    def is_available_command(self, args_str:str) -> str:
        parts = args_str.split(" ") 
        if len(parts) != 3:
            raise ValueError("Неверный формат команды. get_free_slots принимает три аргумента - дата, начало промежутка времени, конец промежутка времени")
        
        date_str = parts[0]
        time_start_str = parts[1]
        time_end_str = parts[2]

        try:
            is_available = self.scheduler_service.is_available(date_str, time_start_str, time_end_str) 
        except Exception as e:
            return f"Ошибка проверки промежутка времени: {e}"

        return str(is_available)

    def find_slot_for_duration_command(self, args_str:str) -> str:
        parts = args_str.split(" ") 
        if len(parts) != 1:
            raise ValueError("Неверный формат команды. find_slot_for_duration принимает один аргумент - число минут")
        
        time_str = parts[0]

        try:
            slot_for_duration = self.scheduler_service.find_slot_for_duration(time_str) 
        except Exception as e:
            return f"Ошибка проверки промежутка времени: {e}"
        if not slot_for_duration:
            return "Ни один из дней в базе не подошел."
        found_date, start_time, end_time = slot_for_duration
        formatted_slot = f"({found_date.isoformat()}, {start_time.strftime('%H:%M')}, {end_time.strftime('%H:%M')})"

        return formatted_slot