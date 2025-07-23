
import sys
from core.builder import ApplicationBuilder
from services.data_loading_service import DataLoadingService
from services.scheduler_management_service import SchedulerManagementService
from data.in_memory_data_store import InMemoryDataStore
from handlers.scheduler_handler import SchedulerHandler

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <data_url>")
        sys.exit(1)
    
    data_url = sys.argv[1]

    builder = ApplicationBuilder(
        data_store_type=InMemoryDataStore,
        data_loading_service_type=DataLoadingService,
        scheduler_management_service_type=SchedulerManagementService,
        scheduler_handler_type=SchedulerHandler, 
        data_url=data_url 
    ) 

    app = builder.build()
    app.run()

if __name__ == "__main__":
    main()