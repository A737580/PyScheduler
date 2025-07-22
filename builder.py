from app import App
from services.data_loading_service import DataLoadingService
from data.in_memory_data_store import InMemoryDataStore
from handlers.scheduler import Scheduler

class ApplicationBuilder:
    def __init__(self, data_store_type: InMemoryDataStore, data_loading_service_type: DataLoadingService, scheduler_type: Scheduler, data_url: str):
        self.data_store_type = data_store_type
        self.data_loading_service_type = data_loading_service_type
        self.scheduler_type = scheduler_type
        self.data_url = data_url
        
        self._services = {} 

    def build(self) -> App:

        data_store = self.data_store_type()
        self._services['data_store'] = data_store

        data_loading_service = self.data_loading_service_type(self.data_url, data_store)
        self._services['data_loading_service'] = data_loading_service

        data_loading_service.load_initial_data()

        scheduler_instance = self.scheduler_type(data_store)
        self._services['scheduler'] = scheduler_instance

        return App(scheduler_instance)