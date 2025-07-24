
import os
import urllib.request
import json
from src.data.in_memory_data_store import InMemoryDataStore 

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
            print(f"Полученный файл не является валидным JSON: {e}")
        except Exception as e:
            print(f"Возникла ошибка при считывании данных: {e}")
    
    def load_initial_data_from_file(self, file_path:str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден по указанному пути: {self.file_path}")
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                decoded_data = f.read()
                data = json.loads(decoded_data)
                
                self.data_store.add_initial_data(data)
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Полученный файл не является валидным JSON: {e}")
        except Exception as e:
            raise Exception(f"Возникла ошибка при считывании данных: {e}")
        