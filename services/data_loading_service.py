import urllib.request
import json
from data.in_memory_data_store import InMemoryDataStore 

class DataLoadingService:
    def __init__(self, url: str, data_store: InMemoryDataStore):
        self.url = url
        self.data_store = data_store 

    def load_initial_data(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                if response.getcode() == 200:
                    raw_data = response.read()
                    decoded_data = raw_data.decode('utf-8')
                    
                    data = json.loads(decoded_data)
                    self.data_store.add_initial_data(data) 
                else:
                    raise Exception("Ответ от сервера != 200.")
        except json.JSONDecodeError as e:
            print("Полученный файл не JSON или не валиден.")
        except Exception as e:
            print(f"Возникла ошибка при считывании данных.{e}")

        