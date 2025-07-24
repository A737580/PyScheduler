from src.core.app import App
from src.core.command_router import CommandRouter
from src.services.data_loading_service import DataLoadingService
from src.services.scheduler_management_service import SchedulerManagementService
from src.data.in_memory_data_store import InMemoryDataStore
from src.handlers.scheduler_handler import SchedulerHandler


class ApplicationBuilder:
    def __init__(self, data_store_type: InMemoryDataStore, data_loading_service_type: DataLoadingService, scheduler_management_service_type: SchedulerManagementService, scheduler_handler_type: SchedulerHandler,  data_url: str):
        self.data_store_type = data_store_type
        self.data_loading_service_type = data_loading_service_type
        self.scheduler_management_service_type = scheduler_management_service_type
        self.scheduler_handler_type = scheduler_handler_type
        self.data_url = data_url
        self._services = {} 

    def build(self) -> App:

        data_store = self.data_store_type()
        self._services['data_store'] = data_store

        data_loading_service = self.data_loading_service_type(self.data_url, data_store)
        self._services['data_loading_service'] = data_loading_service
        data_loading_service.load_initial_data()

        scheduler_management_service = self.scheduler_management_service_type(data_store)
        self._services['scheduler_management_service'] = scheduler_management_service

        scheduler_handler:SchedulerHandler = self.scheduler_handler_type(scheduler_management_service)
        self._services['scheduler_handler'] = scheduler_handler

        command_router = CommandRouter()
        self._services['command_router'] = command_router

        command_router.register_command("get_busy_slots", scheduler_handler.get_busy_slots_command, "<date> - возвращает список занятых слотов")
        command_router.register_command("get_free_slots", scheduler_handler.get_free_slots_command, "<date> - возвращает список свободных слотов")
        command_router.register_command("is_avalibale", scheduler_handler.is_available_command, "<date> <start_time> <end_time> - возвращает булев, доступен ли заданный промежуток")
        command_router.register_command("find_slot_for_duration", scheduler_handler.find_slot_for_duration_command, "<minutes> - возвращает первый свободный промежуток")

        return App(command_router)